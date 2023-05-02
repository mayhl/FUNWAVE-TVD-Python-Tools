import os
import json
import traceback

class FunException(Exception):

    def __init__(self, msg, base=None): 
        self._msg 

        self._is_base = base is not None

        if self._is_base:
            # NOTE: Saving base class exception for correct traceback generation
            self._base = base
        else:
            self._base = None
            super().__init__(self._desc)

    @classmethod
    def is_same(cls, err): return type(err) is cls

    @classmethod
    def handle_generic(cls, exception, output_dir=''):

        # Converting Exception to FunException for json generation 
        if not cls.is_same(exception):
            msg = 'Unexpected Error'
            exception = cls(msg, exception)

        fpath = os.path.join(output_dir, 'error.json')
        exception.write_json(fpath)


    def write_json(self, path):	
 
        # Selecting to correct exception for traceback
        ex = self._base if self._is_base else self
        tb = traceback.TracebackException.from_exception(ex).format() 

        err_dict = {
            'Message'   : self._msg,
	        'Type'      : self.__class__.__name__,
            'Traceback' : ''.join(tb)
	    }
	    
        with open(path, 'w') as fh: json.dump(err_dict, fh, indent=4)
