##
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

from enum import Enum
import pandas as pd

class Datatype(Enum):
    """Datatype enumeration for Parameter class."""
    
    #: String
    STRING  = 1
    #: Float/Double
    FLOAT   = 2
    #: Integer
    INTEGER = 3
    #: Path String
    PATH    = 4

def formatValueByDataType( val , datatype ):   
    
    if datatype == Datatype.STRING : return str(val)
    if datatype == DataType.PATH   : return str(val)
    if datatype == Datatype.INTEGER: return int(val)
    if datatype == Datatype.FLOAT  : return float(val)
    
    raise Exception( "Datatype '%s' conversion not implement" % datatype._name_ )
    
    
class Category(Enum):
    """Parameter class category/subtype enumeration."""
    #: Generic parameters for central FUNWAVE-TVD module
    GENERAL    = 1
    #: Grid/spatial specific parameters for central FUNWAVE-TVD module
    GRID       = 2
    #: Temportal specific parameters for central FUNWAVE-TVD module
    TIME       = 3
    #: Numerical scheme parameters for central FUNWAVE-TVD module
    NUMERICS   = 4
    #: Parameters for optional Vessel FUNWAVE-TVD module
    VESSEL     = 5
    #: Parameters for optional Sediment transport FUNWAVE-TVD module
    SEDIMENT   = 6
    #: Parameters for optional meteotsunamis FUNWAVE-TVD module
    METEO      = 7
    #: Partmeters for optional Lagrangian particle tracking FUNWAVE-TVD module
    LAGRANGIAN = 8
    
class Parameter:

    """Class for interfacing with FUNWAVE input file parameter.
 
    :param name:         Name of parameter in FUNWAVE-TVD input file.
    :type  name:          str
    :param fullname:     Descriptive name for parameter.
    :type  fullname:      str
    :param datatype:     Datatype Enum value for parameter datatype
    :type  datatype:      Datatype
    :param category:     Category Enum value for parameter subttype.
    :type  category:      Category
    :param isRequired:   Logical denoting if parameter is required for FUNWAVE-TVD execution.
    :type  isRequired:    bool
    :param description:  Detail text description of parameter
    :type  description:   str
    :param defaultValue: Optional default value of parameter 
    :type  defaultValue:  any
    """
    def __init__(self, name, fullname, datatype, category, isRequired, description, defaultValue=None):
        #: Doc comment for instance attribute qux.
        self._name         = name
        self._fullname     = fullname
        self._datatype     = datatype
        self._category     = category
        self._description  = description
        self._isRequired   = isRequired
        self._defaultValue = defaultValue
        self.value         = None

    @property
    def name():
        """Getter/property for FUNWAVE-TVD name of.

        :rtype: str
        """
        return self._name
    @property
    def fullname():
        """Getter/property for descriptive name.

        :rtype: str
        """
        return self._fullname

    @property
    def datatype():
        """Getter/property for Datatype Enum value.

        :rtype: Datatype
        """
        return self._datatype

    @property
    def category():
        """Getter/property for Category Enum value.

        :rtype: Category
        """
        return self._category

    @property
    def description():
        """Getter/property for description text.

        :rtype: str
        """
        return self._description

    @property
    def isRequired():
        """Getter/property for is required for simulation logical.

        :rtype: bool
        """
        return self._isRequired

    @property
    def defaultValue():
        """Getter/property for default value.

        :rtype: object
        """
        return self._defaultValue

class InputFile:
   
    """! Class for interfacing a FUNWAVE-TVD input/drive file with Python code."""
 
    def __init__(self, *args):
    
        # Getting parameters from dynamically generated file 
        from inputparameters import values as parameters
        
        # Checking if path argument has been specified 
        if len(args) > 1: raise Exception( 'Only zero or one arguments are allowed in constructor.' ) 
        
        if len(args) == 1:
            self.__isRead = True 
            self._path = args[0] 
        else:
            self.__isRead = False 
            self._path = None
            # Opening input file before interating through 
            fh = None
        
        # Checking if parameter members have been constructed
        if hasattr(type(self),'__generated__'):
            # Sets parameter values to default values or reads values from file if path is specified
            for parameter in parameters: self.__setParameter(parameter, fh)
        else:
            # Add parameter members 
            for parameter in parameters: self.__addParameter(parameter, fh)
            setattr(type(self),'__generated__',True)  
            
        # Closing file handler if it has been open (path specified)
        if self.__isRead: fh.close()
            
    @property 
    def path(): return self._path
    
    def __addParameter(self, parameter, fh):   
        
        # Setting parameter value to default or reading from file if path is specified
        self.__setParameter(parameter, fh)
    
        # Copying parameter to 'private' memeber
        varName    = "_"   + parameter.name
        setattr(self, varName , parameter)    
        
        # Setting read-only property to quickly access parameter value
        getterName = parameter.name
        setattr(type(self), getterName, property(lambda self: getattr(getattr(self, varName),'value')))
        
        # Creating setter for parameter value
        setterName = 'set' + parameter.name[0].upper() +  parameter.name[1::] 
        setattr(type(self), setterName, lambda self, val : setattr(getattr(self, varName),'value', val))

    def __setParameter(self, parameter, fh):   
        
        # Setting value to default value 
        if not self.__isRead:
            parameter.value = parameter.defaultValue
            return
          
        raise Exception('Add input file read code.')
            
            
            
