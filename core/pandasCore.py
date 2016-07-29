import os
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 4096)
pd.set_option('display.max_rows', 65536)
pd.set_option('display.width', 1000)

##__________________________________________________________________||
def convertHistoToDF(infoDict, variable, assignIndexName=False):
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
def writeDFtoFile(tbl, variable, dir):
    if not os.path.exists(dir):
        print("Undefined output directory")
    else:        
        with open('tbl_n_'+variable+'.txt','a') as f:
            tbl.to_string(f, index=True)
            f.write('\n')
            f.close()
            print('DataFrame written to file')
    
##__________________________________________________________________||
def readTable(tbldir=None, tableString=None):
    
    if (tbldir and tableString) is None:
        tableString = tbldir+ 'table_{0}.txt'.format(title)
        
    d1 = pd.read_table(tableString, delim_whitespace=False)
    
    return d1

##__________________________________________________________________||
def produceListOfTables(tbldir, variables):
    
    inFileNames = ['tbl_n_{0}.txt'.format(variable) for variable in variables]
    inFilePath  = [os.path.join(tbldir, fileName) for fileName in inFileNames]
    fileStatus  = [os.path.exists(fileName) for fileName in inFileNames]
    if not all(fileExists is True for fileExists in fileStatus):
        print("Table not found")

    return inFilePath
    
