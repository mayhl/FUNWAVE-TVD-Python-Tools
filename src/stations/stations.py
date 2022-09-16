
from funwavetvdtools.error import FunException
import numpy as np
import os 

class Station():
    
    def __init__(self, output_dir, number, i, j, dx, dy, bathy=None):


        self._fpath = Station.get_file_path(output_dir, number)
        self._number = number 
 
        self._i = i
        self._j = j

        self._x = (i-1)*dx
        self._y = (j-1)*dy

        self._is_data_loaded = False

        self._t = None
        self._u = None
        self._v = None
        self._eta = None
        self._h = None

        if bathy is not None:
            self._h = bathy[j-1,i-1]

    def _check_args(self):
        pass

    @classmethod
    def get_file_path(cls, output_dir, index):
        
        fname = "sta_%04d" % index
        fpath = os.path.join(output_dir, fname)
        return fpath

    def _load_data(self):

        fpath = self._fpath

        if not os.path.exists(fpath):
           brief = "File Not Found"
           desc  = "Could not load station data as file '%s' can not be found." % fpath 
           raise FunException(title, desc)

        try:
            data = np.loadtxt(fpath)
            self._is_data_loaded = True

            self._t   = data[0,:]
            self._eta = data[1,:]
            self._u   = data[2,:]
            self._v   = data[3,:]

        except Expception as e:
            brief = 'File Read Error'
            desc = "Could not read station file '$s'. See traceback for more details." % fpath 
            raise FunException(brief, desc, e)

    @property
    def eta(self):
        if not self._is_data_loaded: self._load_data()
        return self._eta

    @property
    def u(self):
        if not self._is_data_loaded: self._load_data()
        return self._u

    @property
    def v(self):
        if not self._is_data_loaded: self._load_data()
        return self._v

    @property
    def t(self):
        if not self._is_data_loaded: self._load_data()
        return self._t

    @property
    def number(self):
        return self._number

    @property
    def i(self):
        return self._i

    @property
    def j(self):
        return self._j

    @property
    def h(self):
        if h is None:
            brief = 'Station depth was not set.'
            desc = "Can not access station depth. No batheymetry files was passed to class constructor." 
            raise FunException(brief, desc, e)

        return h

class Stations():

    def __init__(self, file_path, output_dir, dx, dy, stations_numbers=None, bathy=None):
        
        idxs = self._read_file(file_path)

        if stations_numbers is None:
            idxs = list(enumerate(idxs))
        else:
            idxs = [ (n, idxs[n]) for n in station_numbers]

        self._initialize_stations(file_path, output_dir, dx, dy, idxs, bathy)        

        
    def _read_file(self, fpath):
        
        if not os.path.exists(fpath):
           brief = "File Not Found"
           desc  = "Could not load stations file '%s' it does not exists." % fpath
           raise FunException(title, desc)

        try:
            data = np.loadtxt(fpath)

        except Expception as e:
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

    @property
    def list(self):
        return self._list


    @property
    def locations(self):
        return [ (s.x, s.y for s in self.list) ]

    @property
    def numbers(self):
        return [s.number for s in self.list]

    @property
    def indices(self):
        return [(s.i, s.j) for s in self.list]

class Profile(Stations):

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
        if args not is None: return args

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
        if args not is None: return args

        a = np.stack([ np.ones(2) , dv ])
        b = np.zeros(2); b[0] = 1 
        args = _try_linalg_solve(a, b)
        if args not is None: return args
 
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

        if xl > yl;
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

