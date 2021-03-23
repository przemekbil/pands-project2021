# Program to analyse data from Iris dataset
# Author: Przemyslaw Bil

import pandas as pd 
import os
import matplotlib.pyplot as plt

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(THIS_FOLDER, '../Data/')

atribute_file = os.path.join(DATA_PATH, 'atribute.names')
data_file = os.path.join(DATA_PATH, 'iris.data')

af = pd.read_csv(atribute_file, header=None, squeeze=True, dtype=str)
df = pd.read_csv(data_file, header=None)

# As a header row use a Series read from the atribute_file:
df.columns = af

# Calculate mean values for each class
mean_values = df.groupby('class').mean()
print(mean_values)

# plot a boxplot for each class for all 4 atributes:
df.groupby('class').boxplot(rot=45, fontsize=8, figsize=(8,10))
plt.show()


#print(df)
