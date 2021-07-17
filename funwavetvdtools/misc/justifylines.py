class JustifyLines:
    
    def __init__(self , justifyModes ):
        
        self.__justifyModes = justifyModes
        self.__nArgs = len(justifyModes)
        self.__lines = []  
        self.__maxLens = [0]*self.__nArgs
        
        
        for i in range (0,len(justifyModes)):
            
            justifyModes[i] = justifyModes[i].lower()
            justifyMode = justifyModes[i]
            
            if ( type(justifyMode) is str ):
                if ( len(justifyMode) == 1 ):
                    if ( not justifyMode =='c' and not justifyMode == 'l' and not justifyMode == 'r' ):
                        raise Exception("Argument %d is '%s', must be 'l' (left), 'c' (center) or 'r' (right)." % (i+1,justifyMode) )
                else:
                    raise Exception("Argument %d is not a single character" % (i+1) )
                
            else:
                raise Exception("Argument %d is not a string/character" % (i+1) )
        
    def append( self, vals ):
         
        if ( len(vals) == self.__nArgs):
            
            for i in range(len(vals)):
                val = vals[i]
                if ( type(val) is str):           
                    lenVal = len(val)
                    if ( lenVal > self.__maxLens[i] ):
                        self.__maxLens[i] = lenVal
                    
                else:
                    raise Exception("Can not append line, argument %d is not a string." % (i+1) )
            
            self.__lines.append(vals) 
        else:
            raise Exception("Can not append line, %d values given when %d are required." % (nVals,self.__nArgs) )
       
    def clear(self):
        self.__lines = []
        self.__maxLens = [0]*self.__nArgs
        
        
    def getFormattedLines(self):
        
        formatedLines = [];
      
        for line in self.__lines:
            
            formattedLine = ""
            
            for arg, justifyMode, maxLen in zip(line, self.__justifyModes, self.__maxLens ):
             
                if  ( justifyMode == 'r'):
                    formattedLine += arg.rjust( maxLen )
                elif( justifyMode == 'c' ):
                    formattedLine += arg.center( maxLen )
                else:
                    formattedLine += arg.ljust( maxLen )
                    
                formattedLine += " "
                
            formatedLines.append(formattedLine)
        
        return formatedLines


