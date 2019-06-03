import pandas as pd

def outputToExcel(data, filename, info = None, sheets = None):
	"""
	data is a list of pandas dataframes to be output into the new excel sheet
	filename is the name of the new excel file
	info is a list of strings that describe the contents of the excel file (default None)
		will be the first sheet in the file if specified
	sheets is a list of sheet names. Number of names should match the number of dataframes specified

	"""

	# add xlsx file extension if not included
	if filename[-5:] != '.xlsx':
		filename = filename + '.xlsx'

	# initialize excel writer
	writer = pd.ExcelWriter(filename)

	# check if sheets is specified. If not, initialize list of default sheet names
	if sheets != None:
		if type(data) == list:
			assert len(data) == len(sheets), 'number of sheet names needs to match number of dataframes'
		elif type(data) == pd.core.frame.DataFrame:
			assert len(sheets) == 1, 'number of sheet names needs to match number of dataframes'

	else:
		sheets = []
		for i in range(len(data)):
			s = 'Sheet ' + str(i + 1)
			sheets.append(s)

	# check if info sheet is provided and write it to excel
	if info != None:
		info_df = pd.DataFrame(info)
		info_df.to_excel(writer, 'info', index = False, header = ['Info'])

	# check if data is a list, else it is a single dataframe
	if type(data) == list:
		for i in range(len(data)):
			data[i].to_excel(writer, sheets[i])
	else:
		data.to_excel(writer, sheets[0])

	writer.save()

	return