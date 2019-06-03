import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def collect(df_list, names_list):
		"""
		collects a list of dataframes and a list of column names per data frame into a list of tuples.
		Meant to be used with mergeDataframes
		"""

		if names_list is not None:
			assert len(df_list) == len(names_list), "number of names don't match number of dataframes"

		output = []
		for i in range(len(df_list)):
			output.append((df_list[i], names_list[i]))
		return output

def mergeDataframes(df_list, names_list):
	"""
	merge a set of list of dataframes. 
	input is a list of tuples
	each tuple has a dataframe and a list of associated column names you wish to include. 
	structure would look like [(df1, names1), (df2, names2), ... (dfn, namesn)]

	if names == None then include all columns 

	outer joins are performed and rows with NA values are dropped
	if genes are duplicated, only the first is considered
	"""
	assert len(df_list) > 1, "Only one dataframe in list. No need to merge."

	print("Merging Dataframes...")
	dataframes = collect(df_list, names_list)

	# initialize outputdf
	df, names = dataframes[0]
	if names == None:
		outputdf = df
	else:
		outputdf = df[names]

	for d in dataframes[1:]:
		df, names = d
		df = df[~df.index.duplicated(keep = 'first')]

		if names == None:
			outputdf = outputdf.join(df, how = 'outer')
		else:
			outputdf = outputdf.join(df[names], how = 'outer')
			
		# merge and clean up 
		outputdf = outputdf.dropna()
		outputdf = outputdf[~outputdf.index.duplicated(keep = 'first')]

	print(outputdf.shape[0], "values in intersection")

	return outputdf
