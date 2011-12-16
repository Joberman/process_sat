'''
Framework for creating output from satellite files

All function classes are named after the convention 
func_out_geo.  The function ValidOutfuncs 
automatically maintains a list of implemented
output functions

When INITIATED, output functions may accept a dictionary of
fieldnames and a dictionary of parameters.  If these parameters
are not passed, the constructor is expected to ask the user for
input, but no actual IO should take place in this class (all
io should be piped through the designated IO class)

All output function classes must accept a list of the outputs
from map_geo functions, a GridDef instance, and a base 
output filename when CALLED, in that order.  Note that all 
output functions are not required to use all these
inputs, but they *do* have to accept them without throwing
errors.  Also note that this means all valid outfunc classes
will have a __call__ method with the following syntax.  Many call functions
also implement an additional parameter "verbose" that, when set, prevents the 
function from dumping to the command line.

Output functions have a significant amount of freedom in
what they can do.  They may write files and/or return
data.  At this point, the specifications for returned
data have not yet been decided upon.  returned files
must be saved into the filenames based on the base
filename passed (IE if output0 is passed, a function
may choose to call outputs output0-0, output0-1, etc...
though something more descriptive is preferable)
'''
import sys
from itertools import izip
import datetime
import warnings
import pdb


import numpy
from scipy.io import netcdf_file

import utils

def ValidOutfuncs():
    '''Return a list of valid output function names'''
    currentModule = sys.modules[__name__]
    names = dir(currentModule)
    return [el[:-9] for el in names if el.endswith("_out_func")]

class out_func:
    '''Abstract class to for <>_out_geo classes'''
    def __init__(self, parmDict=None):
        self.parmDict = parmDict
    def __call__(self, map_geo, griddef, outfilenames, verbose):
        raise NotImplementedError
    @staticmethod
    def required_parms():
        raise NotImplementedError

def _OMNO2e_formula(cloudFrac, fieldOfView, totalFlag):
    eps = 1.5*pow(10,15)*(1+3*cloudFrac)
    capE = pow(10,-16)*(18.5+2.8*pow(10,-4)*pow(abs(fieldOfView-29.7), 3.5))
    return (numpy.logical_not(totalFlag)*pow((eps*capE), -2))
    
class OMNO2e_wght_avg_out_func(out_func):
    '''
    Weighted avg based on OMNO2e algorithm

    Note: this algorithm doesn't note what to do when the weight for a term is
    nonzero, but the term itself contains a fillValue.  This assumption
    is checked by an assert statement in the code, so it won't be checked
    if optimization is requested
    
    OMNO2e algorithm and theoretical basis laid out
    at <http://disc.sci.gsfc.nasa.gov/Aura/data-holdings/OMI/omno2e_v003.shtml>
    
    Set up to work specifically for OMI instruments.
    
    parameters dict must contain keys:
        toAvg
        overallQualFlag
        cloudFrac
        solarZenithAngle
        cloudFractUpperCutoff
        solarZenAngUpperCutoff
        pixIndXtrackAxis
        fillVal
    
    writes out a single file of name outfilename
    when called.  That file is an ASCII representation
    weighted averages for each gridcell.  It is a csv 
    file with all numbers in e-format scientific 
    notation.  Cells without valid measurements contain the fillvalue.
    '''  
    @staticmethod
    def required_parms():
        return {'toAvg' : ('The name of the field to be averaged',None),
                'overallQualFlag' : ('The name of the field containing' \
                                     ' the overall quality flag',None),
                'cloudFrac' : ('The name of the field containing the ' \
                               'cloud fraction',None),
                'solarZenithAngle' : ('The name of the field containing the ' \
                                      'solar zenith angle',None),
                'cloudFractUpperCutoff' : ('The maximum cloud fraction to ' \
                                           'include (0<=x<=1)','decimal'),
                'solarZenAngUpperCutoff' : ('The maximum solar zenith angle ' \
                                            'to include (in degrees 0<=x<=90)'\
                                            ,'decimal'),
                'pixIndXtrackAxis' : ('The element of each index tuple ' \
                                      'representing the cross-track index ' \
                                      '(...whatever that means)','int'),
                'fillVal' : ('The value with which to fill cells without ' \
                             'valid measurements','decimal')}
    
    def __call__(self, maps, griddef, outfilename, verbose):
        '''Write out single weighted-avg file'''
        numpy.seterr(over='raise')
        nRows = griddef.indLims()[1] - griddef.indLims()[0] + 1
        nCols = griddef.indLims()[3] - griddef.indLims()[2] + 1
        sum_weights = numpy.zeros((nRows, nCols))
        sum_weighted_vals = numpy.zeros((nRows, nCols))
        if not isinstance(maps, list):
            maps = [maps] # create list if we didn't get one
        for map in maps:
            with map.pop('parser') as p: # pop out so we can loop
                if verbose:
                    print('Processing {0} for output at {1}.'.format(\
                            p.name, str(datetime.datetime.now())))
                for (k,v) in map.iteritems():
                    sumFlag = numpy.array([p.get_cm(self.parmDict['overallQualFlag'], pxind)
                                            for (pxind, unused_weight) in v])
                    sumFlag = numpy.mod(sumFlag, 2)
                    cFrac = numpy.array([p.get_cm(self.parmDict['cloudFrac'], pxind)
                                          for (pxind, unused_weight) in v])
                    cFracFlag = cFrac > self.parmDict['cloudFractUpperCutoff']
                    solZen = numpy.array([p.get_cm(self.parmDict['solarZenithAngle'], pxind)
                                          for (pxind, unused_weight) in v])
                    solZenFlag = solZen > self.parmDict['solarZenAngUpperCutoff']
                    totFlag = numpy.logical_or(numpy.logical_or(sumFlag, cFracFlag), solZenFlag)
                    fov = numpy.array([pxind[self.parmDict['pixIndXtrackAxis']]
                                        for (pxind, unused_weight) in v])
                    toAvg = numpy.array([p.get_cm(self.parmDict['toAvg'], pxind)
                                          for (pxind, unused_weight) in v])
                    weights = _OMNO2e_formula(cFrac, fov, totFlag)
                    assert ~any(numpy.logical_and(~numpy.isnan(weights), numpy.isnan(toAvg)))
                    sumWeight = numpy.nansum(weights)
                    sumWeightVals = numpy.nansum(toAvg*weights)
                    # only add if we had some element (otherwise we fill
                    # sum_weights with nans)
                    if ~numpy.isnan(sumWeight) and ~numpy.isnan(sumWeightVals): 
                        sum_weights[k] += sumWeight
                        sum_weighted_vals[k] += sumWeightVals
                map['parser'] = p  # return parser to map
        oldsettings = numpy.seterr(divide='ignore')  # ignore any div by zero errors
        avgs = numpy.where(sum_weights != 0, 
                           numpy.divide(sum_weighted_vals, sum_weights), 
                           self.parmDict['fillVal'])
        numpy.seterr(divide=oldsettings['divide'])  # reset to default
        numpy.savetxt(outfilename, avgs, delimiter=',', fmt='%7e')
        return avgs

class OMNO2e_netCDF_avg_out_func(out_func):
    '''
    Weighted average for a given set of filtered values
    based on OMNO2e algorithm.
    
    Assumptions:
        - this algorithm assumes that fields to be averaged will have,
        at most, 1 extra dimension.  If not, an assertion error is raised.
        - this algorithm is undefined for cases where the weight of a term
        is nonzero, but the term contains a fillValue.  If this condition
        is met, unexpected results may occur.  This assumption is NOT checked
        - The timestamp of the file is assumed to be in the TAI93 standard.
    
    OMNO2e algorithm and theoretical basis laid out
    at <http://disc.sci.gsfc.nasa.gov/Aura/data-holdings/OMI/omno2e_v003.shtml>
    
    Set up to work specifically for OMI instruments.

    fieldnames dict must contain keys:
        overallQualFlag:
            Flag used as overall quality.  Assumed that
            when this flag is set, the data is BAD and 
            the pixel is ignored
        cloudFrac:
            field with cloud fraction (0 to 1).  When this
            field is GREATER than the cutoff value the
            pixel is ignored.
        solarZenithAngle: 
            Field with solar zenith angle (in degrees). 
            When this field is GREATER than the cutoff
            value the pixel is ignored.
        time:
            Field with the timestamps for each pixel. 
            Assumed to be in TAI-93 format.  When
            this field is less than the timeStart 
            parameter or greater than the timeStop
            parameter the pixel is ignored.
        longitude:
            Field with the longitudes at cell centers.
            Used to estimate timezones of the pixels if
            'local' is selected for timeComparison.  Not
            used when timeComparison is 'UTC'

    parameters dict must contain keys:
        inFieldNames:
            List of fields to process.  Each of these
            is output as a seperate variable in the 
            netcdf output file.
        outFieldNames:
            List of desired output names.  Must be of the
            same length and co-indexed to the list above.
            These will be the actual variable names in
            the netcdf file.
        outUnits:
            List of string labels for the units of each
            output quantity.  Must be of the same length
            and co-indexed to the lists above.
        extraDimLabel: 
            List of the labels for the above extra 
            dimensions.  1 per variable.  Only used if the
            coindexed field has an extra dim. Must be of the
            same length and co-indexed to the lists above.
        extraDimSize:
            List of the sizes of the above extra dimensions.
            1 per variable.  If the coindexed field does not
            have an extra dim, put in 0 or 1.  Must be
            of the same length and co-indexed to the lists 
            above.
        timeComparison:
            Determines how the timeStart and timeStop 
            arguments are interpreted.  If the user selects
            'local', these arguments are interpreted as local
            times.  Only those pixels whose timestamps 
            indicate they lie in the desired span in local
            time will be included.  Daylight savings time
            is not considered and time zone calculations are
            only approximate.  If the users selects 'UTC'
            a straight comparison is done between the pixel
            timestamp and the timeStart and timeStop 
            arguments to see if the pixel is valid.
        timeStart:
            Initial time we want included in file.  Must
            be in format hh:mm:ss MM-DD-YYYY
        timeStop:
            Final Time we want in included in file.  Must
            be in format hh:mm:ss MM-DD-YYYY
        cloudFractUpperCutoff:
            Pixels with a higher cloud fraction than this 
            value will be ignored.
        solarZenAngUpperCutoff:
            Pixels with a higher solar zenith angle than
            this value will be ignored.
        pixIndXtrackAxis:
            The axis (IE which dimension in memory order)
            that specifies the pixels cross-track position.
            This way, the cross-track index number can
            be retrieved safely and used in the weighting
            function.
        fillVal:
            The value we want to use to denote missing data
            in the output file.  This will be documented
            within the output file itself.

    Outputs a netcdf file with name determined by outFileName
    parameter.  This netcdf file contains as many variables
    as there are inFieldNames passed.  Each variable
    is output as an average over the range of values
    where it was valid acccording to the averaging
    scheme dedfined in the NASA document linked above.
    '''
    @staticmethod
    def required_parms():
        return {'overallQualFlag' : ('The name of the field containing ' \
                                     'the overall quality flag',None),
                'cloudFrac' : ('The name of the field containing the ' \
                               'cloud fraction',None),
                'solarZenithAngle' : ('The name of the field containing the '\
                                      'solar zenith angle',None),
                'time' : ('The name of the field containing the timestamps', \
                          None),
                'longitude' : ('The name of the field containing longitudes '\
                               'at cell centers',None),
                'inFieldNames' : ('The fields to be output.  Input full ' \
                                  'field names delimited by commas','list'),
                'outFieldNames' : ('The names of the output variables.  ' \
                                   'Must be the same length as input fields, '\
                                   'and delimited by commas','list'),
                'outUnits' : ('The units for each of the output variables. ' \
                              'Must be the same length as the input fields, '\
                              'delimited by commas','list'),
                'extraDimLabel' : ('The labels for the extra dimensions '  \
                                   'present in the output variables.  Only ' \
                                   'used if output variable has an extra ' \
                                   'dimension.  Must be same length as input '\
                                   'field, delimited by commas','list'),
                'extraDimSize' : ('The size of the extra dimensions.  For '  \
                                  'variables without an extra dimension, use '\
                                  '0.  Must be the same length as the input'  \
                                  ' field, delimited by commas.','list'),
                'timeComparison' : ('The time filtering selection.  Select ' \
                                    '\'local\' (each pixel\'s timestamp is '  \
                                    'compared to the start/stop time for that'\
                                    ' pixel\'s approximate timezone) or '  \
                                    '\'UTC\'(where each pixel is compared '  \
                                    'to time in UTC standard)',None),
                'timeStart' : ('The first time to be included','int'),
                'timeStop' : ('The final time to be included','int'),
                'cloudFractUpperCutoff' : ('The maximum cloud fraction for ' \
                                           'valid pixels (0<=x<=1)','decimal'),
                'solarZenAngUpperCutoff' : ('The maximum solar zenith angle '\
                                            'for valid pixels (in degrees 0' \
                                            '<=x<=90)','int'),
                'pixIndXtrackAxis' : ('The element of each index tuple ' \
                                      'representing the cross-track index ' \
                                      'number','int'),
                'fillVal' : ('The fill value for cells that do not contain ' \
                             'valid data','decimal')}
    
    def __call__(self, maps, griddef, outfilename, verbose):
        '''Write out a weighted-average file in netcdf format.'''

        #Make sure non-string parameters are in the correct format
        dimsizes = self.parmDict['extraDimSize']
        for i in range(len(dimsizes)):
            try:
                dimsizes[i-1] = int(dimsizes[i-1])
            except ValueError:
                print ("Warning: {0} is not a valid extraDimSize value.  " \
                      "Using 0 instead").format(dimsizes[i-1])
                dimsizes[i-1] = 0
                continue
        self.parmDict['extraDimSize'] = dimsizes

        #Perform some basic sanity checks with parameters
        if self.parmDict['timeStart'] > self.parmDict['timeStop']:
            msg = 'Input start time must come before stop time.'
            raise IOError(msg)
        if (len(self.parmDict['inFieldNames']) !=  \
            len(self.parmDict['outFieldNames']) or  
            len(self.parmDict['inFieldNames']) !=  \
            len(self.parmDict['outUnits']) or      
            len(self.parmDict['inFieldNames']) !=  \
            len(self.parmDict['extraDimLabel'])):
            msg = 'All field/unit inputs ' + \
                'should have the same number of elements.'
            raise IOError(msg)

        # create numpy arrays to hold our data
        (minRow, maxRow, minCol, maxCol) = griddef.indLims()
        nRows = maxRow - minRow + 1
        nCols = maxCol - minCol + 1
        sumWght = numpy.zeros((nRows, nCols, 1))  # needs extra dim to generalize for 3D vars
        sumVars = dict()
        for field, size in zip(self.parmDict['inFieldNames'], self.parmDict['extraDimSize']):
            if size:
                sumVars[field] = numpy.zeros((nRows, nCols, size))
            else:
                # pad with a singlet dim if it was 2D
                sumVars[field] = numpy.zeros((nRows, nCols, 1))
        
        # loop over maps
        if not isinstance(maps, list):
            maps = [maps] # create list if we only got a single map
        
        for map in maps:
            # open up context manager
            with map.pop('parser') as p: # remove parser for looping
                if verbose:
                    print('Processing {0} for output at {1}.'.format(\
                            p.name, str(datetime.datetime.now())))
                # loop over gridboxes in map and calculate weights
                for (gridCell, pixTup) in map.iteritems():
                    # translate gridCell to account for possible non-zero ll corner
                    gridRow = gridCell[0]
                    gridCol = gridCell[1]
                    gridInd = (gridRow - minRow, gridCol - minCol)
                    # get the values needed to calculate weight
                    sumFlag = numpy.array([p.get_cm(self.parmDict['overallQualFlag'], pxind)
                                           for (pxind, unused_weight) in pixTup])
                    sumFlag = numpy.mod(sumFlag, 2)
                    cFrac = numpy.array([p.get_cm(self.parmDict['cloudFrac'], pxind)
                                          for (pxind, unused_weight) in pixTup])
                    cFracFlag = cFrac > self.parmDict['cloudFractUpperCutoff']
                    solZen = numpy.array([p.get_cm(self.parmDict['solarZenithAngle'], pxind)
                                          for (pxind, unused_weight) in pixTup])
                    solZenFlag = solZen > self.parmDict['solarZenAngUpperCutoff']
                    time = numpy.array([p.get_cm(self.parmDict['time'], pxind)
                                        for (pxind, unused_weight) in pixTup])
                    # calculate and factor in offsets if we wanted local time
                    if self.parmDict['timeComparison'] == 'local':
                        pixLons = (p.get_cm(self.parmDict['longitude'], pxind)
                                            for (pxind, unused_weight) in pixTup)
                        offsets = numpy.array([utils.UTCoffset_from_lon(lon) for lon in pixLons])
                        time += offsets
                    # create time flag
                    timeFlag = numpy.logical_or(time < self.parmDict['timeStart'],
                                                time > self.parmDict['timeStop'])
                    totFlag = numpy.logical_or(sumFlag, cFracFlag)
                    totFlag = numpy.logical_or(totFlag, solZenFlag)
                    totFlag = numpy.logical_or(totFlag, timeFlag)
                    fov = numpy.array([pxind[self.parmDict['pixIndXtrackAxis']]
                                        for (pxind, unused_weight) in pixTup])
                    # compute all weights and add if necessary
                    weights = _OMNO2e_formula(cFrac, fov, totFlag)
                    cellWght = numpy.nansum(weights)
                    # only bother with this if it matters
                    if cellWght > 0:
                        sumWght[gridInd] = numpy.nansum([sumWght[gridInd][0], cellWght])
                        # loop over variables we're outputting
                        for field in self.parmDict['inFieldNames']:
                            # pull out the array for this cell 
                            toAvg = numpy.array([p.get_cm(field, pxind) 
                                                 for (pxind, unused_weight) in pixTup])
                            assert len(toAvg.shape) <= 2
                            if len(toAvg.shape) == 1:
                                # pad toAvg 
                                toAvg = toAvg.reshape((toAvg.size, 1))
                                # check that we correctly set size
                                assert sumVars[field].shape[-1] == 1
                            else:
                                # check we correctly set size
                                assert sumVars[field].shape[-1] == toAvg.shape[-1]
                            # calculate weights and compute cell sum
                            weightVals = toAvg*weights[:,numpy.newaxis]              
                            cellVal = numpy.nansum(weightVals, axis=0)
                            # if we have valid data, add to totals 
                            sumVars[field][gridInd] = numpy.nansum([sumVars[field][gridInd], cellVal], axis=0)
                map['parser'] = p  # return parser to map
                
        # divide out variables by weights to get avgs. 
        oldSettings = numpy.seterr(divide='ignore')
        avgs = dict()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for (field,var) in sumVars.iteritems():
                unfiltAvgs = var/sumWght
                filtAvgs = numpy.where(sumWght != 0, unfiltAvgs, \
                           self.parmDict['fillVal'])
                # strip trailing singlet for 2D arrays
                if filtAvgs.shape[-1] == 1:
                    avgs[field] = filtAvgs.reshape(filtAvgs.shape[0:2])
                else:
                    avgs[field] = filtAvgs
        numpy.seterr(divide=oldSettings['divide'])
        
        # associate coindexed parameters into dicts 
        # so we can loop by field
        outFnames = dict(izip(self.parmDict['inFieldNames'], self.parmDict['outFieldNames']))
        units = dict(izip(self.parmDict['inFieldNames'], self.parmDict['outUnits']))
        extraDim = dict(izip(self.parmDict['inFieldNames'], self.parmDict['extraDimLabel']))
                
        # write out results to a netcdf file
        outFid = netcdf_file(outfilename, 'w')
        # create the 2 dimensions all files use
        outFid.createDimension('row', nRows)
        outFid.createDimension('col', nCols)
        # write global attributes
        setattr(outFid, 'File_start_time', utils.nsecs_to_timestr(self.parmDict['timeStart'], '00:00:00 01-01-1993'))
        setattr(outFid, 'File_end_time', utils.nsecs_to_timestr(self.parmDict['timeStop'], '00:00:00 01-01-1993'))
        setattr(outFid, 'Max_valid_cloud_fraction', self.parmDict['cloudFractUpperCutoff'])
        setattr(outFid, 'Max_valid_solar_zenith_angle', self.parmDict['solarZenAngUpperCutoff'])
        setattr(outFid, 'Time_comparison_scheme', self.parmDict['timeComparison'])
        fileListStr = ' '.join([map['parser'].name for map in maps])
        setattr(outFid, 'Input_files', fileListStr)
        setattr(outFid, 'Projection', griddef.__class__.__name__[:-8])
        for (k,v) in griddef.parms.iteritems():
            setattr(outFid, k, v)
        # loop over fields and write variables
        for field in self.parmDict['inFieldNames']:
            # create tuple of dimensions, defining new dim
            # if necessary
            if len(avgs[field].shape) == 2:
                # only row/cols
                varDims = ('row', 'col')
            elif len(avgs[field].shape) == 3:
                # has extra dim
                dimName = extraDim[field]
                dimSize = avgs[field].shape[2]
                outFid.createDimension(dimName, dimSize)
                varDims = ('row', 'col', dimName)
            # create and assign value to variable
            varHandle = outFid.createVariable(outFnames[field], 'd', varDims)
            varHandle[:] = avgs[field]
            # assign variable attributes
            setattr(varHandle, 'Units', units[field])
            setattr(varHandle, '_FillValue', self.parmDict['fillVal'])
        outFid.close()
        # create a dict with teh same data as avgs, but diff names
        outAvg = dict()
        for (k,v) in avgs.iteritems():
            outAvg[outFnames[k]] = v
        return outAvg
    
class wght_avg_vals_netCDF_out_func(out_func):
    '''
    Generalized weighted average algorithm
    
    Designed to compute the average of an arbitrary number of desired 
    parameters, with the value weights based on an arbitrary number of input
    parameters.  Note that values may be weighted according to their own value.
    
    The output will be in the form of a netcdf file with name determined by the
    outFileName parameter.  This netCDF file will have dimensions determined by
    the grid_geo file, as well as additional dimensions as required by the 
    input fields.  
    
    Owing to the complexity of the inputs required for this function and the 
    security problems posed by allowing users to input functions to be 
    evaluated, this output function does not support the I/O interface at this
    time.  It must be run in a script, with the parameters provided in scripts.
    
    fieldnames dict must contain the following keys:  
        time:
            The field associated with the timestamps.  Timestamps may be in any
            format so long as a function is provided to convert them to Unix 
            timestamp values (as this is what the function will use internally)
        longitude:
            Field with the longitudes at cell centers.  Used to estimate
            timezones of the pixels if local is selected for timeComparison.  
            Not used when timeComparison is 'UTC'
        
    parameters dict must contain keys:
        inFieldNames:
            List of strings corresponding to fields for which output is 
            desired.  These must be valid keys for the parser.  Each is output
            as a seperate variable in the netcdf output file.
        outFieldNames:
            List of strings corresponding to the names the output variables
            should have in the final netCDF file.  Must be of the same length
            and co-indexed to the list above.  
        outUnits:
            List of strings corresponding to the labels for the units of each 
            output variable.  These will be attached as the "units" attribute
            for each variable in the output netCDF file.  Must be of the same 
            length and co-indexed to the lists above.
        dimLabels:
            List of tuples, each of which contains as many strings as there are
            extra dimensions in the corresponding field.  IE, if a field has 
            dimensions (xtrack, time, layer, quant) and we allocate along
            xtrack and time, then the tuple for that field should be 
            ('layer', 'quant') so that the dimensions are named properly in the
            otuput netCDF file.  The list (not the individual tuples) must be
            of the same length and co-indexed to the lists above.  Note that 
            the dimensions looped over and allocated to cells in the map_geo
            function DO NOT need to be represented here.
        dimSizes:
            List of tuples, each of which contains as many integers as there
            are extra dimensions in the corresponding field.  IE if the field
            described in dimLabels had dimensions (60, 1300, 9, 4) then the 
            tuple for that field should be (9, 4).  The list (not the 
            individual tuples) must be of the same length and co-indexed to the
            lists above.  If the field has no extra dimensions, then an empty 
            tuple should be used as a placeholder.Note that the dimensions 
            looped over and allocated to cells in the map_geo function DO NOT
            need to be represented here.
        timeComparison:
            Determines how the timeStart and timeStop parameters are 
            interpreted.  Must be either 'local' or 'UTC'.  If 'local' is 
            selected, only those pixels in the desired timespan in in local 
            time will be included.  Daylight savings time is not considered and
            time zone calculations are approximate based on longitude.  If 
            'UTC' is selected, the raw timestamps are compared directly to the 
            timeStart and timeStop parameters, without attempting to account 
            for timezone.
        timeStart:
            Initial time we want included in the output file.  All measurements
            taken before this time will be discarded, even if they are included
            in the files passed to output function.  Must be a string of the 
            the format hh:mm:ss MM-DD-YYYY.
        timeStop:
            Final time to be included in the output file.  All measurements
            taken after this time will be discarded.  Must be a string of the
            format hh:mm:ss MM-DD-YYYY.
        timeConv:
            Function that converts timeStart and timeStop (both of which are 
            strings of the format hh:mm:ss MM-DD-YYYY) into the format used to
            store time within the parser.  IE if the parser returns time in 
            TAI93, then this function should convert a string
            hh:mm:ss MM-DD-YYYY to TAI93.
        fillVal:
            The value with which we want to denote missing data in the output
            file.  This value must be castable to the type of all output 
            variables.  Each variable will document the fill value in its
            attributes.
        logNormal:
            Boolean parameter indicating whether or not we want to take the
            lognormal mean (as opposed to the simple, arithmetic mean).  If 
            this parameter is set to True, the mean will be taken as follows:
                logData = log(data)
                logAvg = sum(logData*wghts)/sum(wghts)
                avg = 10^logAvg
            whereas if this parameter is set to false the mean will be simply:
                avg = sum(data*wghts)/sum(wghts)
        weightFunction:
            Function that computes the weight of a value.  This can be as 
            simple as assigning a weight of 1 to that value (creating an 
            unweighted average) or using multiple fields to generate a weight
            for each pixel.  The function must be of the form:
                weight = weightFunction(parser, index, prevWght)
            where parser is the parser for the file under consideration, ind
            is the tuple of indices for the pixel under consideration, and
            prevWght is the weight as computed by the mapping function.  Note
            that in authoring these functions it is safe to use both the get()
            and get_cm() functions of the parser argument.  The function may 
            return either 0 or NaN for pixels that should not be considered in
            the average.  Either will be handled appropriately.  The docstring 
            for this function will be included as a global attribute in the 
            output file, so the docstring should be sufficient to describe the
            function in it's entirety.
    '''
    def __init__(self, fieldnames, parms):
        out_func.__init__(self, fieldnames, parms)
        # convert all the parameters co-indexed to inFieldNames to dictionaries
        # keyed off of inFieldNames
        toConvert = ['outFieldNames', 'outUnits', 'dimLabels', 'dimSizes']
        inFnames = self.parms['inFieldNames']  
        for key in toConvert:
            self.parms[key] = dict(zip(inFnames, self.parms[key]))
        
    def __call__(self, maps, griddef, outfilename, verbose):
        '''Write out a weighted-average file in netcdf format.'''
        
        # create a dictionary of numpy arrays that will hold the data for all 
        # our variables, keyed to inFieldNames
        (minRow, maxRow, minCol, maxCol) = griddef.indLims()
        nRows = maxRow - minRow + 1
        nCols = maxCol - minCol + 1
        outputArrays = dict()
        for field in self.parms['inFieldNames']:
            dims = [nRows, nCols]
            dims.extend(self.parms['dimSizes'][field])
            outputArrays[field] = numpy.zeros(dims)
            
        # prep for computing weights
        wghtDict = dict()  # we only want to compute each weight once
        wghtFunc = self.parms['weightFunction']
        
        # convert the times to the proper format
        tConvFunc = self.parms['timeConv']
        timeStart = tConvFunc(self.parms['timeStart'])
        timeStop = tConvFunc(self.parms['timeStop'])
            
        # loop over maps
        if not isinstance(maps, list):
            maps = [maps] # create list if we didn't get one
        for map in maps:
            with map.pop('parser') as p: 
                if verbose:
                    print('Processing %s for output at %s' %
                          (p.name, str(datetime.datetime.now())))
                    
                # loop over the cells in the map, processing each
                for (cellInd, pixTups) in map.iteritems():
                    
                    # compute the weight only if we haven't already
                    wghts = [wghtDict.setdefault(ind, wghtFunc(p, ind, wgt))
                            for (ind, wgt) in pixTups]
                    
                    # create the time array we'll be using to filter
                    tArray = numpy.array([p.get_cm(self.fnames['time'], ind)
                                          for (ind, wgt) in pixTups])
                    if self.parms['timeComparison'] == 'local':
                        offsets = numpy.array([utils.UTCoffset_from_lon(
                                               p.get_cm(self.fnames['longitude'], ind)) 
                                               for (ind, wgt) in pixTups])
                        tArray += offsets
                    tFlag = numpy.logical_or(tArray < timeStart, tArray > timeStop)
                    
                    # loop over fields.  For each, compute avg and save
                    for field in self.parms['inFieldNames']:
                        
                        # create the array of weighted values    
                        vals = numpy.array([p.get_cm(field, ind)
                                            for (ind, wgt) in pixTups])
                        if self.parms['logNormal']:
                            vals = numpy.log(vals) # work with logarithm of data
                        wghtSlice = [Ellipsis]
                        nExtraDims = len(self.parms['dimSizes'][field])
                        # create a slice object that will allow us to broadcast
                        # weights against the values
                        wghtSlice.extend([numpy.newaxis]*nExtraDims)
                        wghtVals = numpy.where(tFlag, numpy.NaN, vals*wghts[wghtSlice])
                        
                        # average the weighted Values
                        wghtValSum = numpy.nansum(wghtVals, axis=0)
                        wghtSum = numpy.nansum(wghts, axis=0)
                        # avoid hassle with div/0 warnings
                        if wghtSum != 0:
                            wghtValAvg = wghtValSum/wghtSum
                        else:
                            wghtValAvg = numpy.NaN
                        
                        # re-exponentiate if we took log average
                        wghtValAvg = numpy.exp(wghtValAvg)
                        
                        # mask nan's with fillVal, then slot into output array
                        wghtValAvg = numpy.where(numpy.isnan(wghtValAvg),
                                                 self.parms['fillVal'], 
                                                 wghtValAvg)
                        outputArrays[field][cellInd] = wghtValAvg
        
                    # done looping over fields
                # done looping over cells
            # done with context manager on parser
                        
            # return the parser to the map so it can be used elsewhere
            map['parser'] = p
            if verbose:
                print('Done processing %s at %s' %
                      (p.name, str(datetime.datetime.now())))
            
        # done looping over maps
        
        # set up the parts of the netcdf file that AREN'T field specific
        outFid = netcdf_file(outfilename, 'w')
        outFid.createDimension('row', nRows)
        outFid.createDimension('col', nCols)
        # set global attributes
        setattr(outFid, 'File_start_time', self.parms['timeStart'])
        setattr(outFid, 'File_stop_time', self.parms['timeStop'])
        setattr(outFid, 'Time_comparison_scheme', self.parms['timeComparison'])
        flistStr = ' '.join([map['parser'].name for map in maps])
        setattr(outFid, 'Input_files', flistStr)
        setattr(outFid, 'Avg_func_description', wghtFunc.__doc__)
        # add in attributes for the projection
        setattr(outFid, 'Projection', griddef.__class__.__name[:-8])
        for (k,v) in griddef.parms.iteritems():
            setattr(outFid, k, v)
            
        # loop over fields and write all information for each field
        for field in self.parms['inFieldNames']:
            
            # create the dimensions in the file
            extraDimSizes = self.parms['dimSizes'][field]
            extraDimLabels = self.parms['dimLabels'][field]
            for (size, label) in zip(extraDimSizes, extraDimLabels):
                outFid.createDimension(label, size)
                
            # write the variable to file
            vDims = ['row', 'col']
            vDims.extend(extraDimLabels)
            outFieldName = self.parms['outFieldNames'][field]
            varHand = outFid.createVariable(outFieldName, 'd', vDims)
            varHand[:] = outputArrays[field]
            
            # write variable attributes
            setattr(varHand, 'Units', self.parms['outUnits'][field])
            setattr(varHand, '_FillValue', self.parms['fillVal'])
            
        # flush the output file to disk
        outFid.close()
        
        # create an output dictionary keyed to output field names
        finalOutArrays = dict()
        for (k,v) in outputArrays.iteritems():
            finalOutArrays[self.parms['outFieldNames'][k]] = v
        return finalOutArrays 
            
