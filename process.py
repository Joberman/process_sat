'''
Created on May 26, 2011

@author: oberman
'''

import os
import datetime
from itertools import izip

import cmd_line_io as geo_io

from parse_geo import get_parser
import argparse
from grid_geo import *
from map_geo import *
from out_geo import ValidOutfuncs

def bad_file_default(filename):
    return 1

def bad_file(filename):
    '''
    Determine what the user wants to do when one fo the
    files turns out to be invalid.
    '''
    valid = False
    first = True
    while not valid:
        if not first:
            print("Invalid answer.  Please try again.")
        first = False
        prompt = "File %s couldn't be read properly.  What \n\
        do you wish to do?  Enter (1) to skip this file, \n\
        but continue processing other files.  Enter (2) to \n\
        stop reading files but continue with data \n\
        processing.  Enter (3) to quit this program.  Enter \n\
        your selection here: " % filename
        answer = raw_input(prompt)
        try:
            answer = int(answer)
        except(ValueError, TypeError):
            continue
        valid = answer in [1,2,3]
    return answer
 
"""
Process a series of files, generating some kind of output for each
    
By default, files in the current folder are processed using the generic 
filetype appropriate for their extension.  Griddef is obtained 
interactively from the user if no griddef instance is passed. 
Similarly, map is obtained from user if no mapping function is passed. 
 
OutFuncs are obtained from the user as well.  OutFuncs must be a LIST
of outFuncs, even if only one function is desired.  Outfuncs passed
into the function are expected to be properly initialized.  When
the user specifies outfunctions, the outfunctions are responsible
for obtaining fieldnames and parameters from the user.

OutFileNames are expected to passed as a LIST of the same length
as OutFuncs, if the user provides them.
If no outFileNames are given, any files generated are saved into
the current directory under the name "output<num>" where <num>
is the index of the outFunc associated with that output.
  
Ordinarily, directory signifies the directory and filelist the subset
of files within that directory that should be processed.  If no 
argument is passed for filelist, all files in the directory are 
processed.  If no directory is passed, the current working directory
is assumed.
    
Alternately, a list of pre-instantiated parsers may be passed.  Note that 
if parsers are passed, the files in the filelist are IGNORED and the files
with which the parsers are associated are used instead.
  
If verbose is set to True, all default status updates will be printed.  
If set to False, the program will run silently
"""

parser = argparse.ArgumentParser("Process a series of files, generating some kind of output for each")

class ProjArgsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for string in values:
            pair = string.strip('()').split(',')
            setattr(namespace, pair[0], pair[1])
def double(string):
    if len(string.split(',')) != 2:
        msg = "%r is not correctly formatted.  Correct format: 'varName,varVal'" % string
        raise argparse.ArgumentTypeError(msg)
    return string
parser.add_argument('--directory', help='The directory containing the files to process (default: current working directory)')
parser.add_argument('--filelist', help='The list of files in the directory to process (default: process all files')
parser.add_argument('--gridProj', help='Supply a valid grid projection type with which to form a grid', choices=ValidProjections())
parser.add_argument('--progAttrs', nargs='*', action= ProjArgsAction, type=double, help='Supply the attributes required for the projection')
parser.add_argument('--mapFunc', help='Supply a valid mapping function.', choices = ValidMaps())
parser.add_argument('--outFuncs', nargs='+', help='Supply desired output function(s)', choices=ValidOutfuncs())
parser.add_argument('--outFileNames', nargs='*', help='Optionally, supply the names of the respective output files to be used for each output function.  If none are provided, the output files will be named \'output1\', \'output2\', ...')
parser.add_argument('--extension', help='Optional override extension')
parser.add_argument('--subtype', help='Optional file subtype', default='')
parser.add_argument('--verbose', help='Supply False here to disable verbose execution', default=True)
parser.add_argument('--interactive', help='Supply True here to enable interactive error handling in the event that the program encounters an invalid input file. (default behavior ignores any invalid files and continues processing all requested files)', default=False) 

parserList = None

gnomespice = parser.parse_args()

directory = gnomespice.directory or os.getcwd()
filelist = gnomespice.filelist or os.listdir(directory)
gridDict = dict()
gridDef =  eval(gnomespice.gridProj + '_GridDef')
for attr in gridDef.requiredParms():
    try:
        gridDict[attr] = getattr(gnomespice, attr)
    except AttributeError:
        raise argparse.ArgumentError('Missing argument %r, which is required for selected projection. Please include a value for %r.' % (attr, attr))
griddef = gridDef(gridDict)
mapFunc = gnomespice.mapFunc + '_map_geo'
outFuncs = gnomespice.outFuncs
outFileNames = gnomespice.outFileNames or \
    [os.path.join(directory, 'output%s' % i) for i in range(len(outFuncs))]
verbose = gnomespice.verbose
badfile = gnomespice.interactive and bad_file or bad_file_default

if parserList:
    if verbose: print 'Ignoring filelist, using parserList'
    parsers = parserList
else:
    if verbose: print('building filelist '+str(datetime.datetime.now()))
    files = [os.path.join(directory, f) for f in filelist]
    parsers = []
    if verbose: print('getting parsers '+str(datetime.datetime.now()))
    for f in files:
        try:
            parsers.append(\
                get_parser(f, gnomespice.subtype, gnomespice.extension))
        except(IOError):
            answer = badfile(f)
            if answer is 1:
                continue
            elif answer is 2:
                break
            elif answer is 3:
                raise SystemExit

print(mapFunc)            
if verbose: print('calculating maps '+str(datetime.datetime.now()))
maps = eval('[' + mapFunc + '(p, griddef) for p in parsers]')
if verbose: print('creating outfiles '+str(datetime.datetime.now()))
outputs = [out(maps, griddef, fnames) for (out, fnames) in izip(outFuncs, outFileNames)]

# eventually, we may want to do stuff to outputs, but for now...
del(outputs)

