import unittest
import os
from core.pandasCore import * 
import utils.rootUtils as rtUtils

##_________________________________________________________________||
class CreateHistoDict(object):
    def __init__(self):
        pass

    def setUp(self):
        dir = os.getcwd()
        fileName = 'testfile.root'
        self.fileDir = os.path.join(dir, fileName)
        self.file = r.TFile(self.fileDir, "RECREATE")
        self.hist = r.TH1F("h", "; p_{T}^{Bar} (TeV); Events / 2 TeV (10^{3})", 50, -50, 50)
        gaus1 = r.TF1('gaus1', 'gaus')
        gaus1.SetParameters(1, 0, 5)
        self.hist.FillRandom("gaus1", 50000)
        self.hist.Scale(0.001)
        self.hist.Write()
        
    def tearDown(self):
        os.remove(self.fileDir)

##_________________________________________________________________||
class GetHistoDict(unittest.TestCase):
    '''Test for ROOT example script'''

    def test_readHisto(self):
        histObject = CreateHistoDict()
        histObject.setUp()
        hDict = rtUtils.getHistDictFromFile('h', histObject.file, None)
        self.assertTrue('testfile' in hDict.keys()[0])
        histObject.tearDown()

    def test_readHistDict(self):
        histObject = CreateHistoDict()
        histObject.setUp()
        hDict = rtUtils.getHistDictFromFile('h', histObject.file, None)
        name = histObject.file.GetName().split('/')[-1][:-5]
        h = hDict[name+'__'+histObject.hist.GetName()]
        self.assertTrue(h.GetEntries() == 50000)

##_________________________________________________________________||
if __name__=='__main__':
    unittest.main()

