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
from funwavetvdtools.waves.dispersion import full as wn

import numpy as np




def _check_args(x, h, eta, r_depth=None):
    pass


    # frequency limits
    #   equation (7), Goda 76
# NOTES:
#  1) Stations at different depths?



def compute(eta1, eta2, dl, dt, h, f_min=0.05, f_max=0.45):
    '''
    reflection() returns reflection statistics given two eta time series
    parameters:
    eta1    (numpy.array): time series for eta at x1
    eta2    (numpy.array): time series for eta at x2
    dl      (float): distance between x1, x2
    h       (float): water depth
    **kwargs:
    f_min =     (int): minimum resolvable frequency
    f_max =     (int): maximum resolvable frequency
    return
    a_i     (numpy.array): amplitude of incident wave as frequency series
    a_r     (numpy.array): amplitude of reflected wave as frequency series
    e_i     (float): energy of incident wave
    e_r     (float): energy of reflected wave
    K_r     (float): coefficient of reflection
    '''


    n1 = len(eta1)    
    n2 = len(eta2)

    if not n1 == n2:
        brief = "Invalid Input Arguments"
        desc = "The lengths of arrays eta1 and eta2 must be the same."
        raise FunException(brief, desc)

    n = n1
    if not n % 2 == 0:
        n -= 1
        eta1 = eta1[:n]
        eta2 = eta2[:n]

    nhalf = n//2

    # FFT of eta1, eta2, normalized relative to N/2
    ETA1 = np.fft.fft(eta1, n) / nhalf
    ETA2 = np.fft.fft(eta2, n) / nhalf

    # init A1, A2, B1, B2 by collecting sin/cos and truncating
    #   half time-series due to symmetry 
    A1 = np.real(ETA1[0:nhalf])
    B1 = np.imag(ETA1[0:nhalf])
    A2 = np.real(ETA2[0:nhalf])
    B2 = np.imag(ETA2[0:nhalf])

    w = (2*np.pi/dt/n)*np.arange(1, nhalf+1)
    k = np.array([wn(w=wi, h=h)['k'] for wi in w])


    # amplitude calculation
    # equation (5), Goda 76

    cosk = np.cos(k*dl)
    sink = np.sin(k*dl)

    sqr1 = A2 - A1*cosk - B1*sink
    sqr2 = B2 + A1*sink - B1*cosk
    sqr3 = A2 - A1*cosk + B1*sink
    sqr4 = B2 - A1*sink - B1*cosk

    den = 2*np.abs(sink)
    a_r = np.sqrt(np.square(sqr1) + np.square(sqr2))/den
    a_i = np.sqrt(np.square(sqr3) + np.square(sqr4))/den

    idx = (den == 0)
    a_r[idx] = np.NaN
    a_i[idx] = np.NaN

    # array limits
    i_min = int(np.ceil(f_min * n * dt))       # lower bound
    i_max = int(f_max * n * dt)             # upper bound

    w = w[i_min:i_max]
    a_i = a_i[i_min:i_max]
    a_r = a_r[i_min:i_max]

    # energy calculation, bounded by above limits
    #   equation (8), Goda 76
    e_i = np.sum(np.square(w) * np.square(a_i) / 2)
    e_r = np.sum(np.square(w) * np.square(a_r) / 2)
  
    f = w/(2*np.pi) 
    e_i = np.trapz(np.square(a_i), f)
    e_r = np.trapz(np.square(a_r), f)
 
    # coefficent of reflection calculation
    #   equation (9), Goda 76ç
    K_r = np.sqrt(e_r / e_i)

    f = w/(2*np.pi)

    return f, a_i, a_r, e_i, e_r, K_r







