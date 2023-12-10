from cv2 import cv2
import numpy as np
from kd_tree import Node
from kd_tree import KDTree

def extract_minutiae(image_path):
    image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    image_blur = cv2.GaussianBlur(image,(5,5),0)
    _,image_thresh = cv2.threshold(image_blur,120,255,cv2.THRESH_BINARY_INV)
    image_contours,_ = cv2.findContours(image_thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    image_minutiae = np.zeros_like(image,dtype=np.uint8)
    far_points = []
    for i in image_contours:
        hull = cv2.convexHull(i,returnPoints=False)
        try:
            defects = cv2.convexityDefects(i, np.array([hull]))
            if defects is not None:
                for j in range(defects.shape[0]):
                    s, e, f, _ = defects[j, 0]
                    start = tuple(i[s][0])
                    end = tuple(i[e][0])
                    far = tuple(i[f][0])
                    far_points.append(far)
                    cv2.circle(image_minutiae, far, 3, (255, 255, 255), -1)
        except cv2.error as e:
            continue
    return far_points

def euclidean_distance(point1,point2):
    if point1 is None or point2 is None:
        return float('inf')
    return ((point1[0]-point2[0])**2 + (point1[1]-point2[1]) ** 2) ** 0.5

def match_fingerprints(q_point, r_tree, threshold):
    matches = []
    for i in q_point:
        n_point = r_tree.find_nearest_neighbor(i)
        dis = euclidean_distance(i,n_point)
        if dis <= threshold:
            matches.append((i,n_point))
    return matches