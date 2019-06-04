import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class DataCollection:
	"""
	A collection of dataframes and corresponding columns of interest
	"""
	def __init__(self, data = [], columns = []):
		"""
		data is a list of dataframes
		columns is a list of lists of column names

		Has 4 attributes
		data: list of pandas dataframes
		columns: list of column names of interest for each dataframe (default all columns)
		size: number of dataframes in collection
		mins: minimum values for each column in data collection (used for background correction when plotting heatmaps)
		"""
		if data == pd.core.frame.DataFrame:
			data = [data]
		self.data = data

		if columns == []:
			self.columns = []
			for df in data:
				self.columns.append(list(df.columns.values))
		else:
			self.columns = columns

		self.size = len(data)
		self.mins = []
		for df in data:
			self.mins.append(df.min())
		self.mins = pd.concat(self.mins)

	def addFrame(self, df, columns = None):
		assert df == pd.core.frame.DataFrame, "data must be a dataframe!"

		self.data.append(df)
		self.columns.append(columns)
		self.size += 1
		self.mins = pd.concat([self.mins, df.min()])

	def mergeDataframes(self):
		"""
		merge dataframes held within collection
		joined on index values

		outer joins are performed and rows with NA values are dropped
		if genes are duplicated, only the first is considered
		"""
		assert self.size > 1, "Only one dataframe in collection"

		dataframes = []

		print("Merging Dataframes...")

		dfs = self.data
		cs = self.columns

		output_df = dfs[0][cs[0]].join(dfs[1][cs[0]])
		if len(dfs) > 2:
			for i in range(2, len(dfs)):
				output_df = output_df.join(dfs[i][cs[i]], how = 'outer')

		# merge and clean up 
		outputdf = outputdf.dropna()
		outputdf = outputdf[~outputdf.index.duplicated(keep = 'first')]

		print(outputdf.shape[0], "values in intersection")

		return outputdf

	def findGenes(self, genes, fill = 0):
		"""
		Finds expression values of a list of genes within dataframes passed. 
		Index of dataframe must be gene symbols.

		dataframes: a dataframe or list of dataframes
		columns: list of lists of column names from which to look for data
			each individual list corresponds to the number of 
		genes: list of genes to search for
		fill: value with which to fill missing values
		"""
		data = self.data
		columns = self.columns

		if self.size == 1:
			if columns[0] is None:
				return data[0].reindex(genes).fillna(fill)
			else: 
				return data[0][columns].reindex(genes).fillna(fill)

		elif type(data) == list:
			assert len(data) == len(columns), "number of column lists passed must match number of dataframes"
			dataframes = []

			for i in range(len(data)):
				df = data[i]
				c = columns[i]
				if c is None:
					dataframes.append(df.reindex(genes).fillna(fill))
				else:
					dataframes.append(df[c].reindex(genes).fillna(fill))

			output_df = dataframes[0].join(dataframes[1])
			if len(dataframes) > 2:
				for i in range(2, len(dataframes)):
					output_df = output_df.join(dataframes[i], how = 'outer')
			return output_df
		else:
			raise Exception("data must be a dataframe or a list of dataframes")

	def plotHeatmap(self, genes, save = False, filename = 'figure.jpg', figsize = (5, 5), filterBackground = True):

		df = self.findGenes(genes)
		df = df - self.mins
		df = df.clip(lower = 0)

		fig, ax = plt.subplots(figsize = figsize)
		sns.heatmap(np.log2(df + 1), yticklabels = df.index.values, cmap = sns.color_palette("RdBu_r", 100))
		plt.yticks(rotation=0) 
		if save:
			plt.savefig(filename, bbox_inches = 'tight')

	def filterSubsets(self, threshold = 1):
		"""
		filters each dataframe within self.data for genes above a threshold (default 1)
		returns list of filtered dataframes
		"""
		filtered = []
		for df in self.data:
			df_filtered = df[df.mean(axis = 1) > threshold]
			filtered.append(df_filtered)
		return filtered
