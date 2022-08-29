# -------------------- IMPORT LIBRARIES ---------------
# Import System Libraries
from sys import exit as emess
# Import Data Libraries
import numpy as np
import pandas as pd
# Import Parsing Libraries
import re
# Import Plotly Libraries
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
#--------------------- COMMENTS -------------------------
# Collection of plotly ploting functions. Included functions:
#   1. 1D Plot: Station Files 
#       - station_subplot(eta, u, v, time, fig_title = None) -> Plots Eta, u & v vs time in a single figure for a given station.
#       - station_var_plot(yData, time, fig_title = None, yLabel = None, fig_in = None) -> Plots single variable from a given station. Also supports appending data by using fig_in.
#   2. 2D/3D Plot: Station Files      
#       - surface_plot(surface_array, is_bathy, trace_type, fig_title=None, z_scale=None) -> Plots given FUNWAVE mesh data. Supports 3 trace types: heatmap, contour, and surface3D.
#       - surface_plot_overlay(surface_array, topo_bathy, mask, x_scale=None, y_scale=None, z_scale=None, fig_title=None) -> Function for ploting FUNWAVE mesh data overlayed on topo/bathy.
#       - quiver_plot(xx, yy, u, v, mask, quiver_norm, quiver_scale, axes_ratio, fig_title=None, bottom_surface=None, bottom_trace=None, color_map=None) -> Quiver plot overlayed on given FUNWAVE mesh data.
#
def station_subplot(eta, u, v, time, fig_title = None):
    ''' Function for plotting FUNWAVE station output in a subplot axes.
  
    :param eta:         Free surface heigh data from FUNWAVE station file.
    :type  eta:         ndarray
    :param u:           X velocity data from FUNWAVE station file.
    :type  u:           ndarray
    :param v:           Y velocity data from FUNWAVE station file.
    :type  v:           ndarray
    :param time:        Time data from FUNWAVE station file.
    :type  time:        ndarray
    :param fig_title:   Figure title string.
    :type  fig_title:   str
    '''
    # ------ ARGUMENTS HANDELING ------
    if fig_title is None:
        fig_title = "FUNWAVE Station Data"
    elif isinstance(fig_title,'str') is False:
        emess('Error: Optional input argument fig_title must be a string')

    # ------ FIGURE LAYOUT -------
    # Initialize Plotly Graphical Object 
    fig = make_subplots(rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02)

    # Add Title & Labels To Figure 
    fig.update_layout(
        title={'text': fig_title,
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font=dict(
            family="Arial",
            size=18)
    )

    # Update Y Axes Labels
    fig.update_yaxes(title_text="Free Surface Height [m]", row=1, col=1)
    fig.update_yaxes(title_text="X Velocity [m/s]", row=2, col=1)
    fig.update_yaxes(title_text="Y Velocity [m/s]", row=3, col=1)

    # Update X Axes Labels
    fig.update_xaxes(title_text="Time [s]", row=3, col=1)

    # ------ POPULATE TRACES -------
    # Define Trace 1: Eta [m]
    trace1 = go.Scatter(
        x=time, y=eta,
        mode='lines',
        name='Eta',
        line=dict(width=2)
        )
    # Append Trace To Figure 
    fig.append_trace(trace1,1,1)

    # Define Trace 2: U [m/s]
    trace2 = go.Scatter(
        x=time, y=u,
        mode='lines',
        name='U',
        line=dict(width=2)
        )
    # Append Trace To Figure   
    fig.append_trace(trace2,2,1)

    # Define Trace 3: V [m/s]
    trace3 = go.Scatter(
        x=time, y=v,
        mode='lines',
        name='V',
        line=dict(width=2)
        ) 
    # Append Trace To Figure 
    fig.append_trace(trace3,3,1)

    # ------ TEMP LINE -------
    fig.show()

def station_var_plot(yData, time, fig_title = None, yLabel = None, fig_in = None):
    ''' Function for plotting FUNWAVE station output varaible.
  
    :param yData:       FUNWAVE station file variable data.
    :type  yData:       ndarray
    :param time:        Time data from FUNWAVE station file.
    :type  time:        ndarray
    :param fig_title:   Figure title string.
    :type  fig_title:   str
    :param yLabel:      Axes y label string.
    :type  yLabel:      str
    :param fig_in:       Plotly figure object. Supplying this input will cause new trace to be added to figure.
    :type  fig_in:       obj
    '''
    # ------ ARGUMENTS HANDELING ------
    if fig_title is None:
        fig_title = "FUNWAVE Station Data"
    elif isinstance(fig_title,'str') is False:
        emess('Error: Optional input argument fig_title must be a string')

    # ------ FIGURE LAYOUT -------
    if fig_in is None:
        # Initialize Figure 
        fig = go.Figure()
        # Add Title & Labels To Figure 
        fig.update_layout(
            title={'text': fig_title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            font=dict(
                family="Arial",
                size=18)
        )
        # Update Y Axes Labels
        fig.update_yaxes(title_text=yLabel)
        # Update X Axes Labels
        fig.update_xaxes(title_text="Time [s]")
    else:
        # Copy Figure Object 
        fig = fig_in

    # ------ POPULATE TRACES -------
    # Define Trace 1: Eta [m]
    trace1 = go.Scatter(
        x=time, y=yData,
        mode='lines',
        line=dict(width=2)
        )
    # Append Trace To Figure 
    fig.append_trace(trace1)

    # ------ TEMP LINE -------
    fig.show()
    return fig

def surface_plot(surface_array, is_bathy, trace_type, fig_title=None, z_scale=None): 
    '''Function for ploting 2D surface data.
  
    :param surface_array:  FUNWAVE grid data values.
    :type  surface_array:  ndarray
    :param is_bathy:       Boolean value to define if 'surface_array' is a topo/bathy. If True then 'surace_array' is inverted.
    :type  is_bathy:       bool
    :param trace_type:     Defines trace type to use for 2d surface plot. Supports 'heatmap', 'contour', 'surface3D'.
    :type  trace_type:     str
    :param fig_title:      Figure title string.
    :type  fig_title:      str
    :param z_scale:        Scaling factor used for z axes.
    :type  z_scale:        int
    '''

    # ------ INPUT HANDLING -------
    # is_bathy Error 
    if isinstance(is_bathy,bool) is False:
        emess("Error: is_bathy must be boolean value.")

    # fig_title Error
    if fig_title is None:
        fig_title = "FUNWAVE Surface Data"
    elif isinstance(fig_title,'str') is False:
        emess('Error: Optional input argument fig_title must be a string')

    # Color Map Assignment 
    if is_bathy is True:
        cMap = 'deep'
    else:
        cMap = 'ice'

    # z_scale 
    if z_scale is None:
        # Redefine z_scale 
        z_scale=0.5
    elif z_scale<0:
        # z_scale Error 
        emess('Error: Input argument ''z_scale'' must be greater than 0.')

    # ------ FIGURE LAYOUT -------
    # Initialize Figure 
    fig = go.Figure()
    # Add Title & Labels To Figure 
    fig.update_layout(
        title={'text': fig_title,
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font=dict(
            family="Arial",
            size=18)
    )
    # Update Y Axes Labels
    fig.update_yaxes(title_text='Nglob')
    # Update X Axes Labels
    fig.update_xaxes(title_text="Mglob")

    # ------ ADD TRACES ------
    if trace_type == "heatmap":
        # Add Heatmap Trace
        fig.add_trace(go.Heatmap(z=surface_array, colorscale=cMap))
    elif trace_type == "contour":
        # Add Contour Trace
        fig.add_trace(go.Contour(z=surface_array, colorscale=cMap, showlines=True))
    elif trace_type == "surface3D":
        # Update 3D scene options 
        fig.update_scenes(
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=z_scale)
        )
        # Add 3-D Surface Trace
        fig.add_trace(go.Surface(z=surface_array, colorscale=cMap))
        # Update Surface Trace Properties
        fig.update_traces(contours_z=dict(show=True, usecolormap=True,
            highlightcolor="limegreen"))
            
    else:
        emess("Error: Unsupported trace_type. Please use: heatmap, contour or surface3D")

    # ------ TEMP LINE -------
    fig.show()
    return fig

def surface_plot_overlay(surface_array, topo_bathy, mask, x_scale=None, y_scale=None, z_scale=None, fig_title=None):
    '''Function for ploting 2D surface data on top of topo/bathy.
  
    :param surface_array:  FUNWAVE grid data values.
    :type  surface_array:  ndarray
    :param mask:           FUNWAVE grid mask (Wet/Dry nodes).
    :type  mask:           ndarray
    :param x_scale:        Scaling factor used for x axes.
    :type  x_scale:        int
    :param y_scale:        Scaling factor used for y axes.
    :type  y_scale:        int
    :param z_scale:        Scaling factor used for z axes.
    :type  z_scale:        int
    :param fig_title:      Figure title string.
    :type  fig_title:      str
    '''
    # fig_title Error
    if fig_title is None:
        fig_title = "FUNWAVE Surface Data"
    elif isinstance(fig_title,'str') is False:
        emess('Error: Optional input argument fig_title must be a string')

    # x_scale 
    if x_scale is None:
        # Redefine x_scale 
        x_scale=1
    elif x_scale<0:
        # x_scale Error 
        emess('Error: Input argument ''x_scale'' must be greater than 0.')

    # y_scale 
    if y_scale is None:
        # Redefine y_scale 
        y_scale=1
    elif y_scale<0:
        # y_scale Error 
        emess('Error: Input argument ''y_scale'' must be greater than 0.')

    # z_scale 
    if z_scale is None:
        # Redefine z_scale 
        z_scale=0.5
    elif z_scale<0:
        # z_scale Error 
        emess('Error: Input argument ''z_scale'' must be greater than 0.')

    # ------ APPLY MASK TO OVERLAY SURFACE -------
    surface_array[mask==0] = np.nan
    
    # ------ FIGURE LAYOUT -------
    # Initialize Figure 
    fig = go.Figure()
    # Add Title & Labels To Figure 
    fig.update_layout(
        title={'text': fig_title,
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font=dict(
            family="Arial",
            size=18)
    )
    # Update Y Axes Labels
    fig.update_yaxes(title_text='Nglob')
    # Update X Axes Labels
    fig.update_xaxes(title_text="Mglob")

    # ------ ADD TRACES ------
    # Update 3D scene options 
    fig.update_scenes(
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=z_scale)
    )
    # Add 3-D Surface Trace
    fig.add_trace(go.Surface(z=topo_bathy*-1, colorscale='deep'))
    fig.add_trace(go.Surface(z=surface_array, colorscale='deep',connectgaps=False))

def quiver_plot(xx, yy, u, v, mask, quiver_norm, quiver_scale, axes_ratio, fig_title=None, bottom_surface=None, bottom_trace=None, color_map=None):
    '''Function for overlaying quiver plot on 2D surface. 
  
    :param xx:              FUNWAVE grid x values.
    :type  xx:              ndarray
    :param yy:              FUNWAVE grid y values.
    :type  yy:              ndarray
    :param u:               FUNWAVE x velocity grid.
    :type  u:               ndarray
    :param v:               FUNWAVE y velocity grid.
    :type  v:               ndarray
    :param quiver_norm:     Logical switch that controls the normalization of he vector field. This causes arrows to be of the same size.
    :type  quiver_norm:     bool
    :param quiver_scale:    Scales size of the arrows (ideally to avoid overlap) [0, 1].
    :type  quiver_scale:    ndarray
    :param axes_ratio:      The ratio between the scale of the y-axis and the scale of the x-axis (scale_y / scale_x).
    :type  axes_ratio:      ndarray
    :param fig_title:       Figure title string.
    :type  fig_title:       str
    :param bottom_surface:  FUNWAVE grid output variable data. If None then underlying surface is defined as sqrt(u^2 + v^2).
    :type  bottom_surface:  ndarray
    :param mask:            FUNWAVE grid mask (Wet/Dry nodes).
    :type  mask:            ndarray
    :param bottom_trace:    Trace type for underlying surface data. Supports 'contour' and 'heatmap'. If None then 'heatmap' will be used.
    :type  bottom_trace:    ndarray
    :param color_map:       Plotly included colormap scale.
    :type  color_map:       ndarray
    '''

    # ------- INPUT HANDELING ------
    # Check If User Provided Figure Title 
    if fig_title is None: # No Title Specifed 
        # Use Generic Figure Title 
        fig_title = "FUNWAVE Surface Data"
    elif isinstance(fig_title,'str') is False: # Verify Requested Title Is A String
        # Throw Dependency Error 
        emess('Error: Optional input argument fig_title must be a string')

    # Make Sure Inputs Are the Same Size 
    if np.shape(xx)==np.shape(yy)==np.shape(u)==np.shape(v)==np.shape(mask):
        pass
    else:
        # Dimesion Mismatch Error
        emess('Error: Input arguments ''xx'',''yy'',''u'',''v'',''mask'' must be the same shape.')

    # Quiver Scale Restriction
    if quiver_scale>=0 and quiver_scale<=1:
        pass
    else:
        # Value out Of Range Error 
        emess('Error: Input argument ''quiver_scale'' must be [0,1].')

    # Colormap Default Value 
    if color_map is None:
        # Define Default Continous Colormap
        color_map='ice' 

    # Check If User Provided bottom_surface
    if bottom_surface is None: # Default Surface Will Be Used
        pass
    else: # Using User Provided Surface Variable
        # Check For Surface Trace Preference 
        if bottom_trace is None: # No Surface Trace Specified 
            # Go To Default Value
            bottom_trace='heatmap'
        else: # Check If Specified Surface Trace Is Valid
            if bottom_trace is ['contour','heatmap']:
                pass
            else: # Invalid Trace Type
                # Throw Dependency Error 
                emess('Error: Unrecognized option for optional input argument bottom_trace. Please use: ''contour'', ''heatmap'' or ''surface3D''.')
    
    # ------ FIGURE LAYOUT -------
    # Compute U,V Magnitude 
    mag = np.sqrt(u**2 + v**2)
    # Normalize Quiver
    if quiver_norm is True:
        # Normalize U
        u = u/mag
        # Normalize V
        v = v/mag
    # Create Quiver Object
    q_obj = ff.create_quiver(xx, yy, u, v, scale = quiver_scale, scaleratio = axes_ratio)
    # Check If bottom_surface Exist 
    if bottom_surface is None: # Overlay Quiver On Top Of sqrt(u.^2 + v.^2)
        # Define bottom_surface Default Value
        bottom_surface = mag
    # Add Requested Surface Trace
    if bottom_trace=='heatmap':
        s_obj=go.Heatmap(x=xx, y=yy, z=bottom_surface, colorscale=color_map)
    elif bottom_trace=='contour':
        s_obj=go.Contour(x=xx, y=yy, z=bottom_surface, colorscale=color_map)
    # Intialize Figure Object
    fig=go.Figure()
    # Append Surface Trace 
    fig.add_trace(s_obj)
    # Append Quiver Trace 
    fig.add_trace(q_obj)

    #------ TEMP LINE -----
    # Show Figure
    fig.show()
    return fig
