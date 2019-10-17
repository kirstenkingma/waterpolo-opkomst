import urllib.request
import xlrd

def open_file(path):
    """
    Open and read an Excel file
    """
    book = xlrd.open_workbook(path)
  
    # get the first worksheet
    first_sheet = book.sheet_by_name('Trainingsopkomst')
 
    result = []
    result.append(first_sheet.row_values(0)[1:-1])
    result.append(first_sheet.row_values(3)[1:-1])

    #get percentage
    last_filled_row = -1
    for row_ix in range(first_sheet.nrows):
        if first_sheet.row_values(row_ix)[0] == '' and last_filled_row == -1:
            last_filled_row = row_ix - 1

    
    #append new row to results and then replace these with opkomst streaks
    result.append([0] * len(result[0]))
    for i in range(len(result[0])):
        streak = 0
        found_zero = False
        row_ix = last_filled_row
        while not found_zero:
            if first_sheet.row_values(row_ix)[i+1] == 1:
                streak += 1
                row_ix -= 1
            else:
                found_zero = True

        result[2][i] = streak

    #append new row to results and replace these with absent streaks
    result.append([0] * len(result[0]))
    for i in range(len(result[0])):
        streak = 0
        found_one = False
        row_ix = last_filled_row
        while not found_one:
            if first_sheet.row_values(row_ix)[i+1] == 0:
                streak += 1
                row_ix -= 1
            else:
                found_one = True

        result[3][i] = streak

        

    return result

import os

dir = os.path.dirname(os.path.realpath(__file__))

url = "https://onedrive.live.com/download?resid=C9DD30BE568D26CA!2229&ithint=file%2cxlsx&authkey=!AiHTgfShXL0Mdv4"
file_name = dir+"/static/opkomst.xlsx"

# Download the file from `url` and save it locally under `file_name`:
urllib.request.urlretrieve(url, file_name)


stats = open_file(file_name)

result = "naam,percentage,opkomststreak,absentstreak \n"
for i in range(len(stats[0])):
    result = result + stats[0][i] + "," + str(stats[1][i]) + "," + str(stats[2][i]) + "," + str(stats[3][i]) + "\n"

with open(dir+'/static/opkomst.csv', 'w') as the_file:
    the_file.write(result)

print("success")
 
