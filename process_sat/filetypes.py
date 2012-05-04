'''
List of supported filetypes and associated parameters
Whips.py will consider all classes in this module with names 
ending in "_filetype" to be valid filetype definitions

Each class in this file has, at minimum, an attribute "parser"
that specifies the associated parser for that class and an 
attribute "doutf" that specifies the default output function.
(List the name of the output function, not including "_out_func")

Each class may also contain any other variables that will be 
used for output function attributes if the output function
accepts those attributes

In some cases, output function attributes may consist of lists
associated with field names for that particular filetype.  In 
these cases, the variables for these attributes will be 
dictionaries keyed off the field name strings.

Some parsers require additional attributes (beyond the 
filename, subtype, and extension). These attributes may be
listed in the ParserParms dictionary, and whips.py will 
require valid values for these arguments before processing
files of this type. Entries in the ParserParms dictionary
should follow the form

   'RequiredAttrName':("AttrDescription",'AttrCastType')

where AttrCastType is one of the cast types for OutFuncAttrs

   [None, 'int', 'posint', 'decimal', 'posdecimal',
    'time', 'bool', 'list', 'listoflists']
'''

class OMI_NO2_KNMI_HDF_v2_0_preFeb2006_filetype():
    parser = 'HDFknmiomil2'
    parserParms = {}
    doutf = 'OMNO2e_netCDF_avg'
    overallQualFlag = 'TroposphericColumnFlag'
    cloudFrac = 'CloudFraction'
    solarZenithAngle = 'SolarZenithAngle'
    time = 'Time'
    longitude = 'Longitude'
    pixIndXtrackAxis = 1
    outUnits = { 'AirMassFactor' : 'Unitless',
                 'AirMassFactorGeometric' : 'Unitless',
                 'AirMassFactorTropospheric' : 'Unitless',
                 'AssimilatedStratosphericSlantColumn' : 'Molecules cm^-2 x 10^-15',
                 'AssimilatedStratosphericVerticalColumn' : 'Molecules cm^-2 x 10^-15',
                 'AveragingKernel' : 'Unitless x 1000',
                 'CloudFraction' : 'Unitless x 1000',
                 'CloudFractionStd' : 'Unitless x 1000',
                 'CloudPressure' : 'hPa',
                 'CloudPressureStd' : 'hPa',
                 'CloudRadianceFraction' : 'Percent x 100',
                 'GhostColumn' : 'Molecules cm^-2 x 10^-15',
                 'InstrumentConfigurationId' : 'Unitless',
                 'MeasurementQualityFlags' : 'Unitless',
                 'SlantColumnAmountNO2' : 'Molecules cm^-2 x 10^-15',
                 'SlantColumnAmountNO2Std' : 'Molecules cm^-2 x 10^-15',
                 'Surface Albedo' : 'Unitless x 10,000',
                 'TM4PressurelevelA' : 'Pa',
                 'TM4PressurelevelB' : 'Unitless', 
                 'TM4SurfacePressure' : 'hPa',
                 'TM4TerrainHeight' : 'meters',
                 'TM4TropoPauseLevel' : 'Unitless',
                 'TerrainHeight' : 'meters',
                 'TotalVerticalColumn' : 'Molecules cm^-2 x 10^-15',
                 'TotalVerticalColumnError' : 'Molecules cm^-2 x 10^-15',
                 'TroposphericColumnFlag' : 'Unitless',
                 'TroposphericVerticalColumn' : 'Molecules cm^-2 x 10^-15',
                 'TroposphericVerticalColumnError' : 'Molecules cm^-2 x 10^-15',
                 'TroposphericVerticalColumnModel' : 'Molecules cm^-2 x 10^-15',
                 'VCDErrorUsingAvKernel' : 'Molecules cm^-2 x 10^-15',
                 'VCDTropErrorUsingAvKernel' : 'Molecules cm^-2 x 10^-15',
                 'GroundPixelQualityFlag' : 'Unitless',
                 'Latitude' : 'Degrees',
                 'LatitudeCornerpoints' : 'Degrees',
                 'Longitude' : 'Degrees',
                 'LongitudeCornerpoints' : 'Degrees',
                 'SolarAzimuthAngle' : 'Degrees',
                 'SolarZenithAngle' : 'Degrees',
                 'Time' : 'seconds',
                 'ViewingAzimuthAngle' : 'Degrees',
                 'ViewingZenithAngle' : 'Degrees' }

    extraDimLabel = { 'AirMassFactor' : 'none',
                      'AirMassFactorGeometric' : 'none',
                      'AirMassFactorTropospheric' : 'none',
                      'AssimilatedStratosphericSlantColumn' : 'none',
                      'AssimilatedStratosphericVerticalColumn' : 'none',
                      'AveragingKernel' : 'layer',
                      'CloudFraction' : 'none',
                      'CloudFractionStd' : 'none',
                      'CloudPressure' : 'none',
                      'CloudPressureStd' : 'none',
                      'CloudRadianceFraction' : 'none',
                      'GhostColumn' : 'none',
                      'InstrumentConfigurationId' : 'none',
                      'MeasurementQualityFlags' : 'none',
                      'SlantColumnAmountNO2' : 'none',
                      'SlantColumnAmountNO2Std' : 'none',
                      'SurfaceAlbedo' : 'none',
                      'TM4PressurelevelA' : 'layer',
                      'TM4PressurelevelB' : 'layer',
                      'TM4SurfacePressure' : 'none',
                      'TM4TerrainHeight' : 'none',
                      'TM4TropoPauseLevel' : 'none',
                      'TerrainHeight' : 'none',
                      'TotalVerticalColumn' : 'none',
                      'TotalVerticalColumnError' : 'none',
                      'TroposphericColumnFlag' : 'none',
                      'TroposphericVerticalColumn' : 'none',
                      'TroposphericVerticalColumnError' : 'none',
                      'TroposphericVerticalColumnModel' : 'none',
                      'VCDErrorUsingAvKernel' : 'none',
                      'VCDTropErrorUsingAvKernel' : 'none',
                      'GroundPixelQualityFlag' : 'none',
                      'Latitude' : 'none',
                      'LatitudeCornerPoints': 'corner',
                      'Longitude' : 'none',
                      'LongitudeCornerPoints' : 'corner',
                      'SolarAzimuthAngle' : 'none',
                      'SolarZenithAngle' : 'none',
                      'Time' : 'none',
                      'ViewingAzimuthAngle' : 'none',
                      'ViewingZenithAngle' : 'none' }

    extraDimSize = { 'AirMassFactor' : 0,
                     'AirMassFactorGeometric' : 0,
                     'AirMassFactorTropospheric' : 0,
                     'AssimilatedStratosphericSlantColumn' : 0,
                     'AssimilatedStratosphericVerticalColumn' : 0,
                     'AveragingKernel' : 35,
                     'CloudFraction' : 0,
                     'CloudFractionStd' : 0,
                     'CloudPressure' : 0,
                     'CloudPressureStd' : 0,
                     'CloudRadianceFraction' : 0,
                     'GhostColumn' : 0,
                     'InstrumentConfigurationId' : 0,
                     'MeasurementQualityFlags' : 0,
                     'SlantColumnAmountNO2' : 0,
                     'SlantColumnAmountNO2Std' : 0,
                     'SurfaceAlbedo' : 0,
                     'TM4PressurelevelA' : 35,
                     'TM4PressurelevelB' : 35,
                     'TM4SurfacePressure' : 0,
                     'TM4TerrainHeight' : 0,
                     'TM4TropoPauseLevel' : 0,
                     'TerrainHeight' : 0,
                     'TotalVerticalColumn' : 0,
                     'TotalVerticalColumnError' : 0,
                     'TroposphericColumnFlag' : 0,
                     'TroposphericVerticalColumn' : 0,
                     'TroposphericVerticalColumnError' : 0,
                     'TroposphericVerticalColumnModel' : 0,
                     'VCDErrorUsingAvKernel' : 0,
                     'VCDTropErrorUsingAvKernel' : 0, 
                     'GroundPixelQualityFlag' : 0,
                     'Latitude' : 0,
                     'LatitudeCornerPoints' : 4,
                     'Longitude' : 0,
                     'LongitudeCornerPoints' : 4,
                     'SolarAzimuthAngle' : 0,
                     'SolarZenithAngle' : 0,
                     'Time' : 0,
                     'ViewingAzimuthAngle' : 0,
                     'ViewingZenithAngle' : 0 }

class OMI_NO2_KNMI_HDF_v2_0_postFeb2006_filetype():
    parser = 'HDFknmiomil2'
    parserParms = {}
    doutf = 'OMNO2e_netCDF_avg'
    overallQualFlag = 'TroposphericColumnFlag'
    cloudFrac = 'CloudFraction'
    solarZenithAngle = 'SolarZenithAngle'
    time = 'Time'
    longitude = 'Longitude'
    pixIndXtrackAxis = 1
    outUnits = { 'AirMassFactor' : 'Unitless',
                 'AirMassFactorGeometric' : 'Unitless',
                 'AirMassFactorTropospheric' : 'Unitless',
                 'AssimilatedStratosphericSlantColumn' : 'Molecules cm^-2 x 10^-15',
                 'AssimilatedStratosphericVerticalColumn' : 'Molecules cm^-2 x 10^-15',
                 'AveragingKernel' : 'Unitless x 1000',
                 'CloudFraction' : 'Unitless x 1000',
                 'CloudFractionStd' : 'Unitless x 1000',
                 'CloudPressure' : 'hPa',
                 'CloudPressureStd' : 'hPa',
                 'CloudRadianceFraction' : 'Percent x 100',
                 'GhostColumn' : 'Molecules cm^-2 x 10^-15',
                 'InstrumentConfigurationId' : 'Unitless',
                 'MeasurementQualityFlags' : 'Unitless',
                 'SlantColumnAmountNO2' : 'Molecules cm^-2 x 10^-15',
                 'SlantColumnAmountNO2Std' : 'Molecules cm^-2 x 10^-15',
                 'Surface Albedo' : 'Unitless x 10,000',
                 'TM4PressurelevelA' : 'Pa',
                 'TM4PressurelevelB' : 'Unitless', 
                 'TM4SurfacePressure' : 'hPa',
                 'TM4TerrainHeight' : 'meters',
                 'TM4TropoPauseLevel' : 'Unitless',
                 'TerrainHeight' : 'meters',
                 'TotalVerticalColumn' : 'Molecules cm^-2 x 10^-15',
                 'TotalVerticalColumnError' : 'Molecules cm^-2 x 10^-15',
                 'TroposphericColumnFlag' : 'Unitless',
                 'TroposphericVerticalColumn' : 'Molecules cm^-2 x 10^-15',
                 'TroposphericVerticalColumnError' : 'Molecules cm^-2 x 10^-15',
                 'TroposphericVerticalColumnModel' : 'Molecules cm^-2 x 10^-15',
                 'VCDErrorUsingAvKernel' : 'Molecules cm^-2 x 10^-15',
                 'VCDTropErrorUsingAvKernel' : 'Molecules cm^-2 x 10^-15',
                 'GroundPixelQualityFlag' : 'Unitless',
                 'Latitude' : 'Degrees',
                 'LatitudeCornerpoints' : 'Degrees',
                 'Longitude' : 'Degrees',
                 'LongitudeCornerpoints' : 'Degrees',
                 'SolarAzimuthAngle' : 'Degrees',
                 'SolarZenithAngle' : 'Degrees',
                 'Time' : 'seconds',
                 'ViewingAzimuthAngle' : 'Degrees',
                 'ViewingZenithAngle' : 'Degrees' }

    extraDimLabel = { 'AirMassFactor' : 'none',
                      'AirMassFactorGeometric' : 'none',
                      'AirMassFactorTropospheric' : 'none',
                      'AssimilatedStratosphericSlantColumn' : 'none',
                      'AssimilatedStratosphericVerticalColumn' : 'none',
                      'AveragingKernel' : 'layer',
                      'CloudFraction' : 'none',
                      'CloudFractionStd' : 'none',
                      'CloudPressure' : 'none',
                      'CloudPressureStd' : 'none',
                      'CloudRadianceFraction' : 'none',
                      'GhostColumn' : 'none',
                      'InstrumentConfigurationId' : 'none',
                      'MeasurementQualityFlags' : 'none',
                      'SlantColumnAmountNO2' : 'none',
                      'SlantColumnAmountNO2Std' : 'none',
                      'SurfaceAlbedo' : 'none',
                      'TM4PressurelevelA' : 'layer',
                      'TM4PressurelevelB' : 'layer',
                      'TM4SurfacePressure' : 'none',
                      'TM4TerrainHeight' : 'none',
                      'TM4TropoPauseLevel' : 'none',
                      'TerrainHeight' : 'none',
                      'TotalVerticalColumn' : 'none',
                      'TotalVerticalColumnError' : 'none',
                      'TroposphericColumnFlag' : 'none',
                      'TroposphericVerticalColumn' : 'none',
                      'TroposphericVerticalColumnError' : 'none',
                      'TroposphericVerticalColumnModel' : 'none',
                      'VCDErrorUsingAvKernel' : 'none',
                      'VCDTropErrorUsingAvKernel' : 'none',
                      'GroundPixelQualityFlag' : 'none',
                      'Latitude' : 'none',
                      'LatitudeCornerPoints' : 'corner',
                      'Longitude' : 'none',
                      'LongitudeCornerPoints' : 'corner',
                      'SolarAzimuthAngle' : 'none',
                      'SolarZenithAngle' : 'none',
                      'Time' : 'none',
                      'ViewingAzimuthAngle' : 'none',
                      'ViewingZenithAngle' : 'none' }

    extraDimSize = { 'AirMassFactor' : 0,
                     'AirMassFactorGeometric' : 0,
                     'AirMassFactorTropospheric' : 0,
                     'AssimilatedStratosphericSlantColumn' : 0,
                     'AssimilatedStratosphericVerticalColumn' : 0,
                     'AveragingKernel' : 34,
                     'CloudFraction' : 0,
                     'CloudFractionStd' : 0,
                     'CloudPressure' : 0,
                     'CloudPressureStd' : 0,
                     'CloudRadianceFraction' : 0,
                     'GhostColumn' : 0,
                     'InstrumentConfigurationId' : 0,
                     'MeasurementQualityFlags' : 0,
                     'SlantColumnAmountNO2' : 0,
                     'SlantColumnAmountNO2Std' : 0,
                     'SurfaceAlbedo' : 0,
                     'TM4PressurelevelA' : 34,
                     'TM4PressurelevelB' : 34,
                     'TM4SurfacePressure' : 0,
                     'TM4TerrainHeight' : 0,
                     'TM4TropoPauseLevel' : 0,
                     'TerrainHeight' : 0,
                     'TotalVerticalColumn' : 0,
                     'TotalVerticalColumnError' : 0,
                     'TroposphericColumnFlag' : 0,
                     'TroposphericVerticalColumn' : 0,
                     'TroposphericVerticalColumnError' : 0,
                     'TroposphericVerticalColumnModel' : 0,
                     'VCDErrorUsingAvKernel' : 0,
                     'VCDTropErrorUsingAvKernel' : 0, 
                     'GroundPixelQualityFlag' : 0,
                     'Latitude' : 0,
                     'LatitudeCornerPoints' : 4,
                     'Longitude' : 0,
                     'LongitudeCornerPoints' : 4,
                     'SolarAzimuthAngle' : 0,
                     'SolarZenithAngle' : 0,
                     'Time' : 0,
                     'ViewingAzimuthAngle' : 0,
                     'ViewingZenithAngle' : 0 }

class HDFknmiomil2_generic_filetype():
    parser = "HDFknmiomil2"
    doutf = "OMNO2e_netCDF_avg"
    parserParms = {}

class HDFnasaomil2_generic_filetype():
    parser = "HDFnasaomil2"
    doutf = "OMNO2e_netCDF_avg"
    parserParms = {"cornerFile":("Absolute path to the file containing "\
                                 "geolocation information for the four "\
                                 "corners (OMPIXCOR).  Must be matched "\
                                 "to the input file.", "filePath")}

class HDFmopittl2_generic_filetype():
    parser = "HDFmopittl2"
    doutf = "unweighted_filtered_MOPITT_avg_netCDF"
    parserParms = {}

class MOPITT_CO_NASA_HDF_V5_filetype():
    parser = "HDFmopittl2"
    doutf = "unweighted_filtered_MOPITT_avg_netCDF"
    parserParms = {}
    time = "Time"
    longitude = "Longitude"
    solZenAng = "Solar Zenith Angle"
    surfTypeField = "Surface Index"
    colMeasField = "Retrieved CO Mixing Ratio Profile"
    outUnits = {'Time' : 'Seconds',
                'Latitude' : 'Degrees',
                'Longitude' : 'Degrees',
                'Seconds in Day' : 'Seconds',
                'Pressure Grid' : 'hPa',
                'Solar Zenith Angle' : 'Degrees',
                'Satellite Zenith Angle' : 'Degrees',
                'Surface Pressure' : 'hPa',
                'Retrieved Surface Temperature' : 'K',
                'Retrieved Surface Emissivity' : 'unitless',
                'Retrieved CO Mixing Ratio Profile' : 'ppbv',
                'Retrieved CO Surface Mixing Ratio' : 'ppbv',
                'Retrieved CO Total Column' : 'mol/cm^2',
                'Retrieved CO Total Column Diagnostics' : 'unitless',
                'Retrieval Averaging Kernel Matrix' : 'unitless',
                'Retrieval Error Covariance Matrix' : 'unitless',
                'A Priori Surface Temperature' : 'K',
                'A Priori Surface Emissivity' : 'unitless',
                'A Priori CO Mixing Ratio Profile' : 'ppbv',
                'A Priori CO Surface Mixing Ratio' : 'ppbv',
                'Level 1 Radiances and Errors' : 'W/m^2Sr',
                'Degrees of Freedom for Signal' : 'unitless',
                'Surface Index' : 'unitless',
                'DEM Altitude' : 'm',
                'Cloud Description' : 'unitless', 
                'MODIS Cloud Diagnostics' : 'unitless',
                'Water Vapor Climatology Content' : 'unitless',
                'Retrieval Iterations' : 'unitless',
                'Information Content Index' : 'unitless',
                'Signal Chi2' : 'unitless',
                'Swath Index ' : 'unitless'}
    dimLabels = {'Time' : '',
                'Latitude' : '',
                'Longitude' : '',
                'Seconds in Day' : '',
                'Pressure Grid' : 'Layer',
                'Solar Zenith Angle' : '',
                'Satellite Zenith Angle' : '',
                'Surface Pressure' : '',
                'Retrieved Surface Temperature' : 'ValueOrStandardDeviation',
                'Retrieved Surface Emissivity' : 'ValueOrStandardDeviation',
                'Retrieved CO Mixing Ratio Profile' : 'valueOrStandardDeviation',
                'Retrieved CO Surface Mixing Ratio' : 'valueOrStandardDeviation',
                'Retrieved CO Total Column' : 'valueOrStandardDeviation',
                'Retrieved CO Total Column Diagnostics' : 'valueOrStandardDeviation',
                'Retrieval Averaging Kernel Matrix' : 'column,row',
                'Retrieval Error Covariance Matrix' : 'column,row',
                'A Priori Surface Temperature' : 'valueOrStandardDeviation',
                'A Priori Surface Emissivity' : 'valueOrStandardDeviation',
                'A Priori CO Mixing Ratio Profile' : 'Layer,valueOrStandardDeviation',
                'A Priori CO Surface Mixing Ratio' : 'valueOrStandardDeviation',
                'Level 1 Radiances and Errors' : 'Channel,Radiances/Errors',
                'Degrees of Freedom for Signal' : '',
                'Surface Index' : '',
                'DEM Altitude' : '',
                'Cloud Description' : '', 
                'MODIS Cloud Diagnostics' : 'flagIndex',
                'Water Vapor Climatology Content' : '',
                'Retrieval Iterations' : '',
                'Information Content Index' : '', 
                'Signal Chi2' : '',
                'Swath Index ' : 'nthree'}
    dimSizes = {'Time' : '',
                'Latitude' : '',
                'Longitude' : '',
                'Seconds in Day' : '',
                'Pressure Grid' : '9',
                'Solar Zenith Angle' : '',
                'Satellite Zenith Angle' : '',
                'Surface Pressure' : '',
                'Retrieved Surface Temperature' : '2',
                'Retrieved Surface Emissivity' : '2',
                'Retrieved CO Mixing Ratio Profile' : '9,2',
                'Retrieved CO Surface Mixing Ratio' : '2',
                'Retrieved CO Total Column' : '2',
                'Retrieved CO Total Column Diagnostics' : '2',
                'Retrieval Averaging Kernel Matrix' : '10,10',
                'Retrieval Error Covariance Matrix' : '10,10',
                'A Priori Surface Temperature' : '2',
                'A Priori Surface Emissivity' : '2',
                'A Priori CO Mixing Ratio Profile' : '9,2',
                'A Priori CO Surface Mixing Ratio' : '2',
                'Level 1 Radiances and Errors' : '12,2',
                'Degrees of Freedom for Signal' : '',
                'Surface Index' : '',
                'DEM Altitude' : '',
                'Cloud Description' : '',
                'MODIS Cloud Diagnostics' : '10',
                'Water Vapor Climatology Content' : '',
                'Retrieval Iterations' : '',
                'Information Content Index' : '',
                'Signal Chi2' : '',
                'Swath Index ' : '3'}
