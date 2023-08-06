from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator
import pandas as pd
import numpy as np
from collections import Counter

class RankMatrix():
    """
    Calculate the representetive from a Multiple Sequence Alignment by creating an identity matrix
    and scoring them
    """
    def __init__(self,filename):
        self.filename=filename
        self.dm=self.__create_dm()
        self.df=self.__convert_df()
        self.ranked=self.__rank()

    def __create_dm(self):  #creating an Percentage Identity Matrix (PIM) from a MSA file
        alignment = AlignIO.read(self.filename,"fasta")
        calculator = DistanceCalculator('identity')
        dm = calculator.get_distance(alignment)
        return dm

    def __convert_df(self): #convert it into a DataFrame
        columns=self.dm.names
        self.ids=self.dm.names
        dataf = pd.DataFrame(self.dm.matrix, columns=columns, index=self.ids)
        np.fill_diagonal(dataf.values,'NaN')    #Fill the self sequences with NaN so it does not get considered
        return dataf

    def __rank(self):
        list_to_rank=list()
        for x in self.ids:
            list_to_rank.extend(list(self.df.index[self.df[x] == self.df[x].min()]))    #get the minValue of a column and then get all the ids in the row those are equal that minValue
        self.ranked=iter(Counter(list_to_rank).most_common())

        return self.ranked

    def iterator(self):
        return next(self.ranked,'End of List')
