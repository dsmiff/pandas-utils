import os,sys
import argparse
from core.pandasCore import *

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help = "the path to the input table")
parser.add_argument("-p", "--process", type = str, help = "process to split dataframe into")
parser.add_argument('-o', '--outdir', default = './')
parser.add_argument('-q', '--quiet', action = 'store_true', default = False, help = 'quiet mode')
parser.add_argument("--reverse", action = "store_true", default = False, help = "reverse the order of the variable values for the efficiency ")
parser.add_argument('-a', '--analyzer', action = 'store_true', default = 'plotAnalyzer', help = 'Analyzer used')
parser.add_argument('--force', action = 'store_true', default = False, help = 'recreate all output files')
args = parser.parse_args()

##__________________________________________________________________||
def main():

    tbldir = args.dir
    outdir = args.outdir
    variables = ['jet40_minChi']
    tblsList = produceListOfTables(tbldir, variables)
    for tbl in tblsList:
        varname = os.path.splitext(tbl)[0].split('_')[-1]
        d1 = readTable(tbldir, tbl)
        d1_out = df_operation(d1, varname)
        writeDFtoFile(d1_out, None, outdir)

##__________________________________________________________________||
def split_process(tbl,varname):
    
    process = args.process    
    new_tbl = tbl[[process, varname]]

    return new_tbl

##__________________________________________________________________||
def add_eff(tbl):
    
    tbl['QCDcumn'] = tbl[::-1]['QCD_HT'].cumsum()
    tbl['QCDeff']  =  tbl['QCDcumn']/sum(tbl['QCD_HT'])

    return tbl

##__________________________________________________________________||
def sum_cols(tbl, varname):

    process = args.process
    other_processes = [column for column in tbl.columns if process.split('_')[0] not in column and column != varname]
    tbl['ewk'] = tbl[other_processes].sum(axis=1)
    print tbl.columns.tolist() # Need to reorder list

    return tbl

##__________________________________________________________________||
def df_operation(tbl,varname):

    if len(tbl.index)==0: return None
    tbl[varname] = tbl.index
    tbl = tbl.reset_index(drop=True)
    tbl = sum_cols(tbl,varname)
    tbl = add_eff(tbl)

    return tbl

##__________________________________________________________________||
if __name__ == '__main__':
    main()
