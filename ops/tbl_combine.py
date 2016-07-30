# Dominic Smith <dosmith@cern.ch>
'''
An example script to combine Pandas DataFrames
'''

import os,sys
import argparse
from core.pandasCore import *

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help = "the path to the input table")
parser.add_argument('-o', '--outdir', default = './')
parser.add_argument('-q', '--quiet', action = 'store_true', default = False, help = 'quiet mode')
parser.add_argument('--force', action = 'store_true', default = False, help = 'recreate all output files')
args = parser.parse_args()

##__________________________________________________________________||
def main():
    pass

##__________________________________________________________________||
if __name__ == '__main__':
    main()
