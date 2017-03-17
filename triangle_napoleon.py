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

def redefine_triangle():
	p[0][0].set_data(x[0],y[0])
	p[1][0].set_data(x[1],y[1])
	p[2][0].set_data(x[2],y[2])
	l[0][0].set_data(x[:2],y[:2])
	l[1][0].set_data(x[1:],y[1:])
	l[2][0].set_data([x[2],x[0]],[y[2],y[0]])
	compute_eq_triangles()
	s[0][0].set_data([x[0],v3_x[2]],[y[0],v3_y[2]])
	s[1][0].set_data([x[0],v3_x[1]],[y[0],v3_y[1]])
	s[2][0].set_data([x[1],v3_x[0]],[y[1],v3_y[0]])
	s[3][0].set_data([x[1],v3_x[2]],[y[1],v3_y[2]])
	s[4][0].set_data([x[2],v3_x[1]],[y[2],v3_y[1]])
	s[5][0].set_data([x[2],v3_x[0]],[y[2],v3_y[0]])
	nap[0][0].set_data([centroids_x[0],centroids_x[1]],[centroids_y[0],centroids_y[1]])
	nap[1][0].set_data([centroids_x[1],centroids_x[2]],[centroids_y[1],centroids_y[2]])
	nap[2][0].set_data([centroids_x[0],centroids_x[2]],[centroids_y[0],centroids_y[2]])
	fig.show()

def compute_eq_triangles():
	global v3_x,v3_y,centroids_x,centroids_y
	midpoints_x = (
				0.5*(x[1]+x[2]),
				0.5*(x[0]+x[2]),
				0.5*(x[0]+x[1])  )
	midpoints_y = ( 
				0.5*(y[1]+y[2]),
				0.5*(y[0]+y[2]),
				0.5*(y[0]+y[1])  )

	v3_x = (
			midpoints_x[0] - np.sqrt(3)/2*(y[1]-y[2]),
			midpoints_x[1] - np.sqrt(3)/2*(y[2]-y[0]),
			midpoints_x[2] - np.sqrt(3)/2*(y[0]-y[1])  )
	
	v3_y = (
			midpoints_y[0] - np.sqrt(3)/2*(x[2]-x[1]),
			midpoints_y[1] - np.sqrt(3)/2*(x[0]-x[2]),
			midpoints_y[2] - np.sqrt(3)/2*(x[1]-x[0])  )

	centroids_x = \
			(
				(x[1] + x[2] + v3_x[0])/3,
				(x[0] + x[2] + v3_x[1])/3,
				(x[0] + x[1] + v3_x[2])/3  )

	centroids_y =  \
			(
				(y[1] + y[2] + v3_y[0])/3,
				(y[0] + y[2] + v3_y[1])/3,
				(y[0] + y[1] + v3_y[2])/3  )


fig = figure()
axes(aspect='equal')
gca().set_xmargin(0)

connect('pick_event',mouse_down)
connect('button_release_event',mouse_up)

# vertices
x = [-1,0.5,0.5]
y = [0,-0.5*np.sqrt(3),0.5*np.sqrt(3)]

p = plot(x[0],y[0]),plot(x[1],y[1]),plot(x[2],y[2])
l = plot(x[:2],y[:2],'y'),plot(x[1:],y[1:],'y'),plot([x[2],x[0]],[y[2],y[0]],'y')
compute_eq_triangles()
s = (plot([x[0],v3_x[2]],[y[0],v3_y[2]],'purple'),
plot([x[0],v3_x[1]],[y[0],v3_y[1]],'purple'),
plot([x[1],v3_x[0]],[y[1],v3_y[0]],'purple'),
plot([x[1],v3_x[2]],[y[1],v3_y[2]],'purple'),
plot([x[2],v3_x[1]],[y[2],v3_y[1]],'purple'),
plot([x[2],v3_x[0]],[y[2],v3_y[0]],'purple'))
nap = ( plot([centroids_x[0],centroids_x[1]],[centroids_y[0],centroids_y[1]]),
		plot([centroids_x[1],centroids_x[2]],[centroids_y[1],centroids_y[2]]),
		plot([centroids_x[0],centroids_x[2]],[centroids_y[0],centroids_y[2]])  )


xlim(-2,2)
ylim(-2,2)
for i in range(3):
	p[i][0].set_picker(15.0)

fig.show()
