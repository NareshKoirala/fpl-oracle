"""
DB Writer — Set Pieces
=======================
Parses FPL set-piece notes and updates ``player:{id}:meta``
with taker order rankings.

The API returns unstructured text.  A keyword heuristic classifies
each note as penalty / direct-FK / corner, then player IDs are
resolved either from structured ``element`` fields or by name matching.
"""

from service.oracle.db.db_redis import RedisDB
from service.oracle.utils.log import Logger

LOG = Logger("Set_Pieces_DB", "db")
DB = RedisDB()


# ── Keyword sets for classifying note type ──────────────────────

_SP_PENALTIES = {
    "penalty", "penalties", "spot kick", "spot-kick", "from the spot",
}
_SP_DIRECT_FK = {
    "direct free-kick", "direct free kick", "direct freekick",
    "free-kick", "free kick",
}
_SP_CORNERS = {
    "corner", "corners",
    "indirect free-kick", "indirect free kick", "indirect freekick",
}


def classify_note(text: str) -> str | None:
    """Return the ``PLAYER_META`` field name for a set-piece note, or ``None``."""
    lower = text.lower()
    if any(kw in lower for kw in _SP_PENALTIES):
        return "penalties_order"
    if any(kw in lower for kw in _SP_DIRECT_FK):
        return "direct_freekicks_order"
    if any(kw in lower for kw in _SP_CORNERS):
        return "corners_and_indirect_freekicks_order"
    return None


async def build_name_to_pid() -> dict[str, str]:
    """Build a lookup of lowercase player ``web_name`` → player ID.

    Scans all four position indexes and reads each player's ``name`` field
    from the ``player:{id}`` hash written during bootstrap.
    """
    name_map: dict[str, str] = {}
    for pos in range(1, 5):
        members = await DB.smembers(f"index:position_players:{pos}")
        for m in members:
            pid = m.decode() if isinstance(m, bytes) else str(m)
            pname = await DB.hget_one(f"player:{pid}", "name")
            if pname:
                name_map[pname.lower()] = pid
    return name_map


async def save_set_pieces(data, name_to_pid: dict[str, str]) -> int:
    """Parse set-piece *data* and update ``player:{id}:meta`` fields.

    Args:
        data:          Raw JSON from ``/api/team/set-piece-notes/``.
        name_to_pid:   Pre-built ``{lowercase_name: player_id}`` lookup.

    Returns:
        Number of meta fields updated.
    """
    update_count = 0

    # Handle both list and dict response shapes
    entries = (
        data
        if isinstance(data, list)
        else list(data.values())
        if isinstance(data, dict)
        else []
    )

    for team_entry in entries:
        if not isinstance(team_entry, dict):
            continue

        notes = team_entry.get("notes", [])
        if not notes:
            continue

        for idx, note in enumerate(notes):
            # Extract the note text
            if isinstance(note, dict):
                note_text = (
                    note.get("info_message", "")
                    or note.get("text", "")
                    or ""
                )
            elif isinstance(note, str):
                note_text = note
            else:
                continue

            if not note_text:
                continue

            # Classify note type
            sp_field = classify_note(note_text)
            if not sp_field:
                continue

            # Strategy 1: structured element ID from note data
            element_id = (
                note.get("element") if isinstance(note, dict) else None
            )

            # Strategy 2: name-based matching in the text
            if not element_id:
                for pname, pid in name_to_pid.items():
                    if pname in note_text.lower():
                        element_id = pid
                        break

            if element_id:
                order = idx + 1
                await DB.hset_one(
                    f"player:{element_id}:meta", sp_field, str(order)
                )
                update_count += 1
                LOG.info(
                    f"player:{element_id}:meta → {sp_field}={order}"
                )

    return update_count
