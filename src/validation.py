
from funwavetvdtools.error import FunException
import os
import numpy as np

def check_fpath(fpath, name):
    
    if not os.path.isfile(fpath):
        brief = "Invalid File Path"
        desc = "Can not read file as file path does not exist or is invalid. Path: '%s'." % fpath
        raise FunException(brief, desc)


def check_type(obj, cls, name):

    t_obj = type(obj)
    if t_obj is not cls:
        brief = "Invalid Argument"
        desc = "Input argument '%s' must be of type %s, got %s." % (name, cls, t_obj)
        raise FunException(brief, desc)

def check_types(objs, cls, name):

    objs = convert_array(objs)
        
    brief = "Invalid Argument"
    desc = "Invalid element type at index %d in array %, expected %s, got %s."

    for i, obj in enumerate(objs):

        t_obj = type(obj)
        if t_obj is not cls:
            raise FunException(brief, desc % (i, name, cls, t_obj))

def check_subclass(obj, cls, name):

    t_obj = type(obj)    

    if not issubclass(t_obj, cls):
        brief = "Invalid Arugment"
        desc = "Input argument '%s' must be a subclass of %s, got %s." % (name, cls, t_obj) 
        raise FunException(brief, desc)



def check_ndarray(obj, ndim, name):

    check_type(obj, np.ndarray, name)

    if obj.ndim != ndim:
        brief = "Invalid Arugment"
        desc = "Invalid number of dimensions is array '%s'," \
                " expected %d, got %d." % (name, ndim, obj.ndim)
        raise FunException(brief, name)

def convert_array(arr, name): 

    t_arr = type(arr)
    
    if t_arr is not list and t_arr is not np.ndarray:
        brief = "Invalid Argument"
        desc = "Input argument '%s' must be of type list or numpy array, got %s." % (name, t_arr)
        raise FunException(brief, desc)
         
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
        brief = "Invalid Argument"
        desc = "Input argument %s is not a number, got type %s." % (name, t_val)
        raise FunException

    return val

def convert_int(val, name):

    t_val = type(val)
    
    if not _is_int(val):
        brief = "Invalid Argument"
        desc = "Input argument %s is not an integer, got type %s." % (name, t_val)
        raise FunException(brief, desc)

    return int(val)

def convert_ints(vals, name):

    vals = convert_array(vals, name)

    brief = "Invalid Argument"
    desc = "Invalid element type at index %d in input array %s, expected int-like, got type %s."

    for i, val in enumerate(vals):
        if not _is_int(val):
            t_val = type(val)
            raise FunException(brief, desc % (i, name, t_val))
        vals[i] = int(val)

    return vals 

def convert_pos_int(val, name):

    val = convert_int(val, name)
    if val < 0:
        brief = "Invalid Argument"
        desc = "Input argument %s is not a postive integer, got %d." % (name, val)

    return val

def convert_pos_def_int(val, name):

    val = convert_int(val, name)
    if val < 1:
        brief = "Invalid Argument"
        desc = "Input argument %s is not a positive definite integer, got %d." % (name, val) 
        raise FunException(brief, desc)

    return val
    
def convert_pos_def_ints(vals, name):

    vals = convert_ints(vals, name)
    brief = "Invalid Argument"
    desc = "Non positive definite integer at index %d in input array%s, got %d."
    
    for i, val in enumerate(vals):
        if val < 1: raise FunException(brief, desc % (i, name, val))

    return vals

def convert_max_val_int(val, max_val, name):

    val = convert_int(val, name)
    if val > max_val:
        brief = "Invalid Argument"
        desc = 'Integer %s must be less than or equal to %d, got %d.' % (name, max_val, name)
        raise FunException(brief, desc)

    return val


