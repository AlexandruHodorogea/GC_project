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


def collinear_points(A, B, C):
  return orientation_test(A, B, C) == 0


# def length(A, B):
#   return sqrt(pow((A[0] - B[0]), 2) + pow((A[1] - B[1]), 2))


# def get_angle(A, B, C):
#   return arccos((pow(length(A, B), 2) + pow(length(C, B),2) - pow(length(A, B), 2)) \
#                 / 2 * length(A, B) * length(C, B)) / 3.14 * 180

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
  print(v)
  print(prev)
  print(nxt)
  print("current %s, next %s, prev %s" % (str(v[first_point]), str(v[nxt]), str(v[prev])))
  secound_point = nxt if orientation_test(v[first_point], v[nxt], v[prev]) > 0 else prev
  print("preprocess_orientation_test "+ str(orientation_test(v[first_point], v[nxt], v[prev])))
  print(first_point, ' ,', secound_point)
  print("vert len ", str(len(v)))

  if abs(first_point - secound_point) > 1:
    if first_point > secound_point:
      return v[first_point:] + v[:first_point]
    else:
      return list(reversed(v[:first_point + 1])) + list(reversed(v[first_point+1 : ]))
  else:
    if first_point < secound_point:
      return v[first_point:] + v[:first_point]
    else:
      return list(reversed(v[:first_point + 1])) + list(reversed(v[first_point+1 : ]))



def triangulation(vert, lines_drawer, proints_drawer):
  aux_vert = preprocess(vert)
  print(vert)
  print(aux_vert)
  queue = []
  triangles = []
  for i,p in enumerate(aux_vert):
    queue.append(p)
    # time.sleep(0.5)
    # print("ADDED %s from pos %s" % (p, i))
    # print(queue)

    proints_drawer.color("blue")
    draw_circle(proints_drawer, p, 5)

    
    while len(queue) > 2 \
          and orientation_test(queue[-3],queue[-1],queue[-2]) < 0 \
          and not polygon_intersection(queue[-3],queue[-1],aux_vert) \
          and not points_inside_triangle((queue[-3],queue[-1],queue[-2]), vert):
      triangles.append((queue[-3],queue[-2],queue[-1]))
      # print("REVOVED %s positon %s" % (str(queue[-2]), str(aux_vert.index(queue[-2]))))

      draw_line(lines_drawer, queue[-3], queue[-1])
      proints_drawer.color("red")
      draw_circle(proints_drawer, queue[-2], 5)
      del queue[-2]
      # print(queue)
  #   if len(queue) > 2:
  #     print('orientation, ' + str(orientation_test(queue[-3],queue[-1],queue[-2]) < 0))
  #     print('ply_itersection, ' + str(polygon_intersection(queue[-3],queue[-1],aux_vert))) 
  #     print('points insiide, ' +str(points_inside_triangle((queue[-3],queue[-1],queue[-2]), vert)))
  # print(len(triangles))
  # print(len(vert))
  proints_drawer.clear()
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


def point_inside_polygon(triangles, point):
  for t in triangles:
    if points_inside_triangle(t, [point]):
      return True
  return False
