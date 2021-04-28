# Program to analyse data from Iris dataset
# Author: Przemyslaw Bil

import pandas as pd
import numpy as np
import math
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sbr
from fishermodule import *
from dofmodule import *
from scipy.stats import normaltest

# this function will read data from the data files and will return pandas data frame df
def getdata(datapath):

    verbose.out("Reading file: ")

    atribute_file = os.path.join(datapath, 'atribute.names')
    data_file = os.path.join(datapath, 'iris.data')

    # squeeze=True - If the parsed data only contains one column then return a Series (https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
    af = pd.read_csv(atribute_file, header=None, squeeze=True, dtype=str)
    df = pd.read_csv(data_file, header=None)

    # As a header row use a Series read from the atribute_file:
    df.columns = af

    verbose.close()

    # Return data frame with added header
    return df

# This function accepts a subset of the data with 2 columns: class description and one variable
# The output is a text file with descriptive stats and the histogram
# File name for the histogram and the text file are taken from the second column name
def outsummary(subset, outpath):

    # get a name of the atribute from the name of the second column
    atribute = subset.columns[1]


    verbose.out("Output summary data for "+atribute+":")

    # calculate the mean of this attribute for every class
    stats = subset.groupby('class').describe()

    # calculate mean +/- 3*std, where we expect to find 99.7% of obeservations (only if data is distributed normally)
   
    stats['Mean - 3std'] = subset.groupby('class').mean() - subset.groupby('class').std() * 3
    stats['Mean + 3std'] = subset.groupby('class').mean() + subset.groupby('class').std() * 3

    # normality test as per:https://machinelearningmastery.com/a-gentle-introduction-to-normality-tests-in-python/
    # and https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.normaltest.html
    for classtype in subset['class'].unique():
        class_subset = subset[subset['class'] == classtype]
        
        # Calculate normality test for each class separately
        stat, p = normaltest(class_subset[atribute])
        # access single cell in the data frame: https://kanoki.org/2019/04/12/pandas-how-to-get-a-cell-value-and-update-it/
        stats.at[classtype,'Statistics'] = stat
        stats.at[classtype,'pValue'] = p


    # Append calculated descriptive stats to a Summary.txt file
    with open("Summary.txt", "at") as outfile:
        printtable("Table {}: Descriptive statistics groupped by Class for {}".format(counter.getTab(), atribute), stats, outfile)

    verbose.close()


    # The following part will output histogram, different coulous for each class

    # First, calculate the width of the bins
    # calculate histogram bin width: https://www.qimacros.com/histogram-excel/how-to-determine-histogram-bin-interval/#:~:text=Calculate%20the%20number%20of%20bins%20by%20taking%20the%20square%20root,)%20by%20the%20%23%20of%20bins.
    #nrofbins = math.ceil(math.sqrt(subset.count()/3))
    #binw = (subset[atribute].max()-subset[atribute].min())/nrofbins

    verbose.out("Output histogram for "+atribute+":")
    # Create histogram using seaborn library, add probability density function (kde=True)
    sbr.histplot(subset, x=atribute, hue="class", kde=True)

    # output the histogram to png file named after the attribute name
    plt.savefig(counter.getFig(atribute + " histogram.png"), dpi=150)

    # Added as per https://stackoverflow.com/questions/57533954/how-to-close-seaborn-plots
    # Without plt.close(), each next histogram was printed with the data from the previous ones
    plt.close()
    verbose.close()

    verbose.out("Output boxplot for "+atribute+":")
    # because histograms for different classes are overlapping, it's better to use boxplot to show the data distribution
    #https://seaborn.pydata.org/generated/seaborn.boxplot.html
    sbr.boxplot(data=subset, y=atribute, x="class")

    # output the BOXPLOT to png file named after the attribute name
    plt.savefig(counter.getFig(atribute + " boxplot.png"), dpi=150)
    plt.close()

    verbose.close()
    
    verbose.out("Output violin plot for "+atribute+":")
    # violin plot displays similar information as boxplot and hostogram together
    # https://seaborn.pydata.org/generated/seaborn.violinplot.html
    sbr.violinplot(data=subset, y=atribute, x="class")
    plt.savefig(counter.getFig(atribute + " violin plot.png") , dpi=150)
    plt.close()
    
    verbose.close()

# this function will check if this script was called with -v or -V argument, then it will return true. False for all the rest arg values or no arguments
def isverbose():
    if len(sys.argv)==2 and (sys.argv[1]=="-v" or sys.argv[1]=="-V" ):
        # if one arguments was specified in the command line, check if it's v or V for verbose. Ignore all the rest. 
        return True
    else:
        return False

# initialize folder locations:
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
datafolder = os.path.join(THIS_FOLDER, '../Data/')
outfolder = os.path.join(THIS_FOLDER, '../Out/')


# initialize instance of a Counter class
counter = Counter()
# initialize instance of Verbose class
verbose = Verbose(isverbose())

# Read the data from iris.data and add the columns names from atribute.names
iris = getdata(datafolder)

# Change current folder to /Out folder (as per https://docs.python.org/3/library/os.html#os-file-dir)
os.chdir(outfolder)

# Exploratory analysis as per: https://www.youtube.com/watch?v=-o3AxdVcUtQ
verbose.out("Descriptive statistics: ")
with open(os.path.join(outfolder, "Summary.txt") , "w") as outfile:
    
    # Output descriptive stats for the whole data set
    printtable("Table {}: Simple descriptive statistics for the whole data set".format(counter.getTab()), iris.describe(), outfile)

    # Output descriptive stats for the whole data set groupped by class
    printtable("Table {}: Simple descriptive statistics for the whole data set grouped by Class".format(counter.getTab()), iris.groupby("class").describe(), outfile)

verbose.close()

verbose.out("Output boxplot for the whole data set:")
#https://seaborn.pydata.org/generated/seaborn.boxplot.html
sbr.boxplot(data=iris, orient="v")

# output the BOXPLOT to png file named after the attribute name
plt.savefig(counter.getFig("The whole data set boxplot.png"), dpi=150)
plt.close()

verbose.close()

# Add numeric class column, where  Setosa is 1, Versicolour is 2 and Virginica is 3 
# as per: https://www.dataquest.io/blog/tutorial-add-column-pandas-dataframe-based-on-if-else-condition/
#
# This will be needed to calculate a class-attribute correlation 
# as per: https://stats.stackexchange.com/questions/57776/what-is-class-correlation

verbose.out("Varaiables to Class correlation:")

# create a list of conditions
conditions = [iris['class']=='Iris-setosa', iris['class']=='Iris-versicolor', iris['class']=='Iris-virginica']

# create a list of values
values = [1,2,3]

# create a new column and use np.select assign values
iris['numClass'] = np.select(conditions, values)

# append correlation table to "Summary.txt"
with open(os.path.join(outfolder, "Summary.txt") , "a") as outfile:
    printtable("Table {}: Variable to Class correlation table".format(counter.getTab()), iris.corr().drop(['sepal length','sepal width','petal length','petal width'], axis=1).drop(['numClass']), outfile)

iris = iris.drop(['numClass'], axis=1)
verbose.close()


# iterate through the columns of the iris dataset
# to create histograms, boxplots and descriptive statistics summary for each variable 
for column in iris.columns:
    # if the name of the column is not class, call the outsummary function and pass the subset of the data with only 2 column: class and 1 attribute
    if column!='class':
        # get a subset as per https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html
        outsummary(iris[['class', column]], outfolder)


# create a new table with classes
classes = iris['class'].unique()

# step through the class types
for classtype in classes:
    verbose.out("{} correlation matrix: ".format(classtype))
    # create a correlation table for one iris class
    correlation = iris[iris['class']==classtype].corr()

    # append correlation table to "Summary.txt"
    with open(os.path.join(outfolder, "Summary.txt") , "a") as outfile:
        printtable("Table {}: Attributes correlation matrix for the class {}".format(counter.getTab(), classtype), correlation, outfile)

    # add title to heatmap correlation graphs as per https://stackoverflow.com/questions/32723798/how-do-i-add-a-title-to-seaborn-heatmap
    ax=plt.axes()
    sbr.heatmap(correlation, xticklabels=correlation.columns, yticklabels=correlation.columns, annot=True)
    ax.set_title(classtype)
    plt.savefig(counter.getFig(classtype + ' Correlation heat map.png'), dpi=150)
    plt.close()
    # print "Done"
    verbose.close()

verbose.out("Output scatter plot:")
# Create 6 scatter plots for 4 independent variables
# Exploratory data analysis as per https://www.youtube.com/watch?v=FLuqwQgSBDw 
sbr.set_style("whitegrid")
scatt = sbr.pairplot(iris, hue="class", height=3).add_legend()
plt.savefig(counter.getFig('scatter plot.png'), dpi=150)
plt.close()

verbose.close()

verbose.out("Replicate Fisher results:")
# call the function that recreates calculations from the classic Fisher paper
fisheranalysys(iris, outfolder, "Summary.txt", counter)
verbose.close()