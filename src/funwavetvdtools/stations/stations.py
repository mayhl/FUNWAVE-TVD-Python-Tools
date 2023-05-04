
from funwavetvdtools.error import FunException
import funwavetvdtools.validation as fv

import numpy as np
import os 
import copy


class Station():
    
    def __init__(self, output_dir, number, i, j, dx, dy, is_bathy_change=False):

        self._fpath = Station.get_file_path(output_dir, number)
        self._number = number 
        
        self._i = int(i)
        self._j = int(j)

        self._x = (i-1)*dx
        self._y = (j-1)*dy

        self._is_data_loaded = False

        self._n = None
        self._t = None
        self._u = None
        self._v = None
        self._eta = None
        self._h = None

        self._is_bathy_change = is_bathy_change
        
    def _check_args(self):
        pass

    @classmethod
    def get_file_path(cls, output_dir, index):
        
        fname = "sta_%04d" % index
        fpath = os.path.join(output_dir, fname)
        return fpath

    def update_bathy(self, bathy, t=None):

        fv.check_ndarray(bathy, 2, 'bathy')
        self._load_data()

        n, m = bathy.shape

        # Move to constructor with additional mglob, nglob checks?
        self._i = fv.convert_max_val_int(self._i, m, 'i')
        self._j = fv.convert_max_val_int(self._j, n, 'j')

        i = self._i
        j = self._j


        if not self._is_bathy_change:
            self._h = bathy[j-1,i-1]
            return 

        raise NotImplementedError

        if t is None:
            brief = 'Invalid Argument'
            
        t = fv.convert_number(t, 't')



    def _load_data(self):

        if self._is_data_loaded: return

        fpath = self._fpath
        fv.check_fpath(fpath, 'station')

        try:
            data = np.loadtxt(fpath)
            self._is_data_loaded = True
            self._n, _ = data.shape
            self._t    = data[:,0]
            self._eta  = data[:,1]
            self._u    = data[:,2]
            self._v    = data[:,3]


        except Exception as e:
            msg = "Could not read station file '$s'. See traceback for more details." % fpath 
            raise FunException(msg, e)

    @property
    def eta(self):
        self._load_data()
        return self._eta

    @property
    def u(self):
        self._load_data()
        return self._u

    @property
    def v(self):
        self._load_data()
        return self._v

    @property
    def t(self):
        self._load_data()
        return self._t

    @property
    def n(self):
        self._load_data()
        return self._n

    @property
    def number(self): return self._number

    @property
    def x(self): return self._x

    @property
    def y(self): return self._y
    
    @property
    def i(self): return self._i

    @property
    def j(self): return self._j

    @property
    def h(self):
        if self._h is None:
            msg = "Can not access station depth. No bathymetry data entered." 
            raise FunException(msg, ReferenceError)

        return self._h
    
    
    def compute_overtoping(self, min_depth, t_min=None, t_max=None):
        return ot.compute_flux(self.t, self.h, min_depth, t_min, t_max)
        
        

class Stations():

    def __init__(self, file_path, output_dir, dx, dy, stations_numbers=None, bathy=None):
       
        self._fpath = file_path 
        idxs = self._read_file()

        if stations_numbers is None:
            idxs = list(enumerate(idxs, start=1))
        else:
            idxs = [ (n, idxs[n]) for n in station_numbers]

        self._initialize_stations(file_path, output_dir, dx, dy, idxs, bathy)        

        
    def _read_file(self):

        fpath = self._fpath
        fv.check_fpath(fpath, 'stations')

        try:
            data = np.loadtxt(fpath)

        except Exception as e:
            msg = "Could not read stations file '$s'. See traceback for more details." % fpath
            raise FunException(msg, e)

        return list(zip(data[:,0], data[:,1]))
        

    def _initialize_stations(self, file_path, output_dir, dx, dy, idxs, bathy):

        stations = []
        for n, (i, j) in idxs:
            station = Station(output_dir, n, i, j, dx, dy, bathy)
            stations.append(station)

        self._list = stations

    def update_bathy(self, bathy, t=None):
        for sta in self._list: sta.update_bathy(bathy, t)

    @property
    def list(self):
        return self._list

    @property
    def locations(self):
        return [(s.x, s.y) for s in self.list]

    @property
    def numbers(self):
        return [s.number for s in self.list]

    @property
    def indices(self):
        return [(s.i, s.j) for s in self.list]

    @property
    def h(self):
        return [s.h for s in self.list]





