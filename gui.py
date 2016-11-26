import tkinter
import turtle
import time
from util import *
from drawing import *

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

    self.canvas = tkinter.Canvas(self.frame, width=width, height=height)
    self.canvas.pack()

    self.frame.pack(fill='both', expand=True)

    # initialize turtles
    self.t = turtle.RawTurtle(self.canvas)
    self.t.speed(0)
    self.t.color()
    self.t.hideturtle()
    self.tPV = turtle.RawTurtle(self.canvas)
    self.tPV.color("darkred") # #468499
    self.tPV.hideturtle()
    self.tPV.speed(20)
    self.tErr = turtle.RawTurtle(self.canvas)
    self.tErr.color("red")
    self.tErr.hideturtle()
    self.tErr.speed(10)
    self.trianglualtion_lines_turtle = turtle.RawTurtle(self.canvas)
    self.trianglualtion_lines_turtle.color("lightblue")
    self.trianglualtion_lines_turtle.hideturtle()
    self.trianglualtion_lines_turtle.speed(0)
    self.trianglualtion_points_turtle = turtle.RawTurtle(self.canvas)
    self.trianglualtion_points_turtle.hideturtle()
    self.trianglualtion_points_turtle.speed(0)
    self.tVis = turtle.RawTurtle(self.canvas)
    self.tVis.color("darkred", "lightgreen") # #"#B5CDD6")
    self.tVis.hideturtle()
    self.tVis.speed(0)

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

    currentPoint = self.get_current_point(ev)
    if currentPoint in vert:
      print("You can't add the same point 2 times")
      return

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
          if len(vert) > 2 and collinear_points(vert[-2], vert[-1], currentPoint):
            if raport(vert[-2], currentPoint, vert[-1]) < 0:
              print("Intersection!")
              draw_line(self.tErr,vert[-1], currentPoint)
              self.tErr.clear()
            else:
              del vert[-1]
          vert.append(currentPoint)
        else:
          print("Intersection!")
          draw_line(self.tErr,vert[-1], currentPoint)
          self.tErr.clear()
        
    if self.state == 3:
      tPV.clear()
      self.tVis.clear()
      draw_circle(tPV, currentPoint, 2)

      if point_inside_polygon(self.triangles, currentPoint):
        self.viewPoint = (ev.x - self.canvas.winfo_width()//2, self.canvas.winfo_height()//2 - ev.y - 1)
        paint_visible_area(self.tVis, self.tPV, visible_area(vert, self.triangles, self.viewPoint), self.viewPoint, self.triangles)
        print("Point is inside Polygon")


  def get_current_point(self, ev):
    return (ev.x - self.canvas.winfo_width()//2, \
            self.canvas.winfo_height()//2 - ev.y)


  # buttons click handlers
  def read_drawing_handler(self):
    if self.vert:
      self.comDesen()
    self.completeDrawing = True
    with open("input.in", "r") as f:
      for line in f:
        (x, y) = tuple(line.split())
        self.vert.append((int(x),int(y)))
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
      self.tVis.clear()
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
    self.stateLabel.set("Poligonul este triangulat")
    self.state = 0


  def comArie(self):
    print("Not implemented!")
    self.stateLabel.set("Setati punct")
    self.state = 3