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
def getHistFromFile(process, plot, file, analyzer):

    hDict = rtUtils.getHistDictFromFile(plot, file, analyzer)
    name = file.GetName().split('/')[-1][:-5]
    h = hDict[name+'__'+analyzer+'__'+process+'__all__all__'+plot+'_all_all']

    return h

##__________________________________________________________________||
def getHistogramDict(samples, variable, histdir, analyzer):

    file = r.TFile.Open(histdir)
    histDict = {sample: getHistFromFile(sample, variable, file, analyzer) for sample in samples}
    smYields = rtUtils.produceYieldsDict(histDict)
    tbl = convertDictToDF(smYields, variable, False)

    return tbl

##__________________________________________________________________||
def main():

    histdir  = args.input
    analyzer = args.analyzer
    outdir   = args.outdir
    force    = args.force

    variables = ['jet40_minChi',
                 'biasedDPhi',
                 ]

    signals = ['SMS-T1tttt_mGluino-1400_mLSP-100_25ns',
               'SMS-T1tttt_mGluino-1500_mLSP-100_25ns',
               'SMS-T1tttt_mGluino-1600_mLSP-100_25ns',
               'SMS-T1tttt_mGluino-1700_mLSP-100_25ns',
               ]

    QCD = ['QCD_HT',
       ]        
    EWK = ['TTJets_HT',           
           'Zinv',
           'WJetsToLNu_HT',
           'SingleTop',
           'DiBoson',
           'DYJetsToLL_M50_HT'
           ]

    if 'SignalModels' in histdir: 
        samples = signals
        prefix = 'SMS'
    else: 
        samples = QCD + EWK
        prefix = 'SM'

    for variable in variables:
        tbl = getHistogramDict(samples, variable, histdir, analyzer)
        writeDFtoFile(tbl,variable,outdir,prefix,force)

##__________________________________________________________________||
if __name__ == '__main__':
    main()
