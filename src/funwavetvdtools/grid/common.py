from funwavetvdtools.grid.variable import Variable
from enum import Enum
from abc import ABC, abstractmethod
from collections import namedtuple

class Type(Enum):

    SCATTER=1,
    STRUCTURED=2

# Decorator for a static class property 
class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()  


class Grid(ABC):
    
    # Note: property is still callable from base class wi
    @classproperty
    @abstractmethod
    def type(self): 
        raise TypeError("Can't call abstract property type from abstract class Grid")


    # Short hand for easier access to numpy data 
    @property
    def x(self): return self._x.data

    # Short hand for easier access to numpy data 
    @property
    def y(self): return self._y.data   
    
    # Access to variable object
    @property
    def x_var(self): return self._x

    # Acessing to variable object
    @property
    def y_var(self): return self._y 

    @property
    def data(self): return self._data
    
    @property
    def vars(self): return self._vars

    @property
    def has_vars(self): return not self._vars is None
   
    @property
    def var_names(self): return self.vars._fields
 
    @property 
    @abstractmethod
    def shape(self): pass 

    @abstractmethod
    def bounding_box(self, padding=None, pad_ratio=None): pass

    def _bounding_box(self, x0, x1, y0, y1, padding=None, pad_ratio=None):

        if padding is None and pad_ratio is None:
            return x0, x1, y0, y1

        if not padding is None and not pad_ratio is None:
            raise Exception("Can not specify both padding and pad_ratio")

        if not padding is None:
            pad_x = padding
            pad_y = padding
        else:
            pad_x = (x1 - x0)*pad_ratio
            pad_y = (y1 - y0)*pad_ratio
            
        x0 -= pad_x
        x1 += pad_x

        y0 -= pad_y
        y1 += pad_y

        return x0, x1, y0, y1

    def __init__(self, x, y, variables):
        self._x = x
        self._y = y
        self._add_variables(variables)

    def _add_variables(self, variables):

        if variables is None:
            self._vars = None 
            self._data = None
            return 

        vars_type = type(variables) 

        if vars_type is Variable: 
            variables = [variables]
        elif issubclass(vars_type, tuple):
            #If tuple or namedtuple
            variables = list(variables)
        elif not type(variables) is list: 
            raise Exception("ADD ERROR") 

        for var in variables: self._check_variable(var)


        # Creating a namedtuple for shorter read access to numpy arrays        
        tdict = {var.short_name: var.data for var in variables}
        DataTuple = namedtuple('DataTuple', tdict.keys())
        self._data = DataTuple(**tdict)

        # Creating a namedtuple of variable objects
        tdict = {var.short_name: var for var in variables}
        self._vars = DataTuple(**tdict)
 

    def _check_variable(self, var):
        if not type(var) is Variable: raise Exception("ADD ERROR")
        if not var.shape == self.shape: raise Exception("ADD ERROR")
   
    def add_variable(self, variable):

        self._check_variable(variable)

        tdict = self._data._asdict()
        tdict[datum.short_name] = variable.data
        DataTuple = namedtuple('DataTuple', tdict.keys())
        self._data = DataTuple(**tdict)

        tdict = self._vars._asdict()
        tdict[datum.short_name] = variable
        self._vars = DataTuple(**tdict)
        
    def has_same_metadata(self, other):

        # Checking x and y metadata
        if not self.x_var.is_same_metadata(other.x_var): return False
        if not self.y_var.is_same_metadata(other.y_var): return False
        
        # Checking if both grids have no variables 
        if not self.has_vars: return not other.has_vars

        # Checking if both grids have the some number of variables
        if not len(self.vars) == len(other.vars): return False

        # Iterating through variables and checking if the same
        for var_name in self.var_names:

            if not var_name in other.var_names: return False 
            
            var  = getattr(self.vars , var_name)        
            ovar = getattr(other.vars, var_name)

            if not var.is_same_metadata(ovar): return False

        # All metadatas are the same
        return True

    def interpolate(self, gi):
        # Hack to avoid circular imports 
        from funwavetvdtools.grid.interpolation import interpolate
        interpolate(gi, self)
    

def even_divide_range(num, div, off=0):
    sub, rem = divmod(num, div)
    grps = [sub + (1 if i < rem else 0) for i in range(div)]
    
    idxs = [(off, off+grps[0])]*div
    for i in range(1,div): idxs[i] = (idxs[i-1][1], idxs[i-1][1]+grps[i])
 
    return idxs


def linear(n, m, offset=0):
    sub_n = n//m
    p = n % m
    idxs = [] 
    i0 = offset
    
    for j in range(m):
        i1 = i0 + sub_n
        if (j < p): i1 += 1 
        idxs.append((i0, i1))
        i0 = i1
    
    return idxs
