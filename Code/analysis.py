# Program to analyse data from Iris dataset
# Author: Przemyslaw Bil

import pandas as pd 
import os
import matplotlib.pyplot as plt
import seaborn as sbr
from fishermodule import *

def getdata():

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(THIS_FOLDER, '../Data/')

    atribute_file = os.path.join(DATA_PATH, 'atribute.names')
    data_file = os.path.join(DATA_PATH, 'iris.data')

    # squeeze=True - If the parsed data only contains one column then return a Series (https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
    af = pd.read_csv(atribute_file, header=None, squeeze=True, dtype=str)
    df = pd.read_csv(data_file, header=None)

    # As a header row use a Series read from the atribute_file:
    df.columns = af

    # Return data frame with added header
    return df


def outsummary(subset):
    # get a name of the atribute from the name of the second column
    att = subset.columns[1]
    # calculate the mean of this attribute for every class
    stats = subset.groupby('class').mean()
    # calculate the standard deviation of this attribute for every class
    stats['Std dev'] = subset.groupby('class').std()
    # change the name of the attribute column to Mean
    stats = stats.rename(columns={att: 'Mean'})
    # print the stats on the screen (change this to output to the file)
    print("\n Summary for {}".format(att))
    print(stats)

# Read the data from iris.data and add the columns names from atribute.names
iris = getdata()

# iterate through the columns of the iris dataset
for column in iris.columns:
    # if the name of the column is not class, call the outsummary function and pass the subset of the data with only 2 column: class and 1 attribute
    if column!='class':
        outsummary(iris[['class', column]])

# call the function that recreates calculations from the classic Fisher paper
fisheranalysys(iris)

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
