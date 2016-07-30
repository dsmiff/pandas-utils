# Dominic Smith <dosmith@cern.ch>
'''
An example script to perform arithmetic on 
Pandas DataFrames
'''

import os,sys
import argparse
from core.pandasCore import *

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help = "the path to the input table")
parser.add_argument("-p", "--process", type = str, default='QCD_HT', help = "process to split dataframe into")
parser.add_argument('-o', '--outdir', default = './')
parser.add_argument('-q', '--quiet', action = 'store_true', default = False, help = 'quiet mode')
parser.add_argument("--reverse", action = "store_true", default = False, help = "reverse the order of the variable values for the efficiency ")
parser.add_argument("--addEff", action = "store_true", default = False, help = "add the efficiency computation")
parser.add_argument('-a', '--analyzer', action = 'store_true', default = 'plotAnalyzer', help = 'Analyzer used')
parser.add_argument('--force', action = 'store_true', default = False, help = 'recreate all output files')
args = parser.parse_args()

##__________________________________________________________________||
def main():

    tbldir = args.dir
    outdir = args.outdir
    variables = ['jet40_minChi']
    tblsList = produceListOfTables(tbldir, variables)
    print tblsList
    for tbl in tblsList:
        varname = os.path.splitext(tbl)[0].split('_')[-1]
        if 'SMS' in tbl.split("_"): prefix = '_SMS'
        else: prefix = ''
        d1 = readTable(tbldir, tbl)
        d1_out = df_operation(d1, varname)
        writeDFtoFile(d1_out, None, outdir, prefix)

##__________________________________________________________________||
def split_process(tbl,varname):
    
    process = args.process    
    new_tbl = tbl[[process, varname]]

    return new_tbl

##__________________________________________________________________||
def add_eff(tbl):

    if any('SMS' in column for column in tbl.columns): return tbl    
    tbl['QCDcumn'] = tbl[::-1]['QCD_HT'].cumsum()
    tbl['QCDeff']  =  tbl['QCDcumn']/sum(tbl['QCD_HT'])
    tbl['QCD/EWK'] = tbl['QCD_HT']/tbl['EWK']

    return tbl

##__________________________________________________________________||
def sum_cols(tbl, varname):

    process = args.process
    if any('SMS' in column for column in tbl.columns): return tbl
    other_processes = [column for column in tbl.columns if process.split('_')[0] not in column and column != varname] 

    tbl['EWK'] = tbl[other_processes].sum(axis=1)

    return tbl

##__________________________________________________________________||
def df_operation(tbl,varname):

    addEff = args.addEff
    if len(tbl.index)==0: return None
    tbl[varname] = tbl.index
    tbl = tbl.reset_index(drop=True)
    tbl = rearrangeColumns(tbl, varname)
    tbl = sum_cols(tbl,varname)
    if addEff:
        tbl = add_eff(tbl)
    else:
        pass

    return tbl

##__________________________________________________________________||
if __name__ == '__main__':
    main()
