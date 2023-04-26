import numpy as np
import os
import argparse
import matplotlib.pyplot as plt
import pickle
import matplotlib.colors as colors
from matplotlib import cm
from scipy.signal import find_peaks


def superSample(y1, mult):
        """remove aliasing (jagged and edges) from time series

        INPUT:
        y1: the 1D cross-shore time series vector [1d array]
        mult: the supersampling multiplier [number]

        OUTPUT:
        y2: the resulting supersampled cross-shore time series vector,
        with length mult * len(y1)

        So for example y1 would be the surface water elevation at a single cross-shore
        profile, and we want to do 10x supersampling. So mult = 10 and y2
        would be the supersampled timeseries, which would have length multi *
        len(y1).

        """

        sz1 = len(y1)
        x1 = np.arange(sz1)
        x2 = np.linspace(0, sz1 - 1, (sz1 - 1) * mult + 1)
        y2 = np.interp(x2, x1, y1)
        return y2

def lineBestFile(x, y):
        """provide line of best fit gradient, m, and y intercept, b
        
        INPUT:
        x: vector in x direction [1D array]
        y: vector in y direction [1D array]
        
        OUTPUT:
        m: fit gradient 
        b: y intercep
        
        """
        A = np.column_stack( [x , np.ones(len(y))])

        AtA = np.matmul( A.T , A)

        Aty = np.matmul( A.T , y)

        m, b = np.linalg.solve(AtA, Aty)


        return m , b


def getInterpolatingInfo(x, y, xi, yi):
        """ produce dictionary with interpolating info
        
        INPUT:
        x: original x coordinates of stations per cross-shore profile [1d array]
        y: original y coordinates of stations per cross-shore profile [1d array]
        xi: equispaced x coordinates of stations per cross-shore profile [1d array]
        yi: equispaced y coordinates of stations per cross-shore profile [1d array]
        
        OUTPUT:
        interpolatingInfo: dictionary containing the keys:
            idxs:
            coeff:
        
        
        """
        
        interpolatingInfo = []

        for x0, y0 in zip(xi,yi):

            dx = x - x0
            dy = y - y0
            ds = np.sqrt(dx**2 + dy**2)

            # Getting closest 3 points
            idxs = np.argsort( ds )[0:3]

            # Computing interpolation coefficents 
            A = np.stack([ np.ones(3) , dx[idxs] , dy[idxs] ])
            b = np.zeros(3); b[0] = 1

            try:
                coeff = np.linalg.solve(A, b)

            except np.linalg.LinAlgError:
                # If interpolation fails for 3 points, reducing to 2 points
                idxs = idxs[0:2]
                if np.abs(dx[idxs[1]]) > np.abs(dy[idxs[1]]):
                    A = np.stack([ np.ones(2) , dx[idxs] ])
                else:
                    A = np.stack([ np.ones(2) , dy[idxs] ])

                b = np.zeros(2); b[0] = 1

                try:
                    coeff = np.linalg.solve(A, b)
                except np.linalg.LinAlgError:

                    # If interplation fails for 2 points, just using closes point
                    idxs = idxs[0]
                    coeff = 1

            interpolatingInfo.append( {'idxs': idxs , 'coeff': coeff}  )

        return interpolatingInfo

def interpolate(data, interpolatingInfo):
        """ interpolate data""" 
        n = len(interpolatingInfo)
        dataI = np.zeros(n)

        for i in range(n):
            dataI[i] = np.dot(interpolatingInfo[i]['coeff'],data[interpolatingInfo[i]['idxs']])

        return dataI

def loadBathy(outputDir, mglob, nglob, dx, dy):  
            """ upload output depth 
            
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
            
            
            """
            depthFile = os.path.join(outputDir, 'dep.out')
            if os.path.exists(depthFile)==True:
                try: # try ascii
                    Depth = np.loadtxt(depthFile)
                except(UnicodeDecodeError): # try binary
                    fin = open(depthFile, mode='rb')
                    dataType = np.dtype('<f8')
                    Depth = np.fromfile(fin, dtype=dataType).reshape(nglob, mglob)
            Lx = mglob*dx
            Ly = nglob*dy
            x = np.arange(0,Lx,dx)
            y = np.arange(0,Ly,dy)

            return Depth,x,y

def loadStationIdxsFile(stationFileDir):
        """This function loads the forcing file with the simulation's station indexes.
        
        INPUT:
        stationDir: path to forcing file with station indexes [string]

        OUTPUT:
        indI = station's i indexes [1D array]
        indJ = station's j indexes [1D array]
        
       
        """
        staLocs = np.loadtxt( stationFileDir ).astype('int') - 1
        indI = staLocs[:,0]
        indJ = staLocs[:,1]
        
        return indI, indJ
    
def CheckStationDuplicate(stationDir): 
        """find the percent of duplicate stations

        INPUT:
        stationDir: path to forcing file with station indexes [string]

        OUTPUT:
        indI: station i indexes without duplicates [int]
        indJ: station j indexes without duplicates [int]
        nCS: number of station cross-shore profiles [int]
        crossShoreProfilesIdxs: list of station indexes per profile [list]

        """
        
        
        indI, indJ = loadStationIdxsFile(stationDir)
        staNums = np.arange(1,len(indI)+1)

        di = np.sqrt(np.diff(indI)**2 + np.diff(indJ)**2)
        idxs = list([True])
        idxs.extend( di > 0 )

        nB = len(indI)
        indI = indI[idxs]
        indJ = indJ[idxs]
        staNums = staNums[idxs]
        nA = len(indI)

        di = np.sqrt(np.diff(indI)**2 + np.diff(indJ)**2)
        meanDi = np.mean(di)

        idxs = list([True])
        idxs.extend( di > 22*meanDi )

        crossShoreIdxBounds = np.arange(0,len(indI))[idxs]
        crossShoreIdxBounds = np.insert( crossShoreIdxBounds , len(crossShoreIdxBounds) , len(indI)-1 )
        indI = indI[idxs]
        indJ = indJ[idxs]

        nCS = len(crossShoreIdxBounds)-1

        print( "%d duplicate stations found (%2.1f %%) " % (nB-nA , 100*(nB-nA)/nB ) )
        print( "%d cross-shore profiles found\n" % (nCS ) )

        # Extracting station numbers for each profile
        crossShoreProfilesIdxs = []
        for i in range(nCS):
            indItart = crossShoreIdxBounds[i]
            iEnd   = crossShoreIdxBounds[i+1]
            crossShoreProfilesIdxs.append(staNums[indItart:iEnd])
        
        return indI, indJ, nCS, crossShoreProfilesIdxs
    
def getEquispaceProfile(x, y, m, b, ds):
        """get an equispaced cross-shore station profile 
        
        INPUT:
        x: vector in x direction [1D array]
        y: vector in y direction [1D array]
        m: fit gradient 
        b: y intercept
        ds: desired spacing between stations
        
        OUTPUT:
        xi: vector in x direction with ds spacing between stations [1D array]
        yi: vector in y direction with ds spacing between stations [1D array]
        
        
        """
        dx = ds/ np.sqrt( 1 + m**2 )

        xMax = x.max()
        xMin = x.min()
        xL = xMax - xMin

        n = int(xL/dx)

        xLExtra = xL - n*dx
        xOffset = xLExtra/2

        xi = np.arange( xMin + xOffset , xMax , dx )

        yi = m*xi + b    

        return xi, yi

def loadStationData(outputDir, stationNumber):
        """ This function uploads the station's eta, u and v time series and returns a dictionary
        
        INPUT:
        outputDir: path to simulation's output directory containing the station files [string]
        
        OUTPUT:
        data: dictionary containing the keys:
            't': station time vector in seconds [1D array]
            'eta': station surface water elevation time series in merters [1D array]
            'u': station velocity in x direction time series in meters/second [1D array]
            'v': station velocity in y direction time series in meters/second [1D array]
        
        
        """
        
        stationFileName = 'sta_%04d' % stationNumber
        stationFileDir = os.path.join( outputDir ,stationFileName )

        rawData = np.loadtxt(stationFileDir)

        data = {}
        data['t'] = rawData[:,0]
        data['eta'] = rawData[:,1]
        data['u'] = rawData[:,2]
        data['v'] = rawData[:,3]

        return data

def CompRunup(eta_original,h_original,x_original,Rdir,r_depth=None):
        """Compute Runup from station cross-shore profile surface water elevation time series

        INPUT:
        eta_original: Water surface elevation time series [m] [1D in cross-shore]
        h_original: Bathymetry [m] (positive down)  [cross-shore bathy]
        x_original: x coordinates of h [m]          [cross-shore position]
        Rdir: direction of wave in profile ('right' or 'left') [string]
        r_depth: Runup depth [m] (optional)

        OUTPUT:
        runup: Water surface elevation time series relative to SWL given a contour depth [m]
        x_runup: Across-shore location of runup time series [m]
        r_depth: Contour depth that was tracked

        Notes:
        ------
        - Really meant for 1D simulations.
        - Minimum runup depth as suggested by Salmon 2002 is estimated as
          h0 = 4 * max(dh)

        """
        # super sample the time series by 10
        x = superSample(x_original, 10)
        h = superSample(h_original, 10)
        eta = superSample(eta_original, 10)

        # Find the maximum runup depth
        if r_depth is None:
             runupInd = h < 1.0
             r_depth = 4.0*np.nanmax(np.abs(h[runupInd][1:] - h[runupInd][:-1])) 

        # Preallocate runup variable
        runup = np.zeros(eta.shape[0])
        x_runup = np.zeros_like(runup)

        # Water depth
        wdepth = eta + h
        
        
        if Rdir == 'right':
        # Find the runup contour (search from right to left) 
            wdepth_ind = np.argmax(wdepth>=r_depth)

        elif Rdir == 'left':
        # Find the runup contour (search from left to right) 
            wdepth_ind = np.argmin(wdepth>=r_depth)
        
        
        # Store the water surface elevation in matrix
        runup = eta[wdepth_ind] # unrealistic values for large r_depth
        # runup[aa]= -h[wdepth_ind]

        # Store runup position
        x_runup = x[wdepth_ind] 

        return runup, x_runup, r_depth

def CompR2(R, t):
        """Compute R2%, setup and peaks from station cross-shore profile runup time series

        INPUT:
        R: matrix with cross-shore profile time series of wave runup [m] [matrix]
        t: time vector [1d array]
        
        OUTPUT:
        R2: maximum 2% runup at the cross-shore profile [1d array]
        setup: mean runup [1D array]
        peaks: maximum peaks of runup time series [1d array]
        
        Notes:
        ------
        - Really meant for 1D simulations.
    

        """
        
        peaks, _ = find_peaks(R, width=2)    
        R2 = np.percentile(np.array(R)[peaks], 98)
        Setup = np.mean(R)  

        return R2, peaks, Setup