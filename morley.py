from matplotlib.pyplot import *
import matplotlib.backend_bases as be
import numpy as np 

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
	trisector_redraw()
	inner_triangle_vertices = setup_inner_triangle_vertices()
	for i in range(3):
		inner_triangle[i][0].set_data((inner_triangle_vertices[i][0],inner_triangle_vertices[(i+1)%3][0] ),
									  (inner_triangle_vertices[i][1],inner_triangle_vertices[(i+1)%3][1] )  )
	fig.show()

def trisector_setup():
	global E,sides,angles,trisector_endpoints_x,trisector_endpoints_y
	try:
		E = 3*max([1/min(abs(x[i]-x[(i+1)%3]),abs(y[i]-y[(i+1)%3])) for i in range(3)])
	except:
		E = 1000
	sides = [ np.sqrt((x[i%3]-x[(i+1)%3])**2 + (y[i%3]-y[(i+1)%3])**2) for i in range(1,4)]
	angles = [ np.arccos((sides[(i+1)%3]**2+sides[(i+2)%3]**2 - sides[i]**2)/(2*sides[(i+1)%3]*sides[(i+2)%3]))/3 \
		for i in range(3) ]
	directions = [ (x[(i+1)%3] - x[i],y[(i+1)%3]-y[i]) for i in range(3)]
	rotated_directions = ( rotate_by_angle(directions[2],-angles[0]),
						   rotate_by_angle(directions[0],angles[0]),
						   rotate_by_angle(directions[0],-angles[1]),
						   rotate_by_angle(directions[1],angles[1]),
						   rotate_by_angle(directions[1],-angles[2]),
						   rotate_by_angle(directions[2],angles[2])  )
						   
	trisector_endpoints_x = ( x[0] - E*rotated_directions[0][0],  
							  x[0] + E*rotated_directions[1][0],
							  x[1] - E*rotated_directions[2][0],
							  x[1] + E*rotated_directions[3][0],
							  x[2] - E*rotated_directions[4][0],
							  x[2] + E*rotated_directions[5][0] )

	trisector_endpoints_y = ( y[0] - E*rotated_directions[0][1],  
							  y[0] + E*rotated_directions[1][1],
							  y[1] - E*rotated_directions[2][1],
							  y[1] + E*rotated_directions[3][1],
							  y[2] - E*rotated_directions[4][1],
							  y[2] + E*rotated_directions[5][1] )

def rotate_by_angle(v,theta):
	return ( v[0]*np.cos(theta)-v[1]*np.sin(theta),
			 v[0]*np.sin(theta)+v[1]*np.cos(theta) )
	
def trisector_redraw():
	trisector_setup()
	for i in range(6):
		trisector_plots[i][0].set_data((x[i//2],trisector_endpoints_x[i]),(y[i//2],trisector_endpoints_y[i]))

def line_intersection_formula(x0,x1,x2,x3,y0,y1,y2,y3):
	return ( x0 + (-x0 + x1)*((x0 - x2)*(y2 - y3) - (x2 - x3)*(y0 - y2))/((x0 - x1)*(y2 - y3) - (x2 - x3)*(y0 - y1)),
	y0 + (-y0 + y1)*((x0 - x2)*(y2 - y3) - (x2 - x3)*(y0 - y2))/((x0 - x1)*(y2 - y3) - (x2 - x3)*(y0 - y1))  )

def setup_inner_triangle_vertices():
	return  ( line_intersection_formula( x[0],trisector_endpoints_x[0],x[2],trisector_endpoints_x[5],
									     y[0],trisector_endpoints_y[0],y[2],trisector_endpoints_y[5]),
	  line_intersection_formula( x[0],trisector_endpoints_x[1],x[1],trisector_endpoints_x[2],
	 							 y[0],trisector_endpoints_y[1],y[1],trisector_endpoints_y[2]),
	  line_intersection_formula( x[1],trisector_endpoints_x[3],x[2],trisector_endpoints_x[4],
	  							 y[1],trisector_endpoints_y[3],y[2],trisector_endpoints_y[4]) )  

fig = figure(figsize=(8,8))

connect('pick_event',reg_down)
connect('button_release_event',reg_up)
connect('motion_notify_event',mover)

down_state = 0

# vertices
x = [-1,0.5,0.5]
y = [0,-0.5*np.sqrt(3),0.5*np.sqrt(3)]

p = plot(x[0],y[0]),plot(x[1],y[1]),plot(x[2],y[2])
l = plot(x[:2],y[:2],'y'),plot(x[1:],y[1:],'y'),plot([x[2],x[0]],[y[2],y[0]],'y')
trisector_setup()


trisector_plots = ()
for i in range(6):
	trisector_plots += (plot((x[i//2],trisector_endpoints_x[i]),(y[i//2],trisector_endpoints_y[i]),'b'),)

try:
	inner_triangle_vertices = setup_inner_triangle_vertices()
except:
	pass

inner_triangle = ()

for i in range(3):
	inner_triangle += (plot ( (inner_triangle_vertices[i][0],inner_triangle_vertices[(i+1)%3][0] ),
							  (inner_triangle_vertices[i][1],inner_triangle_vertices[(i+1)%3][1] ), 'w'),)

xlim(-2,2)
ylim(-2,2)
for i in range(3):
	p[i][0].set_picker(5.0)

fig.show()

