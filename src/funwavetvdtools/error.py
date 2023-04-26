import os
import json
import traceback

class FunException(Exception):

    def __init__(self, brief, desc, base=None): 
        self._brief = brief
        self._desc = desc

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
            brief = 'Unexpected Error'
            desc = "An unexpected error has occured, see trace back for more details." 
            exception = cls(brief, desc, exception)

        fpath = os.path.join(output_dir, 'error.json')
        exception.write_json(fpath)


    def write_json(self, path):	
 
        # Selecting to correct exception for traceback
        ex = self._base if self._is_base else self
        tb = traceback.TracebackException.from_exception(ex).format() 

        err_dict = {
            'Brief'	     : self._brief,
	        'Description': self._desc,
            'Traceback'  : ''.join(tb)
	    }
	    
        with open(path, 'w') as fh: json.dump(err_dict, fh, indent=4)
