#! /Library/Frameworks/Python.framework/Versions/Current/bin/python
'''
New command-line io for oberman's process scripts

Process a series of files, generating some kind of output for each
  
If verbose is set to True, all default status updates will be printed.  
If set to False, the program will run silently

@version 3/1/2012
@author: maki, oberman
'''
import os
import sys
import datetime
from itertools import izip
import textwrap
import argparse
import pdb

from process_sat import parse_geo
from process_sat import grid_geo
from process_sat import map_geo
from process_sat import out_geo
from process_sat import utils
'''
Global dictionary mapping filetypes to their default output function
Any new filetypes should be included in this dictionary to ensure
proper AttributeHelp functionality and default output function selection
'''
out_func_mapper = {"HDFknmiomil2":"OMNO2e_netCDF_avg",
                   "HDFmopittl2":"unweighted_filtered_MOPITT_avg_netCDF",
                   "HDFnasaomil2":"OMNO2e_netCDF_avg"}

class NeedToParseInFileException(Exception):
    '''exception class for signaling the need to parse input file'''
    pass

def bad_file_default(filename):
    '''
    Dummy function for non-interactive file handling
    '''
    return 1

def bad_file(filename):
    '''
    Determine what the user wants to do when one of the
    files turns out to be invalid.
    '''
    prompt = '\n'.join(\
             textwrap.wrap("File {0} couldn't be read properly.  What do you " \
                           "wish to do?  Enter (1) to skip this file, but " \
                           "continue processing other files.  Enter (2) to " \
                           "stop reading files but continue with data " \
                           "processing.  Enter (3) to quit this program.  " \
                           "Enter your selection here: ".format(filename)))
    while True:
        print prompt 
        answer = raw_input(" ==> ")
        try:
            answer = int(answer)
        except(ValueError, TypeError):
            answer = 0
        if answer in [1,2,3]:
            return answer
        print ("\nInvalid answer.  Please try again.")

class ProjArgsAction(argparse.Action):
    '''
    values contains a list of strings in the form "name:value" 
    For each string, ProjArgsAction assigns value to namespace.name
    '''
    def __call__(self, parser, namespace, values, option_string=None):
        for string in values:
            pair = string.split(':')
            setattr(namespace, pair[0], ':'.join(pair[1:]))

class inFromFileAction(argparse.Action):
    '''
    Open and read input from the input file
    '''
    def __call__(self, parser, namespace, values, option_string=None):
        fname = os.path.abspath(values[0])
        if not os.access(fname, os.R_OK):
            print textwrap.wrap("Error: Unable to read from file {0}.  Check "\
                                "the input file and try again.".format(fname))
            sys.exit(0)
        raise NeedToParseInFileException(fname)

class ListAttrsAction(argparse.Action):
    '''
    Print the additional parameters required for the given
    grid projections, output functions, and/or filetype(s) 
    and a brief description for each
    ''' 
    def __call__(self, parser, namespace, values, option_string=None):
        # error message if no parameters passed
        if (len(values) == 0):
            ms = ("Warning: Recieved '--AttributeHelp' flag, but no valid " \
                  "projection names, output function names, or filetypes.  "\
                  "Select any number of these from {" + 
                  ', '.join(out_geo.ValidOutfuncs()) + ', ' + \
                  ', '.join(grid_geo.ValidProjections()) + ', ' + \
                  ', '.join(parse_geo.SupportedFileTypes()) + \
                  "} and try again.")
            print '\n'.join(textwrap.wrap(ms, width = 76, 
                                          subsequent_indent = '    '))

        # print the attribute help for each selected projection/outfunc
        indent = '                        '
        follow_up = textwrap.TextWrapper(initial_indent = indent,
                                         subsequent_indent = indent, width = 76,
                                         drop_whitespace = False)

        for string in values:
            if string in parse_geo.SupportedFileTypes():
                print 'Using output function ' + out_func_mapper[string] + \
                      '\n   for filetype ' + string + '.'
                string = out_func_mapper[string]
            if string in out_geo.ValidOutfuncs():
                #build list of attributes
                list = getattr(out_geo, string + '_out_func').parm_list()
                dict = getattr(out_geo, string + '_out_func').required_parms()
            elif string in grid_geo.ValidProjections():
                #build list of attributes
                list = getattr(grid_geo, string + '_GridDef').parm_list()
                dict = getattr(grid_geo, string + '_GridDef').requiredParms() 
            else:
                print string + ' is not a valid projection, output function,'\
                    'or filetype.'
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
                text = dict[key][0].split('\n')
                print '\n'.join(formatter.wrap(text[0]))
                for line in text[1:]:
                    print '\n'.join(follow_up.wrap(line))
            print ''
        sys.exit(0)
    
def double(string):
    '''
    A double is a string of the form "string1:string2",
    where string1 contains no colon characters,
    and string 2 may or may not contain colon characters.
    '''
    if not len(string.split(':')) >= 2:
        msg = "{0} is not correctly formatted.  Correct format: 'varName:" \
              "varVal'".format(string)
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
                    ValidOutfuncs(), required = False)
parser.add_argument('--outFuncAttrs', nargs='*', action=ProjArgsAction, \
                    type=double, help='Supply the attributes required for ' \
                    'the output function', metavar='AttributeName:Value'\
                    '[,value,...]')
parser.add_argument('--outDirectory', help='The directory to which output ' \
                    'files will be written to.  This argument is required.', \
                    metavar = 'DirectoryPath', required = True)
parser.add_argument('--outFileName', help='Optionally, supply the name ' \
                    'of the output file.  If no name is provided, the ' \
                    'output file will be named \'output1\'', metavar = \
                    'FileName')
parser.add_argument('--includeGrid', nargs=1, metavar='GridFileName', \
                    help='Optionally, supply the name of a file to which to '\
                    'write out the latitudes and longitudes of the gridcells '\
                    'defined by the selected projection')
parser.add_argument('--verbose', help='Supply False here to disable ' \
                    'verbose execution', default=True, choices={'True',\
                    'False'})
parser.add_argument('--interactive', help='Supply True here to enable ' \
                    'interactive error handling in the event that the ' \
                    'program encounters an invalid input file. (Default: ' \
                    'False ignores any invalid files and continues ' \
                    'processing all requested files)', default=False, \
                    choices = {'True','False'}) 
parser.add_argument('--AttributeHelp', nargs='*', help='Supply this flag, ' \
                    'followed by a list of one or more projection names, ' \
                    'output function names, or filetypes to see a list of ' \
                    'additional parameters required for those selections, ' \
                    'and a brief description of each parameter.', 
                    action=ListAttrsAction, \
                    metavar = 'Projection/OutputFunction/filetype')
parser.add_argument('--inFromFile', nargs=1, help='Supply this flag, ' \
                    'followed by a file path (relative or absolute) to an ' \
                    'input file which specifies the desired attributes.  '\
                    'See the README for more on the format of this file.', 
                    action=inFromFileAction, metavar = 'FileName')

# ---------------- #
# Parse the inputs #
# ---------------- #

try:
    gnomespice = parser.parse_args()
except NeedToParseInFileException as fname:
    print "parsing from input file {0}".format(fname[0])
    print "This run can be repeated by executing the following call:\n  " \
          + "\n    ".join(textwrap.wrap("whips.py {0}".format(\
                " ".join(utils.parse_fromFile_input_file(fname[0], True))), 70))
    gnomespice = \
        parser.parse_args(utils.parse_fromFile_input_file(fname[0], False))

# Parse verbose flag
verbose = gnomespice.verbose != 'False'

# parse directory input, using '.' character as shorthand 
# for current working directory path
directory = (gnomespice.directory or os.getcwd()).split('.')
if len(directory) == 1:
    directory = directory[0]
else:
    if verbose:
        print "Using '.' character as shorthand for current working directory"
    directory = os.getcwd().join(directory)
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
outFileName = (gnomespice.outFileName and \
                    os.path.join(outDirectory,gnomespice.outFileName)) \
               or os.path.join(outDirectory, 'output1') 

# Make sure that both the output directory and the given output file
# can be accessed and written to 
if not os.access(outDirectory, os.W_OK) or (os.path.isfile(outFileName)\
          and not os.access(outFileName, os.W_OK)):
    print textwrap.wrap("Error: Unable to write output to file {1} in "\
                        "directory {0}.  You may not have write permissions "\
                        "to that directory, or that directory may already "\
                        "contain an existing file of that name, for which "\
                        "you do not have write permissions.  Check the "\
                        "output directory and try again.".format(\
                        outDirectory, gnomespice.outFileName), 75)
    sys.exit(0)

gridFileName = (gnomespice.includeGrid and \
                        os.path.join(outDirectory,gnomespice.includeGrid[0]))
if gridFileName and not os.access(gridFileName, os.W_OK):
    print textwrap.wrap("Error: Unable to write output to file {1} in "\
                        "directory {0}.  That directory may already "\
                        "contain an existing file of that name, for which "\
                        "you do not have write permissions.  Check the "\
                        "output directory and try again.".format(\
                        outDirectory, gnomespice.includeGrid), 75)

# To be implemented later (maybe)
parserList = None                        

# retrieve grid definition function from grid_geo
gridDef = getattr(grid_geo, gnomespice.gridProj + '_GridDef')
# grid definition parameter dictionary
gridDict = dict()

# retrieve output function function from out_geo
if gnomespice.outFunc not in locals():
    if gnomespice.filetype == 'HDFmopitl2':
        gnomespice.outFunc = 'unweighted_filtered_MOPITT_avg_netCDF'
    else:
        gnomespice.outFunc = 'OMNO2e_netCDF_avg'
outFunc = getattr(out_geo, gnomespice.outFunc + '_out_func')
if verbose: print('Using outfunc ' + gnomespice.outFunc)

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
                                                 '{0}.  Argument should be '\
                                                 '{1}.  Please include a valid'\
                                                 ' value for {0}.\n'\
                                                 .format(attr,type))
# error message for uninitialized parameters
unitParms = []

# Build the error message for grid definition parameters
parms = gridDef.requiredParms()
for attr in parms:
    # Need to cast input to correct types, then add to dictionary
    try:
        if parms[attr][1] == 'int':
            try:
                gridDict[attr] = int(getattr(gnomespice, attr))
            except ValueError:
                unitParms = unitParms + formerrmsg(attr, "an integer")
        elif parms[attr][1] == 'decimal':
            try:
                gridDict[attr] = float(getattr(gnomespice, attr))
            except ValueError:
                unitParms = unitParms + formerrmsg(attr, "a decimal")
        elif parms[attr][1] == 'posint':
            try:
                gridDict[attr] = int(getattr(gnomespice, attr))
                if gridDict[attr] <= 0:
                    raise ValueError
            except ValueError:
                unitParms = unitParms + formerrmsg(attr, "a positive integer")
        elif parms[attr][1] == 'posdecimal':
            try:
                gridDict[attr] = float(getattr(gnomespice, attr))
                if gridDict[attr] <= 0:
                    raise ValueError
            except ValueError:
                unitParms = unitParms + formerrmsg(attr, "a positive decimal")
        elif parms[attr][1] == 'list':
            gridDict[attr] = getattr(gnomespice, \
                                     attr).split(',')

        elif parms[attr][1] == 'bool':
            if float(getattr(gnomespice, attr)) == 'True':
                gridDict[attr] = True
            elif float(getattr(gnomespice,attr)) == 'False':
                gridDict[attr] = False
            else:
                unitParms = unitParms + formerrmsg(attr, 
                                                  "either 'True' or 'False'")
        else:
            gridDict[attr] = getattr(gnomespice, attr)
    except AttributeError:
        unitParms = unitParms + argerrmsg(attr, 'projection (' \
                                          + gnomespice.gridProj + ')')

# Build the error message for output function parameters 
parms = outFunc.required_parms()
for attr in parms:
    # Again, need to cast input to correct type, then add to dictionary
    try:
        if parms[attr][1] == 'int':
            try:   
                outParms[attr] = int(getattr(gnomespice, attr))
            except ValueError:
                unitParms = unitParms + formerrmsg(attr,"\bn integer")
        elif parms[attr][1] == 'decimal':
            try:
                outParms[attr] = float(getattr(gnomespice, attr))
            except ValueError:
                unitParms = unitParms + formerrmsg(attr,"decimal")
        elif parms[attr][1] == 'posint':
            try:
                outParms[attr] = int(getattr(gnomespice, attr))
                if outParms[attr] <= 0:
                    raise ValueError
            except ValueError:
                unitParms = unitParms + formerrmsg(attr, "a positive integer")
        elif parms[attr][1] == 'posdecimal':
            try:
                gridDict[attr] = float(getattr(gnomespice, attr))
                if gridDict[attr] <= 0:
                    raise ValueError
            except ValueError:
                unitParms = unitParms + formerrmsg(attr, "a positive decimal")
        elif parms[attr][1] == 'list':
            outParms[attr] = getattr(gnomespice, \
                                     attr).split(',')
        elif parms[attr][1] == 'listoflists':
            lists  = getattr(gnomespice, attr).split(';')
            outParms[attr] = []
            for list in lists:
                if list == '':
                    outParms[attr].append([])
                else:
                    outParms[attr].append(list.split(','))
        elif parms[attr][1] == 'bool':
            if float(getattr(gnomespice, attr)) == 'True':
                outParms[attr] = True
            elif float(getattr(gnomespice,attr)) == 'False':
                outParms[attr] = False
            else:
                unitParms = unitParms + formerrmsg(attr, 
                                                  "either 'True' or 'False'")
        elif parms[attr][1] == 'time':
            epoch = '00:00:00_01-01-1993'
            format = '%H:%M:%S_%m-%d-%Y'
            try:
                outParms[attr] = utils.timestr_to_nsecs(getattr
                                       (gnomespice, attr), epoch, format)
            except:
                unitParms = unitParms + formerrmsg(attr, 
                                                   "in the format " + format)

        else:
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
        if verbose: print "Instantiating parser for file {0}".format(f)
        try:
            parser = parse_geo.get_parser(f, filetype)
        except(IOError):
            if verbose: print "there was an IOError when instantiating parser"
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
if verbose: print('constructing grid '+str(datetime.datetime.now()))
griddef = gridDef(gridDict)
if gridFileName:
    if verbose: print('writing grid to file '+str(datetime.datetime.now()))
    utils.write_grid_to_netcdf(griddef, gridFileName)

# Map data to grid
if verbose: print('calculating maps '+str(datetime.datetime.now()))
mapFunc = getattr(map_geo, gnomespice.mapFunc + '_map_geo')
maps = [mapFunc(p, griddef, verbose) for p in parsers]

# Construct output
if verbose: print('creating outfiles '+str(datetime.datetime.now()))
outputs = outFunc(outParms)(maps,griddef,outFileName, verbose)

# eventually, we may want to do stuff to outputs, but for now...
del(outputs)

