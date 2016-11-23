import tkinter
import turtle
import time
from util import orientation_test, intersection, triangulation, \
                 point_inside_polygon, polygon_intersection
from drawing import draw_line, draw_circle

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
    self.t.speed(2)
    self.t.hideturtle()
    self.tPV = turtle.RawTurtle(self.canvas)
    self.tPV.color("#468499") #B5CDD6 suprafata vizibila
    self.tPV.hideturtle()
    self.tPV.speed(10)
    self.tErr = turtle.RawTurtle(self.canvas)
    self.tErr.color("red")
    self.tErr.hideturtle()
    self.tErr.speed(5)

    # set on click event
    self.canvas.bind("<Button>", self.onClick)

    # initialize buttons 
    butDesen = tkinter.Button(self.frame, \
      text = "Clear Drawing Area", command = self.comDesen)
    butDesen.pack(fill='x')

    butIncheie = tkinter.Button(self.frame, \
      text = "Close Polygon", command = self.comIncheie)
    butIncheie.pack(fill='x')
    
    butTriang = tkinter.Button(self.frame, \
      text = "Triangulation", command = self.comTriang)
    butTriang.pack(fill='x')
    
    butArie = tkinter.Button(self.frame, \
      text = "Check Visible Area (Set a Point)", command = self.comArie)
    butArie.pack(fill='x')

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
          # TODO: IMPORVE THIS
          if len(vert) > 2 and orientation_test(vert[-2], vert[-1], currentPoint) == 0:
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
      if point_inside_polygon(currentPoint, vert):
        print("Point is inside Polygon")
      else:
        print("Point is not inside Polygon")


  def getCurrentPoint(self, ev):
    return (ev.x - self.canvas.winfo_width()//2, \
            self.canvas.winfo_height()//2 - ev.y)


  # buttons click handlers
  def comDesen(self):
    self.stateLabel.set("Desenati poligonul (Click)")
    self.state = 1
    answer = tkinter.messagebox.askquestion("Vechiul desen va fi sters", \
                                        "Doriti sa stergeti desenul actual?")
    if answer == "yes":
      self.vert.clear()
      self.t.clear()
      self.tPV.clear()
      self.viewPoint = (-1, -1)
      self.completeDrawing = False

  def comIncheie(self):
    ok = True
    vert = self.vert
    if len(vert) > 2:
      if not polygon_intersection(vert[0], vert[-1], vert):
        draw_line(self.t, vert[-1], vert[0])
        self.completeDrawing = True
        self.state = 0
        print(vert)
      else:
        draw_line(self.tErr, vert[-1], vert[0])
        self.tErr.clear()
        print("Intersection!")
    else:
      print("You need at least 3 points!")

  def comTriang(self):
    print("Not implemented!")
    triangles = triangulation(self.vert, self.tPV)
    self.t.color('green')
    for t in triangles:
      draw_line(self.t, t[0], t[2])
    self.stateLabel.set("Poligonul este triangulat")
    self.state = 0

  def comArie(self):
    print("Not implemented!")
    self.stateLabel.set("Setati punct")
    self.state = 3
