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



def triangulation(vert):
  print("Not implemented yet")
  pass


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