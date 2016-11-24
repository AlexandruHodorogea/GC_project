import math
import time
from drawing import draw_circle, draw_line

def orientation_test(p1, p2, r):
  direction = p2[0] * r[1] + p1[0] * p2[1] + p1[1] * r[0] - \
    p1[1] * p2[0] - p2[1] * r[0] - p1[0] * r[1]

  if direction > 0:
    return 1
  if direction < 0:
    return -1
  else:
    return 0

def intersection(A, B, C, D):
  if(orientation_test(A, B, C)*orientation_test(A, B, D) < 0 and orientation_test(C, D, A)*orientation_test(C, D, B) < 0):
    return True
  else:
    return False

def polygon_intersection(A, B, vert):
  for i in range(len(vert) - 1):
    if intersection(A, B, vert[i], vert[i+1]):
      return True
  return False


def colinear_points(A, B, C):
  AB = (vert[-1][0] - vert[-2][0], vert[-1][1] - vert[-2][1])
  BC = (currentPoint[0] - vert[-1][0], currentPoint[1] - vert[-1][1])
  # check if last 3 points are collinear
  if AB[0]*BC[1] == AB[1]*BC[0]:
    pass

def length(A, B):
  return sqrt(pow((A[0] - B[0]), 2) + pow((A[1] - B[1]), 2))


def get_angle(A, B, C):
  return arccos((pow(length(A, B), 2) + pow(length(C, B),2) - pow(length(A, B), 2)) / 2 * length(A, B) * length(C, B)) / 3.14 * 180

def preprocess(v):
  first_point = 0
  for i in range(len(v)):
    first_point = i if v[i][0] > v[first_point][0] else first_point

  nxt = first_point + 1
  prev = first_point - 1

  if first_point == 0:
    prev = len(v) - 1
  elif first_point == len(v) -1:
    nxt = 0

  secound_point = nxt if orientation_test(v[first_point], v[nxt], v[prev]) > 0 else prev

  print(first_point, ' ,', secound_point)

  if secound_point == 0 or secound_point == (len(v) -1):
    if first_point > secound_point:
      return v[first_point:] + v[:first_point]
    else:
      return list(reversed(v[:first_point + 1])) + list(reversed(v[first_point+1 : ]))
  else:
    if first_point < secound_point:
      return v[first_point:] + v[:first_point]
    else:
      return list(reversed(v[:first_point + 1])) + list(reversed(v[first_point+1 : ]))



def triangulation(vert, turtle):
  aux_vert = preprocess(vert)
  # print(vert)
  # print(aux_vert)
  queue = []
  triangles = []
  for i,p in enumerate(aux_vert):
    queue.append(p)
    # time.sleep(0.5)
    # print("ADDED %s from pos %s" % (p, i))
    # turtle.color("green")
    # draw_circle(turtle, p, 5)
    # print(queue)
    while len(queue) > 2 \
          and orientation_test(queue[-3],queue[-1],queue[-2]) < 0 \
          and not polygon_intersection(queue[-3],queue[-1],aux_vert) \
          and not points_inside_triangle((queue[-3],queue[-1],queue[-2]), vert):
      triangles.append((queue[-3],queue[-2],queue[-1]))
      # print("REVOVED %s positon %s" % (str(queue[-2]), str(aux_vert.index(queue[-2]))))
      # turtle.color("blue")
      # draw_line(turtle, queue[-3], queue[-1])
      # turtle.color("red")
      # draw_circle(turtle, queue[-2], 5)
      del queue[-2]
  #     print(queue)
  # print(len(triangles))
  # print(len(vert))
  return triangles

def points_inside_triangle(triangle, points):
  for p in points:
    global_dir = orientation_test(triangle[0], triangle[1], p)
    if global_dir != orientation_test(triangle[1], triangle[2], p):
      continue
    if global_dir != orientation_test(triangle[2], triangle[0], p):
      continue
    return True
  return False


def point_inside_polygon(point, vert):
  print("Not implemented yet")
  return None
  global_dir = None
  for i in range(len(vert) - 1):
    if global_dir == None:
      global_dir = orientation_test(vert[i], vert[i + 1], point)
    elif global_dir == -orientation_test(vert[i], vert[i + 1], point):
      return False
  if global_dir == -orientation_test(vert[-1], vert[0], point):
    return False
  return True