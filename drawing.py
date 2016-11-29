import util
#from util import *

#drawing functions
def draw_line(turtle, A, B):
	turtle.penup()
	turtle.goto(A)
	turtle.pendown()
	turtle.goto(B)
	turtle.penup()

def draw_circle(turtle, A, size):
  turtle.penup()
  turtle.goto(A[0], A[1] - size)
  turtle.pendown()
  turtle.begin_fill()
  turtle.circle(size)
  turtle.end_fill()
  turtle.penup()


def paint_visible_area(turtle, tPV, vert, viewPoint, triangles):
  turtle.speed(6)
  #turtle.color("red", "")
  turtle.penup()
  turtle.goto(viewPoint)
  
  for i, v in enumerate(vert):
    turtle.pendown()
    turtle.begin_fill()
    turtle.goto(v)
    turtle.goto(vert[(i+1)%len(vert)])
    turtle.goto(viewPoint)
    turtle.end_fill()
    turtle.penup()
    tPV.begin_fill()
    tPV.circle(2)
    tPV.end_fill()
  
  #turtle.goto(vert[0])


def draw_poly(turtle, vert):
  for i in range(len(vert) - 1):
    draw_line(turtle, vert[i], vert[i + 1])
  draw_line(turtle, vert[len(vert) - 1], vert[0])
