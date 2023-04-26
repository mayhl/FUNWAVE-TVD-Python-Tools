# Software is under the BSD 2-Clause "Simplified" License, see LICENSE file for further details.

##
# @file runup.py
#
# @ breif
#
# @ section 
#


from funwavetvdtools.error import FunException
import funwavetvdtools.validation as fv
from funwavetvdtools.math.newtonraphson import iterator
from functools import partial

import numpy as np


g = 9.80665

class Wave:

    
    # Wrapper functions for checking if at most one argument is set, i.e., not None.
    # Used for arguments whose values are dependent on the otheres, i.e., setting one
    # determines the others
    @classmethod
    def _check_args(cls, args, names):

        # Getting number of not None arguments
        args_set = np.array(args) != None
        n_args = np.sum(args_set)
        # Return True if one group of arugments is set correctly 
        if n_args == 0: return False
        if n_args == 1: return True


        # Error state if more than one arugment is set
        names = np.array(names)
        names = names[args_set]

        # Formatting names as list
        if n_args == 2: 
            string = "%s and %s" % tuple(names)
        else:
            string = ""
            for name in names[:-1]: string += "%s, " % name
            string += "and %s" % names[-1]

        # Raising exception 
        brief = "Invalid Input"
        desc = "Can not specify %s." % string
        raise FunException(brief, desc)    

    def __init__(self, k=None, w=None, h=None, L=None, T=None, f=None):

        num_args = 0

        # Checking if wavenumber and/or wavelength have been initialized
        args = [k, L]
        names = ['wavenumber', 'wavelength']    
        self._is_k = self._check_args(args, names)
        
        self._L = None
        self._k = None
        if self._is_k:
            num_args += 1 
            if k is not None:
                self.k = k
            else:
                self.L = L
                
        # Checking if angular frequency, frequency, and/or period have been initialized
        args = [w, f, T]
        names = ['angular frequency', 'frequency', 'period']
        self._is_w = self._check_args(args, names)

        self._f = None
        self._w = None
        self._T = None
        if self._is_w:
            num_args +=1
            if w is not None:
                self.w = w
            elif f is not None:
                self.f = f
            else:
                self.T = T
        
        # Checking if h as been initialized
        self._is_h = h is not None
        if self._is_h: num_args += 1
        self._h = h

        if num_args > 2:
            brief = "Invalid Input"
            desc = "Too many wave parameters specified, only 2 required."
            raise FunException(brief, desc)

        if num_args < 2:
            brief = "Invalid Input"
            desc = "Not enough wave parameters specified, only 2 required."
            raise FunException(brief, desc)


    # Wrapper function for raise exception if related variable is set
    @classmethod
    def _set_check(cls, val, val_name, set_name):
        if val is not None:
            brief = "Invalid Assignment"
            desc = "Can not set %s since %s has already been set." % (set_name, val_name)
            raise FunException(brief, desc)


    @property
    def k(self): return self._k
    
    @k.setter
    def k(self, k):
        self._set_check(self._L, 'wavelength', 'wavenumber')
        self._k = k
        self._L = 2*np.pi/k

    @property
    def L(self): return self._L

    @L.setter
    def L(self, L): 
        self._set_check(self._k, 'wavenumber', 'wavelength')
        self._L = L
        self._k = 2*np.pi/L

    @property
    def w(self): return self._w

    @w.setter
    def w(self, w):
        self._set_check(self._f, 'frequency', 'angular frequency')
        self._set_check(self._T, 'period', ' angular frequency')
        
        self._w = w
        self._f = w/2*np.pi
        self._T = 1/self._f
        
    @property 
    def f(self): return self._f


    @f.setter
    def f(self, f):
        self._set_check(self._w, 'angular frequency', 'frequency')
        self._set_check(self._T, 'period', 'frequency')      
    
        self._f = f
        self._T = 1/f
        self._w = 2*np.pi*f
        
    @property 
    def T(self): return self._T
    
    @T.setter
    def T(self, T):
        self._set_check(self._w, 'angular frequency', 'period')
        self._set_check(self._f, 'frequency', 'period')
        
        self._T = T
        self._f = 1/T
        self._w = 2*np.pi*self._f

    @property
    def h(self): return self._h
    
    @h.setter
    def h(self, h):
        if self._h is not None:
            brief = "Invalid Assignment"
            desc = "Can not set h since is already been set."
            raise FunException(brief, desc)
            
        self._h = h


def _f(w, k, h):
    return g*k*np.tanh(k*h) - w**2




def _dfdk(w, k, h): 
    tanh = np.tanh(k*h)
    return g*(tanh + k*h*(1-tanh**2))

def _check_args(k, L, w, T, h):

    num_args = 0
    
    if k is not None and L is not None:
        brief = "Invalid Input"
        desc = "Can not specify both the wavelength and wavenumber."
        raise FunException(brief, desc)
    elif k is None and L is None: 
        is_wave = False
    else:
        is_wave = True
        num_args += 1
        if k is None: k = 2*np.pi/L
        
    if w is not None and T is not None:
        brief = "Invalid Input"
        desc = "Can not specify both the frequency and period."
        raise FunException(brief, desc)
    elif w is None and T is None:
        is_freq = False
    else:
        is_freq = True
        num_args += 1
        if w is None: w = 1/T

    is_h = h is not None
    if is_h: num_args += 1

    if num_args > 2:
        brief = "Invalid Input"
        desc = "Too many wave parameters specified, only 2 required."
        raise FunException(brief, desc)

    if num_args < 2:
        brief = "Invalid Input"
        desc = "Not enough wave parameters specified, only 2 required."
        raise FunException(brief, desc)

    return k, w, h, is_wave, is_freq, is_h


def shallow(k=None, w=None, h=None, L=None, T=None, f=None):

    wave = Wave(k=k, w=w, h=h, L=L, T=T, f=f)

    if wave._is_h and wave._is_w:
        # Compute wavenumber
        wave.k = wave.w/np.sqrt(g*wave.h)
    elif wave._is_h and wave._is_k:
        # Compute freqency
        wave.w = wave.k*sqrt(g*wave.h)

    elif wave._is_w and wave._is_k:
        # Compute depth
        wave.h = (wave.w/wave.k)**2/g
    else:
        # Safety check
        brief = "Unexpected State"
        desc = "Unexpected logic state reached."
        raise FunException(brief, desc)

    return wave


def full(k=None, w=None, h=None, L=None, T=None, f=None, tolerence=10**-8, max_iterations=10):

    wave = Wave(k=k, w=w, h=h, L=L, T=T, f=f)


    if wave._is_h and wave._is_w:
        # Compute wavenumber
        def f(x): return _f(k=x, h=wave.h, w=wave.w)
        def df(x): return _dfdk(k=x, h=wave.h, w=wave.w)
        k0 = shallow(h=wave.h, w=wave.w).k
        wave.k = iterator(k0, f, df)

    elif wave._is_h and wave._is_k:
        # Compute freqency
        wave.w = np.sqrt(_f(0, wave.k, wave.h))

    elif wave._is_w and wave._is_k:
        # Compute depth 
        c = wave.w**2/(g*wave.k)
        wave.h = np.tanh(c)/wave.k
    else:
        # Safety check
        brief = "Unexpected State"
        desc = "Unexpected logic state reached."
        raise FunException(brief, desc)

    return wave

