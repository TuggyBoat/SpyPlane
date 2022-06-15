# Data

Initial data setup with eddb dumps
```bash
wget -q -N https://eddb.io/archive/v6/systems_populated.jsonl -P ./workspace;
cat ./workspace/systems_populated.jsonl | jq -r '[.id, .edsm_id, .name, .x, .y, .z, .population, .is_populated, .government_id, .government, .allegiance_id, .allegiance, ([.states[].name]|join(",")), .security_id, .security, .primary_economy_id, .primary_economy, .power, .power_state, .power_state_id, .needs_permit, .updated_at, .minor_factions_updated_at, .simbad_ref, .controlling_minor_faction_id, .controlling_minor_faction, .reserve_type_id, .reserve_type, .ed_system_address] | @csv'  > ./workspace/systems.csv
```
