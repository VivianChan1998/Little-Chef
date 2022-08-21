import cv2
import matplotlib.pyplot as plt
from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()
tiles = []
key = input("press enter to read >> ")

DIR_TH = 10
NUM1_LINE = 450
ROW1_LINE = 600
NUM2_LINE = 750
ROW2_LINE = 900
NUM3_LINE = 900
ROW3_LINE = 1000


def determine_dir(topLeft, topRight, bottomLeft, bottomRight):
    print(topLeft)
    print(bottomRight)
    if topLeft[1] - bottomLeft[1] > DIR_TH and topRight[1] - bottomRight[1] > DIR_TH:
        return 'D'
    elif bottomLeft[1] - topLeft[1] > DIR_TH and bottomRight[1] - topRight[1] > DIR_TH:
        return 'U'
    elif bottomLeft[1] - bottomRight[1] > DIR_TH and topLeft[1] - topRight[1] > DIR_TH:
        return 'R'
    else:
        return 'L'

def sortX(e):
    c = getCenter(e[0][0])
    return c[0]

def sortY(e):
    c = getCenter(e[0][0])
    print(c)
    return c[1]/100

def convert2XY(point):
    return (int(point[0]), int(point[1]))

def getCenter(corners):
    (topLeft, topRight, bottomRight, bottomLeft) = corners
    centerX = (topLeft[0] + bottomRight[0]) / 2
    centerY = (topLeft[1] + bottomRight[1]) / 2
    return (centerX, centerY)

def get_tiles():
    rawCapture = PiRGBArray(camera)

    camera.capture(rawCapture, format="bgr")
    frame = rawCapture.array

    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

    if len(corners) > 0:
        ids = ids.flatten()
        
        markers = zip(corners, ids)
        markers = list(markers)
        markers.sort(reverse=True, key = sortX)
        #markers.sort(key = sortY)
        
        #TODO split rows...

        count = 0
        
        for m in markers:
            corners = m[0].reshape((4,2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            topLeft = convert2XY(topLeft)
            topRight = convert2XY(topRight)
            bottomLeft = convert2XY(bottomLeft)
            bottomRight = convert2XY(bottomRight)
            dir = 'X'
            markerID = m[1]
            if markerID == 0:
                dir = determine_dir(topLeft, topRight, bottomRight, bottomLeft)
                tiles.append(dir)
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
            cv2.putText(frame, dir, (topLeft[0], topLeft[1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            cv2.putText(frame, str(count), (bottomRight[0], bottomRight[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            count += 1
            cv2.line(frame, (0, NUM1_LINE), (1600,NUM1_LINE), (255,0,0), 2)
            cv2.line(frame, (0, ROW1_LINE), (1600,ROW1_LINE), (0,255,0), 2)
            cv2.line(frame, (0, NUM2_LINE), (1600,NUM2_LINE), (255,0,0), 2)
            cv2.line(frame, (0, ROW2_LINE), (1600,ROW2_LINE), (0,255,0), 2)
            cv2.line(frame, (0, NUM3_LINE), (1600,NUM3_LINE), (255,0,0), 2)
            cv2.line(frame, (0, ROW3_LINE), (1600,ROW3_LINE), (0,255,0), 2)
            
    #frameS = cv2.resize(frame, (960,544))
    
    
    print(tiles)

    plt.imshow(frame)
    plt.show()

    return tiles

if __name__ == "__main__":
    while(True):
        if key == '':
            get_tiles()
            tiles = []

        