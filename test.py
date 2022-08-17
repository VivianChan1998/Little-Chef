import cv2
import matplotlib.pyplot as plt
import emoji
from numpy import tile
#import cv2.aruco as aruco
from picamera.array import PiRGBArray
from picamera import PiCamera
#from defisheye import Defisheye

dtype = 'linear'
format = 'fullframe'
fov = 180
pfov = 120

def convert2XY(point):
    return (int(point[0]), int(point[1]))

camera = PiCamera()
tiles = []
key = input("press enter to read >> ")

def determine_dir(topleft, topright, bottomleft, bottomright):
    return 'U'

while(True):
    if key == '':

        rawCapture = PiRGBArray(camera)

        camera.capture(rawCapture, format="bgr")
        frame = rawCapture.array

        arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        arucoParams = cv2.aruco.DetectorParameters_create()
        (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
        
        if len(corners) > 0:
            ids = ids.flatten()
            count = 0
            for (markerCorner, markerID) in zip(corners, ids):
                corners = markerCorner.reshape((4,2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                topLeft = convert2XY(topLeft)
                topRight = convert2XY(topRight)
                bottomLeft = convert2XY(bottomLeft)
                bottomRight = convert2XY(bottomRight)
                if markerID == 0:
                    tiles.append(determine_dir(topLeft, topRight, bottomRight, bottomLeft))
                elif markerID == 1:
                    tiles.append('P')
                elif markerID == 2:
                    tiles.append('2')
                elif markerID == 3:
                    tiles.append('3')
                elif markerID == 4:
                    tiles.append('4')
                elif markerID == 5:
                    tiles.append('5')
                elif markerID == 6:
                    tiles.append('T')
                elif markerID == 7:
                    tiles.append('K')
                elif markerID == 8:
                    tiles.append('C')
                cv2.putText(frame, str(markerID), (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                cv2.putText(frame, str(count), (bottomRight[0], bottomRight[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                count += 1
        frameS = cv2.resize(frame, (960,544))
        #obj = defisheye(frameS, dtype=dtype, format=format, fov=fov, pfov=pfov)
        #obj.convert(img_out)
        plt.imshow(frameS)
        plt.show()
        print(tiles)

        tiles = []

        #cv2.waitKey(0)
    
  
cv2.destroyAllWindows()