# Changelog
## Update 1.0.2
### database.py
- added 'scout_system_data' for possible future use and 'update_system' for updating the table

### Helpers.py
- updated `get_ebgs_systems` to allow for bulk api fetching, def is unused as of now

### ScoutData.py
- fixed incorrect labeling of variables

### Created ScoutSystemData.py

### Sheets.py
- updated system posting to reduce amount of systems posted in both Secondary and Tertiary lists

### SystemScouter.py
- added fallback for NoneType return on call for emoji from database
## Version 1.0.1
### application.py
- moved listener call to run definition for docker compatibility

### constants.py
- added agent color for embed styling

### setup.py
- fixed classes not being listed in packages

### SpyPlaneCommands.py
- spy_plane_system_states_report now calls get_systems() for embed creation

### SystemFactionStatesReporter.py
- added retreating factions to report
- change create_faction_states_embed to allow for generic list support
- changed delayed_system_state_update to account for late tick detections and dynamically calculate time needed between tick and report

### SystemScouter.py
- changed delayed_scout_update to account for late tick detections and dynamically calculate time needed between tick and report

### TickWebSocket.py
- added check to avoid scouting and updates if tick is within 12 hours of the last

### Other
- created Dockerfile

## Version 1.0.0 - Fully Functional Version
### application.py
- updated docstring

### constants.py
- added monitoring channel ids
- added function for operative role and op_plus list 

### database.py
- added `get_system_state_interval` which gets the system state interval report from the database
- added `get_monitoring_channel_id` which does the same as above
- added `get_scout_emoji_id` which does the same as above

### Helpers.py
- removed unused `get_faction_systems` function
- added check role helpers for command restriction

### SpyPlaneCommands.py
- added `check_roles` verification to commands
- commented out debug command
- added `spy_plane_system_states_report` for reporting faction states in scouting systems

### Created SystemFactionStatesReporter.py
- Adds functions for creating the report embed for faction states in scouting systems

### SystemScouter.py
- updated `post_scouting` to get emoji id from database

### TickWebSocket.py
- added logging print to `check_tick`
- added faction state reporting to initial startup sequence
- added scout posting and state posting to new tick detection


## Version 0.2.0
### application.py
- added `on_bot_ready` to start socket client and fix overwrite issue with on_ready calls

### constants.py
- added constants for roles, emoji and default intervals

### database.py
- added call to add default scout interval to the config database
- insured unique config settings in table creation
- added some docstrings
- added `get_scout_interval` which returns the default interval or the set interval from the database
- added `get_all_configs` which returns all config settings from the config table
- added `update_config` for updating config settings in the database
- added `find_config` which finds a config given string in the database
- added `scouting_data_to_csv` which sends a discord message given interaction with a csv of faction member scouting data

### Helpers.py
- added `get_ebgs_system` which requests a system's data from the ebgs api given system name string

### Sheets.py
- `update_row` now updates the dataframe object also
- `get_systems` now also returns the timestamp on each system
- added `post_list_by_priority` which filters each system from `get_systems` by time since last system update, from both the database and ebgs calls

### SpyPlaneCommands.py
- `spy_plane_launch` now only calls `post_scouting()`
- added `spy_plane_config_list` which posts an embed of all config settings and their values from the database
- added `spy_plane_update_config` which allows for updating of a config setting's value in the database
- added `spy_plane_scouting_report` for calling `scouting_data_to_csv`

### SystemScouter.py
- updated `delayed_scout_update` to get scout interval from database rather than hard coded interval
- updated docstrings

### TickWebSocket.py
- updated `check_tick` to properly handle error from None type
## 0.1.0
Majority of functionality built & first commit
