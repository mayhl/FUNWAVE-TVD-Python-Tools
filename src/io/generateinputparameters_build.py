import pandas as pd
import numpy as np 
import os 

from inputfile import Parameter
from inputfile import Datatype
from inputfile import Category
from inputfile import formatValueByDataType

from funwavetvdtools.misc.justifylines import JustifyLines

csvFilePath='inputparameters.csv'
outFilePath = 'inputparameters.py'
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

def getFormatList( name , fullName, datatype, category, description, isRequired, defaultValue  ):
    
    fmtList = [ "Parameter("]
    fmtList.extend(  ["'%s'" % name     , ',' ] )
    fmtList.extend(  ["'%s'" % fullName , ',' ] ) 
    fmtList.extend(  ["%s"   % datatype , ',' ] ) 
    fmtList.extend(  ["%s"   % category , ',' ] ) 
    fmtList.extend(  ["%s"   % isRequired , ',' ] ) 
    if defaultValue is str:
        fmtList.extend(  ["'%s'"   % defaultValue , ',' ] ) 
    else:
        fmtList.extend(  ["%s"   % defaultValue , ',' ] ) 
    
    fmtList.extend(  ["'%s'"   % description , ')' ] ) 
    return fmtList


justs = ['l' ] * 15
jt = JustifyLines(justs)
    
for index, row in df.iterrows():
    
    name         = row['Name'].strip()
    fullName     = row['Full Name'].strip()
    datatype     = getEnumFromString(row['Datatype'] , Datatype )
    category     = getEnumFromString(row['Category'] , Category )
    isRequired   = parseIsRequired( row['Is Required']  )
    description  = parseDescripion( row['Description'] )
    defaultValue = parseDefaultValue( row['Default Value'] , datatype )        
    
    fmtList = getFormatList( name , fullName, datatype, category, description, isRequired, defaultValue  )
    
    jt.append(fmtList)

# Constructing parameterlist.py file
with open( outFilePath , 'w+' ) as fh:

    fh.write('from inputfile import Parameter\n')
    fh.write('from inputfile import Datatype\n')
    fh.write('from inputfile import Category\n\n')
    
    fh.write( 'values = [\n')
    # NOTE 1: Replace removes space between comma automatically inserted by JustifyLines
    # NOTE 2: [:-1] Remove trailing space at end of line
    for formattedLine in jt.getFormattedLines(): fh.write( "    " + formattedLine.replace(' ,' , ',')[:-1] + ",\n" )
    
    # Remove last comma from last item in list
    fh.seek(0, os.SEEK_END)          
    fh.seek(fh.tell() - 2, os.SEEK_SET)
    fh.truncate()
    
    fh.write( '\n] ')