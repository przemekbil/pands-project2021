# pands-project2021
Repository for the final project of the GMIT Programming and Scripting 2021

The Fisher’s Iris data set comes from the 1936 R. A. Fisher paper “The use of multiple measurements in taxonomic problems”. In this paper, the author tackles the problem on how to distinguish between 3 different species of Iris flowers using the measurements of their 4 characteristics (Petal’s and Sepals length and width). The method used in this paper focuses on finding a linear function of these four measurements that would maximize the ratio of the difference between the means to the standard deviations within species. The larger this ratio gets the easier it is to distinguish between different species using the measurement data. 

This repository contains the following folders:

Code – this is the directory where all the Python codes is stored
	analysis.py – main program
	fishermodule.py – this file contains the ‘fisheranalysys’ function that recreates results of Fisher’s paper. This function is called from the main program.

Data – this directory stores the Fisher’s Iris data set in 2 files downloaded from https://archive.ics.uci.edu/ml/datasets/iris:
    -iris.data – file with the data without the attribute names
    -attribute.names – file with the attribute names only

Out – the “Out” directory stores all the output files from the Python code

Papers – Fischer’s original paper downloaded from https://onlinelibrary.wiley.com/doi/epdf/10.1111/j.1469-1809.1936.tb02137.x