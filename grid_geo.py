'''
Framework for gridding/ungridding geolocated data.

GridDef is an abstract class.  It cannot be used
as a standalone because none of the functionality
has been implemented.  It is simply a framework,
with some of the general functionality implemented.

All subclasses of GridDef provide forward and 
inverse projections, both to gridded space
and native projection space.

Subclasses MUST following the naming convention
of projectionName_GridDef for the dispatcher 
to work properly

Functions implemented for each class:
    requiredParms - the parameters required
        to be present in the dictionary argument
        passed to the constructor for the class.
        All parameters not in this list are 
        ignored.  This class MUST be made a 
        static method using the static method
        wrapper.
    indLims - return the limits of indices for
        which information should be stored.  Any
        pixels entirely outside these bounds (as 
        defined by the mapping function) will be 
        thrown out.  Note that fractional indices
        of the maxima should still be included (ie
        if maxRow is 10, data up through 10.99999
        should be be included, but not 11)
        Should return (minRow, maxRow, 
        minCol, maxCol)
    geoToProjected - from geo-coordinates (lat/lon
        in degrees N/E, respectively) to native
        projection coordinates.  Accepts numpy
        arrays.  Returns (y,x)
    geoToGridded - from geo-coordinates to 
        gridded coordinates (indices).  Indices
        must be 0-based.  Accepts numpy arrays.
        Returns (row,col) in DECIMAL INDICES.
        These must be floored before they can 
        be used as actual indices.
    projectedToGeo - from native projection 
        coordinates (y/x, usually in meters) to
        geo-coordinates. Accepts numpy arrays.
        Returns (lat,lon) in degrees.
    griddedToGeo - from decimal indices (row/col) 
        to geo-coordinates.  Accepts numpy arrays.
        Returns (lat,lon) in degrees.
'''
import sys
from pyproj import Proj

def ValidProjections():
    '''Return a list of valid projection names'''
    currentModule = sys.modules[__name__]
    names = dir(currentModule)
    return [el[:-8] for el in names if el.endswith("_GridDef")]
    
class GridDef:
    '''Abstract class to handle projection/gridding of data'''
    def __init__(self, parms):
        pass
    def requiredParms():
        raise NotImplementedError
    requiredParms = staticmethod(requiredParms)
    def indLims(self):
        raise NotImplementedError
    def geoToProjected(self, lat, lon):
        raise NotImplementedError
    def geoToGridded(self, lat, lon):
        raise NotImplementedError
    def projectedToGeo(self, y, x):
        raise NotImplementedError
    def griddedToGeo(self, row, col):
        raise NotImplementedError


class latlon_GridDef(GridDef):
    '''
    Performs transformations on the unprojected lat/lon grid
    
    Convention for this class is that the "projected" coordinates
    are simply lat and lon.  The gridded coordinates
    determine cellsize by xCell and yCell, and place the ll corner
    at the lat lon specified by yOrig and xOrig, respectively.
    
    Cautions:
    - Only use -180 to 180 or 0 to 360.  Do not mix
    - Only use radians or degrees.  Do not mix.
    - Make sure parameters units and standard match
      coordinates being put in.
    '''
    @staticmethod
    def requiredParms():
        '''Parameters that must be in the dictonary passed to instantiate'''
        return {"xOrig":('[xOrig description]', 'decimal'),
                "yOrig":('[yOrig description]', 'decimal'),
                "xCell":('[xCell description]', 'decimal'),
                "yCell":('[yCell description]', 'decimal'),
                "nRows":('[nRows description]', 'int'),
                "nCols":('[nCols description]', 'int')}
    def __init__(self, parmDict):
        GridDef.__init__(self, parmDict)
        self.parms = parmDict
    def indLims(self):
        return (0, self.parms['nRows']-1, 0, self.parms['nCols']-1)
    def geoToProjected(self, lat, lon):
        (y, x) = (lat, lon)
        return (y, x)
    def geoToGridded(self, lat, lon):
        row = (lat-self.parms['yOrig'])/self.parms['yCell']
        col = (lon-self.parms['xOrig'])/self.parms['xCell']
        return (row, col)
    def projectedToGeo(self, y, x):
        (lat, lon) = (y, x)
        return (lat, lon)
    def griddedToGeo(self, row, col):
        lat = row*self.parms['yCell']+self.parms['yOrig']
        lon = col*self.parms['xCell']+self.parms['xOrig']
        return (lat, lon)

    
class lcc2par_GridDef(GridDef):
    '''Performs transformations with the lambert conic conformal'''
    @staticmethod
    def requiredParms():
        '''
        parameters that must be in the dictionary passed to
        instantiate this class
        '''
        return {"stdPar1":('[stdPar1 description]', 'decimal'),
                "stdPar2":('[stdPar2 description]', 'decimal'),
                "refLat":('[refLat description]', 'decimal'),
                "refLon":('[refLon description]', 'decimal'),
                "xOrig":('[xOrig description]', 'decimal'),
                "yOrig":('[yOrig description]', 'decimal'),
                "xCell":('[xCell description]', 'decimal'),
                "yCell":('[yCell description]', 'decimal'),
                "nRows":('[nRows description]', 'int'),
                "nCols":('[nCols description]', 'int'),
                "earthRadius":('[earthRadius description]','decimal')}
    def __init__(self, parms):
        GridDef.__init__(self, parms)
        self.parms = parms

        # remap parms into a dictionary readable by pyproj
        pyprojParms = {'proj'   : 'lcc',
                       'a'      : parms['earthRadius'],
                       'lat_1'  : parms['stdPar1'],
                       'lat_2'  : parms['stdPar2'],
                       'lat_0'  : parms['refLat'],
                       'lon_0'  : parms['refLon'],
                       'x_0'    : 0,
                       'y_0'    : 0}
        self.__proj = Proj(pyprojParms)
    def indLims(self):
        return (0, self.parms['nRows']-1,
                 0, self.parms['nCols']-1)
    def geoToProjected(self, lat, lon):
        (x,y) = self.__proj(lon, lat)
        return (y,x)
    def geoToGridded(self, lat, lon):
        (y,x) = self.geoToProjected(lat, lon)
        # transform x and y to new origin
        y = y-self.parms['yOrig']
        x = x-self.parms['xOrig']
        # convert from projected coordinates to cells
        row = y/self.parms['yCell']
        col = x/self.parms['xCell']
        return (row, col)
    def projectedToGeo(self, y, x):
        (lon,lat) = self.__proj(x, y, inverse=True)
        return (lat, lon)
    def griddedToGeo(self, row, col):
        y = row*self.parms['yCell']+self.parms['yOrig']
        x = col*self.parms['xCell']+self.parms['xOrig']
        return self.projectedToGeo(y,x)        
