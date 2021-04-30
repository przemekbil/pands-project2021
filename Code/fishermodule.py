# module that analyses data as per paper'Multiple measurements in Taxonomic Problems' by R. A Fisher,
# page, table and figure references below are to this paper
#
# Autor: Przemyslaw Bil

import matplotlib.pyplot as plt
import seaborn as sbr
import pandas as pd 
import os
from dofmodule import *


#define coefficients 
# values for the coefficients taken from p186
L1=-3.308998
L2=-2.759132
L3=8.866048
L4=9.392551



def fisheranalysys(df, outpath, outfilename, counter):

    # https://stackoverflow.com/questions/33768122/python-pandas-dataframe-how-to-multiply-entire-column-with-a-scalar
    fm = df.copy()
    fm['sepal length'] = df['sepal length'].multiply(L1)
    fm['sepal width'] = df['sepal width'].multiply(L2)
    fm['petal length'] = df['petal length'].multiply(L3)
    fm['petal width'] = df['petal width'].multiply(L4)

    # https://stackoverflow.com/questions/25748683/pandas-sum-dataframe-rows-for-given-columns
    col_list = list(fm)
    col_list.remove('class')
    fm['sum']= fm[col_list].sum(axis=1)

    # Create data frame with only class and compound measurement values (the 'sum' column)
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

    # classify records using fisfer's coefficients
    compund['classification'] = 'None'

    # iterate through dataframe as per https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
    for index, row in compund.iterrows():

        # calculate absolute distance to each Classes mean
        d_set=abs(row['sum']-tableix.at['Iris-setosa','Mean'])
        d_ver=abs(row['sum']-tableix.at['Iris-versicolor','Mean'])
        d_vir=abs(row['sum']-tableix.at['Iris-virginica','Mean'])
        
        # Find the closest one
        closest = min(d_set, d_ver, d_vir)

        # classify the Species based on the clossest mean
        if closest==d_set:
            compund.at[index, 'classification']='Iris-setosa'
        elif closest==d_ver:
            compund.at[index,'classification']='Iris-versicolor'
        else:
            compund.at[index,'classification']='Iris-virginica'
        
        
        if row['class'] == compund.at[index,'classification']:
            compund.at[index,'error'] = 0
        else:
            compund.at[index,'error'] = 1
    
    # Append classification errors summary to 'Summary.txt' file
    with open(outfilename, "at") as outfile:
        printtable("Table {}: Classification errors using Fishers method".format(counter.getTab()), compund.groupby('class')['error'].sum(), outfile)