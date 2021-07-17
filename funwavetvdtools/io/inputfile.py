from enum import Enum
import pandas as pd

class Datatype(Enum):
    STRING  = 1
    FLOAT   = 2
    INTEGER = 3
    PATH    = 4

def formatValueByDataType( val , datatype ):   
    
    if datatype == Datatype.STRING : return str(val)
    if datatype == DataType.PATH   : return str(val)
    if datatype == Datatype.INTEGER: return int(val)
    if datatype == Datatype.FLOAT  : return float(val)
    
    raise Exception( "Datatype '%s' conversion not implement" % datatype._name_ )
    
    
class Category(Enum):
    GENERAL    = 1,
    GRID       = 2,
    TIME       = 3,
    NUMERICS   = 4,
    VESSEL     = 5,
    SEDIMENT   = 6,
    METEO      = 7,
    LAGRANGIAN = 8
    
class Parameter:
    def __init__(self, name, fullname, datatype, category, isRequired, defaultValue, description):

        self.name         = name
        self.fullname     = fullname
        self.datatype     = datatype
        self.category     = category
        self.description  = description
        self.isRequired   = isRequired
        self.defaultValue = defaultValue
        self.value        = None
        
class InputFile:
    
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
            # Opening inpunt file before interating through 
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
            
            
            
