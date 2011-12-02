'''
New command-line io for oberman's process scripts

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
    
Alternately, a list of pre-instantiated parsers may be passed.**  Note that 
if parsers are passed, the files in the filelist are IGNORED and the files
with which the parsers are associated are used instead.
**It has been noted that this requires knowledge of both python -and-
oberman's parsers classes.  This functionality has therefor been removed
for the forseeable future.
  
If verbose is set to True, all default status updates will be printed.  
If set to False, the program will run silently

@version 11/21/2011
@author: maki, oberman
'''

import os
import sys
import datetime
from itertools import izip
import textwrap
import pdb

import parse_geo
import argparse
import grid_geo
import map_geo
import out_geo

def bad_file_default(filename):
    return 1

def bad_file(filename):
    '''
    Determine what the user wants to do when one of the
    files turns out to be invalid.
    '''
    prompt = "File %s couldn't be read properly.  What \n\
    do you wish to do?  Enter (1) to skip this file, \n\
    but continue processing other files.  Enter (2) to \n\
    stop reading files but continue with data \n\
    processing.  Enter (3) to quit this program.  Enter \n\
    your selection here: " % filename
    while True:
        answer = raw_input(prompt)
        try:
            answer = int(answer)
        except(ValueError, TypeError):
            answer = 0
        if answer in [1,2,3]:
            return answer
        print ("Invalid answer.  Please try again.")

class ProjArgsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for string in values:
            pair = string.strip('()').split(':')
            setattr(namespace, pair[0], pair[1])

class ListAttrsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        indent = '                        '
        for string in values:
            if string in out_geo.ValidOutfuncs():
                #build list of attributes
                list = getattr(out_geo, string + '_out_func').required_parms()
            elif string in grid_geo.ValidProjections():
                #build list of attributes
                list = getattr(grid_geo, string + '_GridDef').requiredParms()
            else:
                print string + ' is not a valid projection or output function.'
                continue
            print 'Attributes required for ' + string + ':'
            for key in list:
                if len(key) < 20:
                    formatter = textwrap.TextWrapper(initial_indent = '  ' +  \
                                key + ''.join((22 - len(key))*[' ']), \
                                subsequent_indent = indent, width = 76)
                else:
                    print '  ' + key
                    formatter = textwrap.TextWrapper(initial_indent = indent,
                                subsequent_indent = indent, width = 76)
                print '\n'.join(formatter.wrap(list[key]))
        sys.exit(0)
    
def double(string):
    if not len(string.split(':')) >= 2:
        msg = "%s is not correctly formatted.  Correct format: 'varName:" \
              "varVal'" % string
        raise argparse.ArgumentTypeError(msg)
    return string

#Initialize the command-line interface
parser = argparse.ArgumentParser("Process a series of files, generating " \
                                 "some kind of output for each")
parser.add_argument('--directory', help='The directory containing the ' \
                    'files to process (default: current working directory)',\
                     metavar='DirectoryPath')
parser.add_argument('--fileList', nargs='*', help='The list of files in ' \
                    'the directory to process (default: process all files)',\
                    metavar='FileName')
parser.add_argument('--filetype', help='Supply a valid input file type to '\
                    'be processed.  This argument is required.', choices = \
                    parse_geo.SupportedFileTypes(), required = True)
parser.add_argument('--gridProj', help='Supply a valid grid projection type ' \
                    'with which to form a grid.  This argument is required', \
                    type = str, choices=grid_geo.ValidProjections(), \
                    required = True)
parser.add_argument('--projAttrs', nargs='*', action=ProjArgsAction, \
                    type=double, help='Supply the attributes required for ' \
                    'the projection', metavar='AttributeName:Value')
parser.add_argument('--mapFunc', help='Supply a valid mapping function.  ' \
                    'This argument is required', choices = map_geo.\
                    ValidMaps(), required = True)
parser.add_argument('--outFunc', help='Supply desired output function.  ' \
                    'This argument is required.', choices=out_geo.\
                    ValidOutfuncs(), required = True)
parser.add_argument('--outFuncAttrs', nargs='*', action=ProjArgsAction, \
                    type=double, help='Supply the attributes required for ' \
                    'the output function', metavar='AttributeName:Value'\
                    '[,value,...]')
parser.add_argument('--outDirectory', help='The directory to which output ' \
                    'files will be written to.', metavar='DirectoryPath', \
                    required = True)
parser.add_argument('--outFileNames', help='Optionally, supply the name ' \
                    'of the output file.  If no name is provided, the ' \
                    'output file will be named \'output1\'', metavar = \
                    'FileName')
parser.add_argument('--verbose', help='Supply False here to disable ' \
                    'verbose execution', default=True, choices={'True',\
                    'False'})
parser.add_argument('--interactive', help='Supply True here to enable ' \
                    'interactive error handling in the event that the ' \
                    'program encounters an invalid input file. (Default: ' \
                    'False ignores any invalid files and continues ' \
                    'processing all requested files)', default=False, \
                    choices={'True','False'}) 
parser.add_argument('--AttributeHelp', nargs='*', help='Supply this flag, ' \
                    'followed by a list of projection names and/or output ' \
                    'functions to see a list of additional parameters ' \
                    'required for those selections, and a brief ' \
                    'description of each parameter.', action=ListAttrsAction, \
                    metavar='ProjectionName/OutputFunctionName')
#Parse the inputs
gnomespice = parser.parse_args()

directory = gnomespice.directory or os.getcwd()
outDirectory = gnomespice.outDirectory
if not os.path.isdir(directory):
    print "Error: {0} is not a valid directory".format(directory)
    sys.exit(0)
if not os.path.isdir(outDirectory):
    print "Error: {0} is not a valid directory".format(outDirectory)
    sys.exit(0)
filelist = gnomespice.fileList or os.listdir(directory)
filetype = gnomespice.filetype
gridDef = getattr(grid_geo, gnomespice.gridProj + '_GridDef')
mapFunc = getattr(map_geo, gnomespice.mapFunc + '_map_geo')
outFunc = getattr(out_geo, gnomespice.outFunc + '_out_func')
outFileNames = os.path.join(outDirectory,gnomespice.outFileNames) or \
               os.path.join(outDirectory, 'output1') 
if not os.access(outDirectory, os.W_OK) or (os.path.isfile(outFileNames)\
          and not os.access(outFileNames, os.W_OK)):
    print textwrap.wrap("Error: Unable to write output to file {1} in "\
          "directory {0}.  You may not have write permissions to that "\
          "directory, or that directory may already contain an existing "\
          "file of that name, for which you do not have write permissions.  "\
          "Check the output directory and try again.".format(outDirectory, \
          gnomespice.outFileNames), 75)
    sys.exit(0)
parserList = None                        # To be implemented later (maybe)
verbose = gnomespice.verbose != 'False'

#Check for required parameters
if verbose: print('Finished parsing inputs. '+str(datetime.datetime.now()) + \
                  '\nChecking for required parameters...')
def argerrmsg(attr, type): 
    return textwrap.TextWrapper(initial_indent = "Argument Error: ", \
                                subsequent_indent = "                ", \
                                width = 80).wrap('Missing argument %s, '\
                                                 'which is required for '\
                                                 'selected %s.  Please '\
                                                 'include a value for '\
                                                 '%s.\n' % (attr,type,attr))
unitParms = []
gridDict = dict()
outParms = dict()
for attr in gridDef.requiredParms():
    try:
        gridDict[attr] = getattr(gnomespice, attr)
    except AttributeError:
        unitParms = unitParms + argerrmsg(attr, 'projection (' \
                                              + gnomespice.gridProj + ')')
parms = outFunc.required_parms()
for attr in parms:

    try:
        if parms[attr][1] is None:
            outParms[attr] = getattr(gnomespice, attr)
        else:
            outParms[attr] = getattr(gnomespice, \
                                       attr).split(',')
    except AttributeError:
        unitParms = unitParms + argerrmsg(attr, 'output function (' + \
                                          gnomespice.outFunc + ')') 
if unitParms != []:
    print '\n'.join(unitParms)
    sys.exit(0)
griddef = gridDef(gridDict)
badfile = gnomespice.interactive == 'True' and bad_file or bad_file_default
if verbose: print('                                    Done.')

#Initialize the parsers
if parserList:
    if verbose: print 'Ignoring filelist, using parserList'
    parsers = parserList
else:
    if verbose: print('building filelist '+str(datetime.datetime.now()))
    files = [os.path.join(directory, f) for f in filelist]
    parsers = []
    if verbose: print('getting parsers '+str(datetime.datetime.now()))

    #This block might need to be edited once subtype and extension are combined
    for f in files:
        try:
            parser = parse_geo.get_parser(f, filetype)
        except(IOError):
            print "there was an IOError when instantiating parser"
            answer = badfile(f) # badfile() depends on --interactive
            if answer is 1:
                continue
            elif answer is 2:
                break
            elif answer is 3:
                raise SystemExit
        if verbose: print "parser appended successfully."
        parsers.append(parser)

#Process the files          
if verbose: print('calculating maps '+str(datetime.datetime.now()))
maps = [mapFunc(p, griddef, verbose) for p in parsers]
paif verbose: print('creating outfiles '+str(datetime.datetime.now()))
outputs = set()
outF = outFunc(outParms) #need to figure these out
outputs.add(outF(maps,griddef,outFileNames))
# eventually, we may want to do stuff to outputs, but for now...
del(outputs)

