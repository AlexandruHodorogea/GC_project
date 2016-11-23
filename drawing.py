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
