from funwavetvdtools.grid.common import classproperty
from enum import Enum
from abc import ABC, abstractmethod
from collections import namedtuple
import numpy as np
class Filter(ABC):

    # Note: property is still callable from base class wi
    @classproperty
    @abstractmethod
    def is_index_filter(self):
        raise TypeError("Can't call abstract property is_index_filter from abstract class Filter")

    @abstractmethod
    def filter(self, arr): pass

    def _get_and_check_dims(self, arr):
        nf = len(self._filts)
        nd = arr.ndim
        if not nd == nf: raise Exception("Can't filter array, dimensions of array do not match number of filters") 
        return nd

    #@abstractmethod
    @property
    def filts(self): return self._filts

    def append(self, new):
        self._filts.extend(new.filts)


class Index(Filter):

    def __init__(self, idx):

        # Converting array of bools to array of indices of True values
        # NOTE: Testing filtering using indices vs bools arrays using random bool arrays show indices
        #       filtering is about 5 times faster.
        if (idx.dtype == 'bool'): idx = np.arange(0,len(idx))[idx]
        self._filts = [idx]

    @property
    def is_index_filter(self): return True


    def filter(self, arr):
        n = super()._get_and_check_dims(arr)
        
        f = self._filts
        if n > 0: arr = arr[f[0]]
        if n > 1: arr = arr[:,f[1]]
        if n > 2: arr = arr[:,:,f[2]]
        if n > 3: raise NotImplementedError("Index filter not implemented for more than 3 dimensions")

        return arr

class Slice(Filter):

    __Slice=namedtuple('SliceTuple', ['s', 'e'])

    def __init__(self, *args):

        n = len(args)

        def input_error():
            raise Exception('Arguments must be either an even number of integers or Slice obects')

        if n == 0: input_error()
        args_type = type(args[0]) 

        if args_type is int:
            if len(args) % 2 == 1:
                raise Exception('Number of indices must be even')
            idxs = args

        elif args_type is Slice:
            n *= 2
            idxs = []
            for s in args:
                for filt in s._filts: idxs.extend([filt.s , filt.e])
            idxs = tuple(idxs)
        else:
            input_error()
        
        self._filts = [Slice.__Slice(*idxs[i:i+2]) for i in range(0, n, 2)]
        #self._filts = [Slice.__Slice(s=s, e=e)]
        
    @property
    def is_index_filter(self): return False

    # DEV NOTE: Explicit copying?
    def filter(self, arr):
        n = super()._get_and_check_dims(arr)

        f = self._filts
        if n == 1: return arr[f[0].s:f[0].e].copy()
        if n == 2: return arr[f[0].s:f[0].e, f[1].s:f[1].e].copy()   
        if n == 3: return arr[f[0].s:f[0].e, f[1].s:f[1].e, f[2].s:f[2].e].copy()

        raise NotImplementedError("Slice filter not implemented for more than 3 dimensions")

    # NOTE: Using a tuple of slices as an index, e.g., array[tuple] is about twice as fast when
    #       compated to the filter function above; however:
    #           1) The creation time of the tuple of slices is about 2 + # filters of a filter step,
    #           2) Incompatiable with multi dimensional index filter,    
    #           3) and calls are on the order of 200 ns and mostly independent of array dimensions
    #       Therefore only useful when using the same slice filter on 1000's of array.
    def create_mdslice(self):
        return tuple(slice(f.s, f.e) for f in filters)




