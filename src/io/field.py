

from funwavetvdtools.error import FunException

import os
import mimetypes
import numpy as np

def read(fpath, mglob=None, nglob=None, stride=1):

    if not os.path.exists(fpath):
        brief = "File Not Found"
        desc = "Can not read field data as file '%s' does not exists." % fpath
        raise FunException(brief, desc)

    mtype, _ = mimetypes.guess_type(fpath, strict=True)

    _check_positive_def_int(stride, 'stride')

    # Detecting if file is a binary file or text file
    if mtype == 'text/plain':
        return _read_text(fpath, mglob, nglob, stride)
    elif mtype is None:
        # Assuming binary file if None is returned
        return _read_binary(fpath, mglob, nglob, stride)
    else:
        brief = "Unexpected Error"
        desc = "Can not read field data, detect mime type '%s' for file '%s'." % ( mtype, fpath)  

def _check_positive_def_int(val, val_str):

    if val != int(val):
        brief = "Invalid Argument"
        desc = "Input argument %s=%f is not an integer." % (val_str, val)
        raise FunException(brief, desc)

    if val < 1:
        brief = "Invalid Argument"
        desc = "Input argument %s=%d is not postive." % (val_str, val)
        raise FunException(brief, desc)


def _check_size(val_arg, val_read, val_str, fpath):

    _check_positive_def_int(val_arg, val_str)
    
    if val_arg > val_read:
        brief = "Invalid Argument"
        desc = "Input argument %s=%d is larger than dimension read, %s=%d, in the " \
                "text file '%s'." % (val_str, val_arg, val_str, val_read, fpath)
        raise FunException(brief, desc)


def _read_text(fpath, mglob, nglob, stride):

    data = np.loadtxt(fpath)
    n, m = data.shape

    if mglob is not None:
        _check_size(mglob, m, "mglob", fpath)
        data = data[:,0:mglob]

    if nglob is not None: 
        _check_size(nglob, n, "nglob", fpath)
        data = data[0:nglob,:]

    return data[::stride,::stride]


def _read_binary(fpath, mglob, nglob, stride):

    if mglob is None:
        brief = "Invalid Argument"
        desc = "Input argument mglob needs to be specifed for binary data file '%s'." % fpath
        raise FunException(brief, desc)

    if nglob is None:
        brief = "Invalid Argument"
        desc = "Input argument nglob needs to be specifed for binary data file '%s'." % fpath
        raise FunException(brief, desc)

    _check_positive_def_int(mglob, 'mglob')
    _check_positive_def_int(nglob, 'nglob')

    fsize = os.path.getsize(fpath)
    fsize_per_item = fsize/(mglob*nglob)

    # Assuming little-endian float or double
    if fsize_per_item == 8:
        dtype = '<f8'
    elif fsize_per_item == 4:
        dtype = '<f4'
    else:
        brief = "File Read Error"
        desc = "Failed to read binary field data, detected %.2f bytes per point, " \
                "expected 4 (single-precision) or 8 (double-precision)." % fsize_per_item
        raise FunException(brief, desc)
 
    data = np.fromfile(fpath, dtype)
    data = data.reshape([nglob, mglob])

    return data[::stride,::stride]

 
