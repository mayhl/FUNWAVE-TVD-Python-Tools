
from funwavetvdtools.error import FunException
import os
import numpy as np

def check_fpath(fpath, name):

    check_type(fpath, str, name)
    
    if not os.path.isfile(fpath):
        msg = "Can not read file as file path does not exist or is invalid. Path: '%s'." % fpath
        raise FunException(msg, ValueError)


def check_type(obj, cls, name):

    t_obj = type(obj)
    if t_obj is not cls:
        msg = "Input argument '%s' must be of type %s, got %s." % (name, cls, t_obj)
        raise FunException(msg, TypeError)

def check_types(objs, cls, name):

    objs = convert_array(objs)
        
    msg = "Invalid element type at index %d in array %, expected %s, got %s."

    for i, obj in enumerate(objs):

        t_obj = type(obj)
        if t_obj is not cls:
            raise FunException(msg % (i, name, cls, t_obj), TypeError)

def check_subclass(obj, cls, name):

    t_obj = type(obj)    

    if not issubclass(t_obj, cls):
        msg = "Input argument '%s' must be a subclass of %s, got %s." % (name, cls, t_obj) 
        raise FunException(msg, TypeError)



def check_ndarray(obj, ndim, name):

    check_type(obj, np.ndarray, name)

    if obj.ndim != ndim:
        msg = "Invalid number of dimensions is array '%s'," \
                " expected %d, got %d." % (name, ndim, obj.ndim)
        raise FunException(msg, TypeError)

def convert_array(arr, name): 

    t_arr = type(arr)
    
    if t_arr is not list and t_arr is not np.ndarray:
        msg = "Input argument '%s' must be of type list or numpy array, got %s." % (name, t_arr)
        raise FunException(msg, TypeError)
         
    if t_arr is list: arr = np.array(arr)
    return arr

def _parse_str(val):

    def cast_type(val, cast):
        try:
            return cast(val)
        except ValueError as e:
            return None
    
    ival = cast_type(val, int)
    fval = cast_type(val, float)
   
    if ival is None and fval is None:
        return None
    elif ival is not None and fval is not None:
        return ival if ival == fval else fval
    elif fval is not None: # and ival is None
        return fval
    else: # fval is None, ival is not None 
        # Case should not be possible 
        raise Exception('Unexpected State')

def _is_int(val):

    if np.issubdtype(type(val), np.str):
        val = _parse_str(val)
        if val is None: return False
        
    return np.issubdtype(type(val), np.integer)

def convert_number(val, name):

    t_val = type(val)
    val = _parse_str(val)

    if val is None:
        msg = "Input argument %s is not a number, got type %s." % (name, t_val)
        raise FunException(msg, TypeError)

    return val

def convert_int(val, name):

    t_val = type(val)
    
    if not _is_int(val):
        msg = "Input argument %s is not an integer, got type %s." % (name, t_val)
        raise FunException(msg, TypeError)

    return int(val)

def convert_ints(vals, name):

    vals = convert_array(vals, name)

    msg = "Invalid element type at index %d in input array %s, expected int-like, got type %s."

    for i, val in enumerate(vals):
        if not _is_int(val):
            t_val = type(val)
            raise FunException(msg % (i, name, t_val), TypeError)
        vals[i] = int(val)

    return vals 

def convert_pos_int(val, name):

    val = convert_int(val, name)
    if val < 0:
        msg = "Input argument %s is not a postive integer, got %d." % (name, val)
        raise FunException(msg, ValueError)


    return val

def convert_pos_def_int(val, name):

    val = convert_int(val, name)
    if val < 1:
        msg = "Input argument %s is not a positive definite integer, got %d." % (name, val) 
        raise FunException(msg, ValueError)

    return val
    
def convert_pos_def_ints(vals, name):

    vals = convert_ints(vals, name)
    msg = "Non positive definite integer at index %d in input array%s, got %d."
    
    for i, val in enumerate(vals):
        if val < 1: raise FunException(msg % (i, name, val), ValueError)

    return vals

def convert_max_val_int(val, max_val, name):

    val = convert_int(val, name)
    if val > max_val:
        msg = 'Integer %s must be less than or equal to %d, got %d.' % (name, max_val, name)
        raise FunException(msg, ValueError)

    return val


