#====================================================================
#                          L I B R A R I E S
#====================================================================

import io
import os
import cv2
import math
import time
import random
import numpy as np
import matplotlib.pyplot as plt 
from google.colab.patches import cv2_imshow

import warnings
warnings.filterwarnings("ignore")

#------------------------- Libraries <end> -------------------------


#====================================================================
#                           Utility :: Output
#====================================================================

def get_points(model_output):
  '''returns 17 keypoints'''
  pts_ar = model_output['instances'].pred_keypoints[0].cpu().detach().numpy()

  _points = []
  for i in range(17):
    _points.append(np.array([pts_ar[i][0], pts_ar[i][1]]))

  return _points

def get_points_extended(_points, _bbox):
  '''returns extended 34 points'''
  p0 = np.array(get_middle(_points[5], _points[6]))     # 17 :: shoulder mid
  p1 = np.array(get_middle(_points[11], _points[12]))   # 18 :: hip mid
  p2 = np.array(get_middle(_points[15], _points[16]))   # 19 :: ankle mid
  
  b0, b1, b2, b3 = process_bbox(_bbox)
  
  p3 = np.array(get_middle(b0, b1))                     # 20 :: upper bbox mid
  p4 = np.array(get_middle(b2, b3))                     # 21 :: lower bbox mid
  
  
  # special points, exercise dependent
  # 4ab
  dist_35 = point_distance(_points[3], _points[5])      
  dist_46 = point_distance(_points[4], _points[6])
  p5 = np.array((_points[5][0], _points[5][1] - dist_35), dtype='float32') # 22 :: used in 4ab
  p6 = np.array((_points[6][0], _points[6][1] - dist_35), dtype='float32') # 23 :: used in 4ab
  
  # Ex.8ab
  # dist_0_17 = point_distance(_points[3], p0)          # alternate :: 20
  # px = np.array(p0[0], p0[1] - dist_0_17)             # used in 8ab
  
  # Ex.12, 13
  dist_57 = point_distance(_points[5], _points[7])
  dist_68 = point_distance(_points[6], _points[8])
  p7 = np.array((_points[5][0], _points[5][1] + dist_57), dtype='float32') # 24 :: used in ex.13  
  p8 = np.array((_points[6][0], _points[6][1] + dist_68), dtype='float32') # 25 :: used in ex.12
  
  # Ex.31, 33
  dist_0_18 = point_distance(_points[0], p1)
  p9 = np.array((_points[0][0], _points[0][1] - dist_0_18), dtype='float32') # 26 :: 
  
  # Ex.36
  dist_3_11 = point_distance(_points[3], _points[11])
  dist_4_12 = point_distance(_points[4], _points[12])
  p10 = np.array((_points[11][0], _points[11][1] - dist_3_11), dtype='float32') # 27 :: 
  p11 = np.array((_points[12][0], _points[12][1] - dist_4_12), dtype='float32') # 28 :: 
  
  # Ex.24, 25
  p12 = np.array(get_middle(_points[9], _points[10]))                       # 29 :: wrist middle
  
  
  _points_ex = _points.copy()
  _points_ex.extend([p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, b0, b1, b2, b3])    # 30, 31, 32, 33 for bbox constraint

  return _points_ex

def get_points_calibrated(_points_ex, adjust, proportion):
  # Ex. 8ab
  c0_x = _points_ex[17][0]
  c0_y = _points_ex[17][1] - adjust / proportion
  c0 = np.array((c0_x, c0_y), dtype='float32')                              # 34 :: mid shoulder, y adjust
  
  # Ex. 5ab, 6ab
  c1_x = _points_ex[0][0]
  c1_y = _points_ex[17][1]
  c1 = np.array((c1_x, c1_y), dtype='float32')                              # 35 :: mid shoulder, by nose

  _points_cal = _points_ex.copy()
  _points_cal.extend([c0, c1])
  
  return _points_cal

def get_bbox(model_output):
  _bbox = model_output['instances'].pred_boxes.tensor[0].cpu().detach().numpy()
  return _bbox
  
def process_bbox(_bbox):
  '''returns four points (x, y) of bbox'''
  b0 = np.array((_bbox[0], _bbox[1]), dtype='float32')
  b1 = np.array((_bbox[2], _bbox[1]), dtype='float32')
  b2 = np.array((_bbox[0], _bbox[3]), dtype='float32')
  b3 = np.array((_bbox[2], _bbox[3]), dtype='float32')
  return b0, b1, b2, b3

def get_height(_bbox):
  '''returns height calculated from bbox'''
  height = abs(_bbox[1] - _bbox[3])
  width  = abs(_bbox[0] - _bbox[2])
  if height > width: return height
  else: return width

#-------------------- Utility :: Output <end> -----------------------


#====================================================================
#                            Utility :: Image
#====================================================================

def process_image(img_dir):
  '''trim left and right black borders of an image'''
  im = cv2.imread(img_dir)
  h, w, c = im.shape
  for i in range(w):
      if np.sum(im[:, i, :]) > 0:
          break
  for j in range(w-1, 0, -1):
      if np.sum(im[:, j, :]) > 0:
          break
  cropped = im[:, i:j+1, :].copy()
  return cropped[:, :, ::-1]

#----------------------- Utility :: Image <end> ----------------------


#====================================================================
#                          Utility :: Geometry
#====================================================================
def get_angle(a, b, c):
  '''
  Calculates angle between the lines drawn from three points
    Parameters:
      a, b, c (np.array of length 2) :: x, y co-ordinates of three points
    Returns:
      angle in degrees
  '''
  ba = a - b
  bc = c - b

  cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
  angle = np.arccos(cosine_angle)
  return np.degrees(angle)

def convert_points_to_xys(list_of_points):
  '''convert points to its xs & ys'''
  _x = []
  _y = []
  for point in list_of_points:
    _x.append(point[0])
    _y.append(point[1])
  return _x, _y

def point_distance(p1, p2):
  '''returns euclidian distance between two points'''
  x1, y1 = p1
  x2, y2 = p2
  return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
    
def get_middle(p1, p2):
  '''returns middle point between two points'''
  x1, y1 = p1
  x2, y2 = p2
  xm, ym = np.float32((x1+x2)/2), np.float32((y1+y2)/2)
  return (xm, ym)
    
def avg(a, b):
  '''returns avg of two values'''
  return (a + b) / 2

#--------------------- Utility :: Geometry <end> ----------------------


#====================================================================
#                       Utility :: Visualization
#====================================================================

#------------------- Utility :: Visualization <end> ------------------


#====================================================================
#                  Utility :: Body Parts Measurement
#====================================================================

def estimate_measurements(model_output, height=160.02, adjust=0.0):
  '''estimate body parts measurement from model_output and subject height'''
  _points = get_points(model_output)
  
  euclid_dist = {}
  nose_lEye = point_distance(_points[0], _points[1])
  nose_rEye = point_distance(_points[0], _points[2])
  euclid_dist['nose_eye'] = avg(nose_lEye, nose_rEye)

  nose_lEar = point_distance(_points[0], _points[3])
  nose_rEar = point_distance(_points[0], _points[4])
  euclid_dist['nose_ear'] = avg(nose_lEar, nose_rEar)

  euclid_dist['eye_eye'] = point_distance(_points[1], _points[2])
  euclid_dist['ear_ear'] = point_distance(_points[3], _points[4])
  
  lArm = point_distance(_points[5], _points[7])
  rArm = point_distance(_points[6], _points[8])
  euclid_dist['arm'] = avg(lArm, rArm)

  lForearm = point_distance(_points[7], _points[9])
  rForearm = point_distance(_points[8], _points[10])
  euclid_dist['forearm'] = avg(lForearm, rForearm)

  lThigh = point_distance(_points[11], _points[13])
  rThigh = point_distance(_points[12], _points[14])
  euclid_dist['thigh'] = avg(lThigh, rThigh)

  lLeg = point_distance(_points[13], _points[15])
  rLeg = point_distance(_points[14], _points[16])
  euclid_dist['leg'] = avg(lLeg, rLeg)

  euclid_dist['body'] = get_height(get_bbox(model_output))
  
  calib_dist = {}
  proportion = height/euclid_dist['body']
  for key in euclid_dist.keys():
    calib_dist[key] = euclid_dist[key]*proportion

  # calib_dist :: cm
  # proportion :: cm / pixel
  return calib_dist, proportion

def evaluate(true_msnt, calc_msnt):
  '''evaluates body measurement estimation'''
  _eval = {}
  abs_err = 0.0
  sqr_err  = 0.0
  for key in true_msnt.keys():
    abs_err += abs(true_msnt[key] - calc_msnt[key])
    sqr_err += abs_err*abs_err
  MSE = sqr_err / len(true_msnt.keys())

  _eval['MAE'] = abs_err / len(true_msnt.keys())
  _eval['RMSE'] = math.sqrt(MSE)

  return _eval

#-------------- Utility :: Body Parts Measurement <end> --------------


#====================================================================
#                          Utility :: Video
#====================================================================

def video_to_frames(video_dir, frames_dir):
  '''generates all frames from a video
    Parameters:
      video_dir  :: directory of the video where the video is kept
      frames_dir :: directory of the frames where the frames are to be saved
  '''
  vidcap = cv2.VideoCapture(video_dir)
  success, image = vidcap.read()
  count = 1
  prefix = '000'
  while success:
    if count == 10: prefix = '00'
    elif count == 100: prefix = '0'
    cv2.imwrite(f'{frames_dir}/frame{prefix+str(count)}.jpg', image)
    success, image = vidcap.read()
    count += 1
#---------------------- Utility :: Video <end> ----------------------
