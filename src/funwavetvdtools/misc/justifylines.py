class JustifyLines:
    
    def __init__(self, modes, seperators=None):
        
        self._modes = modes
        self._n = len(modes)
        self._lines = []  
        self._max_lens = [0]*self._n
        

        nm = self._n-1
        seps_type = type(seperators)
        if seperators is None:
            seperators = [' ']*nm
        elif seps_type is str:
            seperators = [seperators]*nm
        elif seps_type is list:
            if not len(seperators) == nm:
                raise Exception("Length of seperators must be one less than number of items")
        else:
            raise ValueError("Seperators must be a string or list")


        self._seps = seperators

    
        for i in range (0,len(modes)):
            
            modes[i] = modes[i].lower()
            mode = modes[i]
            
            if ( type(mode) is str ):
                if ( len(mode) == 1 ):
                    if ( not mode =='c' and not mode == 'l' and not mode == 'r' ):
                        raise Exception("Argument %d is '%s', must be 'l' (left), 'c' (center) or 'r' (right)." % (i+1,mode) )
                else:
                    raise Exception("Argument %d is not a single character" % (i+1) )
                
            else:
                raise Exception("Argument %d is not a string/character" % (i+1) )
        
    def append( self, vals ):
         
        if ( len(vals) == self._n):
            
            for i in range(len(vals)):
                val = vals[i]
                if ( type(val) is str):           
                    lenVal = len(val)
                    if ( lenVal > self._max_lens[i] ):
                        self._max_lens[i] = lenVal
                    
                else:
                    raise Exception("Can not append line, argument %d is not a string." % (i+1) )
            
            self._lines.append(vals) 
        else:
            raise Exception("Can not append line, %d values given when %d are required." % (nVals,self._n) )
       
    def clear(self):
        self._lines = []
        self._max_lens = [0]*self._n
        

    
        
    def getFormattedLines(self):
        return self.to_formatted_lines()

    def to_formatted_lines(self):

        def get_just(arg, mode, max_len):

            if   mode == 'r':
                return arg.rjust(max_len)
            elif mode == 'c' :
                return arg.center(max_len)
            else:
                return arg.ljust(max_len)
     
        fmt_lines = [] 
        for line in self._lines:
            
            args = list(zip(line, self._modes, self._max_lens))
            fmt_items = [get_just(arg, mode, max_len) + sep for (arg, mode, max_len), sep in zip(args, self._seps)]
            fmt_items.append(get_just(*args[-1]))
            fmt_lines.append(''.join(fmt_items))
        
        return fmt_lines


