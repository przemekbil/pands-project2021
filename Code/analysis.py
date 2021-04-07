# Program to analyse data from Iris dataset
# Author: Przemyslaw Bil

import pandas as pd 
import os
import matplotlib.pyplot as plt
import seaborn as sbr
from fishermodule import *

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(THIS_FOLDER, '../Data/')

atribute_file = os.path.join(DATA_PATH, 'atribute.names')
data_file = os.path.join(DATA_PATH, 'iris.data')

# squeeze=True - If the parsed data only contains one column then return a Series (https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
af = pd.read_csv(atribute_file, header=None, squeeze=True, dtype=str)
df = pd.read_csv(data_file, header=None)

# As a header row use a Series read from the atribute_file:
df.columns = af

# Calculate mean values for each class
mean_values = df.groupby('class').mean()
print(mean_values)

fisheranalysys(df)

'''
# Exploratory data analysis as per https://www.youtube.com/watch?v=FLuqwQgSBDw part 1, 2 and 3
sbr.set_style("whitegrid")
sbr.pairplot(df, hue="class", height=3)\
    .add_legend()
plt.show()
'''

# plot a boxplot for each class for all 4 atributes:
# df.groupby('class').boxplot(rot=45, fontsize=8, figsize=(8,10))
# plt.show()


#print(df)
