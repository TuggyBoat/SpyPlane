import gspread

gc = gspread.service_account(filename='/Users/zasz/repos/ptn/SpyPlane/token.json')

# Open a sheet from a spreadsheet in one go
wks = gc.open("Faction Scouting").sheet1
values_list = wks.row_values(1)
for v in values_list:
    print(v)
values_list = wks.row_values(2)
for v in values_list:
    print(v)
