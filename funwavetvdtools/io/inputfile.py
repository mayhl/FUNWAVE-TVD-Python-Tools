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
                
class InputFile:

    @property
    def path():
        return self._path
    
    def __init__(self, path):
        
        self._path = path 
        raise Exception("Implement class")
        