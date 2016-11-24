import tkinter
import turtle
import time
from util import orientation_test, intersection, triangulation, \
                 point_inside_polygon, polygon_intersection, collinear_points
from drawing import draw_line, draw_circle, draw_poly

class Gui:
  # store state of the window
  state = 1
  # store is user finshed his drawing
  completeDrawing = False
  # store the points
  vert = []
  # point where visible area starts
  viewPoint = (-1, -1) 
  
  def __init__(self, width, height):

    ##initialize Tkinter
    self.root = tkinter.Tk()

    self.stateLabel = tkinter.StringVar()
    self.stateLabel.set("Draw Polygon (Click)")

    self.frame = tkinter.Frame(bg = "white")
    tkinter.Label(self.frame, textvariable=self.stateLabel, \
                  bg='grey', fg='white').pack(fill='x')

    self.canvas = tkinter.Canvas(self.frame, width=500, height=500)
    self.canvas.pack()

    self.frame.pack(fill='both', expand=True)

    # initialize turtles
    self.t = turtle.RawTurtle(self.canvas)
    self.t.speed(5)
    self.t.hideturtle()
    self.tPV = turtle.RawTurtle(self.canvas)
    self.tPV.color("#468499") #B5CDD6 suprafata vizibila
    self.tPV.hideturtle()
    self.tPV.speed(20)
    self.tErr = turtle.RawTurtle(self.canvas)
    self.tErr.color("red")
    self.tErr.hideturtle()
    self.tErr.speed(10)
    self.trianglualtion_lines_turtle = turtle.RawTurtle(self.canvas)
    self.trianglualtion_lines_turtle.color("green")
    self.trianglualtion_lines_turtle.hideturtle()
    self.trianglualtion_lines_turtle.speed(5)
    self.trianglualtion_points_turtle = turtle.RawTurtle(self.canvas)
    self.trianglualtion_points_turtle.hideturtle()
    self.trianglualtion_points_turtle.speed(20)


    # set on click event
    self.canvas.bind("<Button>", self.onClick)

    # initialize buttons 
    read_drawing_button = tkinter.Button(self.frame, \
      text = "Read Drawing", command = self.read_drawing_handler)
    read_drawing_button.pack(fill='x')

    clear_screen_button = tkinter.Button(self.frame, \
      text = "Clear Drawing Area", command = self.comDesen)
    clear_screen_button.pack(fill='x')

    close_poly_button = tkinter.Button(self.frame, \
      text = "Close Polygon", command = self.comIncheie)
    close_poly_button.pack(fill='x')
    
    triangulation_button = tkinter.Button(self.frame, \
      text = "Triangulation", command = self.comTriang)
    triangulation_button.pack(fill='x')
    
    visible_aria_button = tkinter.Button(self.frame, \
      text = "Check Visible Area (Set a Point)", command = self.comArie)
    visible_aria_button.pack(fill='x')

    self.root.mainloop()

  # on click event handler
  def onClick(self,ev):
    vert = self.vert
    tPV = self.tPV

    currentPoint = self.getCurrentPoint(ev)

    # add points to drawing
    if self.state == 1 and not self.completeDrawing:
      print("State 1: ", currentPoint)
      # place first point
      if len(vert) == 0:
        vert.append(currentPoint)
      # draw lines between last point end current one
      else:
        # check if the new segment intersects others
        if not polygon_intersection(currentPoint, vert[-1], vert):
          draw_line(self.t, vert[-1], currentPoint)
          # check if last 3 points are collinear
          # TODO: IMPORVE THIS WITH DISTANCES
          if len(vert) > 2 and collinear_points(vert[-2], vert[-1], currentPoint):
            # remove last point
            del vert[-1]
          vert.append(currentPoint)
        else:
          print("Intersection!")
          draw_line(self.tErr,vert[-1], currentPoint)
          self.tErr.clear()
        
    if self.state == 3:
      tPV.clear()
      draw_circle(tPV, currentPoint, 2)
      if not point_inside_polygon(self.triangles, currentPoint):
        print("Point is not inside poly!")
      else:
        print("Point is inside Polygon")


  def getCurrentPoint(self, ev):
    return (ev.x - self.canvas.winfo_width()//2, \
            self.canvas.winfo_height()//2 - ev.y)


  # buttons click handlers
  def read_drawing_handler(self):
    self.completeDrawing = True
    self.vert = [(19, 205), (-130, 216), (-135, 126), (-58, 160), (48, 120), \
            (-52, 55), (-72, 107), (-183, 42), (-162, -47), (-110, 61), \
            (-23, -76), (-182, -114), (-97, -173), (-59, -130), (164, -173), \
            (139, 124), (55, -41), (111, 200), (181, 183), (67, 233)]
    # self.vert = [(-146, 219), (-209, 92), (-109, 232), (56, 174)]
    vert = self.vert

    #check for sgments intersection
    intersection = False
    for i in range(2,len(vert)):
      if polygon_intersection(vert[i], vert[i-1], vert[:i-1]):
        intersection = True
    if polygon_intersection(vert[0], vert[-1], vert):
      intersection = True

    if not intersection:
      draw_poly(self.t, vert)
    if intersection:
      draw_poly(self.tErr, vert)
      time.sleep(1)
      self.tErr.clear()
      completeDrawing = False



  def comDesen(self):
    self.stateLabel.set("Desenati poligonul (Click)")
    self.state = 1
    answer = tkinter.messagebox.askquestion("Vechiul desen va fi sters", \
                                        "Doriti sa stergeti desenul actual?")
    if answer == "yes":
      self.vert.clear()
      self.t.clear()
      self.tPV.clear()
      self.trianglualtion_points_turtle.clear()
      self.trianglualtion_lines_turtle.clear()
      self.viewPoint = (-1, -1)
      self.completeDrawing = False

  def comIncheie(self):
    ok = True
    vert = self.vert
    print(vert)
    if len(vert) > 2:
      if not polygon_intersection(vert[0], vert[-1], vert):
        draw_line(self.t, vert[-1], vert[0])
        self.completeDrawing = True
        self.state = 0
      else:
        draw_line(self.tErr, vert[-1], vert[0])
        self.tErr.clear()
        print("Intersection!")
    else:
      print("You need at least 3 points!")

  def comTriang(self):
    print("Buggy: need to be tested")
    self.triangles = triangulation(self.vert, self.trianglualtion_lines_turtle,\
                                   self.trianglualtion_points_turtle)
    # self.t.color('green')
    # for t in triangles:
    #   draw_line(self.t, t[0], t[2])
    self.stateLabel.set("Poligonul este triangulat")
    self.state = 0

  def comArie(self):
    print("Not implemented!")
    self.stateLabel.set("Setati punct")
    self.state = 3