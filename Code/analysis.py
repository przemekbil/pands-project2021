# Program to analyse data from Iris dataset
# Author: Przemyslaw Bil

import pandas as pd 
import os
import matplotlib.pyplot as plt
import seaborn as sbr
from fishermodule import *

def getdata(datapath):

    atribute_file = os.path.join(datapath, 'atribute.names')
    data_file = os.path.join(datapath, 'iris.data')

    # squeeze=True - If the parsed data only contains one column then return a Series (https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
    af = pd.read_csv(atribute_file, header=None, squeeze=True, dtype=str)
    df = pd.read_csv(data_file, header=None)

    # As a header row use a Series read from the atribute_file:
    df.columns = af

    # Return data frame with added header
    return df


def outsummary(subset, outpath):
    # get a name of the atribute from the name of the second column
    att = subset.columns[1]
    # calculate the mean of this attribute for every class
    stats = subset.groupby('class').mean()
    # calculate the standard deviation of this attribute for every class
    stats['Std dev'] = subset.groupby('class').std()
    # change the name of the attribute column to Mean
    stats = stats.rename(columns={att: 'Mean'})

    # Output calculated descriptive stats to separate files
    # Change current folder to /Out folder
    os.chdir(outpath)
    with open(att+".txt", "wt") as outfile:
        outfile.write("Summary for {}\n".format(att))
        # Output as perhttps://stackoverflow.com/questions/31247198/python-pandas-write-content-of-dataframe-into-text-file
        # and https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_string.html
        stats.to_string(outfile)


# initialize folder locations
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
datafolder = os.path.join(THIS_FOLDER, '../Data/')
outfolder = os.path.join(THIS_FOLDER, '../Out/')

# Read the data from iris.data and add the columns names from atribute.names
iris = getdata(datafolder)

# iterate through the columns of the iris dataset
for column in iris.columns:
    # if the name of the column is not class, call the outsummary function and pass the subset of the data with only 2 column: class and 1 attribute
    if column!='class':
        # get a subset as per https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html
        outsummary(iris[['class', column]], outfolder)

# call the function that recreates calculations from the classic Fisher paper
fisheranalysys(iris, outfolder)

'''
# Exploratory data analysis as per https://www.youtube.com/watch?v=FLuqwQgSBDw part 1, 2 and 3
sbr.set_style("whitegrid")
sbr.pairplot(iris, hue="class", height=3)\
    .add_legend()
plt.show()
'''

# plot a boxplot for each class for all 4 atributes:
# df.groupby('class').boxplot(rot=45, fontsize=8, figsize=(8,10))
# plt.show()


#print(df)
