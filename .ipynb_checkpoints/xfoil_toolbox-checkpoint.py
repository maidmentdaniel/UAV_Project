"""
Daniel Maidment
maidment.daniel@gmail.com
"""
from jupyter_code_template import*

"""#########################################################################"""
def gen_NACA(series = [6, 4, 12], N = 1000):
    """
        series is a list [a,b,x]
        -a = 100*m is the maximum camber,
        -b = 100*p is the location of maximum camber,
        -t = x/100 is the maximum thickness as a fraction of the chord
        -N is the number of x coordinates in total
        
        returns: N, x, y_c , y_U, y_L
        -N is the length of X
        -x is the x coordinate array
        -y_c is the mean camber line
        -y_U is the upper edge coorndinate array
        -y_L is the lower edge coordinate array
        
        Notes:
        -If a = 0 OR b = 0, then the foil is assumed to be symmertical 
        - in this case y_c is set to None
    """
    x = np.linspace(0, 1, N, endpoint=True)
    m = series[0]/100
    p = series[1]/10
    t = series[2]/100
    c = 1

    y_t = 5*t*(0.2969*sqrt(x)-0.1260*x-0.3516*x**2+0.2844*x**3-0.1015*x**4)
    
    if(m == 0 or p == 0):
        return N, x, None, y_t, -1*y_t
    else:
        y_c = np.zeros(N)
        y_c[0:int(p*N)] = (m/p**2)*(2*p*(x[0:int(p*N)]/c)-(x[0:int(p*N)]/c)**2)
        y_c[int(p*N):] = (m/(1-p)**2)*((1-2*p)+2*p*(x[int(p*N):]/c)-(x[int(p*N):]/c)**2)

        dy_c = np.zeros(N)
        dy_c[0:int(p*N)] = (m/p**2)*(p-(x[0:int(p*N)]/c))
        dy_c[int(p*N):] = (m/(1-p)**2)*(p-(x[int(p*N):]/c))

        theta = np.arctan(dy_c)

        # x_U = x-y_t*sin(theta)
        # x_L= x+y_t*sin(theta)
        y_U = y_c+y_t*cos(theta)
        y_L = y_c-y_t*cos(theta)
    
        return N, x, y_c, y_U, y_L

def cambered_foil_plt(fig, ax, N, x, y_c, y_U, y_L, NACA):
    NACA_str = ''.join(map(str, NACA))
    ax = config_axis(ax, x_lim = (0, 1), Eng = False)

    ax.plot(x, y_c, label =  "Mean camber line: "+r"$y_c$")
    ax.plot(x, y_U, label = "Upper edge: " + r"$y_U$")
    ax.plot(x, y_L, label = "Lower edge: " + r"$y_L$")
    ax.fill_between(x, y_U, y_L, facecolor = "grey", alpha = 0.4, label = "Foil section")

    ax.legend(loc = "upper left", bbox_to_anchor = (1, 1))
    figcaption("Cambered 4-digit NACA " + NACA_str +" airfoil", label="fig:series4cam")
    plt.show()
    
def symmetric_foil_plt(fig, ax, N, x, y_c, y_U, y_L, NACA):
    NACA_str = ''.join(map(str, NACA))
    
    ax = config_axis(ax, x_lim = (0, 1), Eng = False)
    ax.plot(x, y_U, label = "Upper edge: " + r"$y_U$")
    ax.plot(x, y_L, label = "Lower edge: " + r"$y_L$")
    ax.fill_between(x, y_U, y_L, facecolor = "grey", alpha = 0.4, label = "Foil section")
    ax.legend(loc = "upper left", bbox_to_anchor = (1, 1))
    figcaption("Symmetric 4-digit NACA " + NACA_str +" airfoil", label="fig:series4sym")
    plt.show()

def xfoil_foilgen(series = [6, 4, 12], N = 100):
    """
        Takes in a 4-digit NACA code, and number of data points,
        it then generates the corresponding x and y cooridinates
        for use in XFOIL
        -Returns:
        --N the number of points
        --x the x coords
        --y the y coords
    """
    N, x_i, y_c, y_U_i, y_L_i = gen_NACA(series, N = N)
    
    x_U = x_i[::-1]
    x_L = x_i
    x = np.concatenate((x_U, x_L))
    
    y_U = y_U_i[::-1]
    y_L = y_L_i
    y = np.concatenate((y_U, y_L))
    N = len(x)
    NACA_str = 'naca_data/NACA_'+''.join(map(str, series))+'.txt'
    save_to_file(N, x, y, NACA_str)

    return x, y

def save_to_file(N, x, y, filename):
    file = open(filename, 'w')
    file.write(str(N)+'\n')
    for i in range(N):
        file.write("{:07.5f}, {:07.5f}\n".format(x[i], y[i]))
    file.close()
    
def get_from_file(filename):
    file = open(filename, 'r')
    x = []
    y = []
    N = int(file.readline())
    for i in range(N):
        line_str = file.readline().strip().split(', ')
        x.append(float(line_str[0]))
        y.append(float(line_str[1]))
    file.close()
    x = np.array(x)
    y = np.array(y)
    return x, y

def Re_N(v = 10, c = 0.1, vis = 1.5111e-5, kph = False):
    """
    Calculates the Reynold Number.
    
    -v= velocity of the fluid [m/s] or [km/h] if kph = True
    -c= The characteritics length, the chord width of an airfoil [m]
    -vis= The kinematic viscosity of the fluid [m^2/s]
    -kph= boolean, True if v is measured in kph
    
    Example kinematic viscosity values for air and water at 1 atm and various temperatures.   
        m2/s        |°C
        ---------------
        1.2462e-5   |-10
        1.3324e-5   | 0
        1.4207e-5   | 10
        1.5111e-5   | 20
    
    """
    if(kph):v = v/3.6
    return v*c/vis

def Ma(c = 340.3, v = 10, c_kph = False, v_kph = False):
    """
    Calculates the Mach number.
    -c speed of sound [m/s].
    -v fluid velocity [m/s]
    -c_kph or v_kph, select True if values are in units of km/h
    """
    if(c_kph): c = c/3.6
    if(v_kph): v = v/3.6
    
    return v/c

def smoothing(arr):
    arr = arr.flatten()
    nan_idx = np.where(np.isnan(arr))[0][:]
    for idx in nan_idx:
        if(idx<len(arr)-1): arr[idx] = (arr[idx-1]+arr[idx+1])/2
    return arr