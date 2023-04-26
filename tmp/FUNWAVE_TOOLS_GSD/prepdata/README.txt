# README #
POC: Gabriela Salgado-Dominguez
email: gabriela.salgado-dominguez@erdc.dren.mil


PrepdataLib Toolset contains functions capable of preparing data and simplifying
FUNWAVE post-processing steps.

----------

superSample function:Remove aliasing (jagged and edges) from time series

INPUT:
y1: the 1D cross-shore time series vector [1d array]
mult: the supersampling multiplier [number]

OUTPUT:
y2: the resulting supersampled cross-shore time series vector, with length
mult * len(y1)

So for example y1 would be the surface water elevation at a single cross-shore
profile, and we want to do 10x supersampling. So mult = 10 and y2 would be the
supersampled timeseries, which would have length multi *len(y1).

-----------

lineBestFile function: Provide line of best fit gradient, m, and y intercept, b

INPUT:
x: vector in x direction [1D array]
y: vector in y direction [1D array]  

OUTPUT:
m: fit gradient 
b: y intercep

-----------

loadBathy function: Upload output depth 

INPUT:
outputDir: path to output directory [string]
mglob: Global dimension in x direction or number of columns in bathy matrix [int]
nglob: Global dimension in y direction or number of rows in bathy matrix [int]
dx: Spacing (m) in x direction [float]
dy: Spacing (m) in y direction [float]
            
OUTPUT:
Depth: Bathymetry matrix (m) [2D array]
x: x vector with local coordinates [1D array]
y: y vector with local coordinates [1D array]

----------

loadStationIdxsFile function: This function loads the forcing file with the
simulation's station indexes.

INPUT:
stationDir: path to forcing file with station indexes [string]

OUTPUT:
indI = station's i indexes [1D array]
indJ = station's j indexes [1D array]

----------

CheckStationDuplicate function: Find the percent of duplicate stations 

INPUT:
stationDir: path to forcing file with station indexes [string]

OUTPUT:
indI: station i indexes without duplicates [int]
indJ: station j indexes without duplicates [int]
nCS: number of station cross-shore profiles [int]
crossShoreProfilesIdxs: list of station indexes per profile [list]

----------

getEquispaceProfile function: Get an equispaced cross-shore station profile 

INPUT:
x: vector in x direction [1D array]
y: vector in y direction [1D array]
m: fit gradient 
b: y intercept
ds: desired equispaced spacing between stations 
        
OUTPUT:
xi: vector in x direction with ds spacing between stations [1D array]
yi: vector in y direction with ds spacing between stations [1D array]

----------

loadStationData function: This function uploads the station's eta, u and v
time series and returns a dictionary.

INPUT:
outputDir: path to simulation's output directory containing the station
files [string]

OUTPUT:
data: dictionary containing the keys:
    't': station time vector in seconds [1D array]
    'eta': station surface water elevation time series in merters [1D array]
    'u': station velocity in x direction time series in meters/second [1D array]
    'v': station velocity in y direction time series in meters/second [1D array]

----------

CompRunup function: Compute Runup from station cross-shore profile surface
water elevation time series

NOTE: Minimum runup depth as suggested by Salmon 2002 is estimated as
h0 = 4 * max(dh)

INPUT:
eta_original: Water surface elevation time series [m] [1D in cross-shore]
h_original: Bathymetry [m] (positive down)  [cross-shore bathy]
x_original: x coordinates of h [m]          [cross-shore position]
Rdir: direction of wave in profile ('right' or 'left') [string]
r_depth: Runup depth [m] (optional)

OUTPUT:
runup: Water surface elevation time series relative to SWL given a contour
depth [m]
x_runup: Across-shore location of runup time series [m]
r_depth: Contour depth that was tracked

----------

CompR2 function: Compute R2%, setup and peaks from station cross-shore
profile runup time series

INPUT:
R: matrix with cross-shore profile time series of wave runup [m] [matrix]
t: time vector [1d array]

OUTPUT:
R2: maximum 2% runup at the cross-shore profile [1d array]
setup: mean runup [1D array]
peaks: maximum peaks of runup time series [1d array]
