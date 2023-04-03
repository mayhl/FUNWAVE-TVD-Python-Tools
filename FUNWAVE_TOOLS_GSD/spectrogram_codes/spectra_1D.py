# Could add filtering in frequnecy domain fucntion
# Could add function to find the inverse after filtering 
# -------------- IMPORT LIBRARIES
import numpy as np
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt
# -------------- DEFINE 1D Spectra Functions 
def compute_spectra_1D(input_signal, fs):
    ''' Applies the Fast Fourier Transform (FFT) to provided input signal.
  
    :param input_signal:         Continous timeseries input signal.
    :type  input_signal:         ndarray
    :param fs:           Input signal sampling frequency.
    :type  fs:           float
    '''
    # 1. Create Time Vector For Input Data 
    duration = len(input_signal)
    dt = 1/fs # time difference between consecutive samples
    t = np.arange(0,duration,dt) # time
    # 2. Detrend Signal
    input_signal = sp.signal.detrend(input_signal) # detrending data
    # 3. Create Frequency Vector
    N = len(input_signal) # lenght of TS
    df = fs/N # frequency difference beteen consecutive samples
    f = np.arange(0,fs/2+df,df) # freq vector from 0 to fs/2 Hz, equally spaced at df
    # 4. Apply Fast Fourier Transform (FFT)
    signal_fft = np.fft.fft(input_signal) # From f = 0Hz to f = fs Hz
    # of the water surface elevation from f = 0Hz to fNY = fs/2 Hz"""
    signal_fft = signal_fft[0:len(f)] # (N/2+1) elements if N is even; (N+1)/2 elements if N is odd 
    # Half of the two sided power spectral density (psd) from f = 0Hz to fNy=fs/2 Hz
    psd_2_sided=(1/(N*fs))*(np.absolute(signal_fft))**2 # calculating psd using fs in (m^2/Hz)
    # one psd density from f = 0Hz to fNy=fs/2 Hz
    psd_1_sided=psd_2_sided.copy()
    psd_1_sided[0:-1]= 2.*psd_1_sided[0:-1] 
    # ^ onde-sided-spectrum = 2 * two-sided-spectrum in (m^2/Hz)
    # Return Values
    return f, psd_1_sided

def plot_spectra_1D(input_signal, time_vector, f, psd_data, y_label, y_units):
    ''' Plots 1 sided Power Spectrum Density (PSD) plot and signal used to create PSD.
  
    :param input_signal:         Continous timeseries input signal used to compute PSD.
    :type  input_signal:         ndarray
    :param time_vector:         Continous timeseries input signal used to compute PSD time vector.
    :type  time_vector:         ndarray
    :param f:           Input signal 1 sided power spectrum frequency vector.
    :type  f:           ndarray
    :param psd_data:           Input signal 1 sided power spectrum.
    :type  psd_data:           ndarray
    :param y_label:           Y label for continous timeseries input data plot.
    :type  y_label:           str
    :param y_units:           Units for continous timeseries input data.
    :type  y_units:           ndarray
    '''
    # plotting WSE
    plt.figure(1)
    plt.plot(time_vector,input_signal)
    plt.title('WSE')
    plt.xlabel('time (sec)')
    plt.ylabel([y_label + ' (' + y_units + ')'])
    plt.xlim(time_vector[0],time_vector[-1])

    # plotting psd
    plt.figure(2)
    plt.semilogy(f,psd_data)
    plt.title('PSD')
    plt.xlabel('Freq (Hz)')
    plt.ylabel(['Power/Freq (' + y_units + '^2/Hz)'])
    plt.ylim(psd_data.min(),psd_data.max())
    plt.xlim([f[0],f[-1]])


    #------------------------------
freq = 0.2 # frequency
duration = 1024 # total duration of the TS, duration = N*dt
fs = 2 # sampling frequency
"""Step 1: generating a time vector from 0 to (duration - dt), equally spaced"""
dt = 1/fs # time difference between consecutive samples
t = np.arange(0,duration,dt) # time

"""Step 2: generating a water surface TS with an amplitude of -.5m  and a frequency
of 0.2Hz (period = 5sec)"""
Eta = 0.5*np.cos(2*np.pi*freq*t)
rnd = 0.01+(0.1-(-0.1))*np.random.rand(len(t)) # uniformly distributed random signal [-0.1m and 0.1m]
Eta = Eta+rnd # adding random signal to sinosoidal signal

# Compute 1 Sided PSD
f, psd_data = compute_spectra_1D(Eta, fs) # Returns f, psd_1_sided
# Plot 1 Sided PSD
plot_spectra_1D(Eta, t, f, psd_data, 'Surface Elevation', 'm')