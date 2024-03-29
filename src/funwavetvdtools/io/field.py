

from funwavetvdtools.error import FunException
import funwavetvdtools.validation as fv

import os
import mimetypes
import numpy as np

def read(fpath, mglob=None, nglob=None, stride=1):

    fv.check_fpath(fpath, 'fpath')

    mtype, _ = mimetypes.guess_type(fpath, strict=True)

    stride = fv.convert_pos_def_int(stride, 'stride')

    # Detecting if file is a binary file or text file
    if mtype == 'text/plain':
        return _read_text(fpath, mglob, nglob, stride)
    elif mtype is None:
        # Assuming binary file if None is returned
        return _read_binary(fpath, mglob, nglob, stride)
    else:
        msg = "Can not read field data, detect mime type '%s' for file '%s'." % (mtype, fpath)  
        raise FunException(msg, TypeError)


def _check_size(val_arg, val_read, val_str, fpath):

    val_arg = fv.convert_pos_def_int(val_arg, val_str)
    
    if val_arg > val_read:
        msg = "Input argument %s=%d is larger than dimension read, %s=%d, in " \
                "text file '%s'." % (val_str, val_arg, val_str, val_read, fpath)
        raise FunException(msg, ValueError)

    return val_arg


def _read_text(fpath, mglob, nglob, stride):

    data = np.loadtxt(fpath)
    n, m = data.shape

    if mglob is not None:
        mglob = _check_size(mglob, m, "mglob", fpath)
        data = data[:,0:mglob]

    if nglob is not None: 
        nglob = _check_size(nglob, n, "nglob", fpath)
        data = data[0:nglob,:]

    return data[::stride,::stride]


def _read_binary(fpath, mglob, nglob, stride):

    if mglob is None:
        msg = "Input argument mglob needs to be specifed for binary data file '%s'." % fpath
        raise FunException(msg, NameError)

    if nglob is None:
        msg = "Input argument nglob needs to be specifed for binary data file '%s'." % fpath
        raise FunException(msg, NameError)


    mglob = fv.convert_pos_def_int(mglob, 'mglob')
    nglob = fv.convert_pos_def_int(nglob, 'nglob')

#    _check_positive_def_int(mglob, 'mglob')
#    _check_positive_def_int(nglob, 'nglob')

    # NOTE: May need to revise check for very large files 

    fsize = os.path.getsize(fpath)
    fsize_per_item = fsize/(mglob*nglob)

    # Assuming little-endian float or double

    if fsize_per_item == 8:
        dtype = '<f8'
    elif fsize_per_item == 4:
        dtype = '<f4'
    else:
        msg = "Failed to read binary field data, detected %.2f bytes per point, " \
                "expected 4 (single-precision) or 8 (double-precision)." % fsize_per_item
        raise FunException(msg, ValueError)
 
    data = np.fromfile(fpath, dtype)
    data = data.reshape([nglob, mglob])

    return data[::stride,::stride]

 
