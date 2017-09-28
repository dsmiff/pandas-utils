# Dominic Smith <dosmith@cern.ch>
'''
A collection of miscellaneous functions to 
perform Pandas operations
'''

import os
import glob

try:
    import pandas as pd
except ImportError:
    print "Unable to import Pandas"
import matplotlib as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 4096)
pd.set_option('display.max_rows', 65536)
pd.set_option('display.width', 1000)

##__________________________________________________________________||
class PandasHolder(object):
    '''
    Class to assign attributes to DataFrame
    '''
    def __init__(self, columns):
        self.columns = columns

    def makeDataFrame(self):
        self.df = pd.DataFrame(columns=self.columns)

    def fillDataFrame(self, info):
        if isinstance(info,list):
            for result in info:
                self.df = self.df.append(result, ignore_index=True)

    def plotDataFrame(self, variables):
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print "Unable to import matplotlib"
        plt.plot(self.df[variables[0]], self.df[variables[1]])
        plt.xlabel(r"{}".format(variables[0]))
        plt.ylabel(r"$P$")
        plt.minorticks_on()
        plt.show()
        
##__________________________________________________________________||
class PandasChecker(object):
    '''
    Class to diagnose Dataframes
    '''
    
    def __init__(self):
        pass

    @staticmethod
    def check_filled(tbl):
        if tbl.empty:
            return True
        else:
            return False
        
    @staticmethod
    def is_dict_filled(infoDict):
        return bool(infoDict)

##__________________________________________________________________||
def convertDictToDF(infoDict, variable, assignIndexName=False):
    '''
    Convert a python dictionary to a DataFrame
    '''
    
    pds_check = PandasChecker()
    if not pds_check.is_dict_filled(infoDict):
        raise Exception('Input dictionary is empty')

    d1 = pd.DataFrame.from_dict(infoDict)
    if d1.empty:
        print("DataFrame is empty")
    else:
        if assignIndexName:
            if d1.index.name is None:
                d1.index.name = variable
        else: pass

    return d1
    
##__________________________________________________________________||
def writeDFtoFile(tbl, variable, dir, prefix=None, force=False):
    '''
    Write a produced DataFrame to a txt file 
    given a variable name and output directory
    '''

    if variable is None: variable = 'out'
    if not os.path.exists(dir): os.makedirs(dir)

    tblName = os.path.join(dir,'tbl_n{}_{}.txt'.format(prefix, variable))
    if force and os.path.exists(tblName): os.remove(tblName)

    with open(tblName,'a') as f:
        tbl.to_string(f, index=True)
        f.write('\n')
        f.close()
        print('DataFrame {} written to file'.format(tblName))
    
##__________________________________________________________________||
def convertToLatex(tbl, variable, writeFile=False):
    '''
    Convert a pandas DataFrame to a latex table
    '''
    pdscheck = PandasChecker()
    is_empty = pdscheck.check_filled(tbl)
    
    if is_empty:
        raise ValueError("DataFrame is empty")

    dl = tbl.to_latex()
    if not writeFile: return dl
    else:
        with open('tbl_out.tex', 'w') as f:
            f.write(dl)
        print("LaTex table saved")

##__________________________________________________________________||
def readTable(tbldir=None, tableString=None):
    '''
    Return a DataFrame given an input directory and 
    txt file name
    '''
    
    if tbldir is not None:
        if not os.path.exists(tbldir):
            print('Dir {} not found'.format(tbldir))
        try:
            tableString = os.path.join(tbldir, tableString)
        except IOError:
            print("Nothing found")
    else:
        pass

    d1 = pd.read_table(tableString, delim_whitespace=True)
    
    return d1

##__________________________________________________________________||
def produceListOfTables(tbldir, variable):
    '''
    Return a list of txt files containing DataFrames
    '''
    
    inFileNames = glob.glob(os.path.join(tbldir,"tbl_n*"+variable+".txt"))
    inFilePath  = [fileName for fileName in inFileNames]
    fileStatus  = [os.path.exists(fileName) for fileName in inFileNames]
    if not all(fileExists is True for fileExists in fileStatus):
        raise Exception("Table not found")

    return inFilePath
    
##__________________________________________________________________||
def rearrangeColumns(tbl, varName):
    '''
    Reorder the arrangement of columns in a given DataFrame 
    By construction, varName is placed first
    '''

    cols = list(tbl.columns.values)
    varIndexList = [index for index, col in enumerate(cols) if col==varName]
    index = varIndexList[0]

    newCols = [cols[index]] + cols[:index] + cols[index+1:]
    reordered_table = tbl[newCols]

    return reordered_table

##__________________________________________________________________||
def plotDF(df):
    df.plot(kind='line', logx=True)
    plt.show()
