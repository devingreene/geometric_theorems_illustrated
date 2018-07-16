# vim: set expandtab=4 tabstop
from matplotlib.pyplot import *
import matplotlib.backend_bases as be
import numpy as np 

# Mouse movement functions
def mouse_down(evt):
    global vertex,cnct
    artists = [p[i][0] for i in range(6)]
    vertex = artists.index(evt.artist)
    cnct = connect('motion_notify_event',mover)

event = None
def mouse_up(evt):
    if event:
        event.canvas.mpl_disconnect(cnct)

def mover(evt):
    global vertex,event
    event = evt
    if event.inaxes:
        xx = evt.xdata
        yy = evt.ydata
        norm = np.sqrt(xx**2+yy**2)
        x[vertex] = xx/norm
        y[vertex] = yy/norm
        redefine_hexagon()
    
def draw_conic():
    an = np.linspace(0,2*np.pi,501)
    plot(np.cos(an),np.sin(an),'blue')

def redefine_hexagon():
    global E,xE,yE
    for i in range(6):
        p[i][0].set_data(x[i],y[i])
    for i in range(6):
        inext = (i+1)%6
        e[i][0].set_data((x[i],x[inext]),(y[i],y[inext]))
    i = ind = 0
    E = 3*min(1000,max([ 1/min(abs(x[i] - x[(i+1) % 6]),abs(y[i]-y[(i+1)%6])) for i in range(6)]))
    while ind < 12:
        inext = (i+1)%6
        xE = ( x[i] - E*(x[inext]-x[i]),x[inext] - E*(x[i]-x[inext]))
        yE = ( y[i] - E*(y[inext]-y[i]),y[inext] - E*(y[i]-y[inext]))
        l[ind][0].set_data((xE[0],x[i]),(yE[0],y[i]))
        ind += 1
        l[ind][0].set_data((xE[1],x[inext]),(yE[1],y[inext]))
        ind += 1
        i += 1
    redraw_line()
    fig.show()

def set_points_on_line():
    global p1_x,p2_x,p1_y,p2_y
    # Points
    p1_x = x[0] + (-x[0] + x[1] )*((x[0]-x[3])*(y[3]-y[4])
            - (x[3]-x[4])*(y[0]-y[3]))/\
        ((x[0]-x[1])*(y[3]-y[4])-(x[3]-x[4])*(y[0]-y[1]))
    p2_x= x[1] + (-x[1] + x[2] )*((x[1]-x[4])*(y[4]-y[5])
            - (x[4]-x[5])*(y[1]-y[4]))/\
        ((x[1]-x[2])*(y[4]-y[5])-(x[4]-x[5])*(y[1]-y[2]))
    p1_y = y[0] + (-y[0] + y[1] )*((x[0]-x[3])*(y[3]-y[4])
            - (x[3]-x[4])*(y[0]-y[3]))/\
        ((x[0]-x[1])*(y[3]-y[4])-(x[3]-x[4])*(y[0]-y[1]))
    p2_y = y[1] + (-y[1] + y[2] )*((x[1]-x[4])*(y[4]-y[5])
            - (x[4]-x[5])*(y[1]-y[4]))/\
        ((x[1]-x[2])*(y[4]-y[5])-(x[4]-x[5])*(y[1]-y[2]))

def redraw_line():
    global p1_x,p2_x,p1_y,p2_y
    set_points_on_line()
    # Redraw line
    line[0].set_data(p1_x + np.array((-E,E))*(p2_x-p1_x),p1_y + np.array((-E,E))*(p2_y - p1_y))

fig = figure(figsize=(8,8))
axes(aspect='equal')

connect('pick_event',mouse_down)
connect('button_release_event',mouse_up)

# vertices
x = [ np.cos(2*np.pi*i/6) for i in range(6) ]
y = [ np.sin(2*np.pi*i/6) for i in range(6) ]

p = plot(x[0],y[0]),plot(x[1],y[1]),plot(x[2],y[2]),\
        plot(x[3],y[3]),plot(x[4],y[4]),plot(x[5],y[5])
e = plot(x[0:2],y[0:2]),plot(x[1:3],y[1:3]),\
        plot(x[2:4],y[2:4]),plot(x[3:5],y[3:5]),\
        plot(x[4:],y[4:]),plot((x[5],x[0]),(y[5],y[0]))
E = 3*min(1000,max([ 1/min(abs(x[i] - x[(i+1) % 6]),
        abs(y[i]-y[(i+1)%6])) for i in range(6)]))
l = ()
for i in range(6):
    inext = (i+1)%6
    xE = ( x[i] - E*(x[inext]-x[i]),x[inext] - E*(x[i]-x[inext]))
    yE = ( y[i] - E*(y[inext]-y[i]),y[inext] - E*(y[i]-y[inext]))
    l = l+(plot((xE[0],x[i]),(yE[0],y[i])),)
    l = l+(plot((xE[1],x[inext]),(yE[1],y[inext])),)

draw_conic()

# Plot line
set_points_on_line()
line = plot(p1_x + np.array((-E,E))*(p2_x-p1_x),p1_y + 
        np.array((-E,E))*(p2_y - p1_y))

xlim(-4,4)
ylim(-4,4)
for i in range(6):
    p[i][0].set_picker(5.0)

fig.show()
