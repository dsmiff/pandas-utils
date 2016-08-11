'''
A collection of ROOT utilities
'''

import ROOT as r

##__________________________________________________________________||
class EndModule(object):
    def __init__(self, name, debug=False):
        self.debug = debug
        
    @staticmethod
    def printInfo(info):
        print('\n info \n')

    def writeInfo(self, outPath=None):
        writeDir = outPath if outPath else './'
        textFile = open(writePath+'/outputInfo.txt', 'w')
        textFile.close()

##__________________________________________________________________||
class LambdaFunc(object):
    '''
    A class to define a lambda function given a string
    '''

    def __init__(self,inputStr):
        self.inputStr = inputStr

    def begin(self):
        self.func = eval( 'lambda ' + self.inputStr )

    def __call__(self,*item):
        return self.func(*item)

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

##__________________________________________________________________||    
def setProcessName(process):
    '''
    Rewrite columns to a more convenient name
    '''

    names = process.split('_')
    if len(names)==1: return process        
    model = names[0].split('-')

    if len(model)==1: return model[0]
    else: model = model[1]

    ranges = [range.split('-')[1] for range in names[1:-1]]

    if len(ranges) != 2:
        print("Ranges for model not created")

    column_label = '{0}({1},{2})'.format(model, ranges[0], ranges[1])

    return column_label
