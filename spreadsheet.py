def spreadsheet(data = [[5,4],[1, 2],[3, 4],[6,7],[3,4]]):
    import socket
    old_getaddrinfo = socket.getaddrinfo
    def new_getaddrinfo(*args, **kwargs):
        responses = old_getaddrinfo(*args, **kwargs)
        return [response
            for response in responses
            if response[0] == socket.AF_INET]
    socket.getaddrinfo = new_getaddrinfo
    from sheetfu import SpreadsheetApp

    

    sa = SpreadsheetApp('newkey.json')
    spreadsheet = sa.open_by_id('1t60CvJSHba-j9ZGHFIIWmA5i4n25Fn82E7Xhox6L3oU')
    sheet = spreadsheet.get_sheet_by_name('Sheet1')
    range = sheet.get_data_range() 
    print(range.coordinates.number_of_rows)

    data_range = sheet.get_range(row=range.coordinates.number_of_rows+1,column=1,number_of_row=len(data), number_of_column=len(data[0]))
    try:
        data_range.set_values(data) 
    except:
        print("ERROR")
spreadsheet()
