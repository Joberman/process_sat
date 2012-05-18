'''
Framework for parsing geolocated satellite files

Instantiates appropriate class with filename and
optional strings specifying the subtype of file and 
an override extension.

All classes store the following parameters:
    name - the full pathname of the file
    ext - the extension of the file
    sub - the subtype of the file

Variables in the file are accessible through the get method
which optionally retrieves individual indices.  The optional 
parameter indices should specify which indices to retrieve
in a tuple.  Multidimensional variables are retrieved as 
slices along the "common" dimensions (not those unique to the
 variable).  Not passing indices will result in the retrieval
 of all the data from that variable, though the dimensionality
 of that data is not guaranteed.  Returns nan's for
 missing data values ONLY FOR TYPES THAT START AS FLOATS.  Int types 
keep their original fill value, but it it scaled and offset along
with everything else (so if you want to test for it, apply the
scale and offset to the fill value before testing)

Parser is responsible for properly applying scale-offset
to retrieved data.  

Parsers should throw IOError if passed an invalid file

There are several special methods that must return specific
data regardless of filetype.  These methods are used
by mapping functions, so they only have to be implmented
if the desired mapping function requires them.
    get_geo_corners() - returns a record array with three fields.
                        The first field, lat, contains 4 floats, 
                        the latitudes of the 4 corners.  The field
                        lon contains 4 floats, the longitudes of 
                        the 4 corners.  The field ind is as 
                        large as it needs to be to contain the 
                        indices.  each ind should be castable
                        to a tuple that can be fed into get.
    get_geo_centers() - returns a record arraw with 3 fields.  The
                        first field, lat, contains the latitude of
                        the pixel center.  The lon field contains
                        the longitude of the pixel center.  The
                        field ind is as alarge as it needs to be
                        to contain the indices.  If cast to a 
                        tuple and fed into the get() function,
                        it should retrieve the same pixel
                        
The following functions may be implemented or not in any class.
They duplicate the functionality of the get function but in
some cases may allow for much more efficient operation.  If 
they are not implemented, they are expected to throw a
NotImplementedError when called.
    __enter__()                - enter method for context manager
    __exit__()                 - exit method for context manager
    get_cm(key, ind=(:)) - an alternate form of the get statement meant to be
                 used inside of a context manager (with statement).
                 Requiring use of a context manager enables 
                 any files to be left open, improving efficiency.
                 While it is not required, it is recommended that this
                 method throw some kind of error when called outside a
                 context manager.  Must operate exactly the same as
                 the get function in terms of inputs and output.
                 
This framework can be extended by adding classes for particular (sub)class
'''

import os
import sys
import string
import pdb

import tables
import numpy
import pyhdf.HDF
import pyhdf.V
import pyhdf.VS
import pyhdf.SD

import filetypes

def SupportedFileTypes():
    '''Return a list of supported file types'''
    return [el[:-9] for el in dir(filetypes) if el.endswith("_filetype")]


def getOrbitNumber(fPath):    
    '''Takes in the path to a nasa omi hdf file and returns the orbit number'''
    fid = tables.openFile(fPath)
    try:
        node = fid.getNode('/', 'HDFEOS INFORMATION/CoreMetadata')
    except tables.exceptions.NoSuchNodeError:
        node = fid.getNode('/', 'HDFEOS INFORMATION/CoreMetadata.0')
    bigString = str(list(node)[0])
    strings = bigString.split('\n')
    for i in range(len(strings)):
        if 'ORBITNUMBER' in strings[i]:
            break
    line = strings[i+3]
    numArray = [int(el) for el in line.split() if el.isdigit()]
    fid.close()
    return numArray[0]

def getLongName(fPath):
    '''Retrieve the long name of an HDFEOS file'''
    fid = tables.openFile(fPath)
    try:
        node = fid.getNode('/', 'HDFEOS INFORMATION/ArchiveMetadata')
    except tables.exceptions.NoSuchNodeError:
        node = fid.getNode('/', 'HDFEOS INFORMATION/ArchiveMetadata.0')
    bigString = str(list(node)[0])
    strings = bigString.split('\n')
    for i in range(len(strings)):
        if 'LONGNAME' in strings[i]:
            break
    line = strings[i+2]
    chunks = line.split('"')
    fid.close()
    return chunks[-2]

def get_parser(file, filetype, parserParms):
    """Retrieve appropriate instantiated parser for a file"""
    # filename = os.path.split(file)[1]
    subclass = '{0}_File'.format(filetype)
    module = sys.modules[GeoFile.__module__]
    parserClass = getattr(module, subclass) 
                  # or GeoFile
    extension = ''
    subtype = ''
    for i in filetype:
        if subtype == '' and i in string.ascii_uppercase:
            extension += i
        else:
            subtype += i
    return parserClass(file, subtype, extension, **parserParms)

class GeoFile():
    """Provide interface to geofile."""
    def __init__(self, filename, subtype='', extension=None):
        self.name = filename
        self.ext = extension or os.path.splitext(filename)[1][1:]
        self.sub = subtype
    def get(self, key, indices=None):
        raise NotImplementedError
    def get_geo_corners(self):
        raise NotImplementedError
    def get_geo_centers(self):
        raise NotImplementedError
    def __enter__(self):
        raise NotImplementedError
    def __exit__(self):
        raise NotImplementedError
    def get_cm(self, key, indices=None):
        raise NotImplementedError

class HDF4File(GeoFile):
    """Provide generic interface for HDF 4 files"""
    def __init__(self, filename, subtype='', extension=None):
        GeoFile.__init__(self, filename, subtype=subtype, extension=extension)
        if pyhdf.HDF.ishdf(self.name):
            pass
        else:
            raise IOError('Attempt to read non HDF4 file as HDF4')

    def walkHDF4(self, fid, pathList, vInt, vsInt, sdInt):
        """
        Retrives a variable or variable group from an HDF4 file

        Requires the file handle fid and a list that contains each
        element of the path to the leaf that we want.  Returns the leaf,
        which may be of any type.

        Assumes that the leaf we want is a Vgroup or Vdata datatype.

        Arguments vInt and vsInt are the VG and VS interfaces
        as defined by pyhdf.  If passed, they  WILL NOT
        be closed.  

        To repeat, if the interfaces are passed in they will NOT be
        safely closed.
        """
        leafName = pathList[-1] # name of the leaf we want
        # get it the easy way if it's a scientific dataset
        sciData = sdInt.datasets()
        if leafName in sciData:
            return sdInt.select(leafName)
        # it must not be a scientific dataset, so walk the file to find it
        pList = list(pathList) # shallow Copy
        parent = vInt.attach(vInt.getid(-1))
        pName = pList.pop(0)
        if parent._name != pName:
            raise AttributeError("Bad data path (did not start at root).")
        while parent._name != leafName:
            cName = pList.pop(0)
            children = parent.tagrefs()
            for (childType, childRef) in children:
                
                if childType == pyhdf.HDF.HC.DFTAG_VG:
                    child = vInt.attach(childRef)
                elif childType == pyhdf.HDF.HC.DFTAG_VH:
                    child = vsInt.attach(childRef)
                elif childType == pyhdf.HDF.HC.DFTAG_NDG:
                    # we know this can't be it so keep looking
                    continue
                else:
                    raise IOError('Unknown data format.  Check data structure.')

                if child._name == cName:
                    parent.detach()
                    parent = child
                    break
                else:
                    child.detach()
                    
            if parent is not child:
                raise AttributeError('Bad data path.  Check parser/data structure.')

        return parent

    def get(self, key, indices=None, missingValue=None):
        """
        Provide get functionality for HDF 4 files.  

        Assumes absolutely no attributes present.

        If missingValue is provided, it will be used to mask floating
        point data properly with NaN's.  If it is not provided, the data
        will be returned as is, -9999.0's and all.

        Requires that parser be set up with _nameExpMap and _indexMap 
        variables.  These must be defined as:
        
        _nameExpMap -   Dictionary.  Keys are field names available to user.
                        Values are the full path to that field in the HDF file.
                       
        _indexMap -     Dictionary.  Keys are field names available to user.  
                        Values are functions that when passed (var, ind) where
                        ind is a n-element tuple will return the proper slice.
                        n is the number of fundamental dimensions of the 
                        file type.
        """
        fid = pyhdf.HDF.HDF(self.name)
        try:
            vInt = fid.vgstart()
            vsInt = fid.vstart()
            sdInt = pyhdf.SD.SD(self.name)
            path = self._nameExpMap[key]
            pathList = [el for el in path.split('/') if el] # path list with no empty strings
            vNode = self.walkHDF4(fid, pathList, vInt, vsInt, sdInt)
            vData = numpy.array(vNode[:])
        except AttributeError as err:
            raise IOError("No field %s.  May be attempt to read non-MOPPIT file as such." % self._nameExpMap[key])
        except KeyError:
            raise IOError("Attempt to use fieldname not associated with this filetype.")
        finally:
            # clean up from the bottom up
            try:
                vNode.detach()
            except(NameError):
                pass
            except(AttributeError):
                # must have been a scientific dataset
                vNode.endaccess()

            try:
                sdInt.end()
            except(NameError):
                pass

            try:
                vsInt.end()
            except(NameError):
                pass

            try:
                vInt.end()
            except(NameError):
                pass

            fid.close
        
        # convert missing values if appropriate
        if missingValue and vData.dtype in ['float32', 'float64']:
            vData = numpy.where(vData == missingValue, numpy.NaN, vData)

        # use indices if we have them
        if indices is not None:
            # we want specific indices, use _indexMap
            indFunc = self._indexMap.get(key, self._indexMap['default'])
            return indFunc(vData, indices)
        else:
            # just fetch everything
            return vData

    def __enter__(self):
        '''Open up file and leave open.'''
        self._fid = pyhdf.HDF.HDF(self.name)
        self._open_vars = dict()
        self._vsInt = self._fid.vstart()
        self._vInt = self._fid.vgstart()
        self._sdInt = pyhdf.SD.SD(self.name)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        '''Close file and delete references to file object and nodes.'''
        self._sdInt.end()
        self._vsInt.end()
        self._vInt.end()
        self._fid.close()
        del self._open_vars
        del self._fid
        del self._vsInt
        del self._vInt
        return False

    def get_cm(self, key, indices=None, missingValue=None):
        """
        Provide get_cm function for HDF files

        get_cm works the same as get, but relies on a context manager to speed
        up access by allowing it safely leave open variables in memory.

        Assumes absolutely no attributes present.

        If missingValue is provided, it will be used to mask floating
        point data properly with NaN's.  If it is not provided, the data
        will be returned as is, -9999.0's and all.

        Requires that parser be set up with _nameExpMap and _indexMap 
        variables.  These must be defined as:
        
        _nameExpMap -   Dictionary.  Keys are field names available to user.
                        Values are the full path to that field in the HDF file.
                       
        _indexMap -     Dictionary.  Keys are field names available to user.  
                        Values are functions that when passed (var, ind) where
                        ind is a n-element tuple will return the proper slice.
                        n is the number of fundamental dimensions of the 
                        file type.
        """
        # open the variable if it isn't open already.
        if key not in self._open_vars.keys():
            try:
                path = self._nameExpMap[key]
                pathList = [el for el in path.split('/') if el] 
                vNode = self.walkHDF4(self._fid, pathList, self._vInt, self._vsInt, self._sdInt)
                self._open_vars[key] = numpy.array(vNode[:])
                try:
                    vNode.detach()
                except AttributeError:
                    # must have been a scientific dataset
                    vNode.endaccess()
            except AttributeError:
                raise IOError("No field %s.  May be attempt to read non-MOPPIT file as such." % self._nameExpMap[key])
            except KeyError:
                raise IOError("Attempt to use fieldname %s, which is not associated with this filetype." % key)
                
            # convert missing values if appropriate
            if missingValue and self._open_vars[key].dtype in ['float32', 'float64']:
                self._open_vars[key] = numpy.where(self._open_vars[key] == missingValue,
                                                   numpy.NaN, self._open_vars[key])

        # retrieve value of interest from the (newly?) open variable
        if indices is not None:
            # we want specific indices, use _indexMap
            indFunc = self._indexMap.get(key, self._indexMap['default'])
            return indFunc(self._open_vars[key], indices)
        else:
            # just fetch everything
            return self._open_vars[key]
            
class HDFFile(GeoFile):
    """Provide generic interface for HDF 5 files"""
    def __init__(self, filename, subtype='', extension=None):
        GeoFile.__init__(self, filename, subtype=subtype, extension=extension)
        if tables.isHDF5File(self.name):  # sanity check
            pass
        else:
            raise IOError('Attempt to read non-HDF 5 file as HDF 5.')
        
    def get(self, key, indices=None):
        """
        Provide get function for HDF Files.
        
        Requires that parser be set up with _nameExpMap and _indexMap 
        variables.  These must be defined as:
        
        _nameExpMap -   Dictionary.  Keys are field names available to user.
                        Values are the full path to that field in the HDF file.
                       
        _indexMap -     Dictionary.  Keys are field names available to user.  
                        Values are functions that when passed (var, ind) where
                        ind is a n-element tuple will return the proper slice.
                        n is the number of fundamental dimensions of the 
                        file type.
        """
        fid = tables.openFile(self.name)
        try:
            var = fid.getNode('/', self._nameExpMap[key])
            varAtts = var._v_attrs
            missing = getattr(varAtts, '_FillValue', numpy.nan)
            # because attributes are single element arrays
            # and not zero-element arrays, they change the 
            # rank of return values when applied. We take 
            # the first element to get zero-rank arrays
            scale = getattr(varAtts,'ScaleFactor', [1.0])[0]
            offset = getattr(varAtts, 'Offset', [0.0])[0]
            if var[:].dtype in ['float32', 'float64']:
                # only cast if we have a type that features nans
                var = numpy.where(var == missing, numpy.NaN, var)
                
            if indices is not None:
                # we want specific indices, use _indexMap
                indFunc = self._indexMap.get(key, self._indexMap['default'])  # fetch default if not in index map
            else:
                # don't bother with _indexMap, just fetch everything
                indFunc = lambda var, ind: var[:]
            
            if (scale != 1) or (offset != 0):  # avoids casting if we don't need to
                return indFunc(var[:], indices)*scale + offset
            else:
                return indFunc(var[:], indices)
        except (tables.exceptions.NoSuchNodeError, AttributeError):
            raise IOError("No field %s.  May be attempt to read non-KNMI Aura OMI file as such." % self._nameExpMap[key])
        except KeyError:
            raise KeyError("Attempt to use fieldname not associated with this filetype.")
        finally:
            fid.close()
                
    def get_cm(self, key, indices=None):
        """
        Provide get_cm function for HDF files
        
        get_cm works the same as get, but relies on a context manager to speed
        up access to the underlying files.  Just as get, it requires that 
        the parser have _nameExpMap and _indexMap variables.  These must be
        defined as above.
        """
        # open the var if it isn't open already
        if key not in self._open_vars.keys():
            try:
                var = self._fid.getNode('/', self._nameExpMap[key])
                varAtts = var._v_attrs
                missing = getattr(varAtts, '_FillValue', numpy.nan)
                # because attributes are single element arrays
                # and not zero-element arrays, they change the 
                # rank of return values when applied. We take 
                # the first element to get zero-rank arrays   
                scale = getattr(varAtts, 'ScaleFactor', [1.0])[0]
                offset = getattr(varAtts, 'Offset', [0.0])[0]
                if var[:].dtype in ['float32', 'float64']:
                    # only do nan sub if we don't have to cast
                    var = numpy.where(var == missing, numpy.NaN, var)
                self._open_vars[key] = var
                self._scales[key] = scale
                self._offsets[key] = offset
            except(KeyError):
                raise KeyError("No variable " + key + " in file " + self.name)
            except(tables.exceptions.NoSuchNodeError, AttributeError):
                raise IOError("No field %s.  May be attempt to read non-KNMI Aura OMI file as such." % self._nameExpMap[key])
        
        # return the values from the open var
        
        if indices is not None:
            # we have indices, use _indexMap
            indFunc = self._indexMap.get(key, self._indexMap['default']) # fetch default if not index map
        else:
            # we want everything, don't bother with _indexMap
            indFunc = lambda var, ind: var[:]
        
        if (self._scales[key] != 1) or (self._offsets[key] != 0): 
            return (indFunc(self._open_vars[key], indices)
                    *self._scales[key]+self._offsets[key])
        else:
            return indFunc(self._open_vars[key], indices)        
            
    def __enter__(self):
        '''Open up file and leave open.'''
        self._fid = tables.openFile(self.name, mode='r')
        self._open_vars = dict()
        self._scales = dict()
        self._offsets = dict()
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        '''Close file and delete references to file object and nodes'''
        self._fid.close()
        del self._open_vars
        del self._scales
        del self._offsets
        del self._fid
        return False

class HDFknmiomil2_File(HDFFile):
    """Provide interface to KNMI OMI L2 NRT product"""
    _nameExpMap = {"AirMassFactor"                          : "/HDFEOS/SWATHS/DominoNO2/Data Fields/AirMassFactor",
                  "AirMassFactorGeometric"                  : "/HDFEOS/SWATHS/DominoNO2/Data Fields/AirMassFactorGeometric",
                  "AirMassFactorTropospheric"               : "/HDFEOS/SWATHS/DominoNO2/Data Fields/AirMassFactorTropospheric",
                  "AssimilatedStratosphericSlantColumn"     : "/HDFEOS/SWATHS/DominoNO2/Data Fields/AssimilatedStratosphericSlantColumn",
                  "AssimilatedStratosphericVerticalColumn"  : "/HDFEOS/SWATHS/DominoNO2/Data Fields/AssimilatedStratosphericVerticalColumn", 
                  "AveragingKernel"                         : "/HDFEOS/SWATHS/DominoNO2/Data Fields/AveragingKernel",
                  "CloudFraction"                           : "/HDFEOS/SWATHS/DominoNO2/Data Fields/CloudFraction",
                  "CloudFractionStd"                        : "/HDFEOS/SWATHS/DominoNO2/Data Fields/CloudFractionStd",
                  "CloudPressure"                           : "/HDFEOS/SWATHS/DominoNO2/Data Fields/CloudPressure",
                  "CloudPressureStd"                        : "/HDFEOS/SWATHS/DominoNO2/Data Fields/CloudPressureStd",
                  "CloudRadianceFraction"                   : "/HDFEOS/SWATHS/DominoNO2/Data Fields/CloudRadianceFraction",
                  "GhostColumn"                             : "/HDFEOS/SWATHS/DominoNO2/Data Fields/GhostColumn",
                  "InstrumentConfigurationId"               : "/HDFEOS/SWATHS/DominoNO2/Data Fields/InstrumentConfigurationId",
                  "MeasurementQualityFlags"                 : "/HDFEOS/SWATHS/DominoNO2/Data Fields/MeasurementQualityFlags",
                  "SlantColumnAmountNO2"                    : "/HDFEOS/SWATHS/DominoNO2/Data Fields/SlantColumnAmountNO2",
                  "SlantColumnAmountNO2Std"                 : "/HDFEOS/SWATHS/DominoNO2/Data Fields/SlantColumnAmountNO2Std",
                  "SurfaceAlbedo"                           : "/HDFEOS/SWATHS/DominoNO2/Data Fields/SurfaceAlbedo",
                  "TM4PressurelevelA"                       : "/HDFEOS/SWATHS/DominoNO2/Data Fields/TM4PressurelevelA",
                  "TM4PressurelevelB"                       : "/HDFEOS/SWATHS/DominoNO2/Data Fields/TM4PressurelevelB",
                  "TM4SurfacePressure"                      : "/HDFEOS/SWATHS/DominoNO2/Data Fields/TM4SurfacePressure",
                  "TM4TerrainHeight"                        : "/HDFEOS/SWATHS/DominoNO2/Data Fields/TM4TerrainHeight",
                  "TM4TropoPauseLevel"                      : "/HDFEOS/SWATHS/DominoNO2/Data Fields/TM4TropoPauseLevel",
                  "TerrainHeight"                           : "/HDFEOS/SWATHS/DominoNO2/Data Fields/TerrainHeight", # random fact: _FillValue attribute is inaccurate for this field
                  "TotalVerticalColumn"                     : "/HDFEOS/SWATHS/DominoNO2/Data Fields/TotalVerticalColumn",
                  "TotalVerticalColumnError"                : "/HDFEOS/SWATHS/DominoNO2/Data Fields/TotalVerticalColumnError",
                  "TroposphericColumnFlag"                  : "/HDFEOS/SWATHS/DominoNO2/Data Fields/TroposphericColumnFlag",
                  "TroposphericVerticalColumn"              : "/HDFEOS/SWATHS/DominoNO2/Data Fields/TroposphericVerticalColumn",
                  "TroposphericVerticalColumnError"         : "/HDFEOS/SWATHS/DominoNO2/Data Fields/TroposphericVerticalColumnError",
                  "TroposphericVerticalColumnModel"         : "/HDFEOS/SWATHS/DominoNO2/Data Fields/TroposphericVerticalColumnModel",
                  "VCDErrorUsingAvKernel"                   : "/HDFEOS/SWATHS/DominoNO2/Data Fields/VCDErrorUsingAvKernel",
                  "VCDTropErrorUsingAvKernel"               : "/HDFEOS/SWATHS/DominoNO2/Data Fields/VCDTropErrorUsingAvKernel",
                  "GroundPixelQualityFlags"                 : "/HDFEOS/SWATHS/DominoNO2/Geolocation Fields/GroundPixelQualityFlags",
                  "Latitude"                                : "/HDFEOS/SWATHS/DominoNO2/Geolocation Fields/Latitude",
                  "LatitudeCornerpoints"                    : "/HDFEOS/SWATHS/DominoNO2/Geolocation Fields/LatitudeCornerpoints",
                  "Longitude"                               : "/HDFEOS/SWATHS/DominoNO2/Geolocation Fields/Longitude",
                  "LongitudeCornerpoints"                   : "/HDFEOS/SWATHS/DominoNO2/Geolocation Fields/LongitudeCornerpoints",
                  "SolarAzimuthAngle"                       : "/HDFEOS/SWATHS/DominoNO2/Geolocation Fields/SolarAzimuthAngle",
                  "SolarZenithAngle"                        : "/HDFEOS/SWATHS/DominoNO2/Geolocation Fields/SolarZenithAngle",
                  "Time"                                    : "/HDFEOS/SWATHS/DominoNO2/Geolocation Fields/Time",
                  "ViewingAzimuthAngle"                     : "/HDFEOS/SWATHS/DominoNO2/Geolocation Fields/ViewingAzimuthAngle",
                  "ViewingZenithAngle"                      : "/HDFEOS/SWATHS/DominoNO2/Geolocation Fields/ViewingZenithAngle"    
               }
    _indexMap = {"default"                      : lambda var, ind: var[..., ind[0], ind[1]], 
                 "InstrumentConfigurationId"    : lambda var, ind: var[ind[0]],
                 "MeasurementQualityFlags"      : lambda var, ind: var[ind[0]],
                 "TM4PressurelevelA"            : lambda var, ind: var[:],
                 "TM4PressurelevelB"            : lambda var, ind: var[:],
                 "Time"                         : lambda var, ind: var[ind[0]]
                 }
    
    def get_geo_corners(self):
        lat = self.get('LatitudeCornerpoints')
        lon = self.get('LongitudeCornerpoints')
        lat = numpy.transpose(lat, (1,2,0))
        lon = numpy.transpose(lon, (1,2,0))
        ind = numpy.indices(lat.shape[0:2]).transpose((1,2,0))
        protoDtype = [('lat', lat.dtype, 4), ('lon', lon.dtype, 4), ('ind', ind.dtype, 2)]
        struct = numpy.zeros(lat.shape[0:2], dtype=protoDtype)
        (struct['lat'], struct['lon'], struct['ind']) = (lat, lon, ind)
        return struct
    
    def get_geo_centers(self):
        lat = self.get('Latitude')
        lon = self.get('Longitude')
        ind = numpy.indices(lat.shape).transpose((1,2,0))
        protoDtype = [('lat', lat.dtype), ('lon', lon.dtype), ('ind', ind.dtype, 2)]
        struct = numpy.zeros(lat.shape,dtype=protoDtype)
        (struct['lat'], struct['lon'], struct['ind']) = (lat, lon, ind)
        return struct

        
class HDFnasaomil2_File(HDFFile):
    """
    Provide interface to NASA OMI L2 product, with pixel corners
    
    Pixel corners are retrieved from an extra file that must be accessible
    in cornerDir.  The files listed in cornerFileList, if any, will be checked
    first, followed by any files in cornerDir. If no valid pixel corner file
    is found that matches the orbit number of the input file, the parser will
    instantiage but get_geo_corners will fail with an IOError. 

    The corners retrieved are for the visible channel
    used by the NO2 algorithm- using this parser for other products may 
    require altering the parser to use a different channel if 
    appropriate.
    
    The keys to retrieve variables are the names of the variables within actual
    files.  Note that the NASA product documentation has the wrong name for 
    the "SlantColumnAmountH20Std" variable due to a case typo.

    Does not support the fields "UnpolFldCoefficients" or "SmallPixelRadiance"
    because the dimensionality of these fields changes between files and there
    is no way to deal with fields with variable dimension size in the current 
    framework.
    """
    
    OMIAURANO2_FILE_NAME = "OMI/Aura Nitrogen Dioxide (NO2) Total & "\
                           "Troposph.Column 1-Orbit L2 Swath 13x24km"
    OMIAURANO2_CORNER_FILE_NAME = "OMI/Aura Global Ground Pixel Corners "\
                                  "1-Orbit L2 Swath 13x24km"

    def __init__(self, filename, subtype='', extension=None, cornerDir=None,
                 cornerFileList=None):
        HDFFile.__init__(self, filename, subtype, extension)

        # make sure filename is actually an input file
        if getLongName(filename) != HDFnasaomil2_File.OMIAURANO2_FILE_NAME:
            raise IOError('Attempt to read non-NASA OMI L2 file as such.')
        
        # start by assuming we aren't going to find anything
        self.pixCorners = None

        # see if the corner directory even exists.  If it doesn't, we obviously can't 
        # find a corner file
        if os.path.isdir(cornerDir):

            # convert the corner files into full pathnames
            # unless we were given null string (signal to search directory)
            if cornerFileList != ['']:
                cornerFileList = [os.path.join(cornerDir, f) for f in cornerFileList]

            # get orbit number of file for matching
            forbitnumber = getOrbitNumber(filename)

            # try using the list
        
            for f in cornerFileList:
                if f != '' and getLongName(f) == HDFnasaomil2_File.OMIAURANO2_CORNER_FILE_NAME:
                    try:
                        if getOrbitNumber(f) == forbitnumber:
                            self.pixCorners = f
                            break
                    except:
                        pass

            # if necessary, search entire corner file directory
            if self.pixCorners == None:        
                allPossible = [os.path.join(cornerDir, f) for f in os.listdir(cornerDir)]
                for f in allPossible:
                    try:
                        if tables.isHDF5File(f) \
                                and getLongName(f) == HDFnasaomil2_File.OMIAURANO2_CORNER_FILE_NAME \
                                and getOrbitNumber(f) == forbitnumber:
                            self.pixCorners = f
                            break
                    except:
                        pass
                
        if self.pixCorners == None:
            print "No valid corner file found for {0}.".format(filename)
            
    __dataPath = '/HDFEOS/SWATHS/ColumnAmountNO2/Data Fields/'
    __geoPath = '/HDFEOS/SWATHS/ColumnAmountNO2/Geolocation Fields/'
    
    _nameExpMap = {'AMFInitial' : __dataPath+'AMFInitial',
                    'AMFInitialClear' : __dataPath+'AMFInitialClear',
                    'AMFInitialClearStd' : __dataPath+'AMFInitialClearStd',
                    'AMFInitialCloudy' : __dataPath+'AMFInitialCloudy',
                    'AMFInitialCloudyStd' : __dataPath+'AMFInitialCloudyStd',
                    'AMFInitialStd' : __dataPath+'AMFInitialStd',
                    'AMFPolluted' : __dataPath+'AMFPolluted',
                    'AMFPollutedClear' : __dataPath+'AMFPollutedClear',
                    'AMFPollutedClearStd' : __dataPath+'AMFPollutedClearStd',
                    'AMFPollutedCloudy' : __dataPath+'AMFPollutedCloudy',
                    'AMFPollutedCloudyStd' : __dataPath+'AMFPollutedCloudyStd',
                    'AMFPollutedStd' : __dataPath+'AMFPollutedStd',
                    'AMFPollutedToGround' : __dataPath+'AMFPollutedToGround',
                    'AMFPollutedToGroundStd' : __dataPath+'AMFPollutedToGroundStd',
                    'AMFQualityFlags' : __dataPath+'AMFQualityFlags',
                    'AMFUnpolluted' : __dataPath+'AMFUnpolluted',
                    'AMFUnpollutedClear' : __dataPath+'AMFUnpollutedClear',
                    'AMFUnpollutedClearStd' : __dataPath+'AMFUnpollutedClearStd',
                    'AMFUnpollutedCloudy' : __dataPath+'AMFUnpollutedCloudy',
                    'AMFUnpollutedCloudyStd' : __dataPath+'AMFUnpollutedCloudyStd',
                    'AMFUnpollutedStd' : __dataPath+'AMFUnpollutedStd',
                    'ChiSquaredOfFit' : __dataPath+'ChiSquaredOfFit',
                    'CloudFraction' : __dataPath+'CloudFraction',
                    'CloudFractionStd' : __dataPath+'CloudFractionStd',
                    'CloudPressure' : __dataPath+'CloudPressure',
                    'CloudPressureStd' : __dataPath+'CloudPressureStd',
                    'CloudRadianceFraction' : __dataPath+'CloudRadianceFraction',
                    'ColumnAmountNO2' : __dataPath+'ColumnAmountNO2',
                    'ColumnAmountNO2Std' : __dataPath+'ColumnAmountNO2Std',
                    'ColumnAmountNO2BelowCloud' : __dataPath+'ColumnAmountNO2BelowCloud',
                    'ColumnAmountNO2BelowCloudStd' : __dataPath+'ColumnAmountNO2BelowCloudStd',
                    'ColumnAmountNO2Initial' : __dataPath+'ColumnAmountNO2Initial',
                    'ColumnAmountNO2InitialStd' : __dataPath+'ColumnAmountNO2InitialStd',
                    'ColumnAmountNO2Polluted' : __dataPath+'ColumnAmountNO2Polluted',
                    'ColumnAmountNO2PollutedStd' : __dataPath+'ColumnAmountNO2PollutedStd',
                    'ColumnAmountNO2Trop' : __dataPath+'ColumnAmountNO2Trop',
                    'ColumnAmountNO2TropStd' : __dataPath+'ColumnAmountNO2TropStd',
                    'ColumnAmountNO2Unpolluted' : __dataPath+'ColumnAmountNO2Unpolluted',
                    'ColumnAmountNO2UnpollutedStd' : __dataPath+'ColumnAmountNO2UnpollutedStd',
                    'FitQualityFlags' : __dataPath+'FitQualityFlags',
                    'InstrumentConfigurationId' : __dataPath+'InstrumentConfigurationId',
                    'MeasurementQualityFlags' : __dataPath+'MeasurementQualityFlags',
                    'PolynomialCoefficients' : __dataPath+'PolynomialCoefficients',
                    'PolynomialCoefficientsStd' : __dataPath+'PolynomialCoefficientsStd',
                    'RingCoefficient' : __dataPath+'RingCoefficient',
                    'RingCoefficientStd' : __dataPath+'RingCoefficientStd',
                    'RootMeanSquareErrorOfFit' : __dataPath+'RootMeanSquareErrorOfFit',
                    'SlantColumnAmountH2O' : __dataPath+'SlantColumnAmountH2O',
                    'SlantColumnAmountH2OStd' : __dataPath+'SlantColumnAmountH2OStd',
                    'SlantColumnAmountNO2' : __dataPath+'SlantColumnAmountNO2',
                    'SlantColumnAmountNO2Std' : __dataPath+'SlantColumnAmountNO2Std',
                    'SlantColumnAmountO2O2' : __dataPath+'SlantColumnAmountO2O2',
                    'SlantColumnAmountO2O2Std' : __dataPath+'SlantColumnAmountO2O2Std',
                    'SlantColumnAmountO3' : __dataPath+'SlantColumnAmountO3',
                    'SlantColumnAmountO3Std' : __dataPath+'SlantColumnAmountO3Std',
                    'SmallPixelRadiance' : __dataPath+'SmallPixelRadiance',
                    'SmallPixelRadiancePointer' : __dataPath+'SmallPixelRadiancePointer',
                    'TerrainHeight' : __dataPath+'TerrainHeight',
                    'TerrainPressure' : __dataPath+'TerrainPressure',
                    'TerrainReflectivity' : __dataPath+'TerrainReflectivity',
                    'TropFractionUnpolluted' : __dataPath+'TropFractionUnpolluted',
                    'TropFractionUnpollutedStd' : __dataPath+'TropFractionUnpollutedStd',
                    'UnpolFldLatBandQualityFlags' : __dataPath+'UnpolFldLatBandQualityFlags',
                    'WavelengthRegistrationCheck' : __dataPath+'WavelengthRegistrationCheck',
                    'WavelengthRegistrationCheckStd' : __dataPath+'WavelengthRegistrationCheckStd',
                    'XTrackQualityFlags' : __dataPath+'XTrackQualityFlags',
                    'vcdQualityFlags' : __dataPath+'vcdQualityFlags',
                    'GroundPixelQualityFlags' : __geoPath+'GroundPixelQualityFlags',
                    'Latitude' : __geoPath+'Latitude',
                    'Longitude' : __geoPath+'Longitude',
                    'SolarAzimuthAngle' : __geoPath+'SolarAzimuthAngle',
                    'SolarZenithAngle' : __geoPath+'SolarZenithAngle',
                    'SpacecraftAltitude' : __geoPath+'SpacecraftAltitude',
                    'SpacecraftLatitude' : __geoPath+'SpacecraftLatitude',
                    'SpacecraftLongitude' : __geoPath+'SpacecraftLongitude',
                    'Time' : __geoPath+'Time',
                    'ViewingAzimuthAngle' : __geoPath+'ViewingAzimuthAngle',
                    'ViewingZenithAngle' : __geoPath+'ViewingZenithAngle'}
    
    _indexMap = {'default' : lambda var, ind: var[ind[0], ind[1], ...],
                  'SmallPixelRadiance' : lambda var, ind: var[:, ind[1]],
                  'SmallPixelRadiancePointer' : lambda var, ind: var[ind[0], :],
                  'InstrumentConfigurationId' : lambda var, ind: var[ind[0]],
                  'MeasurementQualityFlags' : lambda var, ind: var[ind[0]],
                  'WavelengthRegistrationCheck' : lambda var, ind: var[ind[0], :],
                  'WavelengthRegistrationCheckStd' : lambda var, ind: var[ind[0], :],
                  'UnpolFldLatBandQualityFlags' : lambda var, ind: var[:],
                  'Time' : lambda var, ind: var[ind[0]],
                  'SpacecraftLatitude' : lambda var, ind: var[ind[0]],
                  'SpacecraftLongitude' : lambda var, ind: var[ind[0]],
                  'SpacecraftAltitude' : lambda var, ind: var[ind[0]]}
    
    def get_geo_corners(self):
        '''
        Retrieves array of the corners of the pixels.  
        
        Throws IOError if no pixel corner file specified
        '''
        latNodeName = '/HDFEOS/SWATHS/OMI Ground Pixel Corners VIS/Data Fields/FoV75CornerLatitude'
        lonNodeName = '/HDFEOS/SWATHS/OMI Ground Pixel Corners VIS/Data Fields/FoV75CornerLongitude'
        try:
            pxFid = tables.openFile(self.pixCorners)
        except AttributeError:
            raise IOError('Unable to open pixel corners file.  Need pixel corners file to use corners')
        try:
            latNode = pxFid.getNode('/', latNodeName)
            lonNode = pxFid.getNode('/', lonNodeName)
            # Note: it is assumed that there are no missing values.
            lat = latNode[:].transpose((1,2,0))
            lon = lonNode[:].transpose((1,2,0))            
        finally:
            pxFid.close()
        ind = numpy.indices(lat.shape[0:2]).transpose((1,2,0))
        protoDtype = [('lat', lat.dtype, 4), ('lon', lon.dtype, 4), ('ind', ind.dtype, 2)]
        struct = numpy.zeros(lat.shape[0:2], dtype=protoDtype)
        (struct['lat'], struct['lon'], struct['ind']) = (lat, lon, ind)
        return struct
    
    def get_geo_centers(self):
        lat = self.get('Latitude')
        lon = self.get('Longitude')
        ind = numpy.indices(lat.shape).transpose((1,2,0))
        protoDtype = [('lat', lat.dtype), ('lon', lon.dtype), ('ind', ind.dtype, 2)]
        struct = numpy.zeros(lat.shape, dtype=protoDtype)
        (struct['lat'], struct['lon'], struct['ind']) = (lat, lon, ind)
        return struct
        
class HDFmopittl2_File(HDF4File):
    """
    Provide interface to MOPITT level 2 V5 product

    Automatically setes the missing value for the data to
    -9999.0, as this is the missing value used (but not 
    documented) within the data.
    """
    _nameExpMap = {'Time' : '/MOP02/Geolocation Fields/Time',
                   'Latitude' : '/MOP02/Geolocation Fields/Latitude', 
                   'Longitude' : '/MOP02/Geolocation Fields/Longitude',
                   'Seconds in Day' : '/MOP02/Data Fields/Seconds in Day',
                   'Pressure Grid' : '/MOP02/Data Fields/Pressure Grid',
                   'Solar Zenith Angle' : '/MOP02/Data Fields/Solar Zenith Angle',
                   'Satellite Zenith Angle' : '/MOP02/Data Fields/Satellite Zenith Angle',
                   'Surface Pressure' : '/MOP02/Data Fields/Surface Pressure',
                   'Retrieved Surface Temperature' : '/MOP02/Data Fields/Retrieved Surface Temperature',
                   'Retrieved Surface Emissivity' : '/MOP02/Data Fields/Retrieved Surface Emissivity',
                   'Retrieved CO Mixing Ratio Profile' : '/MOP02/Data Fields/Retrieved CO Mixing Ratio Profile',
                   'Retrieved CO Surface Mixing Ratio' : '/MOP02/Data Fields/Retrieved CO Surface Mixing Ratio',
                   'Retrieved CO Total Column' : '/MOP02/Data Fields/Retrieved CO Total Column',
                   'Retrieved CO Total Column Diagnostics' : '/MOP02/Data Fields/Retrieved CO Total Column Diagnostics',
                   'Retrieval Averaging Kernel Matrix' : '/MOP02/Data Fields/Retrieval Averaging Kernel Matrix',
                   'Retrieval Error Covariance Matrix' : '/MOP02/Data Fields/Retrieval Error Covariance Matrix',
                   'A Priori Surface Temperature' : '/MOP02/Data Fields/A Priori Surface Temperature',
                   'A Priori Surface Emissivity' : '/MOP02/Data Fields/A Priori Surface Emissivity',
                   'A Priori CO Mixing Ratio Profile' : '/MOP02/Data Fields/A Priori CO Mixing Ratio Profile',
                   'A Priori CO Surface Mixing Ratio' : '/MOP02/Data Fields/A Priori CO Surface Mixing Ratio',
                   'Level 1 Radiances and Errors' : '/MOP02/Data Fields/Level 1 Radiances and Errors',
                   'Degrees of Freedom for Signal' : '/MOP02/Data Fields/Degrees of Freedom for Signal',
                   'Surface Index' : '/MOP02/Data Fields/Surface Index',
                   'DEM Altitude' : '/MOP02/Data Fields/DEM Altitude',
                   'Cloud Description' : '/MOP02/Data Fields/Cloud Description',
                   'MODIS Cloud Diagnostics' : '/MOP02/Data Fields/MODIS Cloud Diagnostics',
                   'Water Vapor Climatology Content' : '/MOP02/Data Fields/Water Vapor Climatology Content',
                   'Retrieval Iterations' : '/MOP02/Data Fields/Retrieval Iterations',
                   'Information Content Index' : '/MOP02/Data Fields/Information Content Index',
                   'Signal Chi2' : '/MOP02/Data Fields/Signal Chi2',
                   'Swath Index' : '/MOP02/Data Fields/Swath Index'}
    _indexMap = {'default' : lambda var, ind: var[ind[0], ...],
                 'Pressure Grid' : lambda var, ind: var[:]}
        
    def get(self, key, indices=None):
        '''Overloaded version of get that applies the correct missing value.'''
        return HDF4File.get(self, key, indices, missingValue=-9999.0)

    def get_cm(self, key, indices=None):
        '''Overloaded version of get_cm that applied the correct missing value.'''
        return HDF4File.get_cm(self, key, indices, missingValue=-9999.0)

    def get_geo_centers(self):
        '''Retrieves array of the corners of the pixels'''
        lat = self.get('Latitude').squeeze()
        lon = self.get('Longitude').squeeze()
        ind = numpy.arange(lat.size).reshape(lat.size,1)
        protoDtype = [('lat', lat.dtype), ('lon', lon.dtype), ('ind', ind.dtype, (1,))]
        struct = numpy.zeros(lat.size, dtype = protoDtype)
        (struct['lat'], struct['lon'], struct['ind']) = (lat, lon, ind)
        return struct
