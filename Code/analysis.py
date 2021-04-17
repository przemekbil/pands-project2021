# Program to analyse data from Iris dataset
# Author: Przemyslaw Bil

import pandas as pd
import math
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

# This function accepts a subset of the data with 2 columns: class description and one variable
# The output is a text file with descriptive stats and the histogram
# File name for the histogram and the text file are taken from the second column name
def outsummary(subset, outpath):
    # get a name of the atribute from the name of the second column
    atribute = subset.columns[1]

    # calculate the mean of this attribute for every class
    stats = subset.groupby('class').mean()

    # calculate the standard deviation of this attribute for every class
    stats['Std dev'] = subset.groupby('class').std()

    # change the name of the attribute column to Mean
    stats = stats.rename(columns={atribute: 'Mean'})

    # Change current folder to /Out folder (as per https://docs.python.org/3/library/os.html#os-file-dir)
    os.chdir(outpath)

    # Output calculated descriptive stats to file name after the attribute name
    with open(atribute+".txt", "wt") as outfile:
        outfile.write("Summary for {}\n".format(atribute))
        # Output as perhttps://stackoverflow.com/questions/31247198/python-pandas-write-content-of-dataframe-into-text-file
        # and https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_string.html
        stats.to_string(outfile)
    
    # The following part will output histogram, different coulous for each class

    # First, calculate the width of the bins
    # calculate histogram bin width: https://www.qimacros.com/histogram-excel/how-to-determine-histogram-bin-interval/#:~:text=Calculate%20the%20number%20of%20bins%20by%20taking%20the%20square%20root,)%20by%20the%20%23%20of%20bins.
    #nrofbins = math.ceil(math.sqrt(subset.count()/3))
    #binw = (subset[atribute].max()-subset[atribute].min())/nrofbins

    # Create histogram using seaborn library
    sbr.histplot(subset, x=atribute, hue="class")

    # output the histogram to png file named after the attribute name
    plt.savefig(atribute+" histogram.png", dpi=150)

    # Added as per https://stackoverflow.com/questions/57533954/how-to-close-seaborn-plots
    # Without plt.close(), each next histogram was printed with the data from the previous ones
    plt.close()

    # because histograms for different classes are overlapping, it's better to use boxplot to show the data distribution
    #https://seaborn.pydata.org/generated/seaborn.boxplot.html
    sbr.boxplot(data=subset, y=atribute, x="class")

    # output the BOXPLOT to png file named after the attribute name
    plt.savefig(atribute+" boxplot.png", dpi=150)
    plt.close()

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


# Exploratory data analysis as per https://www.youtube.com/watch?v=FLuqwQgSBDw part 1, 2 and 3
sbr.set_style("whitegrid")
scatt = sbr.pairplot(iris, hue="class", height=3).add_legend()
plt.savefig('scatter plot.png', dpi=150)
plt.close()


# call the function that recreates calculations from the classic Fisher paper
fisheranalysys(iris, outfolder)



#print(df)
