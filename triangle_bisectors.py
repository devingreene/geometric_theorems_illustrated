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
	if event.inaxes:
		x[vertex] = evt.xdata
		y[vertex] = evt.ydata
		redefine_triangle()

# Geometry calculations
def compute_features():
	global s,a
	s = (
		np.sqrt((x[1]-x[2])**2+(y[1]-y[2])**2),
		np.sqrt((x[0]-x[2])**2+(y[0]-y[2])**2),
		np.sqrt((x[0]-x[1])**2+(y[0]-y[1])**2) )
	a = (
		np.arccos((s[1]**2 + s[2]**2 - s[0]**2)/(2*s[1]*s[2])),
		np.arccos((s[0]**2 + s[2]**2 - s[1]**2)/(2*s[0]*s[2])),
		np.arccos((s[0]**2 + s[1]**2 - s[2]**2)/(2*s[0]*s[1]))  )


def compute_bisectors():
	global x,y,b_x,b_y,b,s,a
	compute_features()
	steps = (
			s[2]*np.sin(a[0]/2)/np.sin(a[0]/2+a[1]),
			s[0]*np.sin(a[1]/2)/np.sin(a[1]/2+a[2]),
			s[1]*np.sin(a[2]/2)/np.sin(a[2]/2+a[0])  )
	b_x = (
			x[1] + (x[2]-x[1])/s[0]*steps[0],
			x[2] + (x[0]-x[2])/s[1]*steps[1],
			x[0] + (x[1]-x[0])/s[2]*steps[2]  )
		
	b_y = (
			y[1] + (y[2]-y[1])/s[0]*steps[0],
			y[2] + (y[0]-y[2])/s[1]*steps[1],
			y[0] + (y[1]-y[0])/s[2]*steps[2]  )
			


def redefine_triangle():
	compute_bisectors()
	p[0][0].set_data(x[0],y[0])
	p[1][0].set_data(x[1],y[1])
	p[2][0].set_data(x[2],y[2])
	l[0][0].set_data(x[:2],y[:2])
	l[1][0].set_data(x[1:],y[1:])
	l[2][0].set_data([x[2],x[0]],[y[2],y[0]])
	b[0][0].set_data([x[0],b_x[0]],[y[0],b_y[0]])
	b[1][0].set_data([x[1],b_x[1]],[y[1],b_y[1]])
	b[2][0].set_data([x[2],b_x[2]],[y[2],b_y[2]])
	fig.show()

fig = figure(figsize=(8,8))
axes(aspect='equal')

connect('pick_event',mouse_down)
connect('button_release_event',mouse_up)

# vertices
x = [-1,0.5,0.5]
y = [0,-0.5*np.sqrt(3),0.5*np.sqrt(3)]

p = plot(x[0],y[0]),plot(x[1],y[1]),plot(x[2],y[2])
l = plot(x[:2],y[:2],'y'),plot(x[1:],y[1:],'y'),plot([x[2],x[0]],[y[2],y[0]],'y')
compute_bisectors()
b = plot([x[0],b_x[0]],[y[0],b_y[0]]),plot([x[1],b_x[1]],[y[1],b_y[1]]),plot([x[2],b_x[2]],[y[2],b_y[2]])

xlim(-2,2)
ylim(-2,2)
for i in range(3):
	p[i][0].set_picker(15.0)

fig.show()
