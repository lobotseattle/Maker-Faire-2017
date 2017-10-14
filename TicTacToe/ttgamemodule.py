# pylint: disable=missing-docstring, C0103, E1101, C0325, C0326, W0612, C0301, R0903, W0603, R0914, C0303, W0613, E1126,C0330, W0311, C0326, W0621
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Tic Tac Toe Game
# version:      4
# Description:  imlemented board copy, to simulate moves for computer
#
# Author:      s-TSRIKANTH
#
# Created:     16/04/2017
# Copyright:   (c) s-TSRIKANTH 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import random
# import tkinter
#This is used to specify button dimensions

squarelength=5

#create a class to hold the state of the cell
class cellState:
    cellNumber=-1
    occupied=False
    player="Nobody"
    def __init__(self, cellNumber, occupied, player):
      self.cellNumber = cellNumber
      self.occupied = occupied
      self.player = player

    def printState(self):
        print("Cell number is..", self.cellNumber, " ", self.occupied," ", self.player,"\t")

    def returnCopy(self):
        cellCopy=cellState(self.cellNumber,self.occupied,self.player)
        return cellCopy

    def takenByUser(self):
        self.occupied=True
        self.player="User"

    def takenByComputer(self):
        self.occupied=True
        self.player="Computer"

#Return a copy of the board
def getBoardCopy(ticTacToeBoard):
    ticTacToeBoardCopy=[]
    for t in ticTacToeBoard:
        cell=t.returnCopy()
        ticTacToeBoardCopy.append(cell)
    return ticTacToeBoardCopy

#Change the button's color
def changeButtonColor(b,color):
    b.configure(bg=color)

#Callbaack method to be called when cell 1 is taken by the user
def callback1():
    global ticTacToeBoard
    global gameLevel
    ticTacToeBoard[0].takenByUser()
    winStat = didUserWin(ticTacToeBoard)
    if not winStat:
        computerPlayAI(ticTacToeBoard, gameLevel)
    else:
        declareWinner(ticTacToeBoard,"User")

#Callbaack method to be called when cell 2 is taken by the user
def callback2():
    global ticTacToeBoard
    ticTacToeBoard[1].takenByUser()
    if not didUserWin(ticTacToeBoard):
        computerPlayAI(ticTacToeBoard, gameLevel)
    else:
        declareWinner(ticTacToeBoard,"User")

#Callbaack method to be called when cell 3 is taken by the user
def callback3():
    global ticTacToeBoard
    ticTacToeBoard[2].takenByUser()
    if not didUserWin(ticTacToeBoard):
        computerPlayAI(ticTacToeBoard, gameLevel)
    else:
        declareWinner(ticTacToeBoard,"User")

#Callbaack method to be called when cell 4 is taken by the user
def callback4():
    global ticTacToeBoard
    ticTacToeBoard[3].takenByUser()
    if not didUserWin(ticTacToeBoard):
        computerPlayAI(ticTacToeBoard, gameLevel)
    else:
        declareWinner(ticTacToeBoard,"User")

#Callbaack method to be called when cell 5 is taken by the user
def callback5():
    global ticTacToeBoard
    ticTacToeBoard[4].takenByUser()
    if not didUserWin(ticTacToeBoard):
        computerPlayAI(ticTacToeBoard, gameLevel)
    else:
        declareWinner(ticTacToeBoard,"User")


#Callbaack method to be called when cell 6 is taken by the user
def callback6():
    global ticTacToeBoard
    ticTacToeBoard[5].takenByUser()
    if not didUserWin(ticTacToeBoard):
        computerPlayAI(ticTacToeBoard, gameLevel)
    else:
        declareWinner(ticTacToeBoard,"User")

#Callbaack method to be called when cell 7 is taken by the user
def callback7():
    global ticTacToeBoard
    ticTacToeBoard[6].takenByUser()
    if not didUserWin(ticTacToeBoard):
        computerPlayAI(ticTacToeBoard, gameLevel)
    else:
        declareWinner(ticTacToeBoard,"User")

#Callbaack method to be called when cell 8 is taken by the user
def callback8():
    global ticTacToeBoard
    ticTacToeBoard[7].takenByUser()
    if not didUserWin(ticTacToeBoard):
        computerPlayAI(ticTacToeBoard, gameLevel)
    else:
        declareWinner(ticTacToeBoard,"User")

#Callbaack method to be called when cell 9 is taken by the user
def callback9():
    global ticTacToeBoard
    ticTacToeBoard[8].takenByUser()
    if not didUserWin(ticTacToeBoard):
        computerPlayAI(ticTacToeBoard, gameLevel)
    else:
        declareWinner(ticTacToeBoard,"User")


#returns True is the board is full
def isBoardFull(ticTacToeBoard):
    for t in ticTacToeBoard:
        if not t.occupied:
            return False
    return True

#Get an unoccupied cell by checking the cells in a random order
def getUnoccupiedCell(ticTacToeBoard):
    if not isBoardFull(ticTacToeBoard):
        while (True):
            randomNum=random.randint(0,8)
            occupiedStatus = ticTacToeBoard[randomNum].occupied
            if not occupiedStatus:
                return randomNum
    else:
        return -1

#Get the list of unoccupied cells on the board
def getUnoccupiedCells(ticTacToeBoard):
    emptyCells=[]
    if not isBoardFull(ticTacToeBoard):
        for t in ticTacToeBoard:
            if not t.occupied:
                emptyCells.append(t)
    return emptyCells

#Pick the next move for the computer and mark it on the board
def computerPlay(ticTacToeBoard):
    cell = getUnoccupiedCell(ticTacToeBoard)
    if cell > -1:
        cell = ticTacToeBoard[cell]
        cell.takenByComputer()
        if didComputerWin(ticTacToeBoard):
            declareWinner(ticTacToeBoard,"Computer")
    else:
        declareWinner(ticTacToeBoard,"Both user and computer")
    return cell

#Make a winning move for the computer (if possible)
def makeAWinningMoveIfPossible(ticTacToeBoard):
    winningMove=isThereAWinningMove(ticTacToeBoard)

    ## There us a winning move. Computer should claim it.
    if winningMove != -1:
        cell = ticTacToeBoard[winningMove]
        cell.takenByComputer()
    return winningMove

#Make a move for the computer that can block the user from winning (if possible)
def makeBlockingMoveIfPossible(ticTacToeBoard):
    blockingMove=isThereABlockingMove(ticTacToeBoard)

    ## There us a winning move. Computer should claim it.
    if blockingMove != -1:
        cell = ticTacToeBoard[blockingMove]
        cell.takenByComputer()
    return blockingMove

#Make a corner move for the computer (if any corner is unoccupied)
def makeCornerMoveIfPossible(ticTacToeBoard):
    cornerMove=getACornerMove(ticTacToeBoard)
    if cornerMove != -1:
        cell = ticTacToeBoard[cornerMove]
        cell.takenByComputer()
    return cornerMove

#Make a center move for the computer (if the center is unoccupied)
def makeCenterMoveIfPossible(ticTacToeBoard):
    centerMove=isThereACenterMove(ticTacToeBoard)
    if centerMove != -1:
        cell = ticTacToeBoard[centerMove]
        cell.takenByComputer()
    return centerMove

#Play the computer move using some artificial intelligence
def computerPlayAI(ticTacToeBoard, gameLevel):
    move = makeAWinningMoveIfPossible(ticTacToeBoard)

    if(move == -1):
    ## There is no winning move. Check for a blocking move.
        if(gameLevel.lower() != "e"):
            move=makeBlockingMoveIfPossible(ticTacToeBoard)
        if move == -1:
            move = makeCenterMoveIfPossible(ticTacToeBoard)
            if (move == -1):
                move = makeCornerMoveIfPossible(ticTacToeBoard)
                if (move ==1 ):
                    move = computerPlay(ticTacToeBoard)

    winStat = didComputerWin(ticTacToeBoard)
    if winStat:
         declareWinner(ticTacToeBoard,"Computer")
    
    return move, winStat

#Check if the list of cells is occupied by the player
def columnCheck(columnList, player):
    cell1 = columnList[0]
    cell2 = columnList[1]
    cell3 = columnList[2]
    return (cell1.occupied and cell2.occupied and cell3.occupied and cell1.player==player and cell2.player==player and cell3.player==player)

#Print the tic tac toe grid
def printGrid(ticTacToeBoard):
    print ("\n")
    for t in ticTacToeBoard:
        t.printState()
    return

#check for this conditions
#at least one of these conditions is True
#leftRow is fully occupied by user
#MiddleRow
#TopRow
#leftColumn
#RightColumn
#MiddleColumn
#Diagonal1
#Diagonal2
#Make 8 checks 1 at a time

#Returns a flag that indicates if the either the user or the computer won
def didEitherUserOrComputerWin(ticTacToeBoard,player):
    leftColCheck=columnCheck(leftColumn(ticTacToeBoard),player)
    rightColCheck=columnCheck(rightColumn(ticTacToeBoard),player)
    middleColCheck=columnCheck(middleColumn(ticTacToeBoard),player)
    topRowCheck=columnCheck(topRow(ticTacToeBoard),player)
    middleRowCheck=columnCheck(middleRow(ticTacToeBoard),player)
    bottomRowCheck=columnCheck(bottomRow(ticTacToeBoard),player)
    diagonal1Check=columnCheck(diagonal1(ticTacToeBoard),player)
    diagonal2Check=columnCheck(diagonal2(ticTacToeBoard),player)
    return(leftColCheck or rightColCheck or middleColCheck or topRowCheck or middleRowCheck or bottomRowCheck or diagonal1Check or diagonal2Check)

#Returns a flag that indicates if the user won
def didUserWin(ticTacToeBoard):
    return didEitherUserOrComputerWin(ticTacToeBoard,"User")

#Returns a flag that indicates if the computer won
def didComputerWin(ticTacToeBoard):
    return didEitherUserOrComputerWin(ticTacToeBoard,"Computer")

#Declare the winner (the player - User or c\Computer)
def declareWinner(ticTacToeBoard,player):
    print(player," wins!!!!!!!!!!!")

#Return the list of cells on the left column
def leftColumn(ticTacToeBoard):
    leftColumn=[ticTacToeBoard[0],ticTacToeBoard[3],ticTacToeBoard[6]]
    return leftColumn

#Return the list of cells on the middle column
def middleColumn(ticTacToeBoard):
    rightColumn=[ticTacToeBoard[1],ticTacToeBoard[4],ticTacToeBoard[7]]
    return rightColumn

#Return the list of cells on the right column
def rightColumn(ticTacToeBoard):
    middleColumn=[ticTacToeBoard[2],ticTacToeBoard[5],ticTacToeBoard[8]]
    return middleColumn

#Return the list of cells on the bottom row
def bottomRow(ticTacToeBoard):
    bottomRow=[ticTacToeBoard[6],ticTacToeBoard[7],ticTacToeBoard[8]]
    return bottomRow

#Return the list of cells on the top row
def topRow(ticTacToeBoard):
    topRow=[ticTacToeBoard[0],ticTacToeBoard[1],ticTacToeBoard[2]]
    return topRow

#Return the list of cells on the middle row
def middleRow(ticTacToeBoard):
    middleRow=[ticTacToeBoard[3],ticTacToeBoard[4],ticTacToeBoard[5]]
    return middleRow

#Return the list of cells on diagonal 1
def diagonal1(ticTacToeBoard):
    diagonal1=[ticTacToeBoard[0],ticTacToeBoard[4],ticTacToeBoard[8]]
    return diagonal1

#Return the list of cells on diagonal 2
def diagonal2(ticTacToeBoard):
    diagonal2=[ticTacToeBoard[2],ticTacToeBoard[4],ticTacToeBoard[6]]
    return diagonal2

#Return the list of cells on the corners
def corners(ticTacToeBoard):
    corners=[ticTacToeBoard[0], ticTacToeBoard[2],ticTacToeBoard[6],ticTacToeBoard[8]]
    return corners

#Return the list of cells on sides
def sides(ticTacToeBoard):
    sides=[ticTacToeBoard[1],ticTacToeBoard[3],ticTacToeBoard[5],ticTacToeBoard[7]]
    return sides

#Return the center cell
def center(ticTacToeBoard):
    center=ticTacToeBoard[4]
    return center

#Check if there exists a move for the computer so it can win
def isThereAWinningMove(ticTacToeBoard):
    returncell=-1
    unoccupiedCells=getUnoccupiedCells(ticTacToeBoard)
    for t in unoccupiedCells:
        ## get a fresh copy of the board for evert simulation
        ticTacToeBoardCopy=getBoardCopy(ticTacToeBoard)

        ## get the unoccupied cell
        unoccupiedCellNumber = t.cellNumber

        ##allow the computer to claim this unoccuoied cell
        winningCell=ticTacToeBoardCopy[unoccupiedCellNumber]
        winningCell.takenByComputer()

        ## now check if this claim by the computer, results in a win
        if  didComputerWin(ticTacToeBoardCopy):
##            print("Computer thinks it can win by taking cell ", unoccupiedCellNumber)
##            printGrid(ticTacToeBoardCopy)
            returncell=unoccupiedCellNumber

            break

    return returncell

#Check if there exists a move for the computer that can block the user form winning
def isThereABlockingMove(ticTacToeBoard):
    returncell=-1
    unoccupiedCells=getUnoccupiedCells(ticTacToeBoard)
    for t in unoccupiedCells:
        ## get a fresh copy of the board for evert simulation
        ticTacToeBoardCopy=getBoardCopy(ticTacToeBoard)

        ## get the unoccupied cell
        unoccupiedCellNumber = t.cellNumber

        ##allow the coBlocking mputer to claim this unoccuoied cell
        winningCell=ticTacToeBoardCopy[unoccupiedCellNumber]
        winningCell.takenByUser()

        ## now check if this claim by the computer, results in a win
        if  didUserWin(ticTacToeBoardCopy):
##            print("Computer thinks it can block by taking cell ", unoccupiedCellNumber)
            returncell=unoccupiedCellNumber
            break

    return returncell

#Get a corner move if possible (by checking if there exists an occupied corner
def getACornerMove(ticTacToeBoard):
    returnCell=-1
    cornerCells=corners(ticTacToeBoard)
    unoccupiedCorners = []
    for cell in cornerCells:
        if(not cell.occupied):
            unoccupiedCorners.append(cell)

    availableCorners = len(unoccupiedCorners)

    if (availableCorners > 0):
        randomCorner = random.randint(0,availableCorners-1)
        randomCornerCell = unoccupiedCorners[randomCorner]
##        print("Computer made a corner move ", randomCornerCell.cellNumber)
        returnCell = randomCornerCell.cellNumber

    return returnCell

#Check if the the center move is possible (by checking if the center cell is unoccupied)
def isThereACenterMove(ticTacToeBoard):
    returnCell=-1
    centerCell=center(ticTacToeBoard)
    if (not centerCell.occupied):
##        print("Computer thinks it can block by center move ",centerCell.cellNumber)
        returnCell = centerCell.cellNumber

    return returnCell

#Main program strats here
ticTacToeBoard = []
gameLevel = "H"
TIE=0
CWIN=1
UWIN=2

#Initialize the tic tac toe game board and mark the desired difficulty level
def initTicTacToeGame(gameDifficultyLevel):
    global ticTacToeBoard
    global gameLevel
    gameLevel = gameDifficultyLevel
    for i in range(0,9):
        cell = cellState(i,False,"Nobody")
        ticTacToeBoard.append((cell))

#Mark the user move on the board and check the win status
def userMove(move):
    global ticTacToeBoard
    global gameLevel
    global CWIN
    global UWIN
    global TIE
    computerMove = -1
    result = TIE

    if (move >=0 and move <= 8):
        ticTacToeBoard[move].takenByUser()
        winStat = didUserWin(ticTacToeBoard)
        if not winStat:
            computerMove, winStat = computerPlayAI(ticTacToeBoard, gameLevel)
            if (winStat):
                result=CWIN
        else:
            declareWinner(ticTacToeBoard,"User")
            result=UWIN

    return computerMove, winStat, result
