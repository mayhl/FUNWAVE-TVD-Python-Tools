from funwavetvdtools.grid.common import Type, Grid, classproperty
from funwavetvdtools.grid.variable import Variable
from funwavetvdtools.grid.filter import Index as IdxFilt
import numpy as np
from scipy.spatial import KDTree
import warnings

class Scatter(Grid):
    
    def create_kd_tree(self):    
        if (self._is_kdtree):
            warning.warn('KD Tree already created.')
            return
       
        pts = np.vstack([self.x, self.y]).T 
        self._kdtree = KDTree(pts)
        self._is_kdtree = True

    @property
    def is_kdtree(self): return self._is_kdtree 

    @classproperty
    def type(self): return Type.SCATTER

    @classmethod
    def from_raw(cls, raw_data, create_kd_tree=False):

        x = Variable(raw_data[:,0], 'x')
        y = Variable(raw_data[:,1], 'y')

        _, n = raw_data.shape

        if n==2:
            data = None  
        elif n==3:
            data = Variable(raw_data[:,2], 'z')
        else:
            data = [Variable(raw_data[:,i], 'z%d' % (i-2)) for i in range(2,n)] 

        return cls(x, y, data, create_kd_tree=False)     


    def __init__(self, x, y, variables=None, create_kd_tree=False):

        if not type(x) is Variable: raise Exception("ADD ERROR")
        if not type(y) is Variable: raise Exception("ADD ERROR")
       
        if not x.is_same_size(y): raise Exception("ADD ERROR")

        self._npts = x.shape[0]

        super().__init__(x, y, variables)
        
        self._kdtree = None
        self._is_kdtree = create_kd_tree
        if (self._is_kdtree): self.create_kd_tree()


    @property
    def shape(self): return (self._npts,)
    
    @property
    def npts(self): return self._npts

    @staticmethod
    def __crop_naive(x, y, n, x0, x1, y0, y1):
        filt_x = (x0 <= x) & (x <= x1)
        filt_y = (y0 <= y) & (y <= y1)
        return IdxFilt(filt_x * filt_y)

    def _crop_naive(self, x0, x1, y0, y1):
        return Scatter.__crop_naive(self.x, self.y, self.npts, x0, x1, y0, y1)

    def _crop_kdtree(self, x0, x1, y0, y1):

        # Creating ball containing bounding box        
        xc = (x1+x0)/2
        yc = (y1+y0)/2
        xl = x1-x0
        yl = y1-y0
        r = max(xl,yl)/np.sqrt(2)

        # Filter points in ball using kd tree method
        idxs = np.array(self._kdtree.query_ball_point((xc,yc), r))
        
        # Using naive method to crop points to remove points
        # in ball but outside bounding box
        x = self.x[idxs]
        y = self.y[idxs]
        n = len(x)
        filt = Scatter.__crop_naive(x, y, n, x0, x1, y0, y1) 

        return IdxFilt(filt.filter(idxs))

    def crop(self, x0, x1, y0, y1):

        # NOTE: Add flag to default to naive or check (if possible)
        #       to switch to naive method if faster, e.g.,
        #        crop box is nearly the size of bouding box 
        if self._is_kdtree:
            filt = self._crop_kdtree(x0, x1, y0, y1)
        else:
            filt = self._crop_naive(x0, x1, y0, y1)

        sub_x = self._x.filter(filt)
        sub_y = self._y.filter(filt)
        sub_vars = None if not self.has_vars else [var.filter(filt) for var in self.vars]
        return Scatter(sub_x, sub_y, sub_vars)


        
    def bounding_box(self, padding=None, pad_ratio=None):
        return self._bounding_box(self.x.min(), self.y.max(),
                                  self.y.min(), self.y.max(),
                                  padding, pad_ratio)




