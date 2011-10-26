'''
Created on May 26, 2011

@author: oberman
'''
import os
import datetime
from itertools import izip

import cmd_line_io as geo_io

from parse_geo import get_parser

def process_files(directory=None, filelist=None, extension=None, subtype='',
                   griddef=None, mapFunc=None, outFuncs=None, 
                   outFileNames=None, parserList=None, verbose=True):
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

    OutFileNames are expexted to passed as a LIST of the same length
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
    directory = directory or os.getcwd()
    filelist = filelist or os.listdir(directory)
    griddef = griddef or geo_io.generate_griddef()
    mapFunc = mapFunc or geo_io.ask_for_map()
    outFuncs = outFuncs or geo_io.ask_for_outfuncs()
    outFileNames = outFileNames or \
        [os.path.join(directory, 'output%s' % i) for i in range(len(outFuncs))]
    extension = extension or geo_io.ask_for_extension()
    subtype = subtype or geo_io.ask_for_subtype()
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
                parsers.append(get_parser(f, subtype, extension))
            except(IOError):
                answer = geo_io.bad_file(f)
                if answer is 1:
                    continue
                elif answer is 2:
                    break
                elif answer is 3:
                    raise SystemExit
    if verbose: print('calculating maps '+str(datetime.datetime.now()))
    maps = [mapFunc(p, griddef) for p in parsers]
    if verbose: print('creating outfiles '+str(datetime.datetime.now()))
    outputs = [out(maps, griddef, fnames)
                for (out, fnames) in izip(outFuncs, outFileNames)]
    # eventually, we may want to do stuff to outputs, but for now...
    del(outputs)
    

if __name__ == '__main__':
    process_files()