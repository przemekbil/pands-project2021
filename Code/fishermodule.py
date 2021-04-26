# module that analyses data as per paper'Multiple measurements in Taxonomic Problems' by R. A Fisher,
# page, table and figure references below are to this paper
#
# Autor: Przemyslaw Bil

import matplotlib.pyplot as plt
import seaborn as sbr
import pandas as pd 
import os
from dofmodule import *

def fisheranalysys(df, outpath, outfilename, counter):

    # https://stackoverflow.com/questions/33768122/python-pandas-dataframe-how-to-multiply-entire-column-with-a-scalar
    fm = df.copy()
    # values for the coefficients taken from p186
    fm['sepal length'] = df['sepal length'].multiply(-3.308998)
    fm['sepal width'] = df['sepal width'].multiply(-2.759132)
    fm['petal length'] = df['petal length'].multiply(8.866048)
    fm['petal width'] = df['petal width'].multiply(9.392551)

    # https://stackoverflow.com/questions/25748683/pandas-sum-dataframe-rows-for-given-columns
    col_list = list(fm)
    col_list.remove('class')
    fm['sum']= fm[col_list].sum(axis=1)

    # Create data frame with only class and compound measurement values
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html
    compund = fm.drop(['sepal length','sepal width','petal length','petal width'], axis=1)

    # Calculate mean values and Standard deviation as in Table IX p187
    tableix = compund.groupby('class').mean()
    tableix['Std Dev']=compund.groupby('class').std()

    tableix = tableix.rename(columns={"sum": "Mean"})

    # change current folder to Out folder:
    os.chdir(outpath)

    with open(outfilename, "at") as outfile:
        printtable("Table {}: Mean values and standard deviation of the compound measurement per species as per Table IX from Fisher paper".format(counter.getTab()), tableix, outfile)

    # Create the histograms for the compound measurement, same as Fig1 on p188
    #https://seaborn.pydata.org/generated/seaborn.histplot.html
    sbr.histplot(compund, x="sum", hue="class", binwidth=2, kde=True)

    # save the histogram for the compound Fisher variable
    plt.savefig(counter.getFig('fisherFig1.png'), dpi=150)
    plt.close()