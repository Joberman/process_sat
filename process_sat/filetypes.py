class HDFknmiomil2_generic_filetype():
    parser = "HDFknmiomil2"
    doutf = "OMNO2e_netCDF_avg"

class HDFnasaomil2_generic_filetype():
    parser = "HDFnasaomil2"
    doutf = "OMNO2e_netCDF_avg"

class HDFmopittl2_generic_filetype():
    parser = "HDFmopittl2"
    doutf = "unweighted_filtered_MOPITT_avg_netCDF"

class MOPITT_CO_NASA_HDF_V5_filetype():
    parser = "HDFmopittl2"
    doutf = "unweighted_filtered_MOPITT_avg_netCDF"
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
