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

"""#########################################################################"""
#plt.style.use('jupyter_grey')
plt.style.use('jupyter_color')

plt.ioff()
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

from xfoil.test import naca0012
from xfoil import XFoil

xf = XFoil()
xf.airfoil = naca0012
xf.Re = 1e5
xf.max_iter = 20
a, cl, cd, cm, co = xf.aseq(-20, 20, 0.5)

fig, axarr = plt.subplots(1, 1, figsize = (12,6))
axarr.plot(a,cl)
plt.show()