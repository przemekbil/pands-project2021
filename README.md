# pands-project2021
This is the final project for the 2021 Programming and Scripting course. The purpose of this project is to analyse the Fisher’s Iris data set using Python scripting.

The Fisher’s Iris data set comes from the 1936 R. A. Fisher paper “The use of multiple measurements in taxonomic problems”. In this paper, the author tackles the problem on how to distinguish between 3 different species of Iris flowers using the measurements of their 4 characteristics (Petal’s and Sepals length and width). The method used in this paper focuses on finding a linear function of these four measurements that would maximize the ratio of the difference between the means to the standard deviations within species. The larger this ratio gets the easier it is to distinguish between different species using the measurement data. 

This repository contains the following folders:

    Code – this is the directory where all the Python codes is stored:

	    analysis.py – main program
	    fishermodule.py – this file contains the ‘fisheranalysys’ function that recreates results of Fisher’s paper. This function is called from the main program.
        dofmodule - module with Counter class and printtable function, both used for data output formatting

    Data – this directory stores the Fisher’s Iris data set in 2 files downloaded from https://archive.ics.uci.edu/ml/datasets/iris:

        -iris.data – file with the data without the attribute names
        -attribute.names – file with the attribute names only

    Out – this directory stores all the output files generated by the Python code

    Papers – Fischer’s original paper downloaded from https://onlinelibrary.wiley.com/doi/epdf/10.1111/j.1469-1809.1936.tb02137.x

    Report – the final summary of the analysis is in the file ‘PANDS 2021 Project Report.docx’ stored in this directory

Running the script:

To run the code, run the “analysis.py” file. The script can be run with “-v” command line argument, this will cause it to run in the “verbose” mode, where it will inform the user which part of the code is being executed. There are no other arguments accepted (any other arguments will be ignored) and there is no user interaction with the code once it’s starts running: once started, the program will perform all the analysis each time.


References:

https://stackoverflow.com

https://pandas.pydata.org

https://seaborn.pydata.org

https://realpython.com

https://machinelearningmastery.com

https://docs.scipy.org

https://kanoki.org

https://docs.python.org

https://www.qimacros.com

https://www.youtube.com/watch?v=-o3AxdVcUtQ

https://www.youtube.com/watch?v=FLuqwQgSBDw 

https://archive.ics.uci.edu/ml/datasets/iris

https://onlinelibrary.wiley.com/doi/epdf/10.1111/j.1469-1809.1936.tb02137.x

https://www.dataquest.io

https://stats.stackexchange.com

https://www.scribbr.com/

https://www.pythonfordatascience.org

https://towardsdatascience.com
