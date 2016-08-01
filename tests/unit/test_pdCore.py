import unittest
import os
from core.pandasCore import *

##__________________________________________________________________||
class ConvertDictToDFTest(unittest.TestCase):
    '''Test for pandasCore.py'''
    
    def test_conversion(self):
        testDict = {0: {'Process':100, 'AnotherProcess':200}}
        d1 = convertDictToDF(testDict, variable=None)
        self.assertFalse(d1.empty)
    
    def test_readTable(self):
        testTable = 'tbl_n_test.txt'
        pdsDir = os.environ['PANDASHOME']
        tblDir = os.path.join(pdsDir, 'examples')
        d1 = readTable(tblDir, 'tbl_n_test.txt')
        self.assertFalse(d1.empty)
        
    def test_produceListOfTables(self):
        testTable = 'tbl_n_test.txt'
        pdsDir = os.environ['PANDASHOME']
        tblDir = os.path.join(pdsDir, 'examples')
        tblList = produceListOfTables(tblDir, ['test'])
        self.assertTrue(len(tblList),1)

##__________________________________________________________________||
if __name__=='__main__':
    unittest.main()
