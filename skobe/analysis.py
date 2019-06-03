import numpy as np
import pandas as pd

def logFoldChange(A, B):
	"""
	Find log fold change from A to B for two array-like objects
	"""
	fc = np.log2(B) - np.log2(A)
	return fc

def findGenes(data, columns, genes):
	"""
	Finds expression values of a list of genes within dataframes passed. 
	Index of dataframe must be gene symbols.

	dataframes: a dataframe or list of dataframes
	columns: list of lists of column names from which to look for data
		each individual list corresponds to their respective dataframe
	genes: list of genes to search for
	"""
	if type(data) == pd.core.frame.DataFrame:
		return data[columns].reindex(genes).fillna(0)
	elif type(data) == list:
		assert len(data) == len(columns), "number of column lists passed must match number of dataframes"
		dataframes = []

		for i in range(len(data)):
			df = data[i]
			c = columns[i]
			if c == None:
				dataframes.append(df.reindex(genes).fillna(0))
			else:
				dataframes.append(df[c].reindex(genes).fillna(0))

		output_df = dataframes[0].join(dataframes[1])
		if len(dataframes) > 2:
			for i in range(2, len(dataframes)):
				output_df = output_df.join(dataframes[i], how = 'outer')
		return output_df
	else:
		raise Exception("data must be a dataframe or a list of dataframes")

def filterFPKM(data, fpkm = 1):
	"""
	returns subset of genes where FPKM across all samples is > fpkm (default = 1)
	"""
	df = data[(data.T >= fpkm).all()]

	return df