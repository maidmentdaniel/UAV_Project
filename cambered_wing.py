from jupyter_code_template import *
NACA = [2, 4, 15]
NACA_str = ''.join(map(str, NACA))
N = 1000
x = np.linspace(0, 1, N, endpoint=True)
m = NACA[0]/100
p = NACA[1]/10
t = NACA[2]/100
c = 1

y_t = 5*t*(0.2969*sqrt(x)-0.1260*x-0.3516*x**2+0.2844*x**3-0.1015*x**4)

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

fig, ax = plt.subplots(1, 1, figsize = (12, 3))
ax = config_axis(ax, x_lim = (0, 1), Eng = False)

ax.plot(x, y_c, label =  "Mean camber line: "+r"$y_c$")
# ax.plot(x, y_t, label = "Thickness function: "+r"$y_t$")

ax.plot(x, y_U, label = "Upper edge: " + r"$y_U$")
ax.plot(x, y_L, label = "Lower edge: " + r"$y_L$")
ax.fill_between(x, y_U, y_L, facecolor = "grey", alpha = 0.4, label = "Foil section")

ax.legend(loc = "upper left", bbox_to_anchor = (1, 1))
figcaption("Cambered 4-digit NACA " + NACA_str +" airfoil", label="fig:series4cam")
plt.show()