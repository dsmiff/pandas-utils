import os,sys
import argparse
from core.pandasCore import *

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help = "the path to the input table")
parser.add_argument("-p", "--process", default = 1, type = int, help = "number of processes to run in parallel")
parser.add_argument('-o', '--outdir', default = './')
parser.add_argument('-q', '--quiet', action = 'store_true', default = False, help = 'quiet mode')
parser.add_argument('-a', '--analyzer', action = 'store_true', default = 'plotAnalyzer', help = 'Analyzer used')
parser.add_argument('--force', action = 'store_true', default = False, help = 'recreate all output files')
args = parser.parse_args()

##__________________________________________________________________||
def main():

    tbldir = args.dir
    variables = ['jet40_minChi']
    tblsList = produceListOfTables(tbldir, variables)
    for tbl in tblsList:
        d1 = readTable(tbldir, tbl)
        
##__________________________________________________________________||
if __name__ == '__main__':
    main()
