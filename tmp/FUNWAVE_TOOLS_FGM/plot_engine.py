# -------------------- IMPORT LIBRARIES ---------------
# Import System Libraries
from importlib.resources import path
from os import listdir as ls
from sys import exit as emess
from os import path as pth
import pathlib
import json
# Import Data Libraries
import numpy as np
import pandas as pd
# Import Parsing Libraries
import argparse
import re
# Import ColorMaps 
import cmocean
# Import Plotly Libraries
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#--------------------- COMMENTS -------------------------

# Supported Files:
# 1D Files:
# 1. Station Files (4 Cols -> [time, eta, u, v]) -> sta_####
# 2D Files: 
# 1. Simulation Bathy (from inputs) -> Topo
# 2. Eta_##### -> Water Surface Elevation -> ice
# 3. Mask_##### -> Wet/Dry ?


# * -> Need to discuss if usefull or not with Matt/Michael 
# Sponge Layer Plots 

# 1D Plot -> Station Files 
# Want To Make It So User Can Do The Following:
# Change Stations On The Fly With A Dropdown Menu
# Visualize Eta, U & V (Subplot: 3 Rows 1 Col)?


# 2D Plot 
# Want To Make It So User Can:
# Animate Surface Plot (loop Through Frames)
# Skip To A Specific Frame 
# Change Variable (Bathy,Depth, Mask, eta)

#--------------------- DEFINE CLASS -------------------------
class plot_engine:
    def __init__(self,args):
        self.plotType = args.plot_type
        self.pData = str(pathlib.Path(args.pData[0]))
        self.outPath = str(pathlib.Path(args.outPath[0]))
        if args.plot_type == '2D':
            # Grid Size 
            self.dSize = args.dSize
            # Determine If Its A single Frame Case 
            if pth.isdir(self.pData) and args.isBathy=='True': # If pData is directory then isBathy should be False
                # Correct isBathy If Necessary
                self.isBathy = False 
            elif pth.isfile(self.pData): # If pData Is File Need To Verify If Its Bathy Or Other 
                #  Check Input File Extension 
                fileExt = pathlib.Path(self.pData).suffix # Bathy File -> .txt , This Needs to be Refined , Probably Reading From Input.txt
                # Correct If Necessary 
                if fileExt=='' and args.isBathy=='True': # If File Extension Is '' & isBathy == True -> Wrong Combination
                    # Correct isBathy Flag 
                    self.isBathy = True
                else:
                    if args.isBathy == 'True':
                        self.isBathy = True
                    else:
                        self.isBathy = False
            elif pth.isdir(self.pData) is False and  pth.isfile(self.pData) is False:
                emess('Error: Requested 2D file does not exist.')

    # CMOCEAN AUX FUNCTION 
    # Cmocean to Plotly Translator
    def cmocean_to_plotly(self,cmap, pl_entries):
        h = 1.0/(pl_entries-1)
        pl_colorscale = []
        for k in range(pl_entries):
            C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
            pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])
        return pl_colorscale

    # 1D PLOT FUNWAVE STATIONS
    def plot_1D(self):
        # ---=-- NOTES ------
        # Things to add:
        #   Some indicator for "Ramp-up" time or Remove it from data
        #   Option to read input.txt (optional input)?
        # Need line that checks if pData exist
        # ------ DOC -------
        # pData -> Relative path to FUNWAVE output directory
        # ------ 1-D DATA HANDLER -------
        # Grab Inputs 
        pData = self.pData
        # Define Regular Expression 
        rExp = re.compile("^sta_")
        # Scan Directory And Search For 1D Files (Stations)
        filesList = ls(pData)
        # Filter Out Non-1D files 
        filesList = sorted(list(filter(rExp.match, filesList)))
        # Handle Empty Directory Case 
        if filesList is None:
            emess('Error: No 1-D files found in '+pData+'.')
        # Build Relative Paths To Station Files 
        pData = [pth.join(pData,s) for s in filesList]
        # Read Initial Station Data 
        station_df = []
        for ii in pData:
            station_df.append(pd.DataFrame(np.loadtxt(ii),columns=["time","eta","u","v"]))
        # ------ FIGURE CREATION -------
        # Initialize Plotly Graphical Object 
        fig = make_subplots(rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.02)
        # Add Title & Labels To Figure 
        fig.update_layout(
           title={'text': "FUNWAVE Simulation Station Data",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            font=dict(
                family="Arial",
                size=18)
        )
        # Update Y Axes Labels
        fig.update_yaxes(title_text="Eta [m]", row=1, col=1)
        fig.update_yaxes(title_text="Hor. Velocity [m/s]", row=2, col=1)
        fig.update_yaxes(title_text="Vert. Velocity [m/s]", row=3, col=1)
        # Update X Axes Labels
        fig.update_xaxes(title_text="Time [s]", row=3, col=1)
        # ------ POPULATE TRACES -------
        for df in station_df:
            # Define Trace 1: Eta [m]
            trace1 = go.Scatter(
                x=df["time"], y=df["eta"],
                mode='lines',
                name='Eta',
                line=dict(width=2)
                )
            # Append Trace To Figure 
            fig.append_trace(trace1,1,1)
            # Define Trace 2: U [m/s]
            trace2 = go.Scatter(
                x=df["time"], y=df["u"],
                mode='lines',
                name='U',
                line=dict(width=2)
                )
            # Append Trace To Figure 
            fig.append_trace(trace2,2,1)
            # Define Trace 3: V [m/s]
            trace3 = go.Scatter(
                x=df["time"], y=df["v"],
                mode='lines',
                name='V',
                line=dict(width=2)
                ) 
            # Append Trace To Figure 
            fig.append_trace(trace3,3,1)
        # ------ HIDE ADDITIONAL TRACES ------
        # Determine Number Of Traces  
        nTraces = len(fig.data)
        # Determine Number Of Unique Entries 
        nEntries = len(filesList)
        # Make All Traces Except Initial Invisible 
        for k in range(3, nTraces):
            fig.update_traces(visible=False, selector = k)
        # ------ DROPDOWN MENUS ------
        # Initialize Tuple
        Gbuttons = ()
        for k, stationID in enumerate(filesList):
            # Create Visibility Matrix 
            visibility= [False]*3*nEntries
            # Enable Traces That Belong To Entry 
            for tr in range(k*3,k*3+3):
                # Make Them Visisble
                visibility[tr] = True 
            # Build UI Buttons Per Entry (Tuple) 
            helperVar = (dict(label = stationID,
                        method = 'restyle',
                        args = [{'visible': visibility,
                                'title': stationID,
                                'showlegend': True}]),)
            # Append Tuple
            Gbuttons = Gbuttons+helperVar
        # ------ UDATE & SHOW FIGURE ------ 
        # Update Layout
        fig.update_layout(
            updatemenus=[go.layout.Updatemenu(
            active = 0,
            buttons = Gbuttons
            )])
        # ------ PRINT FIGURE -------
        fig.write_html(str(pathlib.Path(self.outPath))+'_1D_Stations.html')
    # 2D PLOT SINGLE FRAME FUNCTION
    def plot_2D(self):
        # ------ PARSE INPUTS ------
        pData = self.pData
        isBathy = self.isBathy
        # ------ ERROR HANDLELING  ------
        # Make Sure File Exist 
        if isinstance(pData,str) is True:
            if pth.exists(pData) is False:
                emess('Error: ' + pData + ' was not found. Make sure path & file name is correct.')
        else:
            emess('Error: pData must be a string.')
        # ------ READ DATA ------
        # Create Data Frame 
        if isinstance(isBathy,bool) is False:
            emess('Error: isBathy has to be logical value (True or False).')
        elif isBathy is False:
            surface_array = np.loadtxt(pData)
        else:
            surface_array = np.loadtxt(pData)*-1
            
        # ------ FIGURE CREATION ------
        # Initialize Figure 
        fig = go.Figure()
        # Update 3D scene options 
        fig.update_scenes(
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode="manual"
        )
        # ------ COLOR MAPS ------
        # Define Cmocean Colormaps To Use
        cMapList = ['topo','thermal','haline','solar','ice','gray','oxy','deep','dense','algae','matter','turbid','speed','amp','tempo','rain','phase','balance','delta','curl','diff','tarn']
        # Initialize Tuple
        Gbuttons = ()
        # There is A Cleaner Way To Do This Using The Update Method F.G.M
        for cms in cMapList:
            # Convert cmocean to Plotly Colormap
            cMap = eval("json.dumps(pe.cmocean_to_plotly(cmocean.cm."+cms+", 256))")
            # Build UI Buttons Per Entry (Tuple) 
            helperVar = (dict(
                args=["colorscale", cMap],
                label= cms,
                method="restyle"),)
            # Append Tuple
            Gbuttons = Gbuttons+helperVar
        # ------ ADD TRACES ------
        # Add 3-D Surface Trace
        fig.add_trace(go.Surface(z=surface_array, colorscale=pe.cmocean_to_plotly(cmocean.cm.topo, 256)))
        # Update Surface Trace Properties
        fig.update_traces(contours_z=dict(show=True, usecolormap=True,
            highlightcolor="limegreen"))
        #------ DROPDOWN MENUS ------
        # Define First Dropdown Menu Y Coord
        button_layer_1_height = 1.08
        # Color Map Dropdown X Location
        button1_x_loc = 0.1
        # Trace Type Dropdown X Location
        button2_x_loc = 0.35
        # Color Map Invert Dropdown X Location
        button3_x_loc = 0.65
        # Add Dropdowns 
        fig.update_layout(
            updatemenus=[
                dict(  # Colormaps Dropdown 
                    buttons=Gbuttons,
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=button1_x_loc,
                    xanchor="left",
                    y=button_layer_1_height,
                    yanchor="top"
                ),
                dict( # Plot Type Drop down
                buttons=list([
                    dict(
                            args=["type", "surface"],
                            label="3D Surface",
                            method="restyle"
                        ),
                        dict(
                            args=[{"contours.showlines": True,"type": "contour"}],
                            label="Contour",
                            method="restyle"
                        ),
                        dict(
                            args=[{"type": "heatmap"}],
                            label="Heat Map",
                            method="restyle"
                        )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=button2_x_loc,
                xanchor="left",
                y=button_layer_1_height,
                yanchor="top"   
                ),
                dict(   # Reverse Color Scale Dropdown 
                    buttons=list([
                        dict(
                            args=["reversescale", False],
                            label="False",
                            method="restyle"
                        ),
                        dict(
                            args=["reversescale", True],
                            label="True",
                            method="restyle"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=button3_x_loc,
                    xanchor="left",
                    y=button_layer_1_height,
                    yanchor="top"
                )
            ]
        )
        # ------ ANNOTATIONS -------
        # Add Annotation 
        fig.update_layout(
            annotations=[
                dict(text="<b>Colorscale</b>", x=button1_x_loc-0.08, xref="paper", y=button_layer_1_height-0.013, yref="paper",
                                    align="left", showarrow=False),
                dict(text="<b>Trace<br>Type</b>", x=button2_x_loc-0.05, xref="paper", y=button_layer_1_height-0.01,
                                    yref="paper", showarrow=False),
                dict(text="<b>Reverse<br>Colorscale</b>", x=button3_x_loc-0.05, xref="paper", y=button_layer_1_height-0.01,
                                    yref="paper", showarrow=False),
            ])
        # ------ PRINT FIGURE -------
        fig.write_html(str(pathlib.Path(self.outPath))+'_2d_Surface.html')
    
    # 2D PLOT SINGLE MOVIE FUNCTION
    def plot_2D_movie(self):
        # ------ 2-D DATA HANDLER -------
        # Grab Inputs 
        pData = self.pData
        # Get File Dimentions 
        nSize = self.dSize
        # Define Regular Expression 
        rExp = re.compile("\w+_\d\d\d\d\d")
        # Scan Directory And Search For 1D Files (Stations)
        filesList = ls(pData)
        # Filter Out Non-1D files 
        filesList = sorted(list(filter(rExp.match, filesList)))
        # Initialize List
        helperVar = []
        storage_dict = []
        # Determine How Many Variables 
        for i in filesList:
            var = i.split('_',1)[0]
            if var not in helperVar:
                # Add To List 
                helperVar.append(var)
                # Define Regular Expression 
                rExp = re.compile("^"+var+"")
                # Get Var List 
                varList = sorted(list(filter(rExp.findall, filesList)))
                # Initialize Data Cube 
                dataCube = np.zeros([nSize[0],nSize[1],len(varList)])
                # Build Data Cube 
                for k,frame in enumerate(varList): 
                    # Data Cube
                    dataCube[:,:,k] = np.loadtxt(pth.join(pData,frame))
                # Store Data
                storage_dict.append({'sVar':var,'nFrames':len(varList),'Frames':dataCube})
        # ------ CREATE FIGURE ------
        

def CLI_parser():
    # Initialize Parser Object 
    parser = argparse.ArgumentParser()
    # Append Argument: "plot_type" -> 1D or 2D plots. 
    parser.add_argument('plot_type', choices=['1D','2D'], action='store', type=str, help='Plot type to create (1D or 2D).')
    # Append Argument: "pData" -> Define directory containing FUNWAVE output files 
    parser.add_argument('pData', nargs=1,action='store', type=str, help='Full file path of data to plot.')
    # Append Argument: "pData" -> Define directory containing FUNWAVE output files 
    parser.add_argument('--isBathy', choices=['True','False'],action='store', type=str, help='2D only flag. Specifies if 2D file is a topo/bathy file.')
    # Append Argument: dSize -> Define Domain Size 
    parser.add_argument('--dSize', nargs=2,action='store', type=int, help='FUNWAVE domain size Mglob,Nglob')
    # Append Argument: "pData" -> Define directory containing FUNWAVE output files 
    parser.add_argument('outPath', nargs=1,action='store', type=str, help='Output figure save name and relative path.')
    # Parse Arguments
    args = parser.parse_args()
    # Missing Item Fialsafe 
    if args.plot_type=='2D' and not args.isBathy:
        parser.error('--isBathy flag is required when calling 2D plot_type.')
    else:
        args.isBathy = 'False'
        if pth.isfile(args.pData[0]):
            parser.error('For 1D plots pData must be relative path to directory containing FUNWAVE station output files.')
    # 2D Failsafe 
    if args.plot_type=='2D' and not args.dSize:
        parser.error('--dSize flag is required when calling 2D plot_type.')
    # Empty Output Path 
    if args.outPath[0]=='':
        args.outPath = str(pathlib.Path('No_Output_Name'))
    elif pth.isdir(args.outPath[0]): # Missing Output Filename 
        args.outPath = pth.join(args.outPath[0], 'No_Output_Name')
    else:
        if pathlib.Path(args.outPath[0]).suffix != '': # If File Extension Detected, then Remove It
            # Split String
            helperVar=str.split(args.outPath,sep='.')
            # Keep First Part And Redefine 
            args.outPath=helperVar[0]

    # Return 
    return args

# If called From Command Line 
if __name__ == '__main__':
    # Parser Input Arguments 
    parsedArgs = CLI_parser()
    # Call Class 
    pe = plot_engine(parsedArgs)
    # Call Functions Conditionally 
    if pe.plotType == '2D':
        # Determine If Its A single Frame Case 
        if pth.isfile(pe.pData):
            # if PData is File Call 2D Plotter 
            pe.plot_2D()
        else:
            # plot_engine.plot_2D_movie
            pe.plot_2D_movie()
    else: # 1D Case 
        pe.plot_1D()   
else:
    emess('Not set-up for import. Call from CLI.')