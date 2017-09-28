# Dominic Smith <dosmith@cern.ch>
'''
Make a Pandas DataFrame from a hypothetical problem.

Problem: 
   To study the correlation between number of potatos/ name/ vs spelling given name with potato 
   alphabet.

Technique:
   Use Monte Carlo method to generate random collection of shapes of a given size of bag.
   Check if bag contains a name.
   Repeat experiment X times, each time determining the pass/fail rate (p = nPasses/ X)   
   p will converge after large X
'''

import os, sys
import argparse
import random
from string import ascii_uppercase
from core.pandasCore import *

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-x", "--number_of_iterations", nargs = "*", default = [10], type = int, help = "Number of iterations to implement")
parser.add_argument("-s", "--number_of_shapes", default = [50], nargs = "*", type = int, help = "Number of potato shapes in bag")
parser.add_argument("-n", "--names", nargs = "*", default = "DOM", type = str, help = "Input name")
parser.add_argument("-p", "--to_plot", nargs = "*", default = None, help = "Variables to plot")
parser.add_argument('--dry_run', action = 'store_true', default = False, help = "Dry run option to test flow")
parser.add_argument('--force', action = 'store_true', default = False, help = 'recreate all output files')
args = parser.parse_args()
args_dict = vars(args)

##__________________________________________________________________||
class PotatoBag(object):
    def __init__(self, names, number_of_shapes, number_of_iterations, to_plot, force, dry_run):
        self.names  = names
        self.nShapes = number_of_shapes
        self.nIter = number_of_iterations
        self.variables = to_plot
        
    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self._results)
        
    def checkNameInBag(self, name, bag):
        for n in name:
            if n in bag:
                bag.remove(n)
            else:
                return False
        return True

    def probabilityOfSpellingName(self, name, n_shapes, n_iterations):
        probabilities = {}
        probabilities['name'] = name
        probabilities['n_iterations'] = n_iterations
        probabilities['probability'] = 0
        probabilities['n_shapes'] = n_shapes
        name = name.upper()
        success_counter = 0
        for i in xrange(int(n_iterations)):
            bag = [random.choice(ascii_uppercase) for i in xrange(n_shapes)]
            if self.checkNameInBag(name, bag):
                success_counter += 1

        probabilities['probability'] = 1.* success_counter / n_iterations
        return probabilities

##__________________________________________________________________||
def main():    
    nLetters = 26.0
    columns = ['name', 'probability', 'n_iterations', 'n_shapes']
    
    potato_object = PotatoBag(**args_dict)

    pandas_holder = PandasHolder(columns)
    pandas_holder.makeDataFrame()
    prob_list = [potato_object.probabilityOfSpellingName(name, nShapes, nInt)
                 for nInt in args.number_of_iterations
                 for nShapes in args.number_of_shapes
                 for name in args.names]
    
    pandas_holder.fillDataFrame(prob_list)
    print pandas_holder.df
    if args.to_plot: pandas_holder.plotDataFrame(args.to_plot)
    # Send to a file to be read in by ggplot2
    writeDFtoFile(pandas_holder.df, None, './', args.force)
    return pandas_holder.df


##__________________________________________________________________||
if __name__ == '__main__':
    p = main()
