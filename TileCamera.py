from sys import breakpointhook
import cv2
import numpy as np
import matplotlib.pyplot as plt
from picamera.array import PiRGBArray
from picamera import PiCamera
from bisect import bisect_left

camera = PiCamera()
DIR_TH = 10
NUM1_LINE = 200
ROW1_LINE = 300
NUM2_LINE = 450
ROW2_LINE = 600
NUM3_LINE = 800
ROW3_LINE = 900

Y_list = [200,320,450,600,800,900]
X_list = [250,400,600,750,800,900,1100,1400]

TILE_MAP = [
    [(1450, 200), (1350,200), (1200,200), (1000, 200), (800, 200), (600, 200), (450,200), (200,200)],
    [(1450, 320), (1350,320), (1200,320), (1000, 320), (800, 320), (600, 320), (450,320), (200,320)],

    [(1450, 450), (1350,450), (1200,450), (1000, 450), (800, 450), (600, 450), (450,450), (200,450)],
    [(1450, 600), (1350,600), (1200,600), (1000, 600), (800, 600), (600, 600), (450,600), (200,600)],

    [(1450, 800), (1350,800), (1200,800), (1000, 800), (800, 800), (600, 800), (450,800), (200,800)],
    [(1450, 900), (1350,900), (1200,900), (1000, 900), (800, 900), (600, 900), (450,900), (200,900)]
    
]


def determine_dir(topLeft, topRight, bottomLeft, bottomRight):
    if topLeft[1] - bottomLeft[1] > DIR_TH and topRight[1] - bottomRight[1] > DIR_TH:
        return 'D'
    elif bottomLeft[1] - topLeft[1] > DIR_TH and bottomRight[1] - topRight[1] > DIR_TH:
        return 'U'
    elif bottomLeft[1] - bottomRight[1] > DIR_TH and topLeft[1] - topRight[1] > DIR_TH:
        return 'R'
    else:
        return 'L'

def sortX(e):
    return e[3][0]

def sortY(e):
    return e[3][1]

def convert2XY(point):
    return (int(point[0]), int(point[1]))

def getCenter(corners):
    (topLeft, topRight, bottomRight, bottomLeft) = corners
    centerX = (topLeft[0] + bottomRight[0]) / 2
    centerY = (topLeft[1] + bottomRight[1]) / 2
    return (centerX, centerY)

def take_closest(myList, myNumber):
    pos = bisect_left(myList, int(myNumber))
    if pos == 0 or pos == len(myList):
        return pos
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return pos
    else:
        return pos-1

def calc_dist(pos, target):
    x_dist = target[0]-pos[0]
    y_dist = target[1]-pos[1]
    #dist = (pow(x_dist, 2) + pow(y_dist, 2)) ** 1/2

    return x_dist, y_dist

def get_tiles():
    tile_board = np.full((6, 8), None)
    tiles = []
    rawCapture = PiRGBArray(camera)

    camera.capture(rawCapture, format="bgr")
    frame = rawCapture.array

    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

    if len(corners) > 0:
        ids = ids.flatten()
        corners = [c.reshape(4,2) for c in corners]
        centers = [getCenter(c) for c in corners]
        markers = zip(corners, ids, centers, np.zeros(len(corners)), np.zeros(len(corners)))
        markers = list(markers)
        
        for idx,m in enumerate(markers):
            for i in range(6):
                for j in range(8):
                    c = m[2]
                    if c[0] > TILE_MAP[i][j][0] and c[1] > TILE_MAP[i][j][1]:
                        markers[idx] =list(markers[idx])
                        markers[idx][3] = i
                        markers[idx][4] = j
                        break

        count = 0

        for i in range(6):
            for j in range(8):
                cv2.putText(frame, str(i), (TILE_MAP[i][j][0] -10, TILE_MAP[i][j][1] -20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
                cv2.putText(frame, str(j), (TILE_MAP[i][j][0] +10, TILE_MAP[i][j][1] -20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
                cv2.circle(frame, TILE_MAP[i][j], radius=10, color=(0, 255, 255), thickness=-1)

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
                tile_board[m[3]][m[4]] = dir
            elif markerID == 1:
                tile_board[m[3]][m[4]] = 'P'
            elif markerID == 2:
                tile_board[m[3]][m[4]] = '2'
            elif markerID == 3:
                tile_board[m[3]][m[4]] = '3'
            elif markerID == 4:
                tile_board[m[3]][m[4]] = '4'
            elif markerID == 5:
                tile_board[m[3]][m[4]] = '5'
            elif markerID == 6:
                tile_board[m[3]][m[4]] = 'T'
            elif markerID == 7:
                tile_board[m[3]][m[4]] = 'K'
            elif markerID == 8:
                tile_board[m[3]][m[4]] = 'C'
            cv2.putText(frame, str(count), (bottomRight[0], bottomRight[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            
            count += 1
            '''
            cv2.line(frame, (0, NUM1_LINE), (1600,NUM1_LINE), (255,0,0), 2)
            cv2.line(frame, (0, ROW1_LINE), (1600,ROW1_LINE), (0,255,0), 2)
            cv2.line(frame, (0, NUM2_LINE), (1600,NUM2_LINE), (255,0,0), 2)
            cv2.line(frame, (0, ROW2_LINE), (1600,ROW2_LINE), (0,255,0), 2)
            cv2.line(frame, (0, NUM3_LINE), (1600,NUM3_LINE), (255,0,0), 2)
            cv2.line(frame, (0, ROW3_LINE), (1600,ROW3_LINE), (0,255,0), 2)
            '''
        print(tile_board)
    
    print(tiles)

    plt.imshow(frame)
    plt.show()

    return tiles

if __name__ == "__main__":
    while(True):
        get_tiles()


        