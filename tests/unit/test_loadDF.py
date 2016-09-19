import unittest
import ROOT as r
import os
from core.pandasCore import * 

##_________________________________________________________________||
class LoadDF(object):

    def __init__(self):
        pass
    
    def loadDF(self):
        homeDir = os.environ['PANDASHOME']
        tableDir = os.path.join(homeDir, 'examples')
        tblName = 'tbl_n_example.txt'

        df = readTable(tableDir, tblName)

        return df

##_________________________________________________________________||
class TestLoadDF(unittest.TestCase):
    
    def test_load(self):
        dfObject = LoadDF()
        d1 = dfObject.loadDF()

        plotDF(d1)

##_________________________________________________________________||
if __name__=='__main__':
    unittest.main()
