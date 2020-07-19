from xfoil import XFoil
from xfoil.test import naca0012


xf = XFoil()
xf.airfoil = naca0012
xf.Re = 1e6
xf.max_iter = 40
a, cl, cd, cm, co = xf.aseq(-20, 20, 0.5)