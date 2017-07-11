# Dominic Smith <dosmith@cern.ch>
'''
Make a Pandas DataFrame from a ROOT histogram

Input argument should be a ROOT file containing a histogram.
Information used to access the histogram:

Variables: Accesses the distribution
Samples:   Returns histogram from hDict
Analyzer:  ""    ""
'''

import os, sys
import argparse
import ROOT as r
from core.pandasCore import *
import utils.rootUtils as rtUtils

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help = "the path to the input histogram")
parser.add_argument("-p", "--process", default = 1, type = int, help = "number of processes to run in parallel")
parser.add_argument('-o', '--outdir', default = './')
parser.add_argument('-q', '--quiet', action = 'store_true', default = False, help = 'quiet mode')
parser.add_argument('-a', '--analyzer', action = 'store_true', default = 'plotAnalyzer', help = 'Analyzer used')
parser.add_argument('--force', action = 'store_true', default = False, help = 'recreate all output files')
args = parser.parse_args()

##__________________________________________________________________||
def makeDF(yieldDict, histName):
    tbl = convertDictToDF(yieldDict, histName)    
    return tbl

##__________________________________________________________________||
def main():

    inDir  = args.input
    outDir = args.outDir
    file = r.TFile(os.path.join(inDir, inFile),'READ')
    hists = {}
    yieldDict = {}
    pandas_object = PandasChecker()
    for inDirKey in file.GetListOfKeys():
        hist = inDirKey.ReadObj()
        hists[hist.GetName()] = hist
        print hist.GetName()
        for binX in range(1,hist.GetXaxis().GetNbins()+1):
            htLow = str(hist.GetXaxis().GetBinLowEdge(binX))
            yieldDict[htLow] = {}
            for binY in range(1,hist.GetYaxis().GetNbins()+1):
                nBJetBin = hist.GetYaxis().GetBinLabel(binY).split("_")[0]
                nJetBin = hist.GetYaxis().GetBinLabel(binY).split("_")[1]
                nSJetBin = hist.GetYaxis().GetBinLabel(binY).split("_")[2]
                yieldDict[htLow][(nBJetBin, nJetBin, nSJetBin)] =  hist.GetBinContent(binX,binY) 
                
        tbl = makeDF(yieldDict, hist.GetName())
        if pandas_object.check_filled(tbl):
            convertToLatex(tbl, hist.GetName(),True)
            writeDFtoFile(tbl, hist.GetName(), outdir)
        else:
            print "Dataframe was not filled"
##__________________________________________________________________||
if __name__ == '__main__':
    main()
