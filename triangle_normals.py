from matplotlib.pyplot import *
import matplotlib.backend_bases as be
import numpy as np 
from numpy import sqrt


# Mouse movement functions
def reg_down(evt):
	global down_state,vertex
	down_state = 1
	artists = [p[i][0] for i in range(3)]
	vertex = artists.index(evt.artist)

def reg_up(evt):
	global down_state
	if down_state:
		down_state = 0

def mover(evt):
	global vertex
	try:
		if down_state:
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
	draw_normal_lines()
	n[0][0].set_data(nx[0:2],ny[0:2])
	n[1][0].set_data(nx[2:4],ny[2:4])
	n[2][0].set_data(nx[4:],ny[4:])
	fig.show()

def define_ex_factor():
	# Insures that normal lines will extend over 
	# plot
	global E
	ds = ( sqrt((x[0]-x[1])**2 + (y[0]-y[1])**2),\
			sqrt((x[0]-x[2])**2 + (y[0]-y[2])**2),\
			sqrt((x[1]-x[2])**2 + (y[1]-y[2])**2) )
	E = 5/min(ds)

def draw_normal_lines():
	global nx,ny

	define_ex_factor()

	nx = (
		x[0] +  E*(y[1]-y[2]),
		x[0] -  E*(y[1]-y[2]),
		x[1] +  E*(y[2]-y[0]),
		x[1] -  E*(y[2]-y[0]),
		x[2] +  E*(y[0]-y[1]),
		x[2] -  E*(y[0]-y[1])  )

	ny = (
		y[0] +  E*(x[2]-x[1]),
		y[0] -  E*(x[2]-x[1]),
		y[1] +  E*(x[0]-x[2]),
		y[1] -  E*(x[0]-x[2]),
		y[2] +  E*(x[1]-x[0]),
		y[2] -  E*(x[1]-x[0])  )

fig = figure(figsize=(8,8))

connect('pick_event',reg_down)
connect('button_release_event',reg_up)
connect('motion_notify_event',mover)

down_state = 0

# vertices
x = [-1,0.5,0.5]
y = [0,-0.5*np.sqrt(3),0.5*np.sqrt(3)]

define_ex_factor()

p = plot(x[0],y[0]),plot(x[1],y[1]),plot(x[2],y[2])
l = plot(x[:2],y[:2],'y'),plot(x[1:],y[1:],'y'),plot([x[2],x[0]],[y[2],y[0]],'y')
draw_normal_lines()
n = plot(nx[0:2],ny[0:2]),plot(nx[2:4],ny[2:4]),plot(nx[4:],ny[4:])

xlim(-2,2)
ylim(-2,2)
for i in range(3):
	p[i][0].set_picker(15)

fig.show()
