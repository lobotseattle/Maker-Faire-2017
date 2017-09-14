# pylint: disable=missing-docstring, C0103, E1101, C0325, C0326, W0612, C0301, R0903, W0603, R0914, C0303, W0613, E1126,C0330, W0311, C0326, W0702

# import math
from collections import OrderedDict, namedtuple
from operator import attrgetter
import winsound
import time
import io
import sys
import serial

import ttgamemodule as gm


import numpy as np

import cv2

# define the list of boundaries
webcam = None

xRes = int(640)
yRes = int(480)

maxTileArea = 6000*(xRes/640)*(yRes/480)
minTileArea = 3000*(xRes/640)*(yRes/480)
maxChipArea = 600*(xRes/640)*(yRes/480)
minChipArea = 250*(xRes/640)*(yRes/480)

# greenHSVRanges = [
#     ([50, 200, 200], [70, 255, 255])    
# ]
greenHSVRanges = [
    ([50, 100, 70], [60, 190, 100])    
]

redHSVRanges = [
    ([0, 70, 50], [10, 255, 255])
    ,
    ([170, 70, 50], [180, 255, 255])
]

blueHSVRanges = [
    ([10, 50, 50], [160, 255, 255])    
    # ([10, 50, 50], [160, 255, 255])    

]

#use this instead of multiple ranges for red
cyanHSVRanges = [
    ([80, 70, 50], [200, 255, 255])    
]

# Stores the state of the tictactoc grid
ticTacToeGrid = []
gameInProgress = True
waitingForUserMove = False
startGame = False
gameDifficultyLevel = "D"
playerMove = 0
origImgForShow = 0
borderImgForShow = 0
tilesImgForShow = 0
playerImgForShow = 0
croppedImgForShow = 0
ser = None

Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')

coordinateMap = OrderedDict(
    {
        8:8
        ,7:7
        ,6:6
        ,5:5
        ,4:4
        ,3:3
        ,2:2
        ,1:1
        ,0:0
    }
)


class ticTacToeCell:
    UNKNOWN = "U"
    OCCUPIED = "Occupied"
    EMPTY = "Empty"
    PLAYER = "P"
    COMPUTER = "C"

    index = 0
    cellOccupied = UNKNOWN
    cellOwner = UNKNOWN

    def __init__(self):
        pass
    
    def print(self):
        tu1 = (self.index, self.cellOccupied, self.cellOwner)
        printText = "{0:d} {1:s} {2:s}".format(*tu1)
        print(printText)
    
    def printTabular(self):
        val = 0
        if (self.cellOccupied==self.OCCUPIED):
            val=self.cellOwner
        else:
            val=self.EMPTY
        print(self.index,":",val,"\t", end="") 

    def copy(self):
        c = ticTacToeCell()
        c.index = self.index
        c.cellOccupied = self.cellOccupied
        c.cellOwner = self.cellOwner
        return c


def printTicTacToeGrid(tttGrid,context):
    cellCount = len(tttGrid) 
    print(cellCount,context)    
    for i in tttGrid:
        print(i.__class__)
        i.printTabular()
    print()

def getTicTacToeGridCopy(tttGrid):
    grid = []
    cellCount = len(tttGrid)     
    for i in range(0,cellCount):
        c = tttGrid[i].copy()
        grid.append(c)
    return grid

class gridContoursClass:
    TILE = "Tile"
    CHIP = "Chip"
    UNKNOWN = "Unknown"
    index = 0
    x = 0
    y = 0
    w = 0
    h = 0
    cx = 0
    cy = 0
    contour = None
    contourType = UNKNOWN

    def __init__(self):
        pass

    def print(self):
        tu1 = (self.index, self.x, self.y, self.cx, self.cy)
        printText = "{0:d} {1:d} {2:d} {3:d} {4:d}".format(*tu1)
        print(printText)


def getWebCam():
    global webcam
    if (webcam is None):
        webcam = cv2.VideoCapture(1)
    return webcam

def getCameraImage():
    global webcam
    rval = False
    frame = 0
    rotatedFrame = 0
    webcam = getWebCam()
    ramp_frames=20
    # Loop until the camera is working
    while(not rval):
        webcam = getWebCam()
        # Ramp the camera - these frames will be discarded and are only used to allow
        # to adjust light levels, if necessary
        for i in range(ramp_frames):
            (rval, frame) = webcam.read()
        
        # Take the actual image we want to keep

        (rval, frame) = webcam.read()

        #rotate the image
        
        if(not rval):
            print("Failed to open webcam. Trying again...")
            webcam = None
    
    return frame


def getImage(fName):
    img = cv2.imread(fName, cv2.IMREAD_COLOR)

    if img is None:
        print ("File not found", " ", fName)
    return img

def getGrayAndBlurredImage(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (15, 15), 0)
    return gray

def getHSVImage(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return hsv        

def displayBorderCoordinates(img, cell):
    defaultColor = (0,255,0)
    textColor = (255,255,255)

    if (cell is None):
        return

    contour = cell.contour
    x, y, w, h = cv2.boundingRect(contour)
    area = int(cv2.contourArea(contour))
    
    tu1 = (cell.index,area)
    # contourValues1 = "{0:d},{1:d}".format(*tu1)
    contourValues1 = "{0:d}".format(*tu1)

    tu2 = (x,y)
    contourValues2 = "{0:d},{1:d}".format(*tu2)        

    origin1 = (x+5, y+20)
    origin2 = (x+5, y+40)

    cv2.putText ( img, contourValues1, origin1, cv2.FONT_HERSHEY_PLAIN, 1 , textColor )
    # cv2.putText ( img, contourValues2, origin2, cv2.FONT_HERSHEY_PLAIN, 1 , textColor )
        

def markBorders(img, cells):

    defaultColor = (0,255,0)
    textColor = (255,255,255)

    areas = []
    #get how many contours are present

    if (cells is None):
        return
    
    for cell in cells:
        contour = cell.contour
        x, y, w, h = cv2.boundingRect(contour)
        borderColor = defaultColor
        cv2.rectangle(img, (x,y), (x+w, y+h), borderColor, 3)
        displayBorderCoordinates(img, cell)

def rotateImage(image, angle):
    center=tuple(np.array(image.shape[0:2])/2)
    rot_mat = cv2.getRotationMatrix2D(center,angle,yRes/xRes)
    return cv2.warpAffine(image, rot_mat, image.shape[0:2],flags=cv2.INTER_LINEAR)

def sortCellBorders(cells):
    # sort the contours based on left to right,top to bottom,where x is at position0, y at position 1
    sortedcells=sorted(cells, key=attrgetter('x', 'y'),reverse=True)
    return sortedcells

def getCellBorders(contours):
    cells = []
    noOfItems=len(contours)
    if (noOfItems >= 1):
        index=0
        for i in range(0,noOfItems):
            currentContour = contours[i]
            area = cv2.contourArea(currentContour)
            # print ("Cell number and area", i, area)
            if (area >= minTileArea and area <= maxTileArea):
                c = gridContoursClass()
                c.index = index
                c.contourType=c.TILE
                c.contour=currentContour
                x, y, w, h = cv2.boundingRect(currentContour)
                c.x = x
                c.y = y
                c.w = w
                c.h = h
                # compute centroid of the contours
                M = cv2.moments(currentContour)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cells.append(c)
                index = index + 1
    return cells

def getChipBorders(contours):
    cells = []
    noOfItems=len(contours)
    if (noOfItems >= 1):
        index=0
        for i in range(0,noOfItems):
            currentContour = contours[i]
            area = cv2.contourArea(currentContour)
            # print ("Object number and area", i, area)
            if (area >= minChipArea and area <= maxChipArea):
                c = gridContoursClass()
                c.index = index
                c.contourType=c.CHIP
                c.contour=currentContour
                x, y, w, h = cv2.boundingRect(currentContour)
                c.x = x
                c.y = y
                c.w = w
                c.h = h
                cells.append(c)
                index = index + 1
    return cells

def fixSortOrder(sortedCells):
    if sortedCells is None: 
        return
    lenC = len (sortedCells)
    for i in range(0,lenC):
        c = sortedCells[i]
        c.index = i
        # c.print()

    # for c in sortedCells:
    #     oldSortIndex = c.index
    #     newSortIndex = coordinateMap[oldSortIndex]
    #     c.index = newSortIndex


# use the blue object detection and get all the objects
def getSortedCellBorders(img):
    global tilesImgForShow
    hsv = getHSVImage(img)

    lower =  blueHSVRanges[0][0]
    upper =  blueHSVRanges[0][1]

    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(hsv,hsv,mask=mask)
    tilesImgForShow = output.copy()
    # cv2.imshow("tiles", output)
    
    
    grayImg = getGrayAndBlurredImage(output)
    ret, thresh = cv2.threshold(grayImg, 127, 255, cv2.THRESH_BINARY)
    img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    cells = getCellBorders(contours)
    sortedCells = sortCellBorders(cells)
    fixSortOrder(sortedCells)

    return sortedCells

def capToBoundaries(val, val1, val2):
    lowbound = min(val1, val2)
    upperbound = max(val1, val2)
    if (val < lowbound):
        return lowbound
    if (val > upperbound):
        return upperbound
    return val

def upperBound(val, bound):
    if (val > bound):
        return bound
    return val

def getTTTFrameFromImg(img):
    global borderImgForShow
    x=0
    y=0
    w=0
    h=0

    hsv = getHSVImage(img)

    lower =  blueHSVRanges[0][0]
    upper =  blueHSVRanges[0][1]

    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")


    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(hsv,hsv,mask=mask)
    
    borderImgForShow = output.copy()
    
    
    grayImg = getGrayAndBlurredImage(output)
    ret, thresh = cv2.threshold(grayImg, 127, 255, cv2.THRESH_BINARY)
    img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    areas = [cv2.contourArea(c) for c in contours]
    lenAreas = len(areas)
    if (lenAreas > 0):
        max_index = np.argmax(areas)
        cnt=contours[max_index]
        x, y, w, h = cv2.boundingRect(cnt)

        defaultColor = (0,255,0)
        cv2.rectangle(output, (x,y), (x+w, y+h), defaultColor, 3)        

    return x,y,w,h

def getTTTFrame(cells):
    x=0
    y=0
    w=0
    h=0
    margin = -30
    noOfCells = len (cells)
    if (noOfCells == 9):
        x=cells[0].x - margin
        y=cells[0].y - margin
        w=cells[2].x + cells[2].w + margin
        h = cells[6].y + cells[6].h + margin

        #ensure that the values stay within the boundaries of x and y resolutions
        x = capToBoundaries(x,0,xRes)
        y = capToBoundaries(y,0,yRes)
        w = capToBoundaries(w,0,xRes)
        h = capToBoundaries(h,0,yRes)
    return x,y,w,h

def cropImageToBorder(img):
    x,y,w,h = getTTTFrameFromImg(img)
    if (x >= 0 and y >= 0 and w > 0 and h > 0):
        crop_img = img[y:y+h, x:x+w]
        return crop_img
    return img
    
# get all the cells
# sort them
# compute the perimeter
# crop the image
def cropAndCenter(img):
    imgForCrop = img.copy()
    croppedImage = cropImageToBorder(imgForCrop)
    cells = getSortedCellBorders(croppedImage)
    return croppedImage, cells

def detectPlayerChips(img, cells):
    global playerImgForShow
    hsv = getHSVImage(img)
    hsvInvert = ~hsv

    lower1 =  redHSVRanges[0][0]
    upper1 =  redHSVRanges[0][1]
    lower2 =  redHSVRanges[1][0]
    upper2 =  redHSVRanges[1][1]

    lower1 = np.array(lower1, dtype = "uint8")
    upper1 = np.array(upper1, dtype = "uint8")
    lower2 = np.array(lower2, dtype = "uint8")
    upper2 = np.array(upper2, dtype = "uint8")    

    # find the colors within the specified boundaries and apply
    # the mask
    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)
    output = cv2.bitwise_and(hsv,hsv,mask=mask1|mask2)
    playerImgForShow = output.copy()
    # cv2.imshow("player", output)
    
    
    grayImg = getGrayAndBlurredImage(output)
    ret, thresh = cv2.threshold(grayImg, 127, 255, cv2.THRESH_BINARY)
    img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    playerCells = getChipBorders(contours)
    return playerCells

def isCellInTile(cell, tileCells):  # returns None if rectangles don't intersect
    if (cell is not None and tileCells is not None):

        cellarea = cell.w*cell.h
        rc = Rectangle(cell.x,cell.y,cell.x+cell.w,cell.y+cell.h)

        for t in tileCells:
            rt = Rectangle (t.x, t.y, t.x+t.w, t.y+t.h)

            dx = min(rc.xmax, rt.xmax) - max(rc.xmin, rt.xmin)
            dy = min(rc.ymax, rt.ymax) - max(rc.ymin, rt.ymin)
            if (dx>=0) and (dy>=0):
                overlaparea = dx*dy
                if (cellarea == overlaparea):
                    return t.index
    return -1

def getTicTacToeGrid(playerCells, tileCells):
    grid = []
    lenPC = len(playerCells)
    for i in range(0,lenPC):
        pc = playerCells[i]
        val = isCellInTile(pc,tileCells)
        if ( val != -1):
            c = ticTacToeCell()
            c.index=val+1
            c.cellOccupied=c.OCCUPIED
            c.cellOwner=c.PLAYER
            grid.append(c)
    grid =  sorted(grid, key=attrgetter('index'),reverse=False)

    return grid

def getSum(grid):
    s=0
    for i in grid:
        if (i is not None):
            s=s+i.index
    return s

def identifyGridChanges(oldGrid, newGrid):
    gridChanged = False
    gridChangesAreValid = False
    gridChanges = []

    #check if the newGrid has any changes
    #compare the new grid with the old grid
    #for everycell, catalog the equality
    # return the differences

    if (oldGrid is None and newGrid is None):
        gridChanged=False
        gridChangesAreValid=False
        return gridChanged, gridChangesAreValid, gridChanges
    
    if (oldGrid is None and newGrid is not None):
        gridChanged=True
        gridChangesAreValid=False
        return gridChanged, gridChangesAreValid, gridChanges

    if (oldGrid is not None and newGrid is None):
        gridChanged=False
        gridChangesAreValid=False
        return gridChanged, gridChangesAreValid, gridChanges

    sumOld = getSum(oldGrid)
    sumNew = getSum(newGrid)
    delta = sumNew - sumOld
    if (delta == 0):
        gridChanged=False
        gridChangesAreValid=False
        gridChanges=None
        return gridChanged, gridChangesAreValid, gridChanges

    if (delta > 0 and delta <= 9):
        c = ticTacToeCell()
        c.index=delta
        c.cellOccupied=c.OCCUPIED
        c.cellOwner=c.PLAYER
        gridChanges.append(c)
        gridChanged=True
        gridChangesAreValid=True 
        return gridChanged, gridChangesAreValid, gridChanges               
    if (delta < 0 or delta >= 9):
        gridChanged=True
        gridChangesAreValid=False
        gridChanges=None    
    return gridChanged, gridChangesAreValid, gridChanges

def acceptOrRejectNewGrid (oldGrid, newGrid):
    validGrid = False
    #Look for user move
    gridChanged, gridChangesAreValid, gridChanges = identifyGridChanges(oldGrid, newGrid)
    if (gridChanged and gridChangesAreValid):
        print("A.",end="")
        validGrid = True
        
    elif (gridChanged and gridChangesAreValid is False):
        validGrid = False
        print ("R.",end="")
    else:
        validGrid = False
        print(".",end="")

    return validGrid, gridChanged, gridChanges

def makeValidMoveSound():
    Freq = 1000 # Set Frequency To 2500 Hertz
    Dur = 500 # Set Duration To 1000 ms == 1 second
    winsound.Beep(Freq,Dur)

def makeGameEndSound():
    for i in range(1,10):
        Freq = 1500 # Set Frequency To 2500 Hertz
        Dur = 250 # Set Duration To 1000 ms == 1 second
        winsound.Beep(Freq,Dur) 


def makeInValidMoveSound():
    for i in range(1,3):
        Freq = 500 # Set Frequency To 2500 Hertz
        Dur = 250 # Set Duration To 1000 ms == 1 second
        winsound.Beep(Freq,Dur)    

def sendPlayerMoveToGame(move):
    return gm.userMove(move)

def makeRobotMove(move):
    global ser
    ret = 1
    print("Computer move ",move)
    
    if (ser is None):
        return ret

    if (not ser.isOpen()):
        ser.open()

    if (move <= 9 and move > 0 ):
        tu1 = (move,"\n")
        printText = "{0:d}{1:s}".format(*tu1)
        a = bytes(printText,encoding="UTF-8")
        ser.write(a)
        time.sleep(5)
    return ret

def gameStart():
    global ticTacToeGrid
    global gameInProgress
    global playerMove
    global origImgForShow
    global croppedImgForShow
    global borderImgForShow
    global tilesImgForShow
    global playerImgForShow

    while (gameInProgress is True):
        image = getCameraImage()
        image = cv2.medianBlur(image,5)    # 5 is a fairly small kernel size

        croppedImage, cells = cropAndCenter(image)
        markBorders(croppedImage, cells)  
        playerCells = detectPlayerChips(croppedImage,cells) 
        markBorders(croppedImage,playerCells) 
        latestGrid = getTicTacToeGrid(playerCells,cells)
        validGrid, gridChanged, gridChanges = acceptOrRejectNewGrid(ticTacToeGrid, latestGrid)
        if (validGrid is True and gridChanged is True):
            ticTacToeGrid = getTicTacToeGridCopy(latestGrid)
            playerMove = gridChanges[0].index
            print(playerMove)
            makeValidMoveSound()
            computerMove, gameStatus = sendPlayerMoveToGame(playerMove-1)
            if (computerMove != -1):
                makeRobotMove(computerMove+1)
                if (gameStatus):
                    makeGameEndSound()
                    gameInProgress=False
                    break
        if (validGrid is False and gridChanged is True):
            makeInValidMoveSound()
        
        # show the images
        # cv2.imshow("images", np.hstack([image, croppedImage]))
        # cv2.imshow("origimg", image)
        angle = 100
        origImgForShow = rotateImage(cv2.resize(image,(200,200)),angle)
        borderImgForShow = rotateImage(cv2.resize(borderImgForShow,(200,200)),angle)
        tilesImgForShow = rotateImage(cv2.resize(tilesImgForShow,(200,200)),angle)
        playerImgForShow = rotateImage(cv2.resize(playerImgForShow,(200,200)),angle)
        croppedImgForShow = rotateImage(cv2.resize(croppedImage,(200,200)),angle)
        cv2.imshow("cropped image", rotateImage(croppedImage,angle))
        cv2.imshow("images", 
            np.hstack(
                        [
                            origImgForShow
                            ,borderImgForShow
                            ,tilesImgForShow
                            ,playerImgForShow
                            ,croppedImgForShow
                        ]
                    )
                )


        # newx,newy = croppedImage.shape[1]*1.5,croppedImage.shape[0]*1.5 #new size (w,h)
        # newx = int(newx)
        # newy = int(newy)
        # newimage = cv2.resize(croppedImage,(newx,newy))
        # rotatedImage = rotateImage(newimage,95)
        # cv2.imshow("cropped",rotatedImage)

        key = cv2.waitKey(2000) & 0xFF
        if key == 27:
            break


def listsComPorts():
    ports = serial.tools.list_ports.comports()
    connected = []
    for element in ports:
        connected.append(element.device)
    print("Connected COM ports: " + str(connected))

def initializeSerialport():
    global ser
    try:
        ser = serial.Serial(
        port='COM4',
        baudrate=9600
        # parity=serial.PARITY_NONE,
        # stopbits=serial.STOPBITS_ONE,
        # bytesize=serial.EIGHTBITS
        )
    except:
        print("Port cannot be opened. Connect to the board and try again..")
        return

    if (ser is not None):       
        if (not ser.isOpen()):
            ser.open()

def closeSerialPort():
    global ser
    ser.close()

def main():
    global ticTacToeGrid
    global gameInProgress
    global waitingForUserMove
    global startGame
    global gameDifficultyLevel
    gameDifficultyLevel = "H" #H for hard. This is the default
    for arg in sys.argv[1:]:
        print(arg)
        gameDifficultyLevel = "E"
        break
    gm.initTicTacToeGame(gameDifficultyLevel)

    initializeSerialport()

    while True:
        gameStart()
        key = cv2.waitKey(2000) & 0xFF
        if key == 27:
            break
    # clean up
    cv2.destroyAllWindows()
    closeSerialPort()

if __name__ == '__main__':
    main()
