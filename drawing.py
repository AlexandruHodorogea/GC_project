#drawing functions
def draw_line(turtle, A, B):
	turtle.penup()
	turtle.goto(A)
	turtle.pendown()
	turtle.goto(B)
	turtle.penup()

def draw_circle(turtle, A, size):
  turtle.penup()
  turtle.goto(A[0] - size/2, A[1] - size/2)
  turtle.pendown()
  turtle.begin_fill()
  turtle.circle(size)
  turtle.end_fill()
  turtle.penup()


def paint_visible_area(turtle, vert, viewPoint):
  
  
  for i, v in vert:
    turtle.penup()
    turtle.goto(viewPoint)
    turtle.pendown()
    #turtle.begin_fill()
    turtle.goto(v)
    turtle.goto((vert[(i+1)%n])

  turtle.goto(vert[0])

  #turtle.end_fill()
  turtle.penup();


def draw_poly(turtle, vert):
  for i in range(len(vert) - 1):
    draw_line(turtle, vert[i], vert[i + 1])
  draw_line(turtle, vert[len(vert) - 1], vert[0])
