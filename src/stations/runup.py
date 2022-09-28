# Software is under the BSD 2-Clause "Simplified" License, see LICENSE file for further details.

##
# @file runup.py
#
# @ breif
#
# @ section 
#


from funwavetvdtools.error import FunException
import funwavetvdtools.validation as fv

import numpy as np
from scipy.signal import find_peaks


#class Runup():


def _all_same(arr):
    arr = fv.convert_array(arr, 'arr')
    return np.all(arr[1:] == arr[0])

def _compute_single(x, h, eta, r_depth=None):

    ne = len(eta)
    nh = len(h)
    nx = len(x)

    if not _all_same([ne, nh, nx]):
        brief = 'Invalid Array Sizes'
        desc = "The length of the input arrays are not the same, " \
                    "the lengths of 'x', 'h', and 'eta' are %d, %d, and %d" \
                 "respectively." % ( nx, nh, ne)
        raise FunException(brief, desc)    

    n = ne 

    # NOTE: Add filter for h < 1 but check for continous range
    if r_depth is None:
        dh = np.abs(np.diff(h)).max()
        r_depth = 4.0*dh

    m, c = np.polyfit(x, -h, 1)
    w_depth = eta + h    


    if m > 0: # slopes up
        idx = np.argmax(w_depth>=r_depth)    
    else: # slopes down 
        idx = np.argmin(w_depth>=r_depth)

    runup   = eta[idx]
    runup_x = x[idx]

    return runup, runup_x, r_depth 

def _compute_timeseries(x, h, eta, r_depth=None):

    nx = len(x)
    shph = h.shape
    shpe = eta.shape

    ndh = h.ndim

    if ndh == 2:
        if not _all_same([shph, shpe]):
            brief = "Invalid Array Sizes"
            desc = "The dimensions of the arrays do not match. The dimensions of 'x', 'h', and 'eta' " \
                    "are (%d, %d)  and (%d, %d), respectively." % ( shph + shpe)
            raise FunException(brief, desc)
        else:
            npts, nt = shpe
    else:
        nph = shph[0]
        npe, nt = shpe
    
        if npe != nph:
            brief = "Invalid Array Sizes"
            desc = "The number of points in 'h' and 'eta' do not match, got %d and %d, respectively." % (nph, npe)
            raise FunException(brief, desc)

        npts = nph


    if nx != npts:
        brief = "Invalid Array Sizes"
        desc = "The number of 'x' points do not match the number of points in 'h' and 'eta'. Number " \
                "of points in 'x' is %d and the number of points in 'h' and 'eta' are %d." % (nx, np)
        raise FunException(brief, desc)
 

    # NOTE: Fix r_depth name collision 
    runup   = np.zeros(nt)
    runup_x = np.zeros(nt)
    r_depth2 = np.zeros(nt)

    if ndh == 2:
        for i in range(nt):
            runup[i], runup_x[i], r_depth2[i] = _compute_single(x, h[:,i], eta[:,i], r_depth)
    else:
        for i in range(nt):
            runup[i], runup_x[i], r_depth2[i] = _compute_single(x, h, eta[:,i], r_depth)

    return runup, runup_x, r_depth2


def _ndarray_type_test(obj, name):

    obj_type = type(obs)

    if obj_type is not np.ndarry:
        brief = "Invalid Argument Type"
        desc = "Input argument '%s' is of type '%s' and not a numpy array." % (name, obj_type) 
        raise FunException(brief, desc)


def _check_args(x, h, eta, r_depth=None):


    x   = fv.convert_array(x, 'x')
    h   = fv.convert_array(h, 'h')
    eta = fv.convert_array(eta, 'eta')
    
    ndx = x.ndim
    ndh = h.ndim
    nde = eta.ndim
    
    if ndx != 1:
        brief = "Invalid Dimensions of Array"
        desc = "The dimensions of array 'x' must be 1, got %d." % ndx[0]
        raise FunException(brief, desc)
        
    if ndh != 1 and ndh != 2:
        brief = "Invalid Dimensions of Array"
        desc = "The dimensions of array 'h' must be either 1 or 2, got %d." % ndh
        raise FunException(brief, desc)
            
    if nde != 1 and nde != 2:
        brief = "Invalid Dimensions of Array"
        desc = "The dimensions of array 'eta' must be either 1 or 2, got %d." % nde
        raise FunException(brief, desc)
    
    return x, h, eta, r_depth, nde

def compute(x, h, eta, r_depth=None):


    x, h, eta, r_depth, nde = _check_args(x, h, eta)

    if nde == 1:
        return _compute_single(x, h, eta, r_depth)
    elif nde == 2:
        return _compute_timeseries(x, h, eta, r_depth)
    else:
        brief = "Unexpected Error"
        desc = "The number of dimensions of the input array 'eta' must be either 1 or 2, got %d." % nd
        raise FunException(brief, desc)



def compute_stats(runup, upper_centile=2, peak_width=2):

    centile=100-upper_centile
    peak_idxs, _ = find_peaks(runup, width=peak_width)
    r_percent = np.percentile(runup[peak_idxs], centile)
    return r_percent 



def compute_with_stats(x, h, eta, r_depth=None, \
                        t=None, t_max=None, t_Min=None, \
                        upper_centile=2, peak_width=2):

    x, h, eta, r_depth, nde = _check_args(x, h, eta)


    if nde == 2:
        runup, runup_x, r_depth = _compute_timeseries(x, h, eta, r_depth)
        r_percent = compute_stats(runup, upper_centile, peak_width)
        setup = np.mean(runup)

        return runup, runup_x, r_depth, r_percent, setup

    else:
        brief = "Unexpected Error"
        desc = "The number of dimensions of the input array 'eta' must be either 1 or 2, got %d." % nd
        raise FunException(brief, desc)




if __name__ == "__main__":

    from funwavetvdtools.stations import Profile, Stations


    print('hello')





