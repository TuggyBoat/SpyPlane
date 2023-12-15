import asyncio
import pprint
import time
from datetime import datetime

import gspread
import pandas as pd

from ptn.spyplane.database.database import get_last_tick, update_system

from ptn.spyplane.constants import gc
from ptn.spyplane.modules.Helpers import get_ebgs_systems

# gc = gspread.service_account('../data/spyplane-394209-39d59161dedb.json')
# Spreadsheet
sheet = gc.open("Faction Scouting")

# Worksheet
worksheet = sheet.get_worksheet_by_id(0)

# Values
values = worksheet.get_values('A:E')
headers = values.pop(0)
sheet_dataframe = pd.DataFrame(values, columns=headers)


def get_sheet_row(row_name):
    cell = worksheet.find(row_name, in_column=1)
    row_number = cell.row
    return row_number


async def update_row(row_name, username, user_id, timestamp):
    row_number = get_sheet_row(row_name)

    try:
        # Update only the last 3 cells in the sheet
        worksheet.update_cell(row_number, 3, username)
        worksheet.update_cell(row_number, 4, str(user_id))
        worksheet.update_cell(row_number, 5, timestamp)
        df_index = sheet_dataframe[sheet_dataframe.iloc[:, 0] == row_name].index

        # update dataframe
        if not df_index.empty:
            sheet_dataframe.at[df_index[0], sheet_dataframe.columns[2]] = username
            sheet_dataframe.at[df_index[0], sheet_dataframe.columns[3]] = user_id
            sheet_dataframe.at[df_index[0], sheet_dataframe.columns[4]] = timestamp

        # update database
        await update_system(system_name=row_name, last_update=timestamp)

        return True

    except:
        return False


def get_systems():
    return sheet_dataframe[['System', 'Priority', 'Timestamp']].values.tolist()


async def post_list_by_priority():
    systems_list = get_systems()
    last_tick = int((await get_last_tick())[0].tick_time)

    api_check_systems = []
    for system in systems_list:
        dt_obj = datetime.strptime(system[2], "%d/%m/%Y %H:%M:%S")
        timestamp = int(time.mktime(dt_obj.timetuple()))
        difference_from_tick = ((last_tick - timestamp)/3600)

        # Apply initial filtering based on priority and time difference
        if difference_from_tick < 3 or \
           (difference_from_tick < 24 and system[1] == '2') or \
           (difference_from_tick < 36 and system[1] == '3'):
            continue
        else:
            api_check_systems.append(system)

    # Separate lists for each priority
    priority_1_systems = [system for system in api_check_systems if system[1] == '1']
    priority_2_systems = [system for system in api_check_systems if system[1] == '2']
    priority_3_systems = [system for system in api_check_systems if system[1] == '3']

    # Sort priority 2 and 3 systems by last scouted date in ascending order
    priority_2_systems.sort(key=lambda x: x[2])
    priority_3_systems.sort(key=lambda x: x[2])

    # Select top 50% of priority 2 systems
    half_index_p2 = len(priority_2_systems) // 2
    selected_p2_systems = priority_2_systems[:half_index_p2]

    # Select top 33% of priority 3 systems
    third_index_p3 = len(priority_3_systems) // 3
    selected_p3_systems = priority_3_systems[:third_index_p3]

    # Combine the selected systems
    valid_systems = priority_1_systems + selected_p2_systems + selected_p3_systems

    pprint.pp(valid_systems)
    return valid_systems

