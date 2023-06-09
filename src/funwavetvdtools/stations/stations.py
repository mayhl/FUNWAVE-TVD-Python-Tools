import os
import warnings
from abc import ABC, abstractmethod
from collections.abc import Iterator, Sequence

import numpy as np

import funwavetvdtools.validation as fv
from funwavetvdtools.error import FunException


class Station():

    """ Class for handling station desired location, (x0, y0), and computing the nearest FUNWAVE grid 
    position, (x, y), and corrosponding indices, (i, j). NOTE: i and j are not Python indices 
    (zero based array), but FORTRAN indices (one-based array). 

    :param x0: Desired x position of station
    :type x0: float
    :param y0: Desired y position of station
    :type y0: float
    :param num: Station number/index
    :type num: int 
    """ 
    def __init__(self, x0, y0, num = None):
        self.set_location(x0, y0)
        self._x, self._y = None, None
        self._i, self._j = None, None
        if not num is None: self.number = num

    @property
    def number(self): 
        """Station number

        :type: int
        """
        return self._num

    @number.setter
    def number(self, num):
        self._num = fv.convert_pos_def_int(num, 'num') 

    def set_location(self, x0, y0, x=None, y=None):
        """
        Sets the location of the station and finds closest grid points 
        indices if grid arrays are specified

        :param x0: Exact x position of station
        :type x0: float
        :param y0: Exact y position of station
        :type y0: float
        :param x: Array of x grid locations
        :type x: list
        :param y: Array of y grid locations
        :type y: list     
        """
        x0 = fv.convert_number(x0, 'x0')
        y0 = fv.convert_number(y0, 'y0')

        self._x0 = x0
        self._y0 = y0

        if x is None and y is None: 
            self._i, self._j = None, None
            return

        if not x is None and not y is None: 
            self.update_indices(x, y)
            return 

        # Error state if only one of x or y is None
        desc = "x and y must both be specfied, or both be a list"
        raise FunException(desc, NameError)


    def update_grid(self, x, y):

        """ Updates station index location with closest grid points

        :param x: Array of x grid locations
        :type x: list
        :param y: Array of y grid locations
        :type y: list     
        """

        x = fv.convert_array(x, 'x')
        y = fv.convert_array(y, 'y')

        i = np.argmin(np.abs(x-self.x0))
        j = np.argmin(np.abs(y-self.y0))

        self._x, self._y = x[i], y[j]
        self._i, self._j = i + 1, j + 1


    @property
    def x0(self): 
        """Desired x station location"""
        return self._x0
 
    @property
    def y0(self): 
        """Desired y station location"""
        return self._y0

    @property
    def x(self): 
        """FUNWAVE gridx station location. Returns None if no grid information has been specified."""
        return self._x

    @property
    def y(self): 
        """FUNWAVE grid y station location. Returns None if no grid information has been specified."""
        return self._y
    
    @property
    def i(self): 
        """FUNWAVE grid x station location index. Returns None if no grid information has been specified."""
        return self._i

    @property
    def j(self):
        """FUNWAVE grid y station location index. Returns None if no grid information has been specified."""
        return self._j

    @property
    def indices(self):
        """FUNWAVE grid station location indice, (i, j). Returns None if no grid information has been specified."""
        return (self._i, self._j)

    def get_depth(self, bathy):
        """
        Get station depth from bathymetry data

        :param bathy: Bathymetry data
        :type bathy: np.array 
        """   
        fv.check_ndarray(bathy, 2, 'bathy')
        
        n, m = bathy.shape
        i, j = self._i, self._j 

        msg = "Bathymetry data appears to be invalid, station %s index is %d and out of range of bathymetry %s length, %d."
        if i >= m: raise FunException(msg % ('x', i, m, 'x'), IndexError)
        if j >= n: raise FunException(msg % ('y', i, m, 'y'), IndexError)  

        self._h = bathy[j-1,i-1]

    def _get_depth(self, bathy):
        i, j = self._i, self._j
        self._h = bathy[j-1,i-1]

    @property
    def h(self):
        return self._h

class StationData(ABC):
    
    #_DataBuff = namedtuple('DataBuff', ['data', 'is_loaded'])

    class _DataBuff():
    
        def __init__(self, data=None):
            self.data = data

        #def __ilshift__(self, other):
        @property
        def data(self): return self._data

        @data.setter
        def data(self, data):
            self._data = data
            self._is_loaded = not data is None

        @property
        def is_loaded(self): return self._is_loaded
    """
    Abstact class for containing and postprocessing FUNWAVE station data. Class should not be
    instantiated and provides and interface between data and postprocessing tools. f 
    """
    def __init__(self):

        #self._n = None
        self._var_names = ['n', 't', 'eta', 'u', 'v']
        #self._vars = {var: StationData._DataBuff('None', False) for var in self._var_names} 
        self._vars = {var: StationData._DataBuff() for var in self._var_names}

    def _get_variable(self, name, set_var):

        if not name in self._vars.keys():
            desc = "FATAL: Station variable member setup correctly! Please report error."
            raise FunException(desc, NameError) 

        var = self._vars[name]
        if not var.is_loaded: set_var() 
        return var.data


    @property 
    def n(self):
        return self._n

    @classmethod
    def from_file(cls, fpath, dpath, x, y, nums=None, bathy=None):
        return RealStationData(fpath, dpath, x, y, nums, bathy)

    @property
    def t(self):
        """Time in seconds"""
        return self._get_variable('t', self._set_t)

    @abstractmethod
    def _set_t(self): pass

    @property
    def eta(self):
        """Free surface water height in meters"""
        return self._get_variable('eta', self._set_eta)

    @abstractmethod
    def _set_eta(self): pass 

    @property
    def u(self):
        """x direction velocity water height in meters/second"""
        return self._get_variable('u', self._set_u)

    @abstractmethod
    def _set_u(self): pass

    @property
    def v(self):
        """y direction velocity water height in meters/second"""
        return self._get_variable('v', self._set_v)

    @abstractmethod
    def _set_v(self): pass

    @property
    def n(self):
        """y direction velocity water height in meters/second"""
        return self._get_variable('n', self._set_n)

    @abstractmethod
    def _set_n(self): pass

    def compute_overtoping(self, min_depth, t_min=None, t_max=None):
        """ 
        Computes the amount of overtopping at station
 
        :param min_depth: MIN_DEPTH value from FUNWAVE input/driver file
        :type min_depth: float
        :param t_min: Start time to begin computing overtopping
        :type t_min: float
        :param t_max: End time to stop computing overtopping
        :type t_max: float 
        """
        return ot.compute_flux(self.t, self.h, min_depth, t_min, t_max)       


class RealStationData(Station, StationData):

    @classmethod
    def generate_file_path(cls, dpath, num):
        """ Generate station file path with FUNWAVE numbering scheme

        :param dpath: Path to directory
        :type dpath: str
        :param num: Station number
        :type num: int

        :rtype: str
        """
        fname = "sta_%04d" % num
        fpath = os.path.join(dpath, fname)
        return fpath

    """
    Class for reading FUNWAVE station data file

    :param i: x index of FUNWAVE grid location
    :type i: int
    :param j: y index of FUNWAVE grid location
    :type j: int    
    :param x: Array of x grid locations
    :type x: list, np.array
    :param y: Array of y grid locations
    :type y: list, np.array
    :param num: Station number
    :type num: int 
    :param dpath: Path to directory contain station files, typically the output folder
    :type dpath: str
    :param bathy: Optional bathymetry data for set setting station depths
    :type bathy:  np.array
    """
    def __init__(self, i, j, x, y, num, dpath, bathy=None):
    
        x0 = x[i-1]
        y0 = y[j-1]
        self._dpath = dpath

        fpath = RealStationData.generate_file_path(dpath, num)
        fv.check_fpath(fpath, 'station')

        Station.__init__(self, x0, y0, num)
        StationData.__init__(self)
        self._i, self._j = i, j
        self._x, self._y = x0, y0

        if not bathy is None: self.get_depth(bathy)
        self._is_data_loaded = False

    def _load_data(self):

        if self._is_data_loaded: return

        fpath = RealStationData.generate_file_path(self._dpath, self._num)
        fv.check_fpath(fpath, 'station')

        try:
            data = np.loadtxt(fpath)
            self._is_data_loaded = True
            self._vars['n'].data, _ = data.shape
            self._vars['t'].data  = data[:,0]
            self._vars['eta'].data = data[:,1]
            self._vars['u'].data   = data[:,2]
            self._vars['v'].data   = data[:,3]

        except Exception as e:
            msg = "Could not read station file '$s'. See traceback for more details." % fpath
            raise FunException(msg, e)


    def _set_t(self)  : self._load_data()
    def _set_eta(self): self._load_data()
    def _set_u(self)  : self._load_data()
    def _set_v(self)  : self._load_data()
    def _set_n(self)  : self._load_data()

class VirtualStationData(StationData):
    
    """
    Class for handling virtual station locations. Interpolates data from four neighboring stations data using
    bi-linear interpolation.   
    """
    #   Index Mapping
    #   3 ———————— 2    (0,1) —————— (1,1)
    # ↑ │          │      │            │
    # y │  Station │      │  Indices   │
    # ↑ │          │      │            │
    #   0 ———————— 1    (0,0) —————— (1,0)
    #       → x →
    def __init__(self, x0, y0, stations):
        
        self._stations = stations

        s00 = stations[0] 
        s10 = stations[1]
        stations[2]
        s01 = stations[3]

        dx = x0/(s10.x - s00.x)
        dy = y0/(s01.x - s00.y)
        dxdy = dx*dy

        a00 = 1 - dx - dy + dxdy
        a10 = dx - dxdy
        a01 = dy - dxdy
        a11 = dxdy  
    
        self.a = [a00, a10, a11, a01]


    def _interpolate_variable(self, var_name):
        
        val = 0
        for a, s in zip(self._a, self._stations):
            val += a*getattr(s, var_name) 

        return val

    def _interpolate_function(self, func_name, **kwargs):
        
        val = 0
        for a, s in zip(self._a, self._stations):
            val += a*getattr(s, func_name)(**vargs)

        return val 

    def _set_eta(self):
         self._vars['eta'] = self._interpolate_variable(self, 'eta') 



class Stations(Sequence, Iterator):


    """
    Class for a collection of Stations and parsing/generating FUNWAVE station file.

    :param stations: list of stations
    :type stations: list 
    """ 
    def __init__(self, stations):

        fv.check_subclasses(stations, Station, 'stations')
        self._list = stations
        self._map = {s.number: i for i, s in enumerate(stations)}

    def __getitem__(self, i):
        return self._list[i]

    def __len__(self):
        return len(self._list)    

    def __iter__(self):
        return self._list.__iter__()

    def __next__(self):
        return self._list.__next__()

    @classmethod 
    def from_file(cls, fpath, dpath, x, y, nums=None, bathy=None):
        """Class method instantiating class from a FUNWAVE station file
    
        """
        fv.check_fpath(fpath, 'stations')
        
        try:
            data = np.loadtxt(fpath, dtype='int')
            
        except Exception as e:
            msg = "Could not read stations file '$s'. See traceback for more details." % fpath
            raise FunException(msg, e)
            
        idxs = list(zip(data[:,0], data[:,1]))


        if nums is None:
            nums = list(range(1, len(idxs) + 1))
        else:
            n = len(nums)
            nums = np.unique(nums)
            if not n == len(nums): warnings.warn( 'Removing repeated station numbers.')                
            idxs = [idxs[n-1] for n in nums]

        #self._map = {num:i for i, num in enumerate(nums)}

        stas_list = [RealStationData(i, j, x, y, num, dpath) for (i,j), num in zip(idxs, nums)]
        stas_obj = Stations(stas_list)
        
        if not bathy is None: stas_obj.get_depths(bathy)
        return  stas_obj

    def _at(self, num):
        return self._list[self._map[num]]
        
    def at(self, nums):
        """Get subset of stations by station numbers 
        """
        return [self._at(i) for i in nums]

    def extract(self, nums):
        return Stations(self.at(nums)) 

    def to_file(self, fpath):
        """Generates a FUNWAVE station file station list

        :param fpath: Path to output file
        :type fpath: str
        """
        raise NotImplementedError("ADD")

    def get_depths(self, bathy):
        """Get station depths from bathymetry data

        :param bathy: Bathymetry data
        :type bathy: np.array 
        """
        fv.check_ndarray(bathy, 2, 'bathy')

        n, m = bathy.shape        
        i, j = list(zip(*self.indices))
        i, j  = np.max(i), np.max(j)
        
        msg = "Bathymetry data appears to be invalid, maximumn %s index of stations is %d and out of range of bathymetry %s length, %d."
        if i >= m: raise FunException(msg % ('x', i, m, 'x'), IndexError)
        if j >= n: raise FunException(msg % ('y', i, m, 'y'), IndexError)

        for s in self: s._get_depth(bathy)

    def update_grid(self, x, y):

        """ Updates stations index location with closest grid points

        :param x: Array of x grid locations
        :type x: list
        :param y: Array of y grid locations
        :type y: list     
        """

        for station in self._list: station.update_grid(x, y)


    @property
    def list(self):
        """List of stations"""
        return self._list

    @property
    def x(self):
        return [s.x for s in self]

    @property 
    def y(self):
        return [s.y for s in self]

    @property
    def locations(self):
        """Tuple list of station locations"""
        return [(s.x, s.y) for s in self]
    
    @property
    def numbers(self):
        """List of station numbers"""
        return [s.number for s in self]

    @property
    def indices(self):
        """Tuple list of station location indices"""
        return [(s.i, s.j) for s in self]
    
    @property
    def h(self):
        """List of station depths"""
        return [s.h for s in self]
