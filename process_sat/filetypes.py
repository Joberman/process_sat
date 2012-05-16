'''
List of supported filetypes and associated parameters

Each class in this file has, at minimum, an attribute "parser"
that specifies the associated parser for that class and an 
attribute "doutf" that specifies the default output function.
Each class may also contain any other variables that will be 
used for output function attributes if the output function
accepts those attributes

In some cases, output function attributes may consist of lists
associated with field names for that particular filetype.  In 
these cases, the variables for these attributes will be 
dictionaries keyed off the field name strings.

Some parsers require additional attributes (beyond the 
filename, subtype, and extension).
'''

class OMI_NO2_KNMI_HDF_v2_0_preFeb2006_filetype():
    parser = 'HDFknmiomil2'
    parserParms = []
    doutf = 'OMNO2e_netCDF_avg_out_func'
    overallQualFlag = 'TroposphericColumnFlag'
    cloudFrac = 'CloudFraction'
    solarZenithAngle = 'SolarZenithAngle'
    time = 'Time'
    longitude = 'Longitude'
    pixIndXtrackAxis = '1'
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
    parserParms = []
    doutf = 'OMNO2e_netCDF_avg_out_func'
    overallQualFlag = 'TroposphericColumnFlag'
    cloudFrac = 'CloudFraction'
    solarZenithAngle = 'SolarZenithAngle'
    time = 'Time'
    longitude = 'Longitude'
    pixIndXtrackAxis = '1'
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
                                 "to the input file.  If you do not "   \
                                 "want to use corners, set to any "     \
                                 "string and use nearest neighbor "     \
                                 "mapping.", "filePath")}

class OMI_NO2_NASA_HDF_V12_filetype():
    parser = "HDFnasaomil2"
    doutf = "OMNO2e_netCDF_avg"
    parserParms = {"cornerFile":("Absolute path to the file containing "\
                                 "geolocation information for the four "\
                                 "corners (OMPIXCOR).  Must be matched "\
                                 "to the input file.  If you do not "   \
                                 "want to use corners, set to any "     \
                                 "string and use nearest neighbor "     \
                                 "mapping.", "filePath")}
    overallQualFlag = 'vcdQualityFlags'
    cloudFrac = 'CloudFraction'
    solarZenithAngle = 'SolarZenithAngle'
    time = 'Time'
    longitude = 'Longitude'
    pixIndXtrackAxis = '1'
    outUnits = { 'Time' : 'second',
                 'Latitude' : 'degree',
                 'Longitude' :'degree (-180 to 180)',
                 'SpacecraftLatitude' : 'degree', 
                 'SpacecraftLongitude' : 'degree (-180 to 180)',
                 'SpacecraftAltitude' : 'meters',
                 'SolarZenithAngle' : 'degree',
                 'SolarAzimuthAngle' : 'degree',
                 'ViewingZenithAngle' : 'degree',
                 'ViewingAzimuthAngle' : 'degree',
                 'GroundPixelQualityFlags' : 'NoUnits',
                 'ColumnAmountNO2' : 'molecules/cm^2',
                 'ColumnAmountNO2Std' : 'molecules/cm^2',
                 'ColumnAmountNO2Initial' : 'molecules/cm^2',
                 'ColumnAmountNO2InitialStd' : 'molecules/cm^2',
                 'ColumnAmountNO2Trop' : 'molecules/cm^2',
                 'ColumnAmountNO2TropStd' : 'molecules/cm^2',
                 'ColumnAmountNO2BelowCloud' : 'molecules/cm^2',
                 'ColumnAmountNO2BelowCloudStd' : 'molecules/cm^2',
                 'ColumnAmountNO2Unpolluted' : 'molecules/cm^2',
                 'ColumnAmountNO2UnpollutedStd' : 'molecules/cm^2',
                 'ColumnAmountNO2Polluted' : 'molecules/cm^2',
                 'ColumnAmountNO2PollutedStd' : 'molecules/cm^2',
                 'TropFractionUnpolluted' : 'NoUnits',
                 'TropFractionUnpollutedStd' : 'NoUnits',
                 'SlantColumnAmountNO2' : 'molecules/cm^2',
                 'SlantColumnAmountNO2Std' : 'molecules/cm^2',
                 'RingCoefficient' : 'NoUnits',
                 'RingCoefficientStd' : 'NoUnits',
                 'SlantColumnAmountO3' : 'molecules/cm^2',
                 'SlantColumnAmountO3Std' : 'molecules/cm^2',
                 'SlantColumnAmountH2O' : 'molecules/cm^2',
                 'SlantColumnAmountH2Otd' : 'molecules/cm^2',
                 'SlantColumnAmountO2O2' : 'molecules/cm^2',
                 'SlantcolumnAmountO2O2Std' : 'molecules/cm^2',
                 'PolynomialCoefficients' : 'NoUnits',
                 'PolynomialCoefficientsStd' : 'NoUnits',
                 'ChiSquaredOfFit' : 'NoUnits',
                 'RootMeanSquareErrorOfFit' : 'sr^-1',
                 'AMFInitial' : 'NoUnits',
                 'AMFInitialStd' : 'NoUnits',
                 'AMFInitialClear' : 'NoUnits',
                 'AMFInitialClearStd' : 'NoUnits',
                 'AMFInitialCloudy' : 'NoUnits',
                 'AMFInitialCloudStd' : 'NoUnits',
                 'AMFUnpolluted' : 'NoUnits',
                 'AMFUnpollutedStd' : 'NoUnits',
                 'AMFUnpollutedClear' : 'NoUnits',
                 'AMFUnpollutedClearStd' : 'NoUnits',
                 'AMFUnpollutedCloudy' : 'NoUnits',
                 'AMFUnpollutedCloudyStd' : 'NoUnits',
                 'AMFPolluted' : 'NoUnits',
                 'AMFPollutedStd' : 'NoUnits',
                 'AMFPollutedClear' : 'NoUnits',
                 'AMFPollutedClearStd' : 'NoUnits',
                 'AMFPollutedCloudy' : 'NoUnits',
                 'AMFPollutedCloudyStd' : 'NoUnits',
                 'AMFPollutedToGround' : 'NoUnits',
                 'AMFPollutedToGroundStd' : 'NoUnits',
                 'CloudFraction' : 'NoUnits',
                 'CloudFractionStd' : 'NoUnits',
                 'CloudRadianceFraction' : 'NoUnits',
                 'CloudPressure' : 'hPa',
                 'CloudPressureStd' : 'hPa',
                 'TerrainReflectivity' : 'NoUnits',
                 'TerrainPressure' : 'hPa',
                 'TerrainHeight' : 'meters',
                 'SmallPixelRadiancePointer' : 'NoUnits',
                 'InstrumentConfigurationId' : 'NoUnits',
                 'MeasurementQualityFlags' : 'NoUnits',
                 'FitQualityFlags' : 'NoUnits',
                 'AMFQualityFlags' : 'NoUnits',
                 'WavelengthRegistrationCheck' : 'nm',
                 'WavelengthRegistrationCheckStd' : 'nm',
                 'UnpolFldLatBandQualityFlags' : 'NoUnits',
                 'vcdQualityFlags' : 'NoUnits' }

    extraDimLabel = { 'Time' : 'none',
                 'Latitude' : 'none',
                 'Longitude' : 'none',
                 'SpacecraftLatitude' : 'none',
                 'SpacecraftLongitude' : 'none',
                 'SpacecraftAltitude' : 'none',
                 'SolarZenithAngle' : 'none',
                 'SolarAzimuthAngle' : 'none',
                 'ViewingZenithAngle' : 'none',
                 'ViewingAzimuthAngle' : 'none',
                 'GroundPixelQualityFlags' : 'none',
                 'ColumnAmountNO2' : 'none',
                 'ColumnAmountNO2Std' : 'none',
                 'ColumnAmountNO2Initial' : 'none',
                 'ColumnAmountNO2InitialStd' : 'none',
                 'ColumnAmountNO2Trop' : 'none',
                 'ColumnAmountNO2TropStd' : 'none',
                 'ColumnAmountNO2BelowCloud' : 'none',
                 'ColumnAmountNO2BelowCloudStd' : 'none',
                 'ColumnAmountNO2Unpolluted' : 'none',
                 'ColumnAmountNO2UnpollutedStd' : 'none',
                 'ColumnAmountNO2Polluted' : 'none',
                 'ColumnAmountNO2PollutedStd' : 'none',
                 'TropFractionUnpolluted' : 'none',
                 'TropFractionUnpollutedStd' : 'none',
                 'SlantColumnAmountNO2' : 'none',
                 'SlantColumnAmountNO2Std' : 'none',
                 'RingCoefficient' : 'none',
                 'RingCoefficientStd' : 'none',
                 'SlantColumnAmountO3' : 'none',
                 'SlantColumnAmountO3Std' : 'none',
                 'SlantColumnAmountH2O' : 'none',
                 'SlantColumnAmountH2Otd' : 'none',
                 'SlantColumnAmountO2O2' : 'none',
                 'SlantcolumnAmountO2O2Std' : 'none',
                 'PolynomialCoefficients' : 'none',
                 'PolynomialCoefficientsStd' : 'none',
                 'ChiSquaredOfFit' : 'none',
                 'RootMeanSquareErrorOfFit' : 'none',
                 'AMFInitial' : 'none',
                 'AMFInitialStd' : 'none',
                 'AMFInitialClear' : 'none',
                 'AMFInitialClearStd' : 'none',
                 'AMFInitialCloudy' : 'none',
                 'AMFInitialCloudStd' : 'none',
                 'AMFUnpolluted' : 'none',
                 'AMFUnpollutedStd' : 'none',
                 'AMFUnpollutedClear' : 'none',
                 'AMFUnpollutedClearStd' : 'none',
                 'AMFUnpollutedCloudy' : 'none',
                 'AMFUnpollutedCloudyStd' : 'none',
                 'AMFPolluted' : 'none',
                 'AMFPollutedStd' : 'none',
                 'AMFPollutedClear' : 'none',
                 'AMFPollutedClearStd' : 'none',
                 'AMFPollutedCloudy' : 'none',
                 'AMFPollutedCloudyStd' : 'none',
                 'AMFPollutedToGround' : 'none',
                 'AMFPollutedToGroundStd' : 'none',
                 'CloudFraction' : 'none',
                 'CloudFractionStd' : 'none',
                 'CloudRadianceFraction' : 'none',
                 'CloudPressure' : 'none',
                 'CloudPressureStd' : 'none',
                 'TerrainReflectivity' : 'none',
                 'TerrainPressure' : 'none',
                 'TerrainHeight' : 'none',
                 'SmallPixelRadiancePointer' : 'SmallPixelPointer',
                 'InstrumentConfigurationId' : 'none',
                 'MeasurementQualityFlags' : 'none',
                 'FitQualityFlags' : 'none',
                 'AMFQualityFlags' : 'none',
                 'WavelengthRegistrationCheck' : 'WavelengthCheck',
                 'WavelengthRegistrationCheckStd' : 'WavelengthCheck',
                 'UnpolFldLatBandQualityFlags' : 'Latitude',
                 'vcdQualityFlags' : 'none' }

    extraDimSize = { 'Time' : 0,
                 'Latitude' : 0,
                 'Longitude' : 0,
                 'SpacecraftLatitude' : 0,
                 'SpacecraftLongitude' : 0,
                 'SpacecraftAltitude' : 0,
                 'SolarZenithAngle' : 0,
                 'SolarAzimuthAngle' : 0,
                 'ViewingZenithAngle' : 0,
                 'ViewingAzimuthAngle' : 0,
                 'GroundPixelQualityFlags' : 0,
                 'ColumnAmountNO2' : 0,
                 'ColumnAmountNO2Std' : 0,
                 'ColumnAmountNO2Initial' : 0,
                 'ColumnAmountNO2InitialStd' : 0,
                 'ColumnAmountNO2Trop' : 0,
                 'ColumnAmountNO2TropStd' : 0,
                 'ColumnAmountNO2BelowCloud' : 0,
                 'ColumnAmountNO2BelowCloudStd' : 0,
                 'ColumnAmountNO2Unpolluted' : 0,
                 'ColumnAmountNO2UnpollutedStd' : 0,
                 'ColumnAmountNO2Polluted' : 0,
                 'ColumnAmountNO2PollutedStd' : 0,
                 'TropFractionUnpolluted' : 0,
                 'TropFractionUnpollutedStd' : 0,
                 'SlantColumnAmountNO2' : 0,
                 'SlantColumnAmountNO2Std' : 0,
                 'RingCoefficient' : 0,
                 'RingCoefficientStd' : 0,
                 'SlantColumnAmountO3' : 0,
                 'SlantColumnAmountO3Std' : 0,
                 'SlantColumnAmountH2O' : 0,
                 'SlantColumnAmountH2Otd' : 0,
                 'SlantColumnAmountO2O2' : 0,
                 'SlantcolumnAmountO2O2Std' : 0,
                 'PolynomialCoefficients' : 0,
                 'PolynomialCoefficientsStd' : 0,
                 'ChiSquaredOfFit' : 0,
                 'RootMeanSquareErrorOfFit' : 0,
                 'AMFInitial' : 0,
                 'AMFInitialStd' : 0,
                 'AMFInitialClear' : 0,
                 'AMFInitialClearStd' : 0,
                 'AMFInitialCloudy' : 0,
                 'AMFInitialCloudStd' : 0,
                 'AMFUnpolluted' : 0,
                 'AMFUnpollutedStd' : 0,
                 'AMFUnpollutedClear' : 0,
                 'AMFUnpollutedClearStd' : 0,
                 'AMFUnpollutedCloudy' : 0,
                 'AMFUnpollutedCloudyStd' : 0,
                 'AMFPolluted' : 0,
                 'AMFPollutedStd' : 0,
                 'AMFPollutedClear' : 0,
                 'AMFPollutedClearStd' : 0,
                 'AMFPollutedCloudy' : 0,
                 'AMFPollutedCloudyStd' : 0,
                 'AMFPollutedToGround' : 0,
                 'AMFPollutedToGroundStd' : 0,
                 'CloudFraction' : 0,
                 'CloudFractionStd' : 0,
                 'CloudRadianceFraction' : 0,
                 'CloudPressure' : 0,
                 'CloudPressureStd' : 0,
                 'TerrainReflectivity' : 0,
                 'TerrainPressure' : 0,
                 'TerrainHeight' : 0,
                 'SmallPixelRadiancePointer' : 2,
                 'InstrumentConfigurationId' : 0,
                 'MeasurementQualityFlags' : 0,
                 'FitQualityFlags' : 0,
                 'AMFQualityFlags' : 0,
                 'WavelengthRegistrationCheck' : 60,
                 'WavelengthRegistrationCheckStd' : 60,
                 'UnpolFldLatBandQualityFlags' : 180,
                 'vcdQualityFlags' : 0 }

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
