from player import RLTTTPlayer, TTTPlayer, RealTTTPlayer
from board import TTTBoardDecision, BoxState, TTTBoard
from learning import NNLearning, TableLearning
from random import randint
learningModel = TableLearning(TTTBoardDecision)
learningModel.loadLearning("FinalTableModel.json")
player1 = RLTTTPlayer(learningModel)
player2 = RealTTTPlayer()
board = TTTBoard()
BoardDecisionClass = TTTBoardDecision()

player1.startNewGame()
player2.startNewGame()
playOrder = randint(0,1)
while board.getBoardDecision() == BoardDecisionClass.ACTIVE:
    player1.setBoard(board, BoxState.PLAYER_X)
    player2.setBoard(board, BoxState.PLAYER_O)
    if playOrder == 0 and board.getBoardDecision() == BoardDecisionClass.ACTIVE:
        pState1 = player1.makeNextMove()
    board.printBoard()
    if board.getBoardDecision() == BoardDecisionClass.ACTIVE:
        inpplay = input("Select position (1-9): ") 
        pState2 = player2.makeNextMove(BoxState.PLAYER_O, int(inpplay)-1)
    if playOrder == 1 and board.getBoardDecision() == BoardDecisionClass.ACTIVE:
        pState1 = player1.makeNextMove()
player1.finishGame()
player2.finishGame()
board.printBoard()
if board.getBoardDecision() == TTTBoardDecision.DRAW:
    print('This TTT game is a draw!')
elif board.getBoardDecision() != TTTBoardDecision.ACTIVE:
    print('This TTT game was won by %s'%(BoxState.PLAYER_X if board.getBoardDecision() == TTTBoardDecision.WON_X else BoxState.PLAYER_O))