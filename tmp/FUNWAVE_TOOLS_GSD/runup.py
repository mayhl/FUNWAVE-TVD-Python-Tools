import numpy as np
import os
import sys
import argparse
import matplotlib.pyplot as plt
import pickle
import matplotlib.colors as colors
from matplotlib import cm
from scipy.signal import find_peaks
from prepdata import prepdataLib as prepdata
  
class FUNWAVE_runup:
    
    def __init__(self,args):
        """ Initialize variables"""
        
        # initiate directories
        self.simDir = args.path # path to simulation folder
        self.stationDir = os.path.join(self.simDir,args.stationname) # path to station file
        self.outputDir = os.path.join(self.simDir,'output') # path to simulation's output folder
        self.plotDir = os.path.join(self.simDir,'plots') # path to plot/postprocess folder
        try: # Create plot directory if it does not exist
            os.mkdir(self.plotDir)
            print("\nDirectory " , self.plotDir ,  " Created\n") 
        except FileExistsError:
            print("\nDirectory " , self.plotDir ,  " already exists\n")
  
        self.indI, self.indJ, self.nCS, self.crossShoreProfilesIdxs = prepdata.CheckStationDuplicate(self.stationDir)  
        self.waterlevel = args.waterlevel # simulation waterlevel used in input file
        self.multipleindices = args.multipleindices # range of stations
        self.numOfStations = int(args.multipleindices[-1])-int(args.multipleindices[0]) # number of stations 
        self.dx = args.dx # Spacing (m) in x direction 
        self.dy = args.dy # Spacing (m) in y direction 
        self.mglob = args.mglob # global dimension in x direction
        self.nglob = args.nglob # global dimension in y direction
        
        if args.RunupDirection.lower() in ['left','right']:
            self.Rdir = args.RunupDirection.lower() # direction to find the runup contour 
        else:
            print("ERROR: -dir argument incorrect! Choose left or right.")
            sys.exit()
                  
    def RunupFunc(self):
        
        iS, jS = prepdata.loadStationIdxsFile(self.stationDir) 
        dep,x,y = prepdata.loadBathy(self.outputDir, self.mglob, self.nglob, self.dx, self.dy)
        ds = 2 # desired spacing between stations for interpolation

        ## Enpty Variable Lists:
        xSta = []
        ySta = []

        xStaInterp = []
        yStaInterp = []

        depSta = []
        depStaInterp = [] 

        etaSta = []
        etaStaInterp = []

        runupSta = []
        runupStaInterp = []

        xRunupSta = []
        xRunupStaInterp = []

        R2Sta = []
        R2StaInterp = []

        setupSta = []

        for i,crossShoreProfileIdxs in enumerate(self.crossShoreProfilesIdxs):
        
            idxs = crossShoreProfileIdxs - 1
            
            ## Interpolate X & Y
            # Interploting stations to a line of best fit 
            xS = x[iS[idxs]]
            yS = y[jS[idxs]]

            xSta.append(xS)
            ySta.append(yS)

            # Line of best fit gradient, m, and y intercept, c.
            m, b = prepdata.lineBestFile( xS , yS )

            xSI, ySI = prepdata.getEquispaceProfile( xS, yS , m, b, ds)
            xStaInterp.append(xSI)
            yStaInterp.append(ySI)

            interpolatingInfo = prepdata.getInterpolatingInfo( xS, yS , xSI, ySI )
            
            ## Interpolate station's depth
            depS = dep[jS[idxs],iS[idxs]]
            depSta.append(depS)

            depI = prepdata.interpolate( depS , interpolatingInfo )
            depStaInterp.append(depI)
            
            ## Interpolate station's surface elevation time series
            staEtaData = []
            for idx in idxs:
                data = prepdata.loadStationData(self.outputDir , idx + 1 )
                time = data['t']
                staEtaData.append( data['eta'] )
            staEtaData = np.array(staEtaData) 
            etaSta.append(staEtaData)
            
            ## compute runup:
            timeLen = len(time)

            ##runup stations
            runupMatrixS = np.zeros([timeLen])
            xRunupMatrixS = np.zeros([timeLen])

            ##runup interpolated stations
            runupMatrixSI = np.zeros([timeLen])
            xRunupMatrixSI = np.zeros([timeLen])

            etaSI = np.zeros([len(xSI),timeLen])
            for t in range(timeLen):      

                etaS = staEtaData[:,t]
                runupS, x_runupS, r_depth = prepdata.CompRunup(etaS,depS*-1,xS,self.Rdir,0.002)
                runupMatrixS[t] = runupS
                xRunupMatrixS[t] = x_runupS
                etaSI[:,t] = prepdata.interpolate( etaS , interpolatingInfo ) 
                runupSI, x_runupSI, r_depth = prepdata.CompRunup(etaSI[:,t],depI*-1,xSI,self.Rdir,0.002)

            etaStaInterp.append(np.array(etaSI))
            runupSta.append(runupMatrixS)
            xRunupSta.append(xRunupMatrixS)

            runupStaInterp.append(runupMatrixSI)
            xRunupStaInterp.append(xRunupMatrixSI)

            R2S, peaksS, SetupS = prepdata.CompR2(runupMatrixS,time)

            R2Sta.append(R2S)
            setupSta.append(SetupS)
            
        ## save Dictionary
        print("Saving pickle with results at: "+str(os.path.join(self.plotDir,"station_profile_timeseries.p\n")))
        dataDict = {'time':time,
                        'eta':etaSta,
                        'etaInterp':etaStaInterp,
                        'depth':dep,
                        'stationDep':depSta,
                        'stationDepInterp':depStaInterp,
                        'stationX':xSta,
                        'stationXInterp':xStaInterp,
                        'stationY':ySta,
                        'stationYInterp':yStaInterp,
                        'runupSta':runupSta,
                        'xRunupSta':xRunupSta,
                        'runupStaInterp':runupStaInterp,
                        'xRunupStaInterp':xRunupStaInterp,
                        'R2Sta':R2Sta,
                        'SetupSta':setupSta
                        }
        pickle.dump(dataDict, open(os.path.join(self.plotDir,"station_profile_timeseries.p"), "wb"))
            
        for i in range(self.nCS):
            print('Profile #%d'%(i+1))
            print("Mean Runup =",np.mean(runupSta[i]),"m")
            print("Min Runup =",min(runupSta[i]),"m and Max Runup =",max(runupSta[i]),'m')
            print("Min xRunup =",min(xRunupSta[i]),"m and Max xRunup =",max(xRunupSta[i]),'m')
            print("Min x =",min(xSta[i]),"m and Max x =",max(xSta[i]),'m')
            print("R2% =",R2Sta[i])
            print("Setup =",setupSta[i],'\n')

def parseCommandLine():
     """Parse the commend line and assign appropriate argument values - will come from HPC Portal GUI"""
     parser = argparse.ArgumentParser()
     parser.add_argument('-mi', '--multipleindices', help='specify the range of stations to plot in list format [first last]',
                         nargs=2, metavar=('firststation', 'laststation'))
     parser.add_argument('-wa', '--waterlevel', help='Waterlevel in meters for surface water elevation',
                         type=float)
     parser.add_argument('-mg', '--mglob', help='Global dimension in x direction',
                         type=int)
     parser.add_argument('-ng', '--nglob', help='Global dimension in y direction',
                         type=int)
     parser.add_argument('-dx', '--dx', help='Spacing (m) in x direction',
                         type=float)
     parser.add_argument('-dy', '--dy', help='Spacing (m) in y direction',
                         type=float)
     parser.add_argument('-p', '--path', help='full path to simulation directory where output and postprocessing directories are found', type=str)
     parser.add_argument('-s', '--stationname', help='Name of forcing file with station indeces.',
                         type=str)
     parser.add_argument('-Rdir', '--RunupDirection', help='Direction to search the runup contour (right or left).',
                         type=str)
     args = parser.parse_args()
         
     return args


## if called from the command line (not imported)
if __name__ == "__main__":
     commandLineArguments = parseCommandLine()
p1 = FUNWAVE_runup(commandLineArguments)
p1.RunupFunc()