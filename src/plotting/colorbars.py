

import matplotlib.colors as mcolors

def create_divergence(cm, vmin, vmax, vmid, N):
    # Creating an higher resolution equispace linear space for mapping
    u = np.linspace(vmin,vmax,2*N)
    # Dual linear map from [vmin, vmid] -> [0,0.5] and [vmid, vmax] -> [0.5,1] 
    norm =  mcolors.TwoSlopeNorm(vmin=vmin,vcenter=vmid, vmax=vmax)
    # Creating new scaled list of colors 
    new_colors = [mcolors.rgb2hex(color) for color in cm(norm(u))]
    # Returning color map
    return LinearColorMapper(palette = new_colors, low = vmin, high = vmax, nan_color=(0,0,0,0))  