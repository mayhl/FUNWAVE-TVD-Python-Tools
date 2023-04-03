

from funwavetvdtools.grid.common import Grid, Type
from funwavetvdtools.grid.structured import Node as StructNode
from funwavetvdtools import validation as fv
from funwavetvdtools.parallel.simple import simple as parallel_simple

from scipy.interpolate import RegularGridInterpolator
from scipy.interpolate import CloughTocher2DInterpolator
import numpy as np

def interpolate(gi, go, **options):

    fv.check_subclass(gi, Grid, 'gi')
    fv.check_subclass(go, Grid, 'go')
    

    if not gi.has_vars:
        raise Exception("Can not interpolate data, as input grid has not data")

    if go.has_vars:
        if not gi.has_same_metadata(go):
            raise Exception("Can not interpolate data as metadata different between grids")

    int_type = (gi.type, go.type)

    if int_type == (Type.SCATTER, Type.STRUCTURED):
        _scatter_2_grid(gi, go, **options)
    else:
        msg = "Interploation from grid type %s to grid type %s not implemented." % (gi.type.name, gi.type.name)
        raise NotImplementedError(msg)



 



def __scatter_2_grid_inplace(gi, go, iplace=False,  **options):
    

    if not go.has_vars:
        ny, nx = go.shape
        variables = [var.create_metadata_copy(np.zeros([ny,nx])) for var in gi.vars]
        go._add_variables(variables)

    ptsi = list(zip(gi.x, gi.y))
    xo, yo = np.meshgrid(go.x, go.y)
        
    for var_name in go.var_names:
        datai = getattr(gi.data, var_name)
        datao = getattr(go.data, var_name)

        interp = CloughTocher2DInterpolator(ptsi, datai, **options)

        datao[:,:] = interp(xo, yo)[:,:]
    
        if np.isnan(datao).any(): print("WARNING")

def __scatter_2_grid(ptsi, xo, yo, datai, datao, inplace=True, **options):

    xo, yo = np.meshgrid(xo, yo)

    for datumi, datumo in zip(datai, datao):
        interp = CloughTocher2DInterpolator(ptsi, datumi, **options)
        #In inplace mode, data is copy into array instead of replacing array reference 
        datumo[:,:] = interp(xo, yo)[:,:]
        if np.isnan(datumo).any(): print("WARNING")
    # If in parallel mode data can not be copied inplace
    if not inplace: return datao

def _scatter_2_grid(gi, go, **options):

    if not issubclass(type(go), StructNode):
        __scatter_2_grid(gi, go, **options)
    else:

        # NOTE: Due to restrictions of multiprocessing coupled with dynamics named tuples
        #       data has to be unwrapped from classes before parallel execution 
        def prep_args(gi ,go):
            ptsi = list(zip(gi.x, gi.y))
            xo, yo = go.x, go.y
           
            if not go.has_vars:
                ny, nx = go.shape
                variables = [var.create_metadata_copy(np.zeros([ny,nx])) for var in gi.vars]
                go._add_variables(variables)
            
            datai = list(gi.data)
            datao = list(go.data)
        
            return ptsi, xo, yo, datai, datao

        if not gi.is_kdtree: gi.create_kd_tree()


        args_list = [prep_args(*(gi.crop(*go_sub.bounding_box(pad_ratio=0.2)), go_sub)) for go_sub in go.child_iter()]

        n_procs = 4
        inplace = n_procs == 1

        common_args = inplace
        return_args = parallel_simple(__scatter_2_grid, n_procs, args_list, common_args)

        # Copying data in gathered from parallel processes  
        if not inplace:       
            for (*_, datao), new_data in zip(args_list, return_args):
                for datumo, new_datum in zip(datao, new_data): datumo[:,:] = new_datum[:,:] 

        go.copy_children_vars(False)


        
 

    



    
    
     




