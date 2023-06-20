# @file inputfile.py
#
# @brief Interface for FUNWAVE-TVD input/driver text file.
#
# @section description_inputfile Description
# Example Python program with Doxygen style comments.
#
# @section libraries_main Libraries/Modules
# - enum standard library (https://https://docs.python.org/3/library/enum.html)
#   - Access to enumeration functionality.
# - pandas library (https://pandasguide.readthedocs.io/en/latest/)
#   - Access to parsing CSV files.
#
# @section notes_inputfile Notes
# - Comments are Doxygen compatible.
#
# @section todo_doxygen_example TODO
# - None.
#
# @section author_doxygen_example Author(s)
# - Created by Michael-Angelo Y.-H. Lam on 04/29/2022.
#
# Copyright (c) 2022 FUNWAVE-TVD Group.  All rights reserved.

from enum import Enum, Flag, auto
from functools import partial

import funwavetvdtools.validation as fv
from funwavetvdtools.error import FunException

_LARGE_VAL = 99999
_LARGE_STR = "LARGE"
 
class Datatype(Enum):
    """Datatype enumeration for Parameter class."""

    #: Flag
    FLAG    = 1    
    #: String
    STRING  = 2
    #: Float/Double
    FLOAT   = 3
    #: Integer
    INTEGER = 4
    #: Path String
    PATH    = 5
    #: Enum
    ENUM    = 6
    #: Bool
    BOOL    = 7
    #: 2D field data output flag 
    OUT_FLAG = 8
         
    @classmethod 
    def _cast_2_FUNWAVE_bool(cls, val):
        fv.check_type(val, bool, '_cast_2_FUNWAVE_bool')
        return 'T' if val else 'F'
   
    @classmethod
    def _cast_2_FUNWAVE_large_value(cls, val):
        if val == _LARGE_VALUE: return _LARGE_STR 
        return val
 
    @classmethod
    def _cast_2_FUNWAVE_int(cls, val):  
        val = cls.__cast_2_FUNWAVE_large_value(val)
        return "%d" % fv.convert_int(val, '_cast_2_FUNWAVE_int')        

    @classmethod
    def _cast_2_FUNWAVE_flt(cls, val):
        val = cls.__cast_2_FUNWAVE_large_value(val)
        return "%f" % fv.convert_flt(val, '_cast_2_FUNWAVE_flt')

    @classmethod
    def _cast_2_FUNWAVE_str(cls, val):
        return val if type(val) is str else '%s' % val

    @classmethod
    def _cast_2_FUNWAVE(cls, enum, val):

        maps = {
            cls.FLAG    : cls._cast_2_FUNWAVE_bool,
            cls.STRING  : cls._cast_2_FUNWAVE_str,
            cls.FLOAT   : cls._cast_2_FUNWAVE_flt,
            cls.PATH    : cls._cast_2_FUNWAVE_str,
            cls.ENUM    : cls._cast_2_FUNWAVE_str,
            cls.BOOL    : cls._cast_2_FUNWAVE_bool,
            cls.OUT_FLAG: cls._cast_2_FUNWAVE_bool
        }

        if not enum in maps:
            msg = "FATAL: cast_2_FUNWAVE not implemented for Datatype.%s!!!" % enum.name
            raise FunException(msg, NotImplementedError)

        return maps[enum](val)

    def cast_2_FUNWAVE(self, val):
        return Datatype._cast_2_FUNWAVE(self, val)        


    @classmethod
    def _cast_bool(cls, val):

        t_val = type(val)
        if t_val is bool: return val

        if not t_val is str:
            msg = "_cast_bool can only handle a string or bool"
            raise FunException(msg, TypeError)


        lval = val.lower().strip()

        if lval == 'true' : return True
        if lval == 'false': return False
        if lval == 'yes'  : return True
        if lval == 'no'   : return False
        

        if len(lval) == 1:
            if lval == 't': return True
            if lval == 'f': return False 
            if lval == 'y': return True
            if lval == 'n': return False

        msg = "Unable to cast '%s' to a bool." % val
        raise FunException(msg, TypeError)

    @classmethod
    def _cast_large_value(cls, val):
        if (type(val) is str) and (val.strip() == _LARGE_STR): return _LARGE_VALUE
        return val

    @classmethod
    def _cast_int(cls, val):
        val = cls._cast_large_value(val)
        return fv.convert_int(val, '_cast_int')

    @classmethod
    def _cast_flt(cls, val):
        val = cls._cast_large_value(val)
        return fv.convert_flt(val, '_cast_flt')

    @classmethod
    def _cast_str(cls, val): 
        return val

    @classmethod
    def _cast(cls, enum, val):

        maps = {
            cls.FLAG    : cls._cast_bool,
            cls.STRING  : cls._cast_str,
            cls.INTEGER : cls._cast_int,
            cls.FLOAT   : cls._cast_flt,
            cls.PATH    : cls._cast_str,
            cls.ENUM    : cls._cast_str,
            cls.BOOL    : cls._cast_bool,
            cls.OUT_FLAG: cls._cast_bool
        }
        
        if not enum in maps:
            msg = "FATAL: cast not implemented for Datatype.%s!!!" % enum.name
            raise FunException(msg, NotImplementedError)
        
        return maps[enum](val)

    def cast(self, val):
        return Datatype._cast(self, val)


class Mask(Enum):

    NONE=1,
    POSITIVE=2,
    POSITIVE_DEFINITE=3,
    RANGE=4

    def _dummy_validator(val, name):
        return val
    


    @classmethod
    def get_dt_mask(cls, mask, datatype, values):
        
        _map = {
            Datatype.FLAG: {
                Mask.NONE: Mask._dummy_validator
            },
            Datatype.INTEGER: {
                Mask.POSITIVE_DEFINITE: fv.convert_pos_def_int,
                Mask.POSITIVE         : fv.convert_pos_int,
                Mask.NONE             : fv.convert_int,
                Mask.RANGE            : partial(fv.convert_in_range_int, rng=values)
            },
            Datatype.FLOAT: {
                Mask.POSITIVE_DEFINITE: fv.convert_pos_def_flt,
                Mask.POSITIVE         : fv.convert_pos_flt,
                Mask.NONE             : fv.convert_flt,
                Mask.RANGE            : partial(fv.convert_in_range_flt, rng=values)
            },
            Datatype.ENUM: { 
                Mask.RANGE: partial(fv.is_in_list, values=values)
            },
            Datatype.BOOL: {
                Mask.NONE: Mask._dummy_validator
            },
            Datatype.OUT_FLAG: {
                Mask.NONE: Mask._dummy_validator
            },
            Datatype.PATH: {
                Mask.NONE: Mask._dummy_validator
            },
            Datatype.STRING: {
                Mask.NONE: Mask._dummy_validator
            }
        }


        if datatype in _map:
            if mask in _map[datatype]: return _map[datatype][mask]
                
    
        msg = "FATAL: No mask implemented for combination (%s, %s)!!!" % (datatype, mask)
        raise FunException(msg, NotImplementedError)


def format_value_by_datatype(val, datatype):   
    
    if datatype == Datatype.STRING : return str(val)
    if datatype == Datatype.PATH   : return str(val)
    if datatype == Datatype.INTEGER: return int(val)
    if datatype == Datatype.FLOAT  : return float(val)
    if datatype == Datatype.ENUM  : return str
    raise Exception( "Datatype '%s' conversion not implement" % datatype._name_ )

class Substate(Flag):
    """
    Flag Enum for tracking Parameter substates. Uses Flag class and auto to set up bitwise 
    operations.  
    """

    INVALID = auto()
    WARNING = auto() 
    VALID   = auto()


class State(Enum): 

    VALID = Substate.VALID


    """
    Enum for Parameter states based on Substate combinations. Provides a map between
    Parameter Substate combinations and State Enum values using bitwise operations.    
    """

    @classmethod
    def computed_unified_state(cls, substates):
        """ 
        Combine substates using bitwise or operator to generate State Enum value

        :param substrates: Substrate or list of Substrates definine State
        :type substrates : Substrate, list[Substrates]

        """

        if type(substates) is Substate: return substates
        fv.check_types(substates, Substate, 'substates')
        
        state = substates[0]
        for substate in substates[1:]: state = state | substate
        return state

    @classmethod
    def get(cls, substates):
        """ 
        Get State from combination of Substates

        :param substrates: Substrate or list of Substrates definine State
        :type substrates : Substrate, list[Substrates]

        """
        if not type(substates) is list: substates = [substates]
        state = cls.computed_unified_state(substates)

        for enum in cls:
            if enum.value == state: return enum
                    
        substates = '(%s)' % ', '.join([s.name for s in Substate if s in state]) 
        msg = "Substate combination %s, not implemented." % substates
        raise FunException(msg, NotImplementedError)    


class Category(Enum):
    """Parameter class category/subtype enumeration."""
    
    #: No Category. Only use for subcategory
    NONE           = 0
    #: General parameters

    CENTRAL        = 31

    BOUNDARY_CONDITIONS = 32
    SPHERICAL           = 33
    MORPHOLOGY = 34
    AVALANCHE = 35
    GENERAL        = 1
    #: Grid/spatial parameters
    GRID           = 2
    #: Bathymetry/topography parameters
    BATHYMETRY     = 3
    #: Time parameters
    TIME           = 4
    #: File output parameters 
    OUTPUT         = 5
    #: Physics parameters
    PHYSICS        = 6
    #: Breaking  parameters
    BREAKING       = 7
    #: Numerical scheme parameters
    NUMERICS       = 8
    #: Periodic boundary conditions parameters
    PERIODIC       = 9
    #: Boundary sponge layer parameters
    SPONGE_LAYER   = 10
    #: Tide parameters 
    TIDES          = 11
    #: Wave statistics parameters
    STATISTICS     = 12
    #: Stations/Gauges3parameters
    STATIONS       = 14
    #: Wave maker parameters
    WAVE_MAKER     = 15
    #: Obstacle and breakwater parameters
    OBS_AND_BRKWTR = 16
    #: Hot start parameters
    HOT_START      = 17

    

    # Options requiring FORTRAN preprocessor flags 
    #: Parallel processing parameters
    PARALLEL       = 18
    #: Parameters for optional vessel module
    VESSEL         = 19
    #: Deep draft stabilization parameters
    DEEP_DRAFT     = 20
    #: Parameters for optional Sediment transport FUNWAVE-TVD module
    SEDIMENT       = 21
    #: Parameters for optional meteotsunamis FUNWAVE-TVD module
    METEO          = 22
    #: Partmeters for optional Lagrangian particle tracking FUNWAVE-TVD module
    LAGRANGIAN     = 23
    

    @classmethod
    def essential_modules(cls):
        return [cls.GENERAL   , cls.GRID     , cls.TIME   , cls.NUMERICS, 
                cls.BATHYMETRY, cls.OUTPUT   , cls.PHYSICS]

    @property
    def is_essential(self):
        return self in type(self).essential_modules()



class Dependency:

    __slots__ = ('_name', '_values', '_param')

    def __init__(self, param, values):
        self._values = values 
        self._param = param

    @property
    def is_met(self):
        value = param.value 
        if value is None: return False 
        if type(self._values) is list: return value in self._values
        return value == self._values 

    @property
    def param(self):
        return self._param

    @property
    def values(self):
        return self._values 

    
    @property
    def is_set(self):
        return self._param.is_set 

class Parameter():

    """Class for interfacing with FUNWAVE input file parameter.
 
    :param name:          Name of parameter in FUNWAVE-TVD input file.
    :type  name:          str
    :param full_name:      Descriptive name for parameter.
    :type  full_name:      str
    :param datatype:      Datatype Enum value for parameter datatype
    :type  datatype:      Datatype
    :param category:      Category Enum value for parameter subttype.
    :type  category:      Category
    :param is_required:   Logical denoting if parameter is required for FUNWAVE-TVD execution.
    :type  is_required:   bool
    :param description:   Text description of parameter
    :type  description:   str
    :param mask:          Formatting mask to apply to value, e.g., positive definite integer   
    :type mask:           Mask
    :param values:        List of valid values for Enum/List datatype or list of lower and upper boundary values for Mask.RANGE 
    :type values:         list
    :param default_value: Default value of parameter 
    :type  default_value: any
    :param dependencies:  List of (Name, values) tuples denoting Parameter name and value(s) this parameter depends on. 
                          NOTE: It is assumed only one dependency needs to be met. 
    :type dependencies: list(tuple) 
    """

    # NOTE: __slots__ appearing before doc string caused issues in Sphinx
    __slots__ = ('_name', '_full_name', '_datatype', '_category','_description', '_is_required',
                 '_default_value', '_value', '_values', '_dependencies', '_dependents','_mask', '_mask_func', '_is_deprecated', '_fortran_name', '_units' )
    def __init__(self, name, full_name, datatype, category, is_required, description, mask, values=None, default_value=None, dependencies=None, is_deprecated=False, fortran_name=None, is_essential=False, units=None):
        #: Doc comment for instance attribute qux.
        self._name          = name
        self._full_name     = full_name
        self._datatype      = datatype
        self._category      = category
        self._description   = description
        self._is_required   = is_required
        self._default_value = default_value
        self._values        = values 
        self._is_deprecated = is_deprecated 
        self._dependencies = self._init_dependencies(dependencies)
        self._dependents = None
        self._mask = mask
        self._units = units
        self._mask_func = Mask.get_dt_mask(mask, datatype, values)
        self._fortran_name = fortran_name
        self._value = None

        if default_value is None: 
            self._default_value = None
        else:
            if not self.is_valid_val(default_value):
                msg = "Can not initialize parameter '%s', default value, %s, does not satisfy mask, %s." % (self._name, default_value, self._mask)
                raise FunException(msg, TypeError) 

            self._default_value = self._mask_func(default_value, 'Parameter._default_value')

    def _link_dependencies(self, param_dict):
        

        if self.name not in param_dict:
            msg = "FATAL: Can not link parameter '%s' as name is not in dictionary keys!!!" % self.name
            raise FunException(msg, RuntimeError)

        if self._dependencies is None: return 


        self._dependencies = [Dependency(param_dict[name], values) for name, values in self._dependencies]
        for dep in self._dependencies: dep.param._add_dependent(self)


    def _add_dependent(self, dependent):

        if self._dependents is None: self._dependents = {}
        self._dependents[dependent.name] = dependent


    def _init_dependencies(self, dependencies):

        if dependencies is None: return None

        if not type(dependencies) is list: dependencies=[dependencies]            
        fv.check_types(dependencies, tuple, 'dependencies')
            
        for i, dep in enumerate(dependencies):
            d = len(dep)
            if not d == 2:
                msg = "Element %d in dependencies is not of length 2, got length %d." % (i, d)
                raise FunException(msg, ValueError)

        return dependencies

    def value_to_string(self):
        if not self.is_set: return ""
        return str(self.value)

    @property
    def value(self):
        """Parameter value. Returns default value if not set and has default value."""

        if not self.is_set and self.has_default_value: return self.default_value
        return self._value 

    @value.setter
    def value(self, val):
        print(val)
        name = "Parameter %s" % self.full_name 
        val = self._mask_func(val, name)
        self._value = val

    @property 
    def FUNWAVE_value(self):
        val = self.value
        return None if val is None else datatype.cast(self.val)

    
    def is_valid_val(self, val):

        try:
            name = "Parameter %s" % self.full_name
            val = self._mask_func(val, name)
            return True
        except Exception as e: 
            return False


    def get_state(self):

        if not self._dependencies is None:

            are_none_set = True
            for dep in self._dependencies:
                if dep.is_set:
                    are_none_set = False
                    break

            if are_none_set:
                msg = "%s has a value assigned, but prerequisites parameter values have not been set." % self.name   
                return State.WARNING, msg     

                if not dep.is_met:
                    msg = "%s has a value assigned, but requires %s to be set to %s." % (self.name, dep.name, dep.values) 
                    return State.WARNING, msg

        if self.is_required:
            if not self.is_set and not self.has_default_value:
                msg = "%s does not have a default value and requires a value." % self.name
                return State.ERROR, msg 






    def is_dependency_met(self):
       
        for dep in self._dependencies:
            if dep.is_met: return True

        return False   

    

    def is_valid(self):

        def _is_valid(dep):
            param = dep['param']
            values = dep['values']

            if param.is_set: return False
            return param.value in values if type(values) is list else param.value == values

        for name in self._dependencies:
            is_valid = _is_valid(self._dependencies[name])
            if not is_valid: return False 

        if self.is_required:
            if not self.has_default_value and not self.is_set: return False

        return True 
        

    @property
    def name(self):
        """Getter/property for FUNWAVE-TVD name of.

        :rtype: str
        """
        return self._name
    @property
    def full_name(self):
        """Getter/property for descriptive name.

        :rtype: str
        """
        return self._full_name

    @property
    def datatype(self):
        """Getter/property for Datatype Enum value.

        :rtype: Datatype
        """
        return self._datatype

    @property
    def category(self):
        """Getter/property for Category Enum value.

        :rtype: Category
        """
        return self._category

    @property
    def description(self):
        """Getter/property for description text.

        :rtype: str
        """
        return self._description

    @property
    def is_required(self):
        """Getter/property for is required for simulation logical.

        :rtype: bool
        """
        return self._is_required

    @property
    def default_value(self):
        """Getter/property for default value.

        :rtype: object
        """
        return self._default_value

    @property
    def dependencies(self):
        return [(dep.param.name, dep.values) for dep in self._dependencies]

    @property
    def has_default_value(self):
        """Has a default value set.

        :rtype: bool
        """
        return not self.default_value is None

    @property
    def is_set(self):
        """ Parameter has a value sett.

        :rtype: bool
        """
        return not self._value is None

    @property
    def is_minimal(self):
        if self.is_set: return True
        if self.is_required and not self.has_default_value: return True 
        
        return False

    @property
    def is_flag(self):
        return self.datatype == Datatype.FLAG

    @property
    def is_central_modules(self):
        return is_central_module(self.category)


    def to_dict(self, ignore_keys=None):


        literal_keys = ['name', 'full_name', 'datatype', 'category', 'is_required', 'description', 'mask', 'values', 'default_value']

        info = {k: getattr(self, "_%s" % k) for k in literal_keys}

        def convert(d):
            name = "'%s'" % d.param.name
            values = ("%s" if type(d.values) is list else "'%s'") % d.values
            return (name, values)

        info['dependencies'] = [ convert(d) for d in self._dependencies]
        
        return info
         
