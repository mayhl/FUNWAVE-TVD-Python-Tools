import os

import numpy as np

from funwavetvdtools.error import FunException


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

    #objs = convert_array(objs, name)
        
    msg = "Invalid element type at index %d in array '%s', expected %s, got %s."

    for i, obj in enumerate(objs):

        t_obj = type(obj)
        if t_obj is not cls:
            raise FunException(msg % (i, name, cls, t_obj), TypeError)


def check_subclass(obj, cls, name):

    t_obj = type(obj)    

    if not issubclass(t_obj, cls):
        msg = "Variable '%s' must be a subclass of %s, got %s." % (name, cls, t_obj) 
        raise FunException(msg, TypeError)

def check_subclasses(objs, cls, name):

    for i, obj in enumerate(objs):

        t_obj = type(obj)
        if issubclass(t_obj, cls): continue 

        msg = "Object type at index %d in arry %s in not a subclass of %s, got %s."
        raise FunException(msg % (i, name, cls, t_obj), TypeError)  

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
        except ValueError:
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

    if np.issubdtype(type(val), 'str'):
        val = _parse_str(val)
        if val is None: return False
        
    return np.issubdtype(type(val), np.integer)

def _is_flt(val):

    if np.issubdtype(type(val), 'str'):
        val = _parse_str(val)
        if val is None: return False

    return True

def convert_number(val, name):

    t_val = type(val)
    val = _parse_str(val)

    if val is None:
        msg = "Input argument %s is not a number, got type %s." % (name, t_val)
        raise FunException(msg, TypeError)

    return val


def convert_flt(val, name):

    if not _is_flt(val):
        msg = "Input argument %s with value %s is not a float, got type %s." % (name, val, type(val))
        raise FunException(msg, TypeError)

    return float(val)


def _in_range(val, rng):
    vmin, vmax = rng[0], rng[1]
    return (val < vmin) or (val > vmax)


def convert_in_range_flt(val, name, rng):

    val = convert_flt(val, name)    
    if _in_range(val, rng):
        msg = "Variable '%s' is not in the range (%f, %f), got %f." % (name, rng[0], rng[1], val)  
        raise FunException(msg, ValueError)

    return val

    
def convert_pos_flt(val, name):

    val = convert_flt(val, name)
    if val < 0:
        msg = "Input argument %s is not a postive number, got %d." % (name, val)
        raise FunException(msg, ValueError)


    return val

def convert_pos_def_flt(val, name):

    val = convert_flt(val, name)
    if val <= 0:
        msg = "Input argument %s is not a positive definite number, got %d." % (name, val)
        raise FunException(msg, ValueError)

    return val

def convert_int(val, name):

    if not _is_int(val):
        msg = "Input argument %s is not an integer, got type %s." % (name, type(val))
        raise FunException(msg, TypeError)

    return int(val)

def convert_in_range_int(val, name, rng): 
    
    val = convert_int(val, name)
    if _in_range(val, rng):
        msg = "Variable '%s' is not in the range (%f, %f), got %f." % (name, rng[0], rng[1], val) 
        raise FunException(msg, ValueError)
        
    return val

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

def check_max_val_int(val, max_val, name):

    if val > max_val:
        msg = 'Integer %s must be less than or equal to %d, got %d.' % (name, max_val, name)
        raise FunException(msg, ValueError)

    return val


def check_unique_list(vals, name):

    def count(vals, val): return np.sum(np.array(vals)==val)

    uvals = np.unique(vals)
    if len(uvals) == len(vals): return

    dups = [val for val in vals if count(vals, val) > 1]
    msg = "List '%s' contains duplicate entries for %s." % (name, dups)
    raise FunException(msg, ValueError)


def is_in_list(val, name, values):

    if not val in values:
        msg = "Value '%s' must in the list: %s, got %s." % (name, values, val) 
        raise FunException(msg, ValueError)

    return val
