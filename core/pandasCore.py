# Dominic Smith <dosmith@cern.ch>
'''
A collection of miscellaneous functions to 
perform Pandas operations
'''

import os
import glob
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 4096)
pd.set_option('display.max_rows', 65536)
pd.set_option('display.width', 1000)

##__________________________________________________________________||
def convertDictToDF(infoDict, variable, assignIndexName=False):
    '''
    Convert a python dictionary to a DataFrame
    '''

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
def writeDFtoFile(tbl, variable, dir, prefix=None):
    '''
    Write a produced DataFrame to a txt file 
    given a variable name and output directory
    '''

    if variable is None: variable = 'out'
    if not os.path.exists(dir):
        print("Undefined output directory")
    else:        
        tblName = 'tbl_n{}_{}.txt'.format(prefix, variable)
        with open(tblName,'a') as f:
            tbl.to_string(f, index=True)
            f.write('\n')
            f.close()
            print('DataFrame {} written to file'.format(dir+tblName))
    
##__________________________________________________________________||
def readTable(tbldir=None, tableString=None):
    '''
    Return a DataFrame given an input directory and 
    txt file name
    '''

    if (tbldir and tableString) is None:
        print('No directory or table given')
    elif not os.path.exists(tbldir):
        print('Dir {} not found'.format(tbldir))
    else:
        try:
            tableString = os.path.join(tbldir, tableString)
        except IOError:
            print('Nothing found')

    d1 = pd.read_table(tableString, delim_whitespace=True)
    
    return d1

##__________________________________________________________________||
def produceListOfTables(tbldir, variables):
    '''
    Return a list of txt files containing DataFrames
    '''
    
    inFileNames = glob.glob(os.path.join(tbldir,"tbl_n_*"+variables[0]+".txt"))
    inFilePath  = [os.path.join(tbldir, fileName) for fileName in inFileNames]
    fileStatus  = [os.path.exists(fileName) for fileName in inFileNames]
    if not all(fileExists is True for fileExists in fileStatus):
        print("Table not found")

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
