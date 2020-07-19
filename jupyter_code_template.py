"""
Daniel Maidment
maidment.daniel@gmail.com
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
import time
import pandas as pd
import scipy.io
import scipy.signal as signal
import scipy.linalg as linalg
import warnings
from numpy import pi
from numpy import cos
from numpy import sin
from numpy import log10
from numpy import log
from numpy import real
from numpy import imag
from numpy import sqrt
from numpy import e
from numpy import abs
from numpy import angle
from numpy.fft import fft
from numpy.fft import ifft
from numpy.fft import fftshift
from numpy import min
from numpy import max
from numpy import sum
from numpy.linalg import norm
from numpy import dot
from sklearn.preprocessing import normalize
from latex_envs.latex_envs import figcaption

"""#########################################################################"""

# $\renewcommand{\vec}{\mathbf}$
# $\newcommand{\x}{\vec{x}}$
# $\newcommand{\s}{\vec{s}}$
# $\renewcommand{\phi}{\varphi}$
# $\newcommand{\R}{\mathbb{R}}$
# $\newcommand{\y}{\vec{y}}$
# $\newcommand{\v}{\vec{v}}$
# $\newcommand{\A}{\vec{A}}$
# $\newcommand{\w}{\;\!}$

# \begin{equation}
#     \x,\R, \s, \phi, \Phi, \y, \Psi, \v, \A
# \end{equation}

#for Jupyter Notebook inline plots
# %matplotlib inline

"""#########################################################################"""
#C:\Users\Purco\Anaconda3\Lib\site-packages\matplotlib\mpl-data\stylelib
#plt.style.use('report_2_color')
# plt.style.use('report_2_grey')
# plt.style.use('jupyter_grey')
# plt.style.use('jupyter_color')
# plt.style.use('dark_background')# for dark Themes
#plt.style.use('fast')

#turns off automatic plt.plot display, use plt.show()  to re-enable
plt.ioff()
#Turn off pesky from Future Warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def config_axis(ax = None, x_lim = None, y_lim = None, X_0 = None, Y_0 = None, grd = True, minorgrd = False, mult_x = 0.2, mult_y = 0.2, Eng = True):
    if(X_0 != None):
        ax.xaxis.set_major_locator(ticker.MultipleLocator(mult_x*X_0))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator((mult_x/5)*X_0))
    if(Eng):
        ax.xaxis.set_major_formatter(ticker.EngFormatter())
        ax.yaxis.set_major_formatter(ticker.EngFormatter())
    if(Y_0 != None):
        ax.yaxis.set_major_locator(ticker.MultipleLocator(mult_y*Y_0))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(mult_y/5*Y_0))
    if(grd == True):
        ax.grid(b = True, which = 'major', axis = 'both')
    else:
        ax.grid(b = False, which = 'major', axis = 'both')
    if(minorgrd == True):
        ax.grid(b = True, which = 'minor', axis = 'both')
    else:
        ax.grid(b = False, which = 'minor', axis = 'both')

    if(x_lim != None):
        ax.set_xlim(x_lim)
    if(y_lim != None):
        ax.set_ylim(y_lim)
    return ax
"""#########################################################################"""
def decimate(x_arr, factor = 1):
    N = len(x_arr)
    M = int(N/factor)
    y_arr = []
    for i in np.arange(0, N, factor):
        y_arr.append(x_arr[i])
    return y_arr

def apply_window(arr, win = 'None', beta = 8.6):
    M = len(arr)
    if(win == 'bartlett'): window = np.bartlett(M)
    elif(win == 'hamming'): window = np.hamming(M)
    elif(win == 'hanning'): window = np.hanning(M)
    elif(win == 'kaiser'): window = np.kaiser(M, beta = beta)
    elif(win == 'blackman'): window = np.blackman(M)
    elif(win == 'None'): window = np.ones(M)
    else:
        window = np.ones(M)

    ret_arr = np.multiply(arr, window)
    return ret_arr