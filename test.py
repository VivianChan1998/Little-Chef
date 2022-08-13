from lib2to3.pytree import convert
import cv2
import matplotlib.pyplot as plt
#import cv2.aruco as aruco
from picamera.array import PiRGBArray
from picamera import PiCamera

def convert2XY(point):
    return (int(point[0]), int(point[1]))


camera = PiCamera()

while(True):

    rawCapture = PiRGBArray(camera)

    camera.capture(rawCapture, format="bgr")
    frame = rawCapture.array


    
    
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    
    if len(corners) > 0:
        ids = ids.flatten()
        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4,2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            topLeft = convert2XY(topLeft)
            
        
            cv2.putText(frame, str(markerID), (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    frameS = cv2.resize(frame, (960,544))
    cv2.imshow('frame', frameS)

            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
cv2.destroyAllWindows()