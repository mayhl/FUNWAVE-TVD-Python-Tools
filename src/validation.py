
from funwavetvdtools.error import FunException
import os
import numpy as np

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



def convert_array(arr, name): 

    t_arr = type(arr)
    
    if t_arr is not list and t_array is not np.array:
        brief = "Invalid Argument"
        desc = "Input argument '%s' must be of type list or numpy array, got %s." % (name, t_arr)
        raise FunException(brief, desc)
         
    if t_arr is list: arr = np.array(arr)
    return arr


def _is_int(val):
    
    if type(val) is str:
        if not val.isnumeric(): return False
        val = float(val)
        
    if type(val) is float:
        if val != int(val): return False
        val = int(val)
        
    return type(val) is int

    
    

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
    desc = "Invalid element type at index %d in input array %, expected int-like, got %s."

    for i, val in enumerate(vals):
        if not _is_int(val): raise FunException(brief, desc % (i, name, type(val)))
        vals[i] = int(val)

    return vals 



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


