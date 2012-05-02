PROJECT TITLE: WHIPS
PURPOSE OF PROJECT: Provide a well-documented, easy-to-use general-purpose
                    processing module for processing satellite data
VERSION: 1.0.5 (3/26/2012)
AUTHORS: oberman, maki, strom
CONTACT: oberman@wisc.edu


ACKNOWLEDGEMENT POLICY
======================
Whenever you publish research or present results generated with WHIPS,
please include the following acknowledgement or an appropriate
equivalent:

	We wish to thank the University of Wisconsin--Madison for the 
	use and development of the Wisconsin Horizontal Interpolation
	Program for Satellites (WHIPS).  WHIPS was developed by Jacob
	Oberman, Erica Scotty, Keith Maki and Tracey Holloway, with 
	funding from the NASA Air Quality Applied Science Team 
	(AQAST) and the Wisconsin Space Grant Consortium Undergraduate
	Award.


QUICK START
===========


1. Install the program and run the built-in test module to confirm
that it is working properly.  Installation instructions can be found
in the file INSTALL.txt
 

2. Download whatever data you plan to process.  Currently, the program
is designed to process OMI NO2 DOMINO level 2 data, OMI NO2 NASA level
2 data and MOPITT CO data.  See the detailed documentation for the 
--filelist argument for locations of data.


3. Navigate to the folder where whips.py installed or add it to
your path.  It should be the /bin folder corresponding to the /lib 
folder where your python packages live.  Invoke it as:
     
     whips.py --help


4. Follow the on-screen instructions, adding each of the required
parameters.  If you need help with the projection attributes or the
output function attributes, invoke the built-in help as:

     whips.py --AttributeHelp <function_name>

For detailed explanations of all parameters and attributes, see the
"Parameter Details" section below.


5. Invoke whips.py once for each output file you'd like to create.
Note that the software creates output files with only a single
timestep, so you'll need to invoke the command once for each timestep
(IE if you want a month with timesteps every day, you'll probably want
to write a shell script that calls the command once for each day)


6. Additionally, you may create a grid file for your chosen grid by 
including the --includeGrid flag followed by the desired filename.  
A file containing the gridcells used by the projection will be written 
to the same directory as the standard output file.


7. Concatenate your outputs if desired (the authors recommend the NCO
operators at http://nco.sourceforge.net/ if you're using a netCDF
output format) and carry on!  


EXAMPLE/TEMPLATE INVOCATIONS
============================

For clarity and readability, line continuation characters are used to
place each attribute on a separate line.  It is not required to break
up attributes like this, but the command line needs to see the
invocation as a single command, so if you want to break it onto
multple lines you must use line-continuation characters.

1. Process MOPITT level 2 CO data, (Version 5) 
----------------------------------------------

     - Processes a single file
     - Uses a 36km lambert conic conformal grid centered over North
     America
     - Writes out a 2D, 3D, and 4D parameter from the file


     whips.py \
     --directory /path/to/input/files/ \
     --filetype HDFmopittl2 \
     --fileList MOP02T-20050106-L2V10.1.1.prov.hdf \
     --gridProj lcc2par \
     --projAttrs xOrig:-2916000 yCell:36000 refLon:-97 refLat:40 \
     nCols:162 nRows:126 stdPar2:45 stdPar1:33 xCell:36000 \
     earthRadius:6370000 yOrig:-2268000\
     --mapFunc point_in_cell \
     --outFuncAttrs time:Time longitude:Longitude \
     "inFieldNames:Time,Retrieved CO Mixing Ratio Profile,Retrieved CO Surface Mixing Ratio" \
     outFieldNames:time,COprof,COsurf outUnits:TAI93,ppbv,ppbv \
     logNormal:False,True,True "dimLabels:;layer,valOrStdDev;valOrStdDev" \
     "dimSizes:;9,2;2" "timeStart:00:00:00_01-06-2005" \
     "timeStop:23:59:59_01-06-2005" timeComparison:UTC \
     fillVal:-9999.0 \
     solZenAngCutoff:85 \
     "solZenAng:Solar Zenith Angle" dayTime:True \
     "surfTypeField:Surface Index" \
     "colMeasField:Retrieved CO Mixing Ratio Profile" \
     --outDirectory /path/to/output/directory/ \
     --outFileName MOPITT_v5_20050106_daytime_CONUS36km_test.nc \
     --verbose True \
     --interactive True

2. Process OMI level 2 DOMINO NO2 data, (Version 2) 
---------------------------------------------------

     - Processes any number of files
     - Uses a 36km lambert conic conformal grid centered over North
     America
     - Writes out a 2D, and 3D parameter from the file


     whips.py \
     --directory /where/you/keep/the/files/ \
     --filetype HDFknmiomil2 \
     --fileList OMI-Aura_L2-OMDOMINO_2006m0701t0023-o10423_v003-2010m1008t224420.he5 \
       OMI-Aura_L2-OMDOMINO_2006m0701t0112-o10424_v003-20120m1008t224845.he5 \
     --gridProj lcc2par \
     --projAttrs xOrig:-2916000 yCell:36000 refLon:-97 refLat:40 \
       nCols:162 nRows:126 stdPar2:45 stdPar1:33 xCell:36000 \
       earthRadius:6370000 yOrig:-2268000 \
     --mapFunc regional_intersect \
     --outFuncAttrs overallQualFlag:TroposphericColumnFlag cloudFrac:CloudFraction \
       solarZenithAngle:SolarZenithAngle time:Time longitude:Longitude \
       inFieldNames:Time,AveragingKernel,TroposphericVerticalColumn \
       outFieldNames:time,avKern,tropVCD \
       "outUnits:TAI93,unitless x 1000,molec/cm^2x1^-15" extraDimLabel:none,Layers,none \
       extraDimSize:0,34,0 timeStart:00:00:00_07-01-2006 timeStop:23:59:59_07-01-2006 \
       timeComparison:UTC fillVal:-9999 cloudFractUpperCutoff:0.3 \
       solarZenAngUpperCutoff:85 pixIndXtrackAxis:1 \
     --outDirectory /where/you/want/output \
     --outFileName OMI_DOMINO_20060701_test.nc \
     --includeGrid OMI_DOMINO_GridFileName.nc \
     --verbose True \
     --interactive True
     

PARAMETER DETAILS
=================

Each input attribute is explained here.  Note that each output
function has a separate set of required inputs and that the
--outFuncAttrs is therefore broken down by output function.  Make sure
you're referencing the details for the attributes relevant to the
function you want to use.  

  --help
	REQUIRED: NO
	DEFAULT: N/A
	- Display the onscreen help message and exit the program.

  --directory /path/to/input/directory
  	REQUIRED: NO
	DEFAULT: the current working directory at time of invocation  	      
  	- The input directory that the program will search for whatever
  	  input files are specified.  If those files are not found in
  	  this directory, the programs behavior is governed by the
  	  value of the --interactive flag

  --fileList file1 [file2] [file3] ...
  	REQUIRED: NO
	DEFAULT: The list of all files in --directory (non-recursive)
	- The list of files that the program should attempt to
  	  process for output.  Most output functions (with the 
	  exception of the function designed for MOPITT CO) are
  	  designed to accept an arbitrary number of inputs and only
  	  use that data which fits the requirements.  
	- filtering out files a priori which cannot contain the
   	  information required, for instance files known to be on the
	  wrong date, saves computational power.  It is advisable to
	  use this parameter to include only those files which may
          contain the desired information wherever possible.
	- Locations of data (current as of 01/12/12
		MOPITT - <http://eosweb.larc.nasa.gov/HPDOCS/datapool/>
		NASA OMI - <http://mirador.gsfc.nasa.gov/cgi-bin/mirador/collectionlist.pl?keyword=omno2>
		KNMI OMI - <http://www.temis.nl/airpollution/no2col/data/omi/data_v2/>

  --filetype {HDFknmiomil2, HDFmopittl2, HDFnasaomil2}
  	REQUIRED: YES
	DEFAULT: N/A
	- The type of file we're attempting to read in.  Must be one
  	of the options listed above.  This must match the format of
  	the file (currently only the standard level 2 files for each
  	of the above listed instruments/retrievals are supported).
  	- This is probably the easiest part of the program to extend,
  	so if you're looking to use a particular filetype that isn't
  	supported have a look at parse_geo.py and look at possibly
  	extending it to include your filetype.

  --gridProj {latlon, lcc2par}
  	REQUIRED: YES
	DEFAULT: N/A
	- The grid projection used to define the target grid (the grid
  	that we wish to regrid our data to).  Must be one of the above
  	options.  Further details on these options are as follows:
 	
		latlon   - The Plate Caree projection, also known as
		       	 the "unprojected" projection.  x and y are
		       	 mapped directly to longitude and latitude,
		       	 respectively.  
			
			REQUIRED PARAMETERS:
			  xCell	 - The size of a gridcell in the x
			  	 (longitude) direction.  In degrees.
			  yCell  - The size of a gridcell in the y
				 (latitude) direction.  In degrees.
			  xOrig  - The longitude of the lower-left
			  	 corner of the domain
			  yOrig	 - The latitude of the lower-left
			    	 corner of the domain
			  nRows	 - The number of rows in the grid.
			  nCols	 - The number of columns in the grid.

		lcc2par	 - The Lambert Conic Conformal projection (2
		         parallel construction).  x and y are
		         transformed and scaled, then mapped to
		         latitude and longitude via the projection.
		         The projection parameters must be accurate to
		         get the correct output grid.  All required
		         parameters are available in the GRIDDESC file
		         associated with the MM3 modeling system. A
		         description of the GRIDDESC format can be
		         found at
		         http://www.baronams.com/products/ioapi/GRIDDESC.html

			 REQUIRED PARAMETERS:
			 stdPar1 - One of the 2 standard parallels
			  	   used	to define the Lambert Conic
			   	   Conformal projection.  Must be a
				   valid latitude, in degrees.
		 	 stdPar2 - The second standard parallel used
			 	   to define the Lambert Conic
				   Conformal projection.  Set this
			 	   equal to the same value as stdPar1 
				   if the single-parallel form of the
				   projection is being used. Must be a
				   valid latitude in degrees.
			 refLat	 - The reference latitude upon which
			 	   the projection is centered. This is
			 	   the YCENT value in the GRIDDESC
				   file. In degrees
			 refLon  - The reference longitude upon which
			 	   the  projection is centered.  This
				   is BOTH the XCENT and PROJ_GAMMA
			 	   values in the GRIDDESC file.  If
			 	   these values are not identical, do
			 	   not use this function. In degrees.
			 xOrig	 - The location of the origin in
			 	   projected x coordinates.  This
			 	   is the XORIG value in the GRIDDESC
			 	   file. In same units as earthRadius.
			 yOrig	 - The location of the origin in
			 	   projected y coordinates.  This
			 	   is the YORIG value in the GRIDDESC
			 	   file. In same units as earthRadius.
			 xCell	 - The x dimension of a cell, in
			 	   projected coordinates.  In the same
			 	   units as earthRadius.  This is the
			 	   XCELL value in the GRIDDESC file
			 yCell	 - The y dimension of a cell, in
			 	   projected coordinates.  In the same
			 	   units as earthRadius.  This is the
			 	   YCELL value in the GRIDDESC file
			 nRows	 - The number of rows in the grid.
			 nCols   - The number of columns in the grid.
			 earthRadius - The assumed radius of the Earth
			 	   (assumed spherical).  Must match
				   units used for xCell and yCell.

  --projAttrs name1:value1 name2:value2 ...
	REQUIRED: YES
	DEFAULT: N/A
	- The attributes required for the chosen projection.  Must
	  have all the required attributes for that projection.  The
	  required parameters for each projection are listed under
          that projection's name above.
	- Case-sensitive.  Attribute names must EXACTLY match those
	  laid out above.

  --mapFunc {point_in_cell, regional_intersect}
  	REQUIRED: YES
	DEFAULT: N/A
	- The mapping function that will be used to assign pixels to
  	  cell(s).  Certain datasets have restrictions on which
	  mapping functions are usable.
	- Also responsible for computing the "geometric weight" of
  	  pixels.  That is, this function computes the weight unique
	  to a cell/pixel combination.  At present, neither of the
	  functions provide this functionality.
	        
		point_in_cell - Maps pixels defined by a single
			lat/lon (usually the cell center) to whatever
			grid cell that point lies inside in projected
			space.  This assigns each pixel to a unique
			grid cell.  Grid cells are open on the top and
			right sides and closed on the left and lower
			sides (with directions defined according to
			the projected coordinate system).  This
			function is supported by all currently
			available input filetypes.  NOTE: for 
			filetypes where regional_intersect is 
			available it is strongly recommended to use
			regional_intersect over point_in_cell.

		regional_intersect - Maps pixels (as defined by 
			pairs of geocoordinates that nominally
			correspond to pixel corners) to ALL gridcells
			intersected.  No geometric weights are
			calculated.  This function is currently
			supported by HDFnasaomil2 and HDFknmiomil2
			filetypes only.  Makes several assumptions:
			  - Polar discontinuities not encountered
			  - Projection is NOT global
			  - grid is rectilinear in projected space.
			  - Pixels are convex polygons.
		
  --outFunc {OMNO2e_netCDF_avg,OMNO2e_wght_avg,unweighted_filtered_MOPITT_avg_netCDF}
  	REQUIRED: NO
	DEFAULT: Depends on the value chose for --filetype
	- The function that computes the output and writes the output
  	  file.  Functions are given significant freedom, but all
	  current functions take some kind of average and write it to
  	  an output file.
	- These functions are frequently designed around a particular
  	  instrument or input format.  Efforts are made to make them
  	  as general as possible, but specialized output functions are
	  only guaranteed (and really should only be used) for the
	  parser types for which they have been designed.  To this 
	  end, the associated function will be chosen by default for 
	  all filetypes, though it can always be overridden with this 
	  command.
	- Currently, functions are assigned to filetypes as follows:
	     HDFknmiomil2 --> OMNO2e_netCDF_avg
	     HDFnasaomil2 --> OMNO2e_netCDF_avg
	     HDFmopittl2  --> unweighted_filtered_MOPITT_avg_netCDF
	- In all cases where a fieldname must be given for a
   	  parameter it is the short name (the name used to access the
  	  field through the parser) that must be given.  The 
	  fieldnames must correspond to the official field names 
          in the data file.  These can usually be found in the data
	  documentation.  Documentation for a few commonly processed
	  formats can be found at:
		OMI (KNMI) - <http://www.temis.nl/docs/OMI_NO2_HE5_1.0.2.pdf>
		OMI (NASA) - <http://toms.gsfc.nasa.gov/omi/no2/OMNO2_data_product_specification.pdf>
		MOPITT - <http://www.acd.ucar.edu/mopitt/v5_users_guide_beta.pdf>

	     	 OMNO2e_netCDF_avg - Averaging algorithm based on the
		 	NASA OMI level 2 to level 3 processing
		 	algorithm.  Designed for the OMI level 2
		 	filetypes (HDFnasaomil2 and HDFknmiomil2) and 
			is the default for those filetypes use with 
			other filetypes is of questionable utility.  

			Outputs results to a netCDF file.
			
			Further details available in the
		 	official NASA documentation located at 
			<http://disc.sci.gsfc.nasa.gov/Aura/data-holdings/OMI/omno2e_v003.shtml>
			
			Assumptions:
			  - Data is at most 3 dimensional.
			  - Invalid pixels are marked with an overall
		 	  quality flag.
			  - Timestamps are in the TAI93 format.
			
			
		 OMNO2e_wght_avg - Weighted averaging algorithm based
		 	on the NASA algorithm used to process OMI from
		 	level 2 to level 3.  Designed for the OMI
		 	level 2 filetypes (currently HDFnasaomil2 and
		 	HDFknmiomil2) but is NOT the default for those
			filetypes.  Use with other filetypes is of
		 	questionable utility.

			Outputs results to a CSV file.  Does
			not filter based on time as OMNO2e_netcdf_avg
			does.

			CSV file is designed such that if it is put
			into an array from top left to bottom right,
			the indices of the values will be correct.

			Further details available in the official NASA
			documentation located at
			<http://disc.sci.gsfc.nasa.gov/Aura/data-holdings/OMI/omno2e_v003.shtml>
			
			Assumptions:
			- Data is 2 dimensional
			- Invalid pixels are marked with an overall
			quality flag
			- Timestamps within the file should be in the
			TAI-93 standard
			

		 unweighted_filtered_MOPITT_avg_netCDF - Averaging
		 	algorithm based on the NASA algorithm for
		 	processing level 2 MOPITT CO data to level 3
		 	MOPITT CO data.  Designed for the MOPITT level
		 	2 filetypes (HDFmopittl2 only at present) and 
			is the default for that filetype. Use with 
			other filetypes is discouraged.
			
			Outputs results to a netCDF file.

			IMPORTANT: Only 1 input file may be used with
			this function.  Conveniently, NASA currently
			provides data in 1-day granules.

			Further details available in the official NASA
			documentation:
			
			Deeter, Merritt N (2009). MOPITT (Measurements
			    of Pollution in the Troposphere) Validated
			    Version 4 Product Users Guide.  Available from
			    <http://www.acd.ucar.edu/mopitt/products.shtml>

			Assumptions/caveats:
			  - All fields are filtered based on the
			  number of valid layers present in the
			  specified column field.  Including 2D
			  fields.
			  - Timestamps are in the TAI93 format.


  --outFuncAttrs name1:value1 name2:value2
  	REQUIRED: YES
	DEFAULT: N/A
	- The attributes required for the chosen output function.
	  Must have all required attributes for that output function.
  	  The required parameters for each projection are listed
	  above.
	- If one of the "value" elements contains whitespace, enclose
	  the entire name:value pair in double quotes.  For example:
	      the:full_monty  	     <- okay
	      "the:full monty" 	     <- okay
	      the:full monty	     <- not okay
	- In many cases, a comma delimited list is requested.  Make
	  sure that elements of the list are not separated by spaces.
	  For example:
	      pythons:EricIdle,JohnCleese	<- okay
	      pythons:EricIdle, JohnCleese	<- not okay
	      "pythons:Eric Idle,John Cleese"	<- okay
	      "pythons:Eric Idle, John Cleese"	<- not okay
	- Case-sensitive.  Attribute names must EXACTLY match those
	  laid out below.
	- Below are the required parameters for each existing output
	  function.  { } contain usable/recommended parameters for 
	  applicable filetypes.  These are based on the current 
	  versions of the data at the time of writing and should be
	  double-checked:

		OMNO2e_netCDF_avg -
			overallQualFlag - The name of the field
				containing the overall quality flag
				for the pixels.  This flag should be
				true (1) for invalid pixels and false
				(0) for valid pixels.
				{ OMI KNMI - TroposphericColumnFlag
				  OMI NASA - vcdQualityFlags }
			cloudFrac - The name of the field containing
				the cloud fractions.
				{ OMI KNMI - CloudFraction
				  OMI NASA - CloudFraction }
			solarZenithAngle - The name of the field
				containing the solar zenith angles in
				degrees.
				{ OMI KNMI - SolarZenithAngle
				  OMI NASA - SolarZenithAngle }
			time - The name of the field containing the
				timestamps.  Timestamps are assumed to
				be in the TAI-93 format.
				{ OMI KNMI - Time
				  OMI NASA - Time }
			longitude - The name of the field containing
				the longitudes at cell centers.
				Longitudes should be in degrees east.
				{ OMI KNMI - Longitude
				  OMI NASA - Longitude }
			inFieldNames - The names of the fields desired
				to be output.  Input as comma
				delimited list.
			outFieldNames - The names of the output
				variables (even if they are to be the
				same as input variables).  Should be a
				comma-delimited list co-indexed to
				inFieldNames
			outUnits - The units of the variables to be
				written out.  Should be a
				comma-delimited list co-indexed to
				inFieldNames
			extraDimLabel - Label for the extra dimension
				(should the variable have an extra
				dimension).  Ignored in the case of a
				2D variable.  Should be a
				comma-delimited list co-indexed to
				inFieldNames
			extraDimSizes - The size of the extra
				dimensions (should the variable have
				an extra dimension).  For 2D
				variables, must be set to 0. (zero)
				Should be a comma-delimited list
				co-indexed to inFieldNames.
			timeComparison - Must be set to either "local"
				or "UTC".  Determines how the file
				timestamps are compared to the
				start/stop time.  If set to "local",
				then the file timestamps are converted
				to local time on a pixel-by-pixel
				basis (using longitude to estimate
				time zone) before being compared to
				time boundaries.  If set to "UTC" the
				file timestamps (which are assumed to
				be in UTC) are compared against the
				start/stop time directly.
			timeStart - The earliest time for which data
				should be recorded into the output
				file.  All times in input files before
				this time will be filtered out. Must 
				be in the format:
				    hh:mm:ss_MM-DD-YYYY
			timeStop - The latest time for which data
				should be recorded into the output
				files.  All times in input files 
				after this time will be filtered out.  
				Must be in the format:
				    hh:mm:ss_MM-DD-YYYY
			cloudFractUpperCutoff - The maximum cloud
				fraction to allow before excluding
				pixel from average.  Suggested value
				from NASA is 0.3
			solarZenAngUpperCutoff - The maximum solar
				zenith angle to allow before excluding
				pixel from average.  Suggested value
				from NASA is 85.  Must be in degrees.
			pixIndXtrackAxis - The dimension order (0
				based) of the "cross-track" dimension
				(whichever dimension has size 60).
				For all currently known cases set 
				equal to 1 (depends on the 
				construction of the parser function.  
				If you rewrite the parser, check 
				this).
			fillVal - The value to use as a fill value in
				the output netCDF file.  This value
				will replace any missing or invalid
				output values.
			
		OMNO2e_wght_avg -
			toAvg - The name of the field to be averaged
			overallQualFlag - The name of the field
				containing the overall quality flag
				for the pixels.  Flag should be true (1)
				for invalid pixels and false (0) for
				valid pixels.
				{ OMI KNMI - TroposphericColumnFlag
				  OMI NASA - vcdQualityFlags }
			cloudFrac - The name of the field containing
				the cloud fraction.
				{ OMI KNMI - CloudFraction
				  OMI NASA - CloudFraction }
			solarZenithAngle - The name of the field
				containing the solar zenith angles.
				{ OMI KNMI - SolarZenithAngle
				  OMI NASA - SolarZenithAngle }
			cloudFractUpperCutoff - The maximum cloud
				fraction to allow before excluding
				pixel from average.  Suggested value
				from NASA is 0.3
			solarZenAngUpperCutoff - The maximum solar
				zenith angle to allow before excluding
				pixel from average.  Suggested value
				from NASA is 85.  Must be in degrees.
			pixIndXtrackAxis - The dimension order (0
				based) of the "cross-track" dimension
				(whichever dimension has size 60).
				For all currently known cases should
				be 1 (may change in future versions of
				OMI products).
			fillVal - The value to use as a fill value in
				the output netCDF file.  This value
				will replace any missing or invalid
				output values.
			
		unweighted_filtered_MOPITT_avg_netCDF -
			time - The name of the field containing
				timestamps.  Timestamps are assumed to
				be in the TAI-93 format.
				{ MOPITT - Time }
			longitude - The name of the field containing
				the longitudes at cell centers.
				Longitudes should be in degrees east.
				{ MOPITT - Longitude }
			inFieldNames - The names of the fields desired
				to be output.  Input as comma
				delimited list.
			outFieldNames - The names of the output
				variables (even if they are to be the
				same as input variables).  Should be a
				comma-delimited list co-indexed to
				inFieldNames
			outUnits - The units of the variables to be
				written out.  Should be a
				comma-delimited list co-indexed to
				inFieldNames
			logNormal - List of boolean strings that
				specify how to take the averages of
				the corresponding fields.  If the
				string is "True" that field is
				averaged assuming a lognormal
				distribution.  If the string is
				"False" that field is averaged
				assuming a normal distribution.
				Official documentation (linked above)
				has further information on when
				log-average is appropriate.  Should be
				a comma-delimited list co-indexed to
				inFieldNames
			dimLabels - List of names of the extra
				dimensions in the output file.  Must
				be a semicolon-delimited list of
				comma-delimited lists of labels.  
				Fields with no extra dimensions may
				be left blank.  For example, if
				there are four inFields, the first
				and third of which have no extra
				dimensions, the second of which has
				one ("foo"), and the fourth has two
				("foo" and "bar"), the dimLabels
				entry should look like this:
				    ;foo;;foo,bar
				The outer (semicolon-delimited) list
				must be	co-indexed to inFieldNames.
			dimSizes - List of the sizes of the extra
				dimensions in the output file.  Must
				be a semicolon-delimited list of
				comma-delimited lists of integers.
				Fields with no extra dimensions may
				be left blank.  For example, if there
				are four inFields, the first and
				third of which have no extra
				dimensions, the second of which has
				one (which has length 4), and the
				fourth has two (which have lengths 
				four and five, respectively), the
				dimSizes entry should look like this:
				    ;4;;4,5
				The outer (semicolon-delimited list
				must be co-indexed to inFieldNames 
				and each inner (comma-delimited) list 
				should be the same size as the 
				corresponding sublist in dimLabels.
			timeStart - The earliest time for which data
				should be recorded into the output
				file.  All times before this time in
				the input file(s) will be filtered 
				out.  Must be in the format:
				    hh:mm:ss_MM-DD-YYYY
			timeStop - The latest time for which data
				should be recorded into the output
				file.  All times after this time in
				the input file(s) will be filtered
				out.  Must be in the format:
				    hh:mm:ss_MM-DD-YYYY
			timeComparison - Must be set to either "local"
				or "UTC".  Determines how the file
				timestamps are compared to the
				start/stop time.  If set to "local",
				then the file timestamps are converted
				to local time on a pixel-by-pixel
				basis (using longitude to estimate
				time zone) before being compared to
				time boundaries.  If set to "UTC" the
				file timestamps (which are assumed to
				be in UTC) are compared against the
				start/stop time directly.
			fillVal - The value to use as a fill value in
				the output netCDF file.  This value
				will replace any missing or invalid
				output values.
			solZenAngCutoff - The solar zenith angle that
				defines the day to night transition
				(we use the SZA to separate day and
				night pixels, which should not be
				averaged together).  The geometric
				value here would be 90.  Recommended 
				value is 85. In degrees.
			solZenAng - The name of the field containing
				the solar zenith angle (in degrees).
				{ MOPITT - Solar Zenith Angle }
			dayTime - Boolean variable that indicates
				whether the output file should contain
				values from day or night.  If set to
				"True" the output file will have
				daylight values.  If set to "False"
				the output file will have night
				values.
			surfTypeField - The name of the field
				containing the surface type index.
				{ MOPITT - Surface Index }
			colMeasField - The name of the field
				containing the column measurement that
				will be used to determine how many
				valid layers are present in the cell.
				This field must be 4 dimensional, with
				the first extra dimension being the
				level and the first element of the
				second extra dimension containing
				NaN's at the appropriate levels.
				{ MOPITT - Retrieved CO Mixing Ratio Profile }

  --outDirectory /path/to/output/directory
  	REQUIRED: YES
	DEFAULT: N/A
	- The output directory to which the output file(s) should be
	  written.  Make sure that you have write permissions to this
	  directory (the program will complain and quit out if you do
  	  not).

  --outFileName FileName
  	REQUIRED: NO
	DEFAULT: output1
	- The name of the output file itself.  User is responsible for
	  adding any file extensions here (IE .nc if it's a netCDF,
	  .txt if it's an ASCII).  Output will be written in
	  outDirectory under this name.

  --includeGrid GridFileName
        REQUIRED: NO
        DEFAULT: N/A
        - Supply this flag along with the name of a file (in the output directory)
          to which to write out the latitudes and longitudes of the gridcells
          defined by the selected projection.

  --verbose {True,False}
  	REQUIRED: NO
	DEFAULT: True
	- Determines how much command-line output the software
	  provides while running.  The default behavior (--verbose
	  True) provide command line updates for most major
	  subprocesses inside the software.  Setting "False" here will
	  cause the software to be completely silent while running.

  --interactive {True,False}
  	REQUIRED: NO
	DEFAULT: False
	- Determines how the program will handle invalid/nonexistent
	  files.  Under the default behavior (--interactive False)
	  the software will automatically ignore any file it can't
	  process and continue processing any other files in
	  --fileList.  If set to True, exectuion will be suspended and
	  the user will be given several options when an invalid file
	  is encountered.

  --AttributeHelp ProjectionName/OutputFunctionName/FileType [...]
  	REQUIRED: NO
	DEFAULT: N/A
	- Prints a message explaining the required attributes for a
	  given output function or projection and then exits the
	  program.
	- Inputting a filetype outputs the required attributes for
	  the default output function associated with that filetype.

  --inFromFile FileName
  	REQUIRED: NO
	DEFAULT: N/A
	- Optionally, instead of parsing the command line for input,
	  WHIPS can read in an input file which specifies the desired
	  parameters.

The remainder of this readme will cover the format of this parameter input file.
The input file should be an ascii text file containing a 'BEGIN' statement,
followed by a list of assignment statements ('PARAM = value') for each of 
the desired parameters, separated by newlines.  Sample input file templates 
will be released on the SAGE website at a later date.  Comments (which will 
be ignored by the parser) are indicated by a period at the start of the line.  
Each output function attribute and each projection attribute should be given 
its own assignment statement, separated from the others by newlines.  Anything
before BEGIN or after END will be ignored, as will quotation mark characters ".

By way of example, the two sample WHIPS commands given above are expressed
here in input file form.  Either of these cases, if saved in a text file,
(e.g. "in.txt") can be run using the simple command 

    whips.py --inFromFile in.txt

1. Process MOPITT level 2 CO data, (Version 5) 
----------------------------------------------
- Processes a single file
- Uses a 36km lambert conic conformal grid centered over North
  America
- Writes out a 2D, 3D, and 4D parameter from the file

WHIPS INPUT FILE
BEGIN

DIRECTORY = /path/to/input/files/
FILETYPE = HDFmopittl2
FILELIST = MOP02T-20050106-L2V10.1.1.prov.hdf
GRIDPROJ = lcc2par

.PROJATTRS
xOrig = -2916000
yCell = 36000
refLon = -97
refLat = 40
nCols = 162
nRows = 126
stdPar2 = 45
stdPar1 = 33
xCell = 36000
earthRadius = 6370000
yOrig = -2268000

MAPFUNC = point_in_cell

.OUTFUNCATTRS
time = Time
longitude = Longitude
inFieldNames = Time,Retrieved CO Mixing Ratio Profile,Retrieved CO Surface Mixing Ratio
outFieldNames = time,COprof,COsurf
outUnits = TAI93,ppbv,ppbv
logNormal = False,True,True
dimLabels = ;layer,valOrStdDev;valOrStdDev
dimSizes = ;9,2;2
timeStart = 00:00:00_01-06-2005
timeStop = 23:59:59_01-06-2005
timeComparison = UTC
fillVal = -9999.0
solZenAngCutoff = 85
solZenAng = Solar Zenith Angle
dayTime = True
surfTypeField = Surface Index
colMeasField = Retrieved CO Mixing Ratio Profile

OUTDIRECTORY = /path/to/output/directory/
OUTFILENAME = MOPITT_v5_20050106_daytime_CONUS36km_test.nc
VERBOSE = True
INTERACTIVE = True

END
			

2. Process OMI level 2 DOMINO NO2 data, (Version 2) 
---------------------------------------------------

- Processes any number of files
- Uses a 36km lambert conic conformal grid centered over North
  America
- Writes out a 2D, and 3D parameter from the file

WHIPS INPUT FILE
BEGIN

DIRECTORY = /where/you/keep/the/files/
FILETYPE = HDFknmiomil2 \
FILELIST = OMI-Aura_L2-OMDOMINO_2006m0701t0023-o10423_v003-2010m1008t224420.he5 OMI-Aura_L2-OMDOMINO_2006m0701t0112-o10424_v003-20120m1008t224845.he5
GRIDPROJ = lcc2par

.PROJATTRS
xOrig = -2916000
yCell = 36000
refLon = -97
refLat = 40
nCols = 162
nRows = 126
stdPar2 = 45
stdPar1 = 33
xCell = 36000
earthRadius = 6370000
yOrig = -2268000

MAPFUNC = regional_intersect

.OUTFUNCATTRS
overallQualFlag = TroposphericColumnFlag
cloudFrac = CloudFraction
solarZenithAngle = SolarZenithAngle
time = Time
longitude = Longitude
inFieldNames = Time,AveragingKernel,TroposphericVerticalColumn
outFieldNames = time,avKern,tropVCD
outUnits = TAI93,unitless x 1000,molec/cm^2x1^-15
extraDimLabel = none,Layers,none
extraDimSize = 0,34,0
timeStart = 00:00:00_07-01-2006
timeStop = 23:59:59_07-01-2006
timeComparison = UTC
fillVal = -9999
cloudFractUpperCutoff = 0.3
solarZenAngUpperCutoff = 85
pixIndXtrackAxis = 1

OUTDIRECTORY = /where/you/want/output
OUTFILENAME = OMI_DOMINO_20060701_test.nc
INCLUDEGRID = OMI_DOMINO_GridFileName.nc
VERBOSE = True
INTERACTIVE = True

END
										
			
