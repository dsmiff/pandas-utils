'''
A collection of ROOT utilities
'''

import ROOT as r

##__________________________________________________________________||
def findObject(objects,name, dict):
    '''
    Find an object in a ROOT file
    '''
    
    for key in objects.GetListOfKeys():
        obj = key.ReadObj()
        if not obj.IsA().InheritsFrom( r.TDirectory.Class() ):
            dict[name+'__'+obj.GetName()] = obj.Clone()
        else:
            findObject(obj, name+'__'+obj.GetName(), dict)           
            pass
        pass
    return dict

##__________________________________________________________________||
def getHistDictFromFile(plot, file, analyzer):
    '''
    Return a dictionary of ROOT histograms from a file
    '''

    histDict = {}
    name = file.GetName().split('/')[-1][:-5]
    hDict = findObject(file, name, histDict)
    return hDict

##__________________________________________________________________||
def produceYieldsDict(histDict):
    '''
    Produce a dictionary of process: yields from a given histogram
    '''
    
    yieldsDict = {process: {h.GetBinLowEdge(bin): h.Integral(bin, h.GetNbinsX()) for bin in range(1,h.GetNbinsX())} for process, h in histDict.iteritems()}
    if not bool(yieldsDict):
        print("Dictionary not filled")

    return yieldsDict
    
