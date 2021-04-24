# Program to analyse data from Iris dataset
# Author: Przemyslaw Bil

import pandas as pd
import math
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sbr
from fishermodule import *

# this function will read data from the data files and will return pandas data frame df
def getdata(datapath):

    verbose("Reading file: ")

    atribute_file = os.path.join(datapath, 'atribute.names')
    data_file = os.path.join(datapath, 'iris.data')

    # squeeze=True - If the parsed data only contains one column then return a Series (https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
    af = pd.read_csv(atribute_file, header=None, squeeze=True, dtype=str)
    df = pd.read_csv(data_file, header=None)

    # As a header row use a Series read from the atribute_file:
    df.columns = af

    verbose()

    # Return data frame with added header
    return df

# This function accepts a subset of the data with 2 columns: class description and one variable
# The output is a text file with descriptive stats and the histogram
# File name for the histogram and the text file are taken from the second column name
def outsummary(subset, outpath):

    # get a name of the atribute from the name of the second column
    atribute = subset.columns[1]


    verbose("Output summary data for "+atribute+":")

    # calculate the mean of this attribute for every class
    stats = subset.groupby('class').mean()

    # calculate the standard deviation of this attribute for every class
    stats['Std dev'] = subset.groupby('class').std()

    # calculate min and max values per class
    stats['min'] = subset.groupby('class').min()
    stats['max'] = subset.groupby('class').max()

    # change the name of the attribute column to Mean
    stats = stats.rename(columns={atribute: 'Mean'})

    # calculate mean +/- 3*std, where we expect to find 99.7% of obeservations (only if data is distributed normally)
    stats['Mean - 3std'] = stats['Mean'] - stats['Std dev'] * 3
    stats['Mean + 3std'] = stats['Mean'] + stats['Std dev'] * 3

    # Change current folder to /Out folder (as per https://docs.python.org/3/library/os.html#os-file-dir)
    os.chdir(outpath)

    # Append calculated descriptive stats to a single file
    with open("Summary.txt", "at") as outfile:
        outfile.write("Summary for {}\n".format(atribute))
        # Output as perhttps://stackoverflow.com/questions/31247198/python-pandas-write-content-of-dataframe-into-text-file
        # and https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_string.html
        stats.to_string(outfile)
        # add empty line after the table
        outfile.write("\n\n")

    verbose()


    # The following part will output histogram, different coulous for each class

    # First, calculate the width of the bins
    # calculate histogram bin width: https://www.qimacros.com/histogram-excel/how-to-determine-histogram-bin-interval/#:~:text=Calculate%20the%20number%20of%20bins%20by%20taking%20the%20square%20root,)%20by%20the%20%23%20of%20bins.
    #nrofbins = math.ceil(math.sqrt(subset.count()/3))
    #binw = (subset[atribute].max()-subset[atribute].min())/nrofbins

    verbose("Output histogram for "+atribute+":")
    # Create histogram using seaborn library, add probability density function (kde=True)
    sbr.histplot(subset, x=atribute, hue="class", kde=True)

    # output the histogram to png file named after the attribute name
    plt.savefig(atribute+" histogram.png", dpi=150)

    # Added as per https://stackoverflow.com/questions/57533954/how-to-close-seaborn-plots
    # Without plt.close(), each next histogram was printed with the data from the previous ones
    plt.close()
    verbose()

    verbose("Output boxplot for "+atribute+":")
    # because histograms for different classes are overlapping, it's better to use boxplot to show the data distribution
    #https://seaborn.pydata.org/generated/seaborn.boxplot.html
    sbr.boxplot(data=subset, y=atribute, x="class")

    # output the BOXPLOT to png file named after the attribute name
    plt.savefig(atribute+" boxplot.png", dpi=150)
    plt.close()

    verbose()
    
    verbose("Output violin plot for "+atribute+":")
    # violin plot displays similar information as boxplot and hostogram together
    # https://seaborn.pydata.org/generated/seaborn.violinplot.html
    sbr.violinplot(data=subset, y=atribute, x="class")
    plt.savefig(atribute+" violin plot.png", dpi=150)
    plt.close()
    

    verbose()

# this function will check if this script was called with -v or -V argument, then it will return true. False for all the rest arg values or no arguments
def isverbose():
    if len(sys.argv)==2 and (sys.argv[1]=="-v" or sys.argv[1]=="-V" ):
        # if one arguments was specified in the command line, check if it's v or V for verbose. Ignore all the rest. 
        return True
    else:
        return False

# The idea for defining this function this way, taken from: https://stackoverflow.com/questions/5980042/how-to-implement-the-verbose-or-v-option-into-a-script
# if verbose() returns true, function for displaying messages will be defined, if it's false, lambda function will be defined (do nothing function)
if isverbose():
    def verbose(msg=" Done"):
    # default message is "Done", if function is called without argument, "Done will be printed"
    # this is simplified version of the progress bar from: https://stackoverflow.com/questions/3160699/python-progress-bar
    # sys.stdout.write used instead of print to make sure "Done" is printed in the same line as the message text
        sys.stdout.write(msg)
        sys.stdout.flush()
        # go to new line after "Done" message
        if msg==" Done":
            sys.stdout.write("\n")
else:
    # define verbose as lambda function: do nothing
    verbose = lambda *a: None


# initialize folder locations:
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
datafolder = os.path.join(THIS_FOLDER, '../Data/')
outfolder = os.path.join(THIS_FOLDER, '../Out/')


# Read the data from iris.data and add the columns names from atribute.names
iris = getdata(datafolder)

# Open Summary.txt in write mode to clear any previous info while adding the header
with open(os.path.join(outfolder, "Summary.txt") , "w") as outfile:
    outfile.write("Descriptive statistics for each variable in the Iris dataset\n\n")


# iterate through the columns of the iris dataset
# to create histograms, boxplots and descriptive statistics summary for each variable 
for column in iris.columns:
    # if the name of the column is not class, call the outsummary function and pass the subset of the data with only 2 column: class and 1 attribute
    if column!='class':
        # get a subset as per https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html
        outsummary(iris[['class', column]], outfolder)



# Exploratory analysis as per: https://www.youtube.com/watch?v=-o3AxdVcUtQ
verbose("Descriptive statistics: ")
with open(os.path.join(outfolder, "Summary.txt") , "a") as outfile:
    iris.groupby("class").describe().to_string(outfile)

verbose()

classes = iris['class'].unique()

for classtype in classes:
    verbose("{} correlation matrix: ".format(classtype))
    correlation = iris[iris['class']==classtype].corr()
    with open(os.path.join(outfolder, "Summary.txt") , "a") as outfile:
        outfile.write("\n\nCorrelation matrix for {}\n\n".format(classtype))
        correlation.to_string(outfile)    
    sbr.heatmap(correlation, xticklabels=correlation.columns, yticklabels=correlation.columns, annot=True)
    plt.savefig(classtype +' Correlation heat map.png', dpi=150)
    plt.close()
    verbose()

verbose("Output scatter plot:")
# Create 6 scatter plots for 4 independent variables
# Exploratory data analysis as per https://www.youtube.com/watch?v=FLuqwQgSBDw 
sbr.set_style("whitegrid")
scatt = sbr.pairplot(iris, hue="class", height=3).add_legend()
plt.savefig('scatter plot.png', dpi=150)
plt.close()

verbose()

verbose("Replicate Fisher results:")
# call the function that recreates calculations from the classic Fisher paper
fisheranalysys(iris, outfolder)
verbose()