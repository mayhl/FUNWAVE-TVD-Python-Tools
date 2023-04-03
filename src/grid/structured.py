

from funwavetvdtools.grid import common as gc
from funwavetvdtools.grid.common import Type, Grid, classproperty
from funwavetvdtools.grid.filter import Slice as SlcFilt

from scipy.spatial import KDTree
import numpy as np

from abc import abstractmethod
from collections import namedtuple
import warnings

class Structured(Grid):

    def __init__(self, x, y, variables=None):

        self._nx = len(x.data)
        self._ny = len(y.data)
   
        super().__init__(x, y, variables)

    @classproperty
    def type(self): return Type.STRUCTURED
    
    @property
    def nx(self): return self._nx

    @property
    def ny(self): return self._ny

    @property
    def npts(self): return self._nx*self._ny

    @property
    def shape(self): return (self.ny, self.nx)

    @staticmethod
    def get_index_range(s, s0, s1):
        i0 = np.argmin(np.abs(s - s0))
        if s[i0] < s0: i0 += 1
        i1 = np.argmin(np.abs(s- s1))
        if s[i1] > s1: i1 -= 1
        #NOTE: +1 to include i1 in slice
        return i0, i1+1
        
    def crop(self, x0, x1, y0, y1):

        filt_x = SlcFilt(*Structured.get_index_range(self.x, x0, x1))
        filt_y = SlcFilt(*Structured.get_index_range(self.y, y0, y1))

        sub_x = self.x_var.filter(filt_x)
        sub_y = self.y_var.filter(filt_y)

        filt_y.append(filt_x)
        filt = filt_y

        sub_vars = None if not self.has_vars else [var.filter(filt) for var in self.vars]

        return Structured(sub_x, sub_y, sub_vars)        


    def bounding_box(self, padding=None, pad_ratio=None):
        return self._bounding_box(self.x[0], self.x[-1], 
                                  self.y[0], self.y[-1],
                                  padding, pad_ratio)

class Node(Structured):

    __Indices = namedtuple('Indices', ['i0', 'i1', 'j0' , 'j1'])
    def __init__(self, x, y, idxs, parent, variables=None):

        self._parent = parent

        self._idxs = None if idxs is None else Node.__Indices(*idxs)
        self._children = None

        self._level = 0 if parent is None else parent.level+1

        super().__init__(x, y, variables)


    @property
    def parent(self): return self._parent

    @property
    def idxs(self): return self._idxs

    @property
    def children(self): return self._children

    @property
    def has_children(self): return not self.children is None

    @property
    def level(self): return self._level

    @abstractmethod
    def child_iter(self): pass

    # DEV NOTE: Check memory usage
    def clear_children(self): 

        if not self.has_children: 
            raise Exception('Can not clear children as grid does not have any')
        self._children = None

    def are_children_metadata_consistent(self):

        if not self.has_children:
            raise Exception('Can not check children metadata as grid does not have any')

        c_iter = self.child_iter()
        fchild = next(c_iter)

        for nchild in c_iter:
            if not fchild.has_same_metadata(nchild): return False 
        
        # All children has same metadata
        return True


class SubdividedStructured(Node):

    def __init__(self, x, y, idxs=None, parent=None, variables=None):
        super().__init__(x, y, idxs, parent, variables)

    @classmethod
    def convert_structured(cls, old):
        return SubdividedStructured(old.x_var, old.y_var, variables=old.vars)

    def child_iter(self):
        if not self.has_children:
            raise Exception('Can not create iterator on children since grid does not have any')

        return iter(self.children.flatten())

    def equi_subdivide(self, n_pts=100):

        # NOTE: Probably not necessary to allow further subdivisions 
        if not self.level == 0:
            raise Exception("Can not subdivided a child grid.")
    
        nx = self.nx
        ny = self.ny

        mx = int(np.ceil(nx/n_pts))
        my = int(np.ceil(ny/n_pts))

        idxs_x = gc.even_divide_range(nx, mx)
        idxs_y = gc.even_divide_range(ny, my)

        is_nested_grid = False

        self._children = np.empty([my,mx]).astype(SubdividedStructured)
        list = [None]*(mx*ny)

        # Initializing x filters to avoid redundant reinitialization 
        filts_x = [SlcFilt(i0, i1) for i0, i1 in idxs_x]


        for y, (j0, j1) in enumerate(idxs_y):

            filt_y = SlcFilt(j0,j1)
            sub_y = self.y_var.filter(filt_y)

            for x, ((i0, i1), filt_x) in enumerate(zip(idxs_x, filts_x)):

                sub_x = self.x_var.filter(filt_x)

                if not self.has_vars:
                    sub_data = None
                else:
                    filt = SlcFilt(filt_y, filt_x)
                    sub_data = [var.filter(filt) for var in self.vars]

                idxs = (i0, i1, j0, j1)
                self._children[y,x] = SubdividedStructured(sub_x, sub_y, idxs, self, sub_data)

        return self._children


    def copy_children_vars(self, is_clear_children=True):

        if not self.has_children:
            raise Exception("Grid does not have child grids to copy data from")

        if not self.are_children_metadata_consistent():
            raise Exception("Can not copy data from child grids as their metadata are inconsistent")

        # DEV NOTE: Add x,y metadata comparison?
        # Comparing child metadata t
        child = self.children[0,0]
        if self.has_vars:
            if not self.has_same_metadata(child):
                raise Exception('Can not copy data from child grids as grid metadata is inconsistent with children')

        else:
            # Copying variables metadata from children 
            nx = len(self.x)
            ny = len(self.y)

            variables = [var.create_metadata_copy(np.zeros([ny,nx])) for var in child.vars]
            self._add_variables(variables)

        # DEV NOTE: Test which loop ordering is faster 
        # Copying data from children
        for var_name in self.var_names:

            var = getattr(self.vars, var_name)
            for child in self.child_iter():
                i0, i1, j0, j1 = child.idxs
                var._data[j0:j1,i0:i1] = getattr(child.data, var_name)
                
        
        if is_clear_children: self.clear_children()


        
        




 



