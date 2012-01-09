PROJECT TITLE: Process_sat
PURPOSE OF PROJECT: Provide a well-documented, easy-to-use general-purpose
                    processing module for processing satellite data
VERSION: 0.2.72 (12/16/2011)
AUTHORS: oberman, maki
CONTACT: oberman@wisc.edu


-----------------
-- QUICK START --
-----------------


1. Install the program and run the built-in test module to confirm
that it is working properly.  Installation instructions can be found
in the file INSTALL.txt
 

2. Download whatever data you plan to process.  Currently, the program
is designed to process OMI NO2 DOMINO level 2 data, OMI NO2 NASA level
2 data and MOPITT CO data.


3. Navigate to the folder where process.py is located (or add it to
your path) and invoke it as:
     
     process.py --help


4. Follow the on-screen instructions, adding each of the required
parameters.  If you need help with the projection attributes or the
output function attributes, invoke the built-in help as:

     process.py --AttributeHelp <function_name>

For detailed explanations of all parameters and attributes, see the
"Parameter Details" section below.


5. Invoke process.py once for each output file you'd like to create.
Note that the software creates output files with only a single
timestep, so you'll need to invoke the command once for each timestep
(IE if you want a month with timesteps every day, you'll probably want
to write a shell script that calls the command once for each day)


6. Create a grid file for your chosen grid by PLACEHOLDER PLACEHOLDER
PLACEHOLDER PLACEHOLDER PLACEHOLDER


7. Concatenate your outputs if desired (the authors recommend the NCO
operators at http://nco.sourceforge.net/ if you're using a netCDF
output format) and carry on!  


----------------------------------
-- EXAMPLE/TEMPLATE INVOCATIONS --
----------------------------------

For clarity and readability, line continuation characters are used to
place each attribute on a separate line.  It is not required to break
up attributes like this, but the command line needs to see the
invocation as a single command, so if you want to break it onto
multple lines you must use line-continuation characters.

1. Process MOPITT level 2 CO data, (Version 5) 
     - processes a single file
     - Uses a 36km lambert conic conformal grid centered over North
     America
     - Writes out a 2D, 3D, and 4D parameter from the file


     process.py \
     --directory /path/to/input/files/ \
     --fileList MOP02T-20050106-L2V10.1.1.prov.hdf \
     --filetype HDFmopittl2 \
     --gridProj lcc2par \
     --projAttrs xOrig:-2916000 yCell:36000 refLon:-97 refLat:40 \
     nCols:162 nRows:126 stdPar2:45 stdPar1:33 xCell:36000 \
     earthRadius:6370000 yOrig:-2268000\
     --mapFunc point_in_cell \
     --outFunc unweighted_filtered_MOPITT_avg_netCDF \
     --outFuncAttrs time:Time longitude:Longitude \
     "inFieldNames:Time,Retrieved CO Mixing Ratio Profile,Retrieved CO Surface Mixing Ratio" \
     outFieldNames:time,COprof,COsurf outUnits:TAI93,ppbv,ppbv \
     logNormal:False,True,True "dimLabels:(),(layer.valOrStdDev),(valOrStdDev)" \
     "dimSizes:(),(9.2),(2)" "timeStart:00:00:00 01-06-2005" \
     "timeStop:23:59:59 01-06-2005" timeComparison:UTC \
     fillVal:-9999.0 \solZenAngCutoff:85 \
     "solZenAng:Solar Zenith Angle" dayTime:True \
     "surfTypeField:Surface Index" \
     "colMeasField:Retrieved CO Mixing Ratio Profile" \
     --outDirectory /path/to/output/directory/ \
     --outFileName MOPITT_v5_20050106_daytime_CONUS36km_test.nc \
     --verbose True \
     --interactive True
     

-----------------------
-- PARAMETER DETAILS --
-----------------------


Each input attribute is explained here.  Note that each output
function has a separate set of required inputs and that the
--outFuncAttrs is therefore broken down by output function.  Make sure
you're referencing the details for the attributes relevant to the
function you want to use.  


  --help
	Display the onscreen help message and exit the program.


  --directory /path/to/input/director


