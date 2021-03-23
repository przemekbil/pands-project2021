# Program to analyse data from Iris dataset
# Author: Przemyslaw Bil

import pandas as pd 
import os
import csv


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(THIS_FOLDER, '../Data/')

atribute_file = os.path.join(DATA_PATH, 'atribute.names')
data_file = os.path.join(DATA_PATH, 'iris.data')

af = pd.read_csv(atribute_file, header=None, squeeze=True, dtype=str)
df = pd.read_csv(data_file, header=None, dtype=str)
print(af)
print(df)
