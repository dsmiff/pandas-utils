# Dominic Smith <dosmith@cern.ch>
'''
An example script to combine Pandas DataFrames
'''

import os,sys
import argparse
from core.pandasCore import *
from utils.rootUtils import *

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help = "the path to the input table")
parser.add_argument('-o', '--outdir', default = './')
parser.add_argument('-q', '--quiet', action = 'store_true', default = False, help = 'quiet mode')
parser.add_argument('--force', action = 'store_true', default = False, help = 'recreate all output files')
args = parser.parse_args()

##__________________________________________________________________||
def main():
    
    tbldir = args.dir
    outdir = args.outdir
    tbl1 = 'tbl_n_SMS_out.txt'
    tbl2 = 'tbl_n_out.txt'
    variable = 'minChi'
    d1 = readTable(tbldir, tbl1)
    d2 = readTable(tbldir, tbl2)

    d = pd.merge(d2,d1)
    columns_to_rename = d.columns
    for column in columns_to_rename:
        d = d.rename(columns = {column: setProcessName(column)})

    writeDFtoFile(d, variable, outdir, 'comb')

##__________________________________________________________________||
if __name__ == '__main__':
    main()
