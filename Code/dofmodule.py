# Data Out Formatting Module - dofmodule.py
# Author: Przemyslaw Bil

# Defining class Counter, to keep track of the Tables and Figures numbering
# I will create only one instance of this Class. Each time getTab or getFig method is called,
# it will return the counter incresed by 1, therefore providing a way to automatically keep track of Tables and Figures numbering
# This tutorial helped me define the methods correctly: https://realpython.com/python3-object-oriented-programming/#instance-methods
class Counter:
    tab = 0
    fig = 0

    def getTab(self):
        self.tab+=1
        # This function will return Table number only
        return self.tab
    
    def getFig(self, in_str):
        self.fig+=1
        if self.fig < 10:
            out_str = 'Figure 0' + str(self.fig) + ' - ' + in_str
        else:
            out_str = 'Figure ' + str(self.fig) + ' - ' + in_str
        # This function will return the full file name
        # There is a bit of inconsistency between these two get functions, but I decided to leave them this way
        # And focus on writing the filnal report instead
        return  out_str

# Defining printtable function, to format output of each table the same way
def printtable(title, table, tofile):
    tofile.write("----------------------------------------------------------------------------------------------------------------")
    tofile.write("\n{}\n".format(title))
    tofile.write("================================================================================================================\n")
    # Output as per https://stackoverflow.com/questions/31247198/python-pandas-write-content-of-dataframe-into-text-file
    # and https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_string.html
    table.to_string(tofile)
    tofile.write("\n----------------------------------------------------------------------------------------------------------------\n\n\n")
