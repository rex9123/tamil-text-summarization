import math
import editdistance # type: ignore

def euclideanDistance(vector1, vector2):
  dist = [(a - b)**2 for a, b in zip(vector1, vector2)]
  dist = math.sqrt(sum(dist))
  return dist

def editDistance(w1, w2):
  return float(editdistance.eval(w1, w2))
