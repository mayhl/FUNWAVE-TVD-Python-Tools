import pandas as pd
import numpy as np 

from inputfile import Parameter
from inputfile import Datatype
from inputfile import Category
from inputfile import formatValueByDataType

csvFilePath='parameterList.csv'
outFilePath = 'parameterList.py'
df = pd.read_csv(csvFilePath)

def getEnumFromString( value , enumClass ):
    
    # Iterating through enum values
    for enumItem in enumClass:   
        if value.strip().upper() == enumItem._name_: return enumItem
    
    # If end of loop is reached, no matching enum value found
    raise Exception( "Did not find matching enum value '%s' for %s"  % ( value , enumClass ) )


def parseIsRequired( val ):   
    val = val.strip().lower()
    
    if val == 'y' or val == 'yes' or val == 'true'  or val == 't': return True
    if val == 'n' or val == 'no'  or val == 'false' or val == 'f': return False
    
    raise Exception( "Could not parse 'Is Required' value '%s' to a boolean")
    
    
def parseDefaultValue( val , datatype ): 
    val = val.strip()
    lowVal = val.lower()
    
    if lowVal == 'none' or '': return None
    
    return formatValueByDataType(val, datatype)
    
def parseDescripion( val ):
    if val is np.nan: return ''
    return val.strip()

for index, row in df.iterrows():
    
    name         = row['Name'].strip()
    fullName     = row['Full Name'].strip()
    datatype     = getEnumFromString(row['Datatype'] , Datatype )
    category     = getEnumFromString(row['Category'] , Category )
    isRequired   = parseIsRequired( row['Is Required']  )
    description  = parseDescripion( row['Description'] )
    defaultValue = parseDefaultValue( row['Default Value'] , datatype )    