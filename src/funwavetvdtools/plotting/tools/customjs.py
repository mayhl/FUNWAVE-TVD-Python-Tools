
import os
from funwavetvdtools.error import FunException
from bokeh.models import CustomJS
import funwavetvdtools.validation as fv

def load(fpath, args_dict):
    
    # Figure out better method
    dir_path = os.path.realpath(os.path.dirname(__file__))
    fpath = os.path.join(dir_path, fpath)

    fv.check_fpath(fpath, 'fpath')   
        
    with open(fpath) as fh: code = '\n'.join(fh.readlines())
    
    return CustomJS(args=args_dict, code=code)
