# Software is under the BSD 2-Clause "Simplified" License, see LICENSE file for further details.

##
# @file runup.py
#
# @ breif
#
# @ section 
#


import warnings

import numpy as np
from scipy.signal import find_peaks

import funwavetvdtools.validation as fv
from funwavetvdtools.error import FunException

#class Runup():


def _all_same(arr):
    arr = fv.convert_array(arr, 'arr')
    return np.all(arr[1:] == arr[0])

def _compute_single(x, h, eta, x0, r_depth):

    ne = len(eta)
    nh = len(h)
    nx = len(x)

    if not _all_same([ne, nh, nx]):
        msg = "The length of the input arrays are not the same, " \
                "the lengths of 'x', 'h', and 'eta' are %d, %d, and %d" \
                "respectively." % ( nx, nh, ne)
        raise FunException(msg, ValueError)    


    # NOTE: Add filter for h < 1 but check for continous range
    if r_depth is None:
        dh = np.abs(np.diff(h)).max()
        r_depth = 4.0*dh

    m, c = np.polyfit(x, -h, 1)
    w_depth = eta + h    

    r_depth = 0.002
    thresh = w_depth - r_depth
    sign_changes = thresh[:-1]*thresh[1:] < 0

    ic = np.arange(len(thresh)-1)[sign_changes]
    nsc = len(ic)
    
    if nsc == 0:
        warnings.warn("Runup: No wet/dry line found, setting to NaN.")
        return np.nan, np.nan, r_depth

    if nsc > 1:
        warnings.warn("Runup: Found multiple wet/dry lines. Using point furthest up slope")
        ic = ic[-1] if m > 0 else ic[0]
    else:
        ic = ic[0]

    si = ic - 2
    ei = ic + 3

    runup = np.interp(r_depth, w_depth[si:ei], eta[si:ei])
    runup_x = np.interp(r_depth, w_depth[si:ei], x[si:ei]) - x0

    return runup, runup_x, r_depth 

def _compute_timeseries(x, h, eta, x0, r_depth):

    nx = len(x)
    shph = h.shape
    shpe = eta.shape

    ndh = h.ndim

    if ndh == 2:
        if not _all_same([shph, shpe]):
            msg = "The dimensions of the arrays do not match. The dimensions of 'x', 'h', and 'eta' " \
                    "are (%d, %d)  and (%d, %d), respectively." % ( shph + shpe)
            raise FunException(msg, TypeError)
        else:
            npts, nt = shpe
    else:
        nph = shph[0]
        npe, nt = shpe
    
        if npe != nph:
            msg = "The number of points in 'h' and 'eta' do not match, got %d and %d, respectively." % (nph, npe)
            raise FunException(msg, TypeError)

        npts = nph


    if nx != npts:
        msg = "The number of 'x' points do not match the number of points in 'h' and 'eta'. Number " \
                "of points in 'x' is %d and the number of points in 'h' and 'eta' are %d." % (nx, np)
        raise FunException(msg, TypeError)
 

    # NOTE: Fix r_depth name collision 
    runup   = np.zeros(nt)
    runup_x = np.zeros(nt)
    r_depth2 = np.zeros(nt)

    if ndh == 2:
        for i in range(nt):
            runup[i], runup_x[i], r_depth2[i] = _compute_single(x, h[:,i], eta[:,i], x0, r_depth)
    else:
        for i in range(nt):
            runup[i], runup_x[i], r_depth2[i] = _compute_single(x, h, eta[:,i], x0, r_depth)

    return runup, runup_x, r_depth2


def _check_args(x, h, eta, x0, r_depth, t, t_min, t_max):


    x   = fv.convert_array(x, 'x')
    h   = fv.convert_array(h, 'h')
    eta = fv.convert_array(eta, 'eta')
    
    ndx = x.ndim
    ndh = h.ndim
    nde = eta.ndim

    
    if x0 is None: x0 = 0.0

    
    if ndx != 1:
        msg = "The dimensions of array 'x' must be 1, got %d." % ndx[0]
        raise FunException(msg, TypeError)
        
    if ndh != 1 and ndh != 2:
        msg = "The dimensions of array 'h' must be either 1 or 2, got %d." % ndh
        raise FunException(msg, TypeError)
            
    if nde != 1 and nde != 2:
        msg = "The dimensions of array 'eta' must be either 1 or 2, got %d." % nde
        raise FunException(msg, TypeError)


    is_t_none = t is None
    is_t0_none = t_min is None
    is_t1_none = t_max is None
    def get_t_state(t, t_min, t_max):
        if is_t_none and (not is_t0_none or not is_t1_none):
            warnings.warn("Runup: t_min and/or t_max specified without t being specified, ignoring bound(s).")
            return [None] * 5

        if not is_t_none and (is_t0_none and is_t1_none): 
            warnings.warn("Runup: t specified without t_min or t_max being specified, ignoring t.")
            
            return [t, None, None, 0, len(t)]

        if is_t_none: return [None] * 5

        if is_t0_none: t_min = np.min(t) 
        if is_t1_none: t_max = np.max(t)

        i0 = np.argmin(np.abs(t-t_min))
        i1 = np.argmin(np.abs(t-t_max)) + 2

        return t, t_min, t_max, i0, i1

    if nde == 2 or ndh == 2:

        is_t_none = t is None
        is_t0_none = t_min is None
        is_t1_none = t_max is None

        t, t_min, t_max, i0, i1 = get_t_state(t, t_min, t_max)

        if not t is None:
            t = t[i0:i1]
            if nde == 2 : eta = eta[:,i0:i1]
            if ndh == 2 : h = h[:,i0:i1]

    return t, x, h, eta, x0, r_depth, nde

def compute(x, h, eta, x0=None, r_depth=None, t=None, t_min=None, t_max=None):

    t, x, h, eta, x0, r_depth, nde = _check_args(x, h, eta, x0, r_depth, t, t_min, t_max)

    if nde == 1:
        return _compute_single(x, h, eta, x0, r_depth)
    elif nde == 2:
        return (t,) + _compute_timeseries(x, h, eta, x0, r_depth)
    else:
        "The number of dimensions of the input array 'eta' must be either 1 or 2, got %d." % nd
        raise FunException(brief, TypeError)



def compute_stats(runup, upper_centile=2, peak_width=2):

    centile=100-upper_centile
    peak_idxs, _ = find_peaks(runup, width=peak_width)
    peaks = runup[peak_idxs]

    if len(peaks) > 0:
        return np.percentile(runup[peak_idxs], centile)
    else:
        return 0



def compute_with_stats(x, h, eta, x0=None, r_depth=None, \
                        t=None, t_min=None, t_max=None, \
                        upper_centile=2, peak_width=2):

    print( eta.shape)
    t, x, h, eta, x0, r_depth, nde = _check_args(x, h, eta, x0, r_depth, t, t_min, t_max)
    print( eta.shape)
    if nde == 2:
        runup, runup_x, r_depth = _compute_timeseries(x, h, eta, x0, r_depth)
        r_percent = compute_stats(runup, upper_centile, peak_width)
        setup = np.mean(runup)

        return t, runup, runup_x, r_depth, r_percent, setup

    else:
        msg = "The number of dimensions of the input array 'eta' must be either 1 or 2, got %d." % nd
        raise FunException(msg, TypeError)




if __name__ == "__main__":

    pass
    





