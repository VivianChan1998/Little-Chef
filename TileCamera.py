from sys import breakpointhook
import cv2
import numpy as np
import matplotlib.pyplot as plt
from picamera.array import PiRGBArray
from picamera import PiCamera
from bisect import bisect_left

SHOW = True

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
    [(1156,278), (1032,271), ( 910, 256), (759, 254), (626, 280), (512,286), (396,301),(308,309)],
    [(1152,364), (1030,360), ( 897,350), (755,365), (610,380), (470,388), (385,397), (312,398)],

    [(1178,499), (1047,511), (920,497), (757,503), (650,515), (515,512), (420,514), (318,516)],
    [(1176,599), (1049,609), (896,616), (774,615), (635,608), (530, 600), (407,605), (317,598)],

    [(1175,746), (1037,752), (914,763), (760,760), (641,766), (523,755), (424,737), (331,736)],
    [(1167,841), (1040,865), (902,867), (761,864), (647,858), (524,854), (419,834), (333,823)]
    
]


def determine_dir(topLeft, topRight, bottomLeft, bottomRight):
    if topLeft[1] - bottomLeft[1] > DIR_TH and topRight[1] - bottomRight[1] > DIR_TH:
        return 'D'
    elif bottomLeft[1] - topLeft[1] > DIR_TH and bottomRight[1] - topRight[1] > DIR_TH:
        return 'U'
    elif topLeft[0] - bottomLeft[0] > DIR_TH and topRight[0] - bottomRight[0] > DIR_TH:
        return 'L'
    else:
        return 'R'

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
    tile_pos = np.full((6, 8), None)
    tiles = []
    tiles_p = []
    rawCapture = PiRGBArray(camera)

    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array

    alpha = 2.2
    beta = 0

    frame = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

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
            i = int(m[3])
            j = int(m[4])
            if markerID == 0:
                dir = determine_dir(topLeft, topRight, bottomRight, bottomLeft)
                tile_board[i][j] = dir
                tile_pos[i][j] = (i,j)
            elif markerID == 1:
                tile_board[i][j] = 'P'
                tile_pos[i][j] = (i,j)
            elif markerID == 2:
                tile_board[i][j] = '2'
                tile_pos[i][j] = (i,j)
            elif markerID == 3:
                tile_board[i][j] = '3'
                tile_pos[i][j] = (i,j)
            elif markerID == 4:
                tile_board[i][j] = '4'
                tile_pos[i][j] = (i,j)
            elif markerID == 5:
                tile_board[i][j] = '5'
                tile_pos[i][j] = (i,j)
            elif markerID == 6:
                tile_board[i][j] = 'T'
                tile_pos[i][j] = (i,j)
            elif markerID == 7:
                tile_board[i][j] = 'K'
                tile_pos[i][j] = (i,j)
            elif markerID == 8:
                tile_board[i][j] = 'C'
                tile_pos[i][j] = (i,j)
            else:
                tile_board[i][j] = None
                tile_pos[i][j] = (i,j)
            cv2.putText(frame, str(count), (bottomRight[0], bottomRight[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            
            count += 1
    
    for i in range(3):
        for j in range(8):
            n = tile_board[i*2][j]
            n_pos = tile_pos[i*2][j]
            t = tile_board[i*2+1][j]
            t_pos = tile_pos[i*2+1][j]
            if t != None:
                if n != None:
                    tiles.append(n)
                    tiles_p.append(n_pos)
                tiles.append(t)
                tiles_p.append(t_pos)


    print(tiles)
    print(tiles_p)
    print("------------------------------")

    if(SHOW):
        plt.imshow(frame)
        plt.show()

    return tiles, tiles_p

def get_tiles_5():
    t = []
    for i in range(5):
        ti = get_tiles()
        if len(ti) > len(t):
            t = ti
    return t

if __name__ == "__main__":
    tt = get_tiles_5()
    print(tt)


        