import cv2
import matplotlib.pyplot as plt
#import cv2.aruco as aruco
from picamera.array import PiRGBArray
from picamera import PiCamera


camera = PiCamera()

while(True):

    rawCapture = PiRGBArray(camera)

    camera.capture(rawCapture, format="bgr")
    frame = rawCapture.array
  
    cv2.imshow('frame', frame)
    
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv2.destroyAllWindows()