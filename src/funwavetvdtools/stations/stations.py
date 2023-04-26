
from funwavetvdtools.error import FunException
import funwavetvdtools.validation as fv

import funwavetvdtools.stations.runup as ru

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
            brief = 'File Read Error'
            desc = "Could not read station file '$s'. See traceback for more details." % fpath 
            raise FunException(brief, desc, e)

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
            brief = 'Station depth was not set.'
            desc = "Can not access station depth. No batheymetry files was passed to class constructor." 
            raise FunException(brief, desc, e)

        return self._h

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
            brief = 'File Read Error'
            desc = "Could not read stations file '$s'. See traceback for more details." % fpath
            raise FunException(brief, desc, e)

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


class Profile(Stations):

    def _check_profile_stations(self):
    
        i_idxs, j_idxs = zip(*self._raw.indices)
        iL = max(i_idxs) - min(i_idxs)
        jL = max(j_idxs) - min(j_idxs)

        if jL > 0 and iL > 0:
            brief = "Can Not Generate Stations Profile"
            desc = "Can not generate stations profile in mode 'stations' as stations points " \
                   "not aligned in the x or y axis. "
            raise FunException(brief, desc)

        x, y = zip(*self._raw.locations)
        x = list(x)
        y = list(y)


        is_x_prof = iL > 0
        s = x if is_x_prof else y
            
        diff = np.diff(s)

        if not (np.all(diff>0) or np.all(diff<0)):
            brief = "Can Not Generate Stations Profile"
            desc = "Can not generate stations profile in mode 'stations' as stations locations are not strictly " \
                   "increasing or decreasing in either the %s direction." % ( 'x' if is_x_prof else "y") 
            raise FunException(brief, desc)

        self._s = s
        self._list = self._raw._list
 
    def _check_profile_best(self):
        raise NotImplementedError

    def _check_profile_specifed(self, s):
        raise NotImplementedError


    def __init__(self, stations, numbers, mode='stations', profile_pts=None):

        fv.check_type(stations, Stations, 'stations')
        numbers = fv.convert_pos_def_ints(numbers, 'numbers')

        ndims = numbers.ndim 
        if ndims != 1:
            brief = "Invalid Argument" 
            desc = "The number of dimensions in input argument numbers must be 1, got '%s'." % ndims
            raise FunException(brief, desc)

        self._raw = copy.copy(stations)
        self._raw._list = [ stations.list[n-1] for n in numbers]

        if mode == 'stations':
            self._check_profile_stations()
        elif mode == 'best':
            self._check_profile_best()
        elif mode == 'specifed':
            self.__check_profile_specifed(s)
        else:
            brief="Invalid Stations Profile Mode"
            desc="Invalid mode '%s' selected. Valid modes are 'stations', 'best', 'specifed']." % mode
            raise FunException(brief, desc)


    def _prep_runup_input(self):

        x = self._s
        h = self.h
        nt = self.list[0].n
        ns = len(self.list)
        eta = np.zeros([ns, nt])
        for i in range(ns): eta[i,:] = self.list[i].eta

        return x, h, eta 

    def compute_runup(self):

        x, h, eta = self._prep_runup_input()
        return ru.compute(x, h, eta)

    def compute_runup_with_stats(self):
        x, h, eta = self._prep_runup_input()
        return ru.compute_with_stats(x, h, eta)


class Profile2(Stations):

    def __init__(self, stations, dx, dy):
        
        self._raw = stations
        u, v, ui, vi, are_flipped = self._compute_linear_best_fit(self, dx, dy)
        

    def _try_linalg_solve(selfa, b):
        try:
            coeffs = np.linalg.solve(a, b)
        except np.linalg.LinAlgError: pass
        except Exception as e:
            brief = 'test'
            desc = 'test'
            raise FunException(brief, desc, e)
        else:
            return idxs, coeffs
            
    def _compute_interpolate_scheme( xi, yi, x, y):

        dx = x - xi
        dy = y - yi

        ds = np.sqrt(dx**2 + dy**2)

        idxs = np.argsort( ds )[0:3]

        a = np.stack([ np.ones(3) , dx[idxs] , dy[idxs] ])
        b = np.zeros(3); b[0] = 1
        args = _try_linalg_solve(a, b)
        if not args is None: return args

        idxs = idxs[0:-1]

        mean_dx = np.mean(np.abs(dx[idxs]))
        mean_dy = np.mean(np.abs(dy[idxs]))
    
        if mean_dx < mean_dy:
            du, dv = dx[idxs], dy[idxs]  
        else:
            du, dv = dy[idxs], x[idxs]

        a = np.stack([ np.ones(2) , du ])
        b = np.zeros(2); b[0] = 1
        args = _try_linalg_solve(a, b)
        if not args is None: return args

        a = np.stack([ np.ones(2) , dv ])
        b = np.zeros(2); b[0] = 1 
        args = _try_linalg_solve(a, b)
        if not args is None: return args
 
        coeffs = [1]
        idxs   = idx[0:-1]
        idxs, coeffs


    def _compute_linear_best_fit(self, dx, dy):

        def get_bounds_and_length(s):
            s0, s1 = min(s), max(s)
            sl = s0-s1

        x, y = zip(*self._raw._locations)
        x0, x1, xl = get_bounds_and_length(x)
        y0, y1, yl = get_bounds_and_length(y)

        if xl > yl:
            are_flipped = False
            u0, u1, ul = x0, x1, xl
            v0, v1, vl = y0, y1, yl
            u, v  = x, y
            du = dx

        else:
            are_flipped = True
            u0, u1, ul = y0, y1, yl
            v0, v1, vl = x0, x1, xl
            u, v  = y, x
            du = dy
        
        sl = np.sqrt( xl**2 + yl**2)
        m, c = np.polyfit(u, v, 1)

        sl = np.sqrt( ul**2 + vl**2)
        ds = du*np.sqrt(1 + m**2)

        n = sl//ds

        ui = np.linspace(u0, u1, n)
        vi = m*u + c

        return u, v, ui, vi, are_flipped

        self._u = u
        self._v = v
        self._du = du
        self._dv = dv
        self._is_flipped = is_flipped


def _try_linalg_solve(a, b):

    try:
        coeffs = np.linalg.solve(a, b)

    except np.linalg.LinAlgError: pass

    except Exception as e:
        brief = 'test'
        desc = 'test'
        raise FunException(brief, desc, e)

    else:
        return idxs, coeffs

    finally:
        return None

