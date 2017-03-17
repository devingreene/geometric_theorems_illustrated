from matplotlib.pyplot import *
import matplotlib.backend_bases as be
import numpy as np 

# Mouse movement functions
def mouse_down(evt):
	global vertex,cnct
	artists = [p[i][0] for i in range(3)]
	vertex = artists.index(evt.artist)
	cnct = connect('motion_notify_event',mover)

event = None
def mouse_up(evt):
	if event:
		event.canvas.mpl_disconnect(cnct)
	

def mover(evt):
	global vertex,event
	event = evt
	try:
		x[vertex] = evt.xdata
		y[vertex] = evt.ydata
		redefine_triangle()
	except:
		return 

def set_midpoints():
	global x,y,m_x,m_y
	m_x = [0.5*(x[1]+x[2]),0.5*(x[0]+x[2]),0.5*(x[0]+x[1])]
	m_y = [0.5*(y[1]+y[2]),0.5*(y[0]+y[2]),0.5*(y[0]+y[1])]

def redefine_triangle():
	p[0][0].set_data(x[0],y[0])
	p[1][0].set_data(x[1],y[1])
	p[2][0].set_data(x[2],y[2])
	l[0][0].set_data(x[:2],y[:2])
	l[1][0].set_data(x[1:],y[1:])
	l[2][0].set_data([x[2],x[0]],[y[2],y[0]])
	set_midpoints()
	m[0][0].set_data([x[0],m_x[0]],[y[0],m_y[0]])
	m[1][0].set_data([x[1],m_x[1]],[y[1],m_y[1]])
	m[2][0].set_data([x[2],m_x[2]],[y[2],m_y[2]])
	fig.show()

fig = figure(figsize=(15,15))
axes(aspect='equal')

connect('pick_event',mouse_down)
connect('button_release_event',mouse_up)

# vertices
x = [-1,0.5,0.5]
y = [0,-0.5*np.sqrt(3),0.5*np.sqrt(3)]
set_midpoints()


p = plot(x[0],y[0]),plot(x[1],y[1]),plot(x[2],y[2])
l = plot(x[:2],y[:2],'y'),plot(x[1:],y[1:],'y'),plot([x[2],x[0]],[y[2],y[0]],'y')
m = plot([x[0],m_x[0]],[y[0],m_y[0]]),plot([x[1],m_x[1]],[y[1],m_y[1]]),plot([x[2],m_x[2]],[y[2],m_y[2]])

xlim(-2,2)
ylim(-2,2)
for i in range(3):
	p[i][0].set_picker(25.0)

fig.show()
