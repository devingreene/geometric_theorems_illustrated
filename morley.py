from matplotlib.pyplot import *
import matplotlib.backend_bases as be
from numpy import sqrt,arccos,cos,sin

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
		redraw_triangle()
	except:
		return 

# Change geometry of figure
def redraw_triangle():
	p[0][0].set_data(x[0],y[0])
	p[1][0].set_data(x[1],y[1])
	p[2][0].set_data(x[2],y[2])
	l[0][0].set_data(x[:2],y[:2])
	l[1][0].set_data(x[1:],y[1:])
	l[2][0].set_data([x[2],x[0]],[y[2],y[0]])
	redraw_trisectors()
	inner_triangle_vertices = setup_inner_triangle_vertices()
	for i in range(3):
		inner_triangle[i][0].set_data((inner_triangle_vertices[i][0],inner_triangle_vertices[(i+1)%3][0] ),
									  (inner_triangle_vertices[i][1],inner_triangle_vertices[(i+1)%3][1] )  )
	fig.show()

	
# Utility for rotating sides to 
# trisectors
def rotate_by_angle(v,theta):
	return ( v[0]*cos(theta)-v[1]*sin(theta),
			 v[0]*sin(theta)+v[1]*cos(theta) )

def point_2_point(x0,x1,y0,y1,v0,v1,w0,w1):
	return ( v0*(v1*(y0 - y1) - w1*(x0 - x1))/(v0*w1 - v1*w0) + x0,
 	w0*(v1*(y0 - y1) - w1*(x0 - x1))/(v0*w1 - v1*w0) + y0 )

def setup_trisectors():
	global sides,angles,r_d
	sides = [ sqrt((x[i%3]-x[(i+1)%3])**2 + (y[i%3]-y[(i+1)%3])**2) for i in range(1,4)]
	angles = [ arccos((sides[(i+1)%3]**2+sides[(i+2)%3]**2 - sides[i]**2)/(2*sides[(i+1)%3]*sides[(i+2)%3]))/3 \
		for i in range(3) ]
	directions = [ (x[(i+1)%3] - x[i],y[(i+1)%3]-y[i]) for i in range(3)]
	
	#rotated directions
	r_d = ( rotate_by_angle(directions[2],-angles[0]),
						   rotate_by_angle(directions[0],angles[0]),
						   rotate_by_angle(directions[0],-angles[1]),
						   rotate_by_angle(directions[1],angles[1]),
						   rotate_by_angle(directions[1],-angles[2]),
						   rotate_by_angle(directions[2],angles[2])  )

def setup_inner_triangle_vertices():
	return  ( point_2_point( x[0],x[2],y[0],y[2],r_d[0][0],r_d[5][0],r_d[0][1],r_d[5][1]),\
			point_2_point( x[0],x[1],y[0],y[1],r_d[1][0],r_d[2][0],r_d[1][1],r_d[2][1]),\
			point_2_point( x[1],x[2],y[1],y[2],r_d[3][0],r_d[4][0],r_d[3][1],r_d[4][1])  )

def redraw_trisectors():
	setup_trisectors()
	vertices = setup_inner_triangle_vertices()
	for i in range(6):
		iq = i//2
		iq1 =((i-1) % 6 //2  + 1) % 3
		trisector_plots[i][0].set_data((x[iq],vertices[iq1][0]),(y[iq],vertices[iq1][1]))

fig = figure(figsize=(8,8))

connect('pick_event',mouse_down)
connect('button_release_event',mouse_up)

# vertices
x = [-1,0.5,0.5]
y = [0,-0.5*sqrt(3),0.5*sqrt(3)]

p = plot(x[0],y[0]),plot(x[1],y[1]),plot(x[2],y[2])
l = plot(x[:2],y[:2],'y'),plot(x[1:],y[1:],'y'),plot([x[2],x[0]],[y[2],y[0]],'y')

# Sets up data for trisectors
setup_trisectors()
try:
	vertices = setup_inner_triangle_vertices()
except:
	pass


# Trisector lines
trisector_plots = ()
for i in range(6):
	iq = i//2
	iq1 = ((i-1) % 6 //2  + 1 ) % 3
	trisector_plots += (plot((x[iq],vertices[iq1][0]),(y[iq],vertices[iq1][1]),'b'),)
	
# Inner triangle
inner_triangle = ()

for i in range(3):
	inner_triangle += (plot ( (vertices[i][0],vertices[(i+1)%3][0] ),
							  (vertices[i][1],vertices[(i+1)%3][1] ), 'w'),)

xlim(-2,2)
ylim(-2,2)
for i in range(3):
	p[i][0].set_picker(5.0)

fig.show()

