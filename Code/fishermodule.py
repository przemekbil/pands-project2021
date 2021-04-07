# module that analyses data as per paper'Multiple measurements in Taxonomic Problems' by R. A Fisher 
# Autor: Przemyslaw Bil

import matplotlib.pyplot as plt
import seaborn as sbr

def fisheranalysys(df):

    # https://stackoverflow.com/questions/33768122/python-pandas-dataframe-how-to-multiply-entire-column-with-a-scalar
    fisherMethod = df.copy()
    # values for the coefficients taken from p186
    fisherMethod['sepal length'] = fisherMethod['sepal length'].multiply(-3.308998)
    fisherMethod['sepal width'] = fisherMethod['sepal width'].multiply(-2.759132)
    fisherMethod['petal length'] = fisherMethod['petal length'].multiply(8.866048)
    fisherMethod['petal width'] = fisherMethod['petal width'].multiply(9.392551)

    # https://stackoverflow.com/questions/25748683/pandas-sum-dataframe-rows-for-given-columns
    col_list = list(fisherMethod)
    col_list.remove('class')
    fisherMethod['sum']= fisherMethod[col_list].sum(axis=1)

    # Calculate mean values
    print(fisherMethod.groupby('class').mean())
    print(fisherMethod.groupby('class').std())

    #https://seaborn.pydata.org/generated/seaborn.histplot.html
    sbr.histplot(fisherMethod, x="sum", hue="class", binwidth=2)
    plt.show()