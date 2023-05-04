# Import Plot Library 
import FUNWAVE_plotly_functions as fp



# ------ 1D subplot: Single Station Viewer ------ 
# Get Station Data 
station_data = fp.np.loadtxt('Debug_Dir\\output\\sta_0001')
# Call Subplot Function
fig = fp.station_subplot(eta=station_data[:,1], u=station_data[:, 2], v=station_data[:, 3], time=station_data[:, 0], fig_title='This is a custom title')
# Show Figure 
fig.show()

# ------ 1D Station Var Plot: Comparing Station Data ------ 
# Get Station 2 Data 
station_data_2 = fp.np.loadtxt('Debug_Dir\\output\\sta_0002')
# Call Plot Function For Station 1 
fig = fp.station_var_plot(yData=station_data[:,1], time=station_data[:, 0], station_name='station_1_eta', fig_title='This is a custom title', y_label='Free Surface Height [m]')
# Appen Station 2 Data To Existing Figure Object
fig = fp.station_var_plot(station_data_2[:,1], station_data_2[:, 0], station_name='station_2',fig_title='This is a custom title', fig_in=fig)
# Show Figure 
fig.show()

# ------ 2D Plot: Data Prep ------ 
# Read Random Eta Frame 
eta_mesh = fp.np.loadtxt('Debug_Dir\\output\\eta_00025')
# Read Bathy 
topo_bathy = fp.np.loadtxt('Debug_Dir\\dep_shoal_inlet_brk.txt')
# Get Mask 
mask = fp.np.loadtxt('Debug_Dir\\output\\mask_00025')
# Define Rows (Nglob)
y = fp.np.arange(0, eta_mesh.shape[0], 1)
# Define Cols (Mglob)
x = fp.np.arange(0, eta_mesh.shape[1], 1)
# Create Mesh 
xx, yy = fp.np.meshgrid(x,y)
# Create Dummy Velocity Field 
u = xx**2
v = yy**2

# ------ 2D Plot: Surface Plots With Different Traces ------ 
# is_bathy=True -> surface_array=surface_array*-1
# 2D/3D Surface Plot (Bathy) - surface3D
fig = fp.surface_plot(surface_array=topo_bathy, is_bathy=True, trace_type='surface3D', fig_title='This is a 3D Bathy, z_scale=1', z_scale=0.45)
# Show Fig
fig.show()
# 2D/3D Surface Plot (Bathy) - heatmap
fig = fp.surface_plot(surface_array=topo_bathy, is_bathy=True, trace_type='heatmap', fig_title='This is a heatmap')
# Show Fig
fig.show()
# 2D/3D Surface Plot (Bathy) - contour
fig = fp.surface_plot(surface_array=topo_bathy, is_bathy=True, trace_type='contour', fig_title='This is a contour')
# Show Fig
fig.show()
# ------ 2D Plot: Surface Var Overlayed On Topo/Bathy ------ 
fig = fp.surface_plot_overlay(surface_array=eta_mesh, topo_bathy=topo_bathy, mask=mask, x_scale=1, y_scale=1, z_scale=0.7, fig_title='This is a custom title')
# Show Figure 
fig.show()
# ------ 2D Plot: Quiver Overlayed On Surface Still Debugging ------ 
fig = fp.quiver_plot(xx=xx, yy=yy, u=u, v=v, mask=mask, quiver_norm=True, quiver_scale=1, axes_ratio=1, fig_title='This is a custom title', bottom_surface=eta_mesh, bottom_trace='heatmap', color_map='ice')
# Show Figure 
fig.show()