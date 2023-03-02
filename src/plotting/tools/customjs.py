
import os
from funwavetvdtools.error import FunException
from bokeh.models import CustomJS


def load(fpath, args_dict):
    
    # Figure out better method
    dir_path = os.path.realpath(os.path.dirname(__file__))
    fpath = os.path.join(dir_path, fpath)
    
    if not os.path.exists(fpath):
        brief = "Error loading CustomJS file."
        desc = "File '%s' does not exists." % fpath
        raise FunException(brief, desc)
        
        
    with open(fpath) as fh: code = '\n'.join(fh.readlines())
    
    return CustomJS(args=args_dict, code=code)