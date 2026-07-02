import asyncio
import os
import sys
import redis.asyncio as redis

# Ensure PYTHONPATH or system paths are set up if running directly
from service.oracle.config.settings import LIVE_HOST, LIVE_PORT
from service.oracle.config.data_struct import PLAYER, PLAYER_META

async def validate():
    # Connect using REDIS_URL if provided, else use default settings
    redis_url = os.environ.get("REDIS_URL")
    if redis_url:
        r = redis.Redis.from_url(redis_url, decode_responses=True)
    else:
        r = redis.Redis(host=LIVE_HOST, port=LIVE_PORT, db=0, decode_responses=True)

    # 1. Scan and categorize keys
    all_keys = await r.keys("*")
    
    player_keys = []
    player_meta_keys = []
    player_gw_keys = []
    fixture_keys = []
    gw_keys = []
    index_keys = []
    legacy_keys = []
    
    for key in all_keys:
        if key.startswith("raw_"):
            legacy_keys.append(key)
            continue
            
        parts = key.split(":")
        if parts[0] == "player":
            if len(parts) == 2:
                if parts[1].isdigit():
                    player_keys.append(key)
            elif len(parts) == 3 and parts[2] == "meta":
                player_meta_keys.append(key)
            elif len(parts) == 4 and parts[2] == "gw":
                player_gw_keys.append(key)
        elif parts[0] == "fixture":
            if len(parts) == 2 and parts[1].isdigit():
                fixture_keys.append(key)
        elif parts[0] == "gw":
            if len(parts) == 2 and parts[1].isdigit():
                gw_keys.append(key)
        elif parts[0] == "index":
            index_keys.append(key)

    # Prepare templates
    player_template_keys = set(PLAYER.keys())
    player_meta_template_keys = set(PLAYER_META.keys())

    # Validation States
    overall_pass = True
    
    # --- Pillar 1: Hash Segregation & Cost ---
    p1_pass = True
    p1_reasons = []
    for pkey in player_keys:
        fields = await r.hgetall(pkey)
        field_set = set(fields.keys())
        
        # Verify no meta fields leaked into player
        leaked_meta = field_set & player_meta_template_keys
        if leaked_meta:
            p1_pass = False
            p1_reasons.append(f"{pkey} contains meta fields: {leaked_meta}")
            
        # Cost check
        cost = fields.get("cost")
        if cost is None:
            p1_pass = False
            p1_reasons.append(f"{pkey} is missing 'cost' field")
        else:
            try:
                cost_val = float(cost)
                if cost_val >= 25.0:
                    p1_pass = False
                    p1_reasons.append(f"{pkey} cost '{cost}' is not normalized (expected < 25.0, e.g. '8.5')")
                if "." not in cost:
                    p1_pass = False
                    p1_reasons.append(f"{pkey} cost '{cost}' lacks decimal point")
            except ValueError:
                p1_pass = False
                p1_reasons.append(f"{pkey} cost '{cost}' is not a valid float")
                
    for pmkey in player_meta_keys:
        fields = await r.hgetall(pmkey)
        field_set = set(fields.keys())
        
        # Verify no core identity fields leaked into meta
        identity_fields = {"first_name", "second_name", "name", "position", "team_id", "status"}
        leaked_identity = field_set & identity_fields
        if leaked_identity:
            p1_pass = False
            p1_reasons.append(f"{pmkey} contains identity fields: {leaked_identity}")

    if not p1_pass:
        overall_pass = False

    # --- Pillar 2: Flattening & Type Constraints ---
    p2_pass = True
    p2_reasons = []
    for fkey in fixture_keys:
        fields = await r.hgetall(fkey)
        for fname, val in fields.items():
            if "[" in val or "{" in val:
                p2_pass = False
                p2_reasons.append(f"{fkey} field '{fname}' contains JSON brackets: '{val}'")
                break
                
    for gwkey in player_gw_keys:
        fields = await r.hgetall(gwkey)
        for fname, val in fields.items():
            if "[" in val or "{" in val:
                p2_pass = False
                p2_reasons.append(f"{gwkey} field '{fname}' contains JSON brackets: '{val}'")
                break
                
    if not p2_pass:
        overall_pass = False

    # --- Pillar 3: String-Boolean Enforcement ---
    p3_pass = True
    p3_reasons = []
    for fkey in fixture_keys:
        fields = await r.hgetall(fkey)
        for field in ("finished", "started"):
            val = fields.get(field)
            if val not in ("true", "false"):
                p3_pass = False
                p3_reasons.append(f"{fkey} field '{field}' is '{val}' (expected 'true'/'false')")
                
    for pmkey in player_meta_keys:
        fields = await r.hgetall(pmkey)
        val = fields.get("in_dreamteam")
        if val not in ("true", "false"):
            p3_pass = False
            p3_reasons.append(f"{pmkey} field 'in_dreamteam' is '{val}' (expected 'true'/'false')")
            
    for gkey in gw_keys:
        fields = await r.hgetall(gkey)
        for field in ("is_current", "is_previous", "is_next", "finished", "data_checked"):
            val = fields.get(field)
            if val is not None and val not in ("true", "false"):
                p3_pass = False
                p3_reasons.append(f"{gkey} field '{field}' is '{val}' (expected 'true'/'false')")

    if not p3_pass:
        overall_pass = False

    # --- Pillar 4: Set-Piece Order Integrity ---
    p4_pass = True
    p4_reasons = []
    for pmkey in player_meta_keys:
        fields = await r.hgetall(pmkey)
        for field in ("penalties_order", "direct_freekicks_order", "corners_and_indirect_freekicks_order"):
            val = fields.get(field)
            if val is None:
                p4_pass = False
                p4_reasons.append(f"{pmkey} is missing set-piece field '{field}'")
            elif val != "":
                # Check if it is a positive integer taker order
                try:
                    val_int = int(val)
                    if val_int <= 0:
                        p4_pass = False
                        p4_reasons.append(f"{pmkey} field '{field}' has invalid taker value '{val}' (expected positive int or '')")
                except ValueError:
                    p4_pass = False
                    p4_reasons.append(f"{pmkey} field '{field}' has invalid non-integer value '{val}' (expected positive int or '')")

    if not p4_pass:
        overall_pass = False

    # --- Pillar 5: Index Membership Verification ---
    p5_pass = True
    p5_reasons = []
    
    # Check index:team_players:{team_id}
    team_players_keys = [k for k in index_keys if k.startswith("index:team_players:")]
    if not team_players_keys:
        p5_pass = False
        p5_reasons.append("No index:team_players:* keys found")
    else:
        for k in team_players_keys:
            k_type = await r.type(k)
            if k_type != "set":
                p5_pass = False
                p5_reasons.append(f"{k} type is '{k_type}', expected 'set'")
            members = await r.smembers(k)
            if not members:
                p5_pass = False
                p5_reasons.append(f"{k} is empty")
            for m in members:
                if not m.isdigit():
                    p5_pass = False
                    p5_reasons.append(f"{k} contains non-numeric member: {m}")
                    
    # Check index:position_players:{1-4}
    for pos in (1, 2, 3, 4):
        k = f"index:position_players:{pos}"
        k_type = await r.type(k)
        if k_type != "set":
            p5_pass = False
            p5_reasons.append(f"{k} type is '{k_type}', expected 'set'")
        members = await r.smembers(k)
        if not members:
            p5_pass = False
            p5_reasons.append(f"{k} is empty")
            
    # Check index:season_players:{year}
    season_players_keys = [k for k in index_keys if k.startswith("index:season_players:")]
    if not season_players_keys:
        p5_pass = False
        p5_reasons.append("No index:season_players:* keys found")
    else:
        for k in season_players_keys:
            k_type = await r.type(k)
            if k_type != "set":
                p5_pass = False
                p5_reasons.append(f"{k} type is '{k_type}', expected 'set'")
            members = await r.smembers(k)
            if not members:
                p5_pass = False
                p5_reasons.append(f"{k} is empty")
                
    # Check index:season_fixtures:{year}
    season_fixtures_keys = [k for k in index_keys if k.startswith("index:season_fixtures:")]
    if not season_fixtures_keys:
        p5_pass = False
        p5_reasons.append("No index:season_fixtures:* keys found")
    else:
        for k in season_fixtures_keys:
            k_type = await r.type(k)
            if k_type != "set":
                p5_pass = False
                p5_reasons.append(f"{k} type is '{k_type}', expected 'set'")
            members = await r.smembers(k)
            if not members:
                p5_pass = False
                p5_reasons.append(f"{k} is empty")

    # Check index:team_name:{name} -> HASH
    team_name_keys = [k for k in index_keys if k.startswith("index:team_name:")]
    if not team_name_keys:
        p5_pass = False
        p5_reasons.append("No index:team_name:* keys found")
    else:
        for k in team_name_keys:
            k_type = await r.type(k)
            if k_type != "hash":
                p5_pass = False
                p5_reasons.append(f"{k} type is '{k_type}', expected 'hash'")
            fields = await r.hgetall(k)
            if "tid" not in fields:
                p5_pass = False
                p5_reasons.append(f"{k} is missing field 'tid'")
            else:
                tid = fields["tid"]
                if not tid.isdigit():
                    p5_pass = False
                    p5_reasons.append(f"{k} field 'tid' has non-integer value: '{tid}'")

    if not p5_pass:
        overall_pass = False

    # --- Pillar 6: Legacy State Cleanliness ---
    p6_pass = len(legacy_keys) == 0
    p6_reasons = []
    if not p6_pass:
        p6_reasons.append(f"Found {len(legacy_keys)} legacy raw_ keys: {legacy_keys[:5]}")
        overall_pass = False

    # --- PRINT DASHBOARD ---
    print("=" * 80)
    print("                    REDIS STRUCTURAL VALIDATION REPORT")
    print("=" * 80)
    print("Metrics Summary:")
    print(f"  - Total Players Checked:    {len(player_keys)}")
    print(f"  - Total Metas Checked:      {len(player_meta_keys)}")
    print(f"  - Total Fixtures Checked:   {len(fixture_keys)}")
    print(f"  - Total Player GWs Checked: {len(player_gw_keys)}")
    print(f"  - Total Legacy Keys Found:  {len(legacy_keys)}")
    print("-" * 80)
    print("Validation Checklist:")
    
    def print_result(passed, name, reasons):
        if passed:
            print(f"  [PASS] {name}")
        else:
            reason_str = reasons[0] if reasons else "Unknown violation"
            if len(reasons) > 1:
                reason_str += f" (+{len(reasons)-1} more)"
            print(f"  [FAIL: {reason_str}] {name}")
            
    print_result(p1_pass, "Pillar 1: Hash Segregation (The Player Split)", p1_reasons)
    print_result(p2_pass, "Pillar 2: Flattening & Type Constraints", p2_reasons)
    print_result(p3_pass, "Pillar 3: String-Boolean Enforcement", p3_reasons)
    print_result(p4_pass, "Pillar 4: Set-Piece Order Integrity", p4_reasons)
    print_result(p5_pass, "Pillar 5: Index Membership Verification", p5_reasons)
    print_result(p6_pass, "Pillar 6: Legacy State Migration Cleanliness", p6_reasons)
    print("=" * 80)
    
    if overall_pass:
        print("  OVERALL STATUS: COMPLIANT")
        print("=" * 80)
        await r.aclose()
        sys.exit(0)
    else:
        print("  OVERALL STATUS: NON-COMPLIANT (Structural violations caught)")
        print("=" * 80)
        await r.aclose()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(validate())
