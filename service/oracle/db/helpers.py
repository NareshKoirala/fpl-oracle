"""
Shared helpers for Redis DB writer modules.

Provides the generic field mapper and reverse field-name lookups
used by every writer to translate FPL API responses into data_struct
templates before writing to Redis.
"""

from service.oracle.config.data_maps import (
    FIXTURE_MAP,
    PLAYER_GW_KEY_MAP,
    PLAYERS_KEY_MAP,
)


# =============================================================================
# REVERSE FIELD MAPS  (struct_field → api_field)
# =============================================================================
# PLAYERS_KEY_MAP is api→struct.  Reverse it so writers can iterate the
# template and look up the corresponding API field name.

PLAYER_FIELD_MAP = {v: k for k, v in PLAYERS_KEY_MAP.items()}
# Fix: team_id should reference 'team' (FPL team ID 1-20), not 'team_code'
# (a legacy asset code).  team:{id} keys use FPL team ID, so the FK must match.
PLAYER_FIELD_MAP["team_id"] = "team"

# FIXTURE_MAP and PLAYER_GW_KEY_MAP are already struct→api.
FIXTURE_FIELD_MAP = FIXTURE_MAP
PLAYER_GW_FIELD_MAP = PLAYER_GW_KEY_MAP


# =============================================================================
# GENERIC FIELD MAPPER
# =============================================================================


def map_fields(
    template: dict,
    api_data: dict,
    field_map: dict | None = None,
) -> dict:
    """Populate a struct *template* from *api_data*.

    Args:
        template:  Data struct dict ``{field_name: default_value}``.
        api_data:  Raw API JSON dict.
        field_map: Optional ``struct_field → api_field`` overrides for
                   fields whose API name differs from the struct name.

    Returns:
        Dict with every template field populated (as strings).
        Complex values (list/dict) are replaced with the template default.
    """
    result = {}
    fm = field_map or {}

    for struct_field, default in template.items():
        api_field = fm.get(struct_field, struct_field)
        value = api_data.get(api_field)

        # Flatten complex types to default (Redis Hashes need scalars)
        if isinstance(value, (list, dict)):
            value = None

        if value is None:
            val_str = default
        elif isinstance(value, bool):
            val_str = "true" if value else "false"
        else:
            val_str = str(value)

        # Normalize uppercase booleans to lowercase
        if val_str == "True":
            val_str = "true"
        elif val_str == "False":
            val_str = "false"

        result[struct_field] = val_str

    return result


# =============================================================================
# SEASON NORMALIZER
# =============================================================================


def normalize_season(season_name: str) -> str:
    """Normalize FPL season label to end year.

    ``'2024/25'`` → ``'2025'``
    """
    if "/" in season_name:
        parts = season_name.split("/")
        short_year = parts[-1]
        century = parts[0][:2]
        return f"{century}{short_year}"
    return season_name
