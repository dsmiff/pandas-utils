import os
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 4096)
pd.set_option('display.max_rows', 65536)
pd.set_option('display.width', 1000)

##__________________________________________________________________||
def convertHistoToDF(infoDict, variable):
    d1 = pd.DataFrame.from_dict(infoDict)
    if d1.empty:
        print("DataFrame is empty")
    if d1.index.name is None:
        d1.index.name = variable
    
    return d1
    
##__________________________________________________________________||
def writeDFtoFile(tbl, variable, dir):
    if not os.path.exists(dir):
        print("Undefined output directory")
    else:        
        with open('table_'+variable+'.txt','a') as f:
            tbl.to_string(f, index=True)
            f.write('\n')
            f.close()
    
