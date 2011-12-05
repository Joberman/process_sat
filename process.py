'''
New command-line io for oberman's process scripts

Process a series of files, generating some kind of output for each
  
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
    '''
    values contains a list of strings in the form "name:value" 
    ProjArgsAction assigns value to namespace.name for each pair
    '''
    def __call__(self, parser, namespace, values, option_string=None):
        for string in values:
            pair = string.strip('()').split(':')
            setattr(namespace, pair[0], ':'.join(pair[1:]))

class ListAttrsAction(argparse.Action):
    '''
    Print the additional parameters required for the given
    grid projections and/or output functions and a brief
    description for each
    ''' 
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
    '''
    A double is a string of the form "string1:string2",
    where string1 contains no colon characters,
    and string 2 may or may not contain colon characters.
    '''
    if not len(string.split(':')) >= 2:
        msg = "%s is not correctly formatted.  Correct format: 'varName:" \
              "varVal'" % string
        raise argparse.ArgumentTypeError(msg)
    return string

# ------------------------------------- #
# Initialize the command-line interface #
# ------------------------------------- #
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

# ---------------- #
# Parse the inputs #
# ---------------- #
gnomespice = parser.parse_args()

# parse directory input, using '.' character as shorthand 
# for current working directory path
directory = (gnomespice.directory or os.getcwd()).split('.')
if len(directory) == 1:
    directory = directory[0]
else:
    print "Using '.' character as shorthand for current working directory"
    directory = os.getcwd().join(outDirectory)
outDirectory = gnomespice.outDirectory.split('.')
if len(outDirectory) == 1:
    outDirectory = outDirectory[0]
else:
    print "Using '.' character as shorthand for current working directory"
    outDirectory = os.getcwd().join(outDirectory)

# Make sure the directories are valid
if not os.path.isdir(directory):
    print "Error: {0} is not a valid directory".format(directory)
    sys.exit(0)
if not os.path.isdir(outDirectory):
    print "Error: {0} is not a valid directory".format(outDirectory)
    sys.exit(0)

# parse output filename
outFileNames = os.path.join(outDirectory,gnomespice.outFileNames) or \
               os.path.join(outDirectory, 'output1') 

# Make sure that both the output directory and the given output file
# can be accessed and written to 
if not os.access(outDirectory, os.W_OK) or (os.path.isfile(outFileNames)\
          and not os.access(outFileNames, os.W_OK)):
    print textwrap.wrap("Error: Unable to write output to file {1} in "\
          "directory {0}.  You may not have write permissions to that "\
          "directory, or that directory may already contain an existing "\
          "file of that name, for which you do not have write permissions.  "\
          "Check the output directory and try again.".format(outDirectory, \
          gnomespice.outFileNames), 75)
    sys.exit(0)

# To be implemented later (maybe)
parserList = None                        

# Parse verbose flag
verbose = gnomespice.verbose != 'False'

# grid definition parameter dictionary
gridDict = dict()
# output function parameter dictionary
outParms = dict()

# parse input to initialize gridDict and outParms
# if any parameters aren't found, print an error message for each
# and quit the program.
if verbose: print('Parsing inputs... '+str(datetime.datetime.now()) + \
                  '\nChecking for required parameters...')
def argerrmsg(attr, type): 
    return textwrap.TextWrapper(initial_indent = "Argument Error: ", \
                                subsequent_indent = "                ", \
                                width = 80).wrap('Missing argument {0}, '\
                                                 'which is required for '\
                                                 'selected {1}.  Please '\
                                                 'include a value for '\
                                                 '{0}.\n'.format(attr,type))
def formerrmsg(attr, type):
    return textwrap.TextWrapper(initial_indent = "Argument Error: ", \
                                subsequent_indent = "                ", \
                                width = 80).wrap('Invalid input for argument '\
                                                 '{0}.  Argument should be a '\
                                                 '{1}.  Please include a valid'\
                                                 'value for {0}.\n'\
                                                 .format(attr,type))
# error message for unitialized parameters
unitParms = []
# Build the error message for grid definition parameters
for attr in gridDef.requiredParms():
    try:
        gridDict[attr] = getattr(gnomespice, attr)
    except AttributeError:
        unitParms = unitParms + argerrmsg(attr, 'projection (' \
                                              + gnomespice.gridProj + ')')
parms = outFunc.required_parms()
# Build the error message for output function parameters 
for attr in parms:
    # This is a little tougher; some values have to be of certain types
    if parms[attr][1] == 'int':
        try:   
            outParms[attr] = int(getattr(gnomespice, attr))
        except AttributeError:
            unitParms = unitParms + formerrmsg(attr,"\bn integer")
    elif parms[attr][1] == 'decimal':
        try:
            outParms[attr] = float(getattr(gnomespice, attr))
        except AttributeError:
            unitParms = unitParms + formerrmsg(attr,"decimal")
    elif parms[attr][1] == 'list':
        try:
            outParms[attr] = getattr(gnomespice, \
                                   attr).split(',')
        except AttributeError:
            unitParms = unitParms + argerrmsg(attr, 'output function (' + \
                                    gnomespice.outFunc + ')')
    else:
        try:
            outParms[attr] = getattr(gnomespice, attr)
        except AttributeError:
            unitParms = unitParms + argerrmsg(attr, 'output function (' + \
                                    gnomespice.outFunc + ')') 
# Unless everything checked out, print those messages and quit
if unitParms != []:
    print '\n'.join(unitParms)
    sys.exit(0)
if verbose: print('                                    Done.')

# ---------------------- #
# Initialize the parsers #
# ---------------------- #
if parserList:
    # Note: This functionality is not implemented
    # and is probably not worth implementing anyway
    if verbose: print 'Ignoring filelist, using parserList'
    parsers = parserList
else:
    if verbose: print('building filelist '+str(datetime.datetime.now()))
    filetype = gnomespice.filetype
    # if a filelist was provided, use those files,
    # otherwise, just use every file in the directory
    files = [os.path.join(directory, f) for f in \
             gnomespice.fileList or os.listdir(directory)]
    parsers = []
    if verbose: print('getting parsers '+str(datetime.datetime.now()))
    badfile = gnomespice.interactive == 'True' and bad_file or bad_file_default
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

# ----------------- #
# Process the files #
# ----------------- #

# Construct the grid definition
griddef = getattr(grid_geo, gnomespice.gridProj + '_GridDef')(gridDict)

# Map data to grid
if verbose: print('calculating maps '+str(datetime.datetime.now()))
mapFunc = getattr(map_geo, gnomespice.mapFunc + '_map_geo')
maps = [mapFunc(p, griddef, verbose) for p in parsers]

# Construct output
if verbose: print('creating outfiles '+str(datetime.datetime.now()))
outFunc = getattr(out_geo, gnomespice.outFunc + '_out_func')
outputs = outFunc(outParms)(maps,griddef,outFileNames)

# eventually, we may want to do stuff to outputs, but for now...
del(outputs)

