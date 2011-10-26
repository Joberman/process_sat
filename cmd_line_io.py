'''
User-interface (command line only) for the raster processing
routines

Contains functions to interactively get the requirements
from the user.  However, it should be possible to run
all functions from a python script/command line without
needing to do anything interactively
'''
import map_geo
import grid_geo
import out_geo
    
def generate_griddef():
    """Interactively generate a GridDef instance from console input"""
    propLimits = {"stdPar1"  : ((lambda x: x > -90 and x < 90), float),
                  "stdPar2"  : ((lambda x: x > -90 and x < 90), float),
                  "refLat"   : ((lambda x: x > -90 and x < 90), float),
                  "refLon"   : ((lambda x: True), float),
                  "earthRadius" : ((lambda x: True), float),
                  "xOrig"    : ((lambda x: True), float),
                  "yOrig"    : ((lambda x: True), float),
                  "xCell"    : ((lambda x: x > 0), float),
                  "yCell"    : ((lambda x: x > 0), float),
                  "nRows"    : ((lambda x: x > 0), int),
                  "nCols"    : ((lambda x: x > 0), int)}
    while True:
        print("Valid projections are: ")
        print("\n".join(grid_geo.ValidProjections()))
        projName = raw_input("Please enter a valid projection: ")
        try:
            projClass = getattr(grid_geo, "%s_GridDef" % projName)
        except(AttributeError):
            print("Projection not available. Please try again")
            continue
        break
    gridDict = dict()
    for (prop, (limsFunc, caster)) in propLimits.items():
        if prop in projClass.requiredParms():
            valid = False
            first = True
            while not valid:
                if not first: print("Invalid entry.  Please try again.")
                value = raw_input("Please enter a value for %s: " % prop)
                first = False
                try:
                    value = caster(value)
                except(ValueError, TypeError):
                    continue
                valid = limsFunc(value)
            gridDict[prop] = value
    return projClass(gridDict)

def ask_for_map():
    '''Get the user to specify a valid mapping function'''
    while True:
        print("Valid mapping functions are: ")
        print('\n'.join(map_geo.ValidMaps()))
        mapName = raw_input("Please enter a valid mapping function: ")
        try:
            mapClass = getattr(map_geo, '%s_map_geo' % mapName)
        except(AttributeError):
            print("Map not available.  Please try again.")
            continue
        break
    return mapClass

def get_val_instr():
    '''Display instructions to user for get_val'''
    print("\nPress enter to accept value in parentheses.\n")

def get_val(default, prompt, limFunc=(lambda x: True), cast=(lambda x: x)):
    '''
    Get a value from the user using prompt.
    
    If the user presses enter w/o entering anything,
    the default value is returned.  These instructions
    are contained in get_val_instr().
    
    cast represents how the answer is cast before being
    checked by limFunc/returned.  It should be a callable
    that casts the input.  If cast is not passed, a string
    is returned
    
    limFunc, if given, represents a limit on valid values.
    It should return True for valid values, False otherwise.
    It checks all values that would be output, including
    the default.  If no limFunc is given, all values that
    cast correctly are allowed.
    '''
    valid = False
    first = True
    while not valid:
        if not first:
            print("Invalid answer.  Please try again.")
        first = False
        ans = raw_input(prompt+' (%s): ' % str(default))
        # replace empty string with default
        if not ans: ans = default
        try:
            ans = cast(ans)
        except(AttributeError, TypeError):
            continue
        valid = limFunc(ans)
    return ans

def ask_for_outfuncs():
    '''Get the user to specify desired output function(s)'''
    outfuncs = []
    while True:
        print("Valid output functions are: ")
        print('\n'.join(out_geo.ValidOutfuncs()))
        outName = raw_input("Please enter a valid output function name: ")
        try:
            outfuncClass = getattr(out_geo, '%s_out_func' % outName)
        except(AttributeError):
            if len(outfuncs) > 0:
                # provide user option if they want to accept what they
                # have already, or keep trying.
                ans = get_yn("Invalid name.  Do you wish to try entering\
                another new name?  If no, those functions already \
                specified will be used. (y/n): ")
                if ans == 'y':
                    continue
                else:
                    break
            else:
                print("Invalid name.  Please enter different name.")
                continue
        # the next line likely causes more IO from outfuncClass.__init__
        outfuncs.append(outfuncClass())
        ans = get_yn("Do you wish to specify more output functions? (y/n): ")
        if ans == 'y':
            continue
        else:
            break
    return outfuncs

def get_yn(prompt):
    '''
    Get an answer of yes or no from user
    
    returns 'y' or 'n'
    '''
    valid = False
    first = True
    while not valid:
        if not first:
            print("Answer must be y or n.")
        first = False
        ans = raw_input(prompt)
        valid = ans in ['Y', 'y', 'n', 'N']
    return ans.lower()

def ask_for_extension():
    '''See if the user wants to specify override extension'''
    override = get_yn("Do you want to enter an override extension? (y/n): ")
    if override == 'y':
        return get_val(None, "Enter override extension without punctuation.")
    else:
        return None
    
def ask_for_subtype():
    '''See if the user wants to specify a subtype'''
    wantstype = get_yn("Do you want to enter a file subtype? (y/n): ")
    if wantstype == 'y':
        return get_val('', "Enter file subtype.")
    else:
        return ''

def bad_file(filename):
    '''
    Determine what the user wants to do when one of the
    files turns out to be invalid.  
    
    Outputs an integer 1, 2 or 3.
        1 - skip file and move on
        2 - stop reading in files but continue processing
        3 - quit program
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
        processing.  Enter (3) to quit this program. Enter \n\
        your selection here: " % filename
        answer = raw_input(prompt)
        try:
            answer = int(answer)
        except(ValueError, TypeError):
            continue
        valid = answer in [1,2,3]
    return answer
    
