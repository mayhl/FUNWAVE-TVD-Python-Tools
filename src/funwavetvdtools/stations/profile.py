
from funwavetvdtools.error import FunException
import funwavetvdtools.validation as fv

import funwavetvdtools.stations.runup as ru
import funwavetvdtools.stations.overtopping as ot
from funwavetvdtools.stations.stations import Stations

import numpy as np
from shapely import Polygon, LineString

class Profile(Stations):

    def _check_profile_stations(self):
    
        i_idxs, j_idxs = zip(*self._raw.indices)
        iL = max(i_idxs) - min(i_idxs)
        jL = max(j_idxs) - min(j_idxs)

        if jL > 0 and iL > 0:
            msg = "Can not generate stations profile in mode 'stations' as stations points " \
                   "not aligned in the x or y axis. "
            raise FunException(msg, ValueError)

        x, y = zip(*self._raw.locations)
        x = list(x)
        y = list(y)


        is_x_prof = iL > 0
        s = x if is_x_prof else y
            
        diff = np.diff(s)

        if not (np.all(diff>0) or np.all(diff<0)):
            msg = "Can not generate stations profile in mode 'stations' as stations locations are not strictly " \
                   "increasing or decreasing in the %s direction." % ( 'x' if is_x_prof else "y") 
            raise FunException(msg, ValueError)

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
            desc = "The number of dimensions in input argument numbers must be 1, got '%s'." % ndims
            raise FunException(msg, ValueError)

        self._raw = copy.copy(stations)
        self._raw._list = [ stations.list[n-1] for n in numbers]

        if mode == 'stations':
            self._check_profile_stations()
        elif mode == 'best':
            self._check_profile_best()
        elif mode == 'specifed':
            self.__check_profile_specifed(s)
        else:
            msg = "Invalid mode '%s' selected. Valid modes are 'stations', 'best', 'specifed']." % mode
            raise FunException(msg, ValueError)


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


class UnitRectangle:

    def __init__(self, x, i, y, j):
        self._i = i
        self._j = j

        x1, x2 = x[i], x[i+1]
        y1, y2 = y[j], y[j+1]
        self._poly = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])

    def intersects(self, geo):
        return self._poly.intersects(geo)

    @property
    def sw_vertex(self): return i, j

    @property
    def vertices(self):
        i, j = self._i, self._j
        # Note: Numpy dtype required for concatenate to persevere tuples 
        return np.array([(i, j), (i+1, j), (i+1, j+1), (i, j+1)], dtype=np.dtype('int, int'))


def _get_outer_indices(s, s1, s2):
    i1 = np.argmin(np.abs(s-s1))
    if s[i1] > s1: i1 -= 1
    i2 = np.argmin(np.abs(s-s2))
    if s[i2] < s2: i2 += 1
    return i1, i2

def generate_stations(x, y, x1, x2, y1, y2):

    # Computing grid indices that bound  line/profile 
    i1, i2 = get_outer_indices(x, x1, x2)
    j1, j2 = get_outer_indices(y, y1, y2)
    
    # Generating Polygon rectangles of each grid sqaure
    idxs = np.concatenate([np.array([(i, j) for i in range(i1, i2)]) for j in range(j1, j2)])
    rects = [UnitRectangle(x, i, y, j) for i, j in idxs]

    # Filtering out grid rectangles that contain line 
    line = LineString([(x1, y1), (x2, y2)])
    rects = [rect.vertices for rect in rects if rect.intersects(line)]
 
    sw_idxs = [rect.sw_vertex for rect in rects]

    # Removing duplicate station indices 
    sta_idxs = np.unique(np.concatenate([rect.vertices for rect in rects))

    return sta_idxs, sw_idxs


