import math
import time
from drawing import *

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


def orientation_test_Err(p1, p2, r):
  direction = p2[0] * r[1] + p1[0] * p2[1] + p1[1] * r[0] - \
    p1[1] * p2[0] - p2[1] * r[0] - p1[0] * r[1]

  if direction > 0.0001:
    return 1
  if direction < -0.0001:
    return -1
  else:
    return 0

def collinear_points(A, B, C):
  return orientation_test(A, B, C) == 0

def collinear_points_Err(A, B, C):
  return orientation_test_Err(A, B, C) == 0


def length(A, B):
 return math.sqrt(pow((A[0] - B[0]), 2) + pow((A[1] - B[1]), 2))


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

    proints_drawer.color("green")
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


def point_of_intersection(A, B, C, D):
  aAB = A[1] - B[1]
  bAB = B[0] - A[0]
  cAB = A[0]*B[1] - A[1]*B[0]

  aCD = C[1] - D[1]
  bCD = D[0] - C[0]
  cCD = C[0]*D[1] - C[1]*D[0]

  # test if AB and CD are parallel
  if aAB*bCD - bAB*aCD != 0: #< -0.0001 or aAB*bCD - bAB*aCD > 0.0001:
    interX = (-cAB*bCD - bAB*-cCD)/(aAB*bCD - bAB*aCD)
    interY = (aAB*-cCD - (-cAB)*aCD)/(aAB*bCD - bAB*aCD)
    return(interX, interY)
  else:
    return None

def raport(A, B, C):

  if B[0] == C[0] and B[1] == C[1]:
    return None

  AB = (B[0] - A[0], B[1] - A[1])
  BC = (C[0] - B[0], C[1] - B[1])
  
  if BC[0] != 0: #A[1] != B[1]:
    return AB[0]/BC[0]
  elif A[0] != B[0]:
    return AB[1]/BC[1]    

def on_edge(AB, X):
  if collinear_points_Err(AB[0], AB[1], X):
    if AB[0][0] != AB[1][0] and (AB[0][0] <= X[0] <= AB[1][0] or AB[0][0] >= X[0] >= AB[1][0]):
      return True
    elif AB[0][0] == AB[1][0] and (AB[0][1] <= X[1] <= AB[1][1] or AB[0][1] >= X[1] >= AB[1][1]):
      return True
  return False

def same_edge(vert, A, B):
  n = len(vert)
  for i in range(0, n):
    MN = (vert[i%n], vert[(i+1)%n])
    if on_edge(MN, A) and on_edge(MN, B):
      return True
  return False


def correct_order(vert, allVertices, vP):
  vert.sort(key=lambda vertex: (math.atan2(vertex[1] - vP[1], vertex[0] - vP[0]), +(math.sqrt((vertex[0]-vP[0])**2 + (vertex[1]-vP[1])**2))))
  
  for i in range(0, len(vert)):
    A = vert[i%len(vert)]
    B = vert[(i+1)%len(vert)]
    C = vert[(i+2)%len(vert)]
    D = vert[(i-1)%len(vert)]

    if collinear_points_Err(vP, A, B):

      if B in allVertices:
        (A, B) = (B, A)
        print("A <-> B")
        (vert[i%len(vert)], vert[(i+1)%len(vert)]) = (vert[(i+1)%len(vert)], vert[i%len(vert)])

      if A in allVertices and orientation_test(vP, A, allVertices[allVertices.index(A)-1]) > 0:
        (vert[i%len(vert)], vert[(i+1)%len(vert)]) = (vert[(i+1)%len(vert)], vert[i%len(vert)])


  return vert

def visible_area(vertices, triangles, viewPoint):
  vert = vertices[:]
  vert.append(vert[0])
  result = []
  M = viewPoint    # M = view point
  
  for V in vert:
    # intermediar list
    interList = []
    interList.append(V)
    
    for i in range(1, len(vert)):
      if vert[i] == V or vert[i-1] == V:
        continue
      
      I = point_of_intersection(M, V, vert[i-1], vert[i])

      if I and raport(vert[i-1], I, vert[i]) and raport(vert[i-1], I, vert[i]) > 0:   # daca se intersecteaza in interior
        if raport(M, V, I) and raport(M, V, I) > 0:                                                       # daca ordinea este pe M-V-I
          if len(interList) == 1:
            interList.append(I)
          elif len(interList) > 1 and length(interList[0], I) < length(interList[0], interList[1]):
            interList.pop()
            interList.append(I)
        elif raport(M, I, V) and raport(M, I, V) > 0:
          interList[:] = []
          continue
    
    if len(interList) > 1 and not point_inside_polygon(triangles, ((V[0] + interList[1][0])/2, (V[1] + interList[1][1])/2)):
      interList[:] = interList[0:1]

    result.extend(interList)
        
  #result.sort(key=lambda vertex: math.atan2(vertex[1] - viewPoint[1], vertex[0] - viewPoint[0]))

  i = 0
  while i < len(result)-1:
    if result[i] == result[i+1]:
      result.pop(i)
    else:
      i = i+1
  
  result = correct_order(result, vertices, viewPoint)

  print(result)
  return result

    
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
