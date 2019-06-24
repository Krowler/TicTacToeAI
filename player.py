from board import TTTBoardDecision, TTTBoard
from learning import TableLearning
import random

class TTTPlayer(object):
    def __init__(self):
        self.board = None
        self.player = None

    def setBoard(self, board, player):
        self.board = board
        self.player = player

    def isBoardActive(self):
        return (self.board is not None and self.board.getBoardDecision() == TTTBoardDecision.ACTIVE)

    def makeNextMove(self):
        raise NotImplementedError

    def learnFromMove(self, prevBoardState):
        raise NotImplementedError

    def startNewGame(self):
        pass

    def finishGame(self):
        pass

class RandomTTTPlayer(TTTPlayer):
    def makeNextMove(self):
        previousState = self.board.getBoardState()
        if self.isBoardActive():
            emptyPlaces = self.board.getEmptyBoardPlaces()
            pickOne = random.choice(emptyPlaces)
            self.board.makeMove(self.player, pickOne)
        return previousState

    def learnFromMove(self, prevBoardState):
        pass

    def isBoardActive(self):
        return (self.board is not None and self.board.getBoardDecision() == TTTBoardDecision.ACTIVE)

class RLTTTPlayer(TTTPlayer):
    def __init__(self, algo):
        self.learningAlgo = algo
        super(RLTTTPlayer, self).__init__()

    def printValues(self):
        self.learningAlgo.printValues()

    def testNextMove(self, state, i):
        boardCopy = list(state)
        boardCopy[i] = self.player
        return ''.join(boardCopy)

    def makeNextMove(self):
        previousState = self.board.getBoardState()
        if self.isBoardActive():
            emptyPlaces = self.board.getEmptyBoardPlaces()
            pickOne = random.choice(emptyPlaces)
            if random.uniform(0, 1) < 0.8:
                moveChoices = {}
                for i in emptyPlaces:
                    possibleNextState = self.testNextMove(previousState, i)
                    moveChoices[i] = self.learningAlgo.getBoardStateValue(self.player, self.board, possibleNextState)
                pickOne = max(moveChoices, key=moveChoices.get)
            self.board.makeMove(self.player, pickOne)
        return previousState

    def learnFromMove(self, prevBoardState):
        self.learningAlgo.learnFromMove(self.player, self.board, prevBoardState)

    def isBoardActive(self):
        return (self.board is not None and self.board.getBoardDecision() == TTTBoardDecision.ACTIVE)

class RealTTTPlayer(TTTPlayer):
    def makeNextMove(self, player, position):
        self.board.makeMove(player, position)
        return self.board.getBoardState()

    def isBoardActive(self):
        return (self.board is not None and self.board.getBoardDecision() == TTTBoardDecision.ACTIVE)
if __name__  == '__main__':
    board = TTTBoard()
    player1 = RLTTTPlayer()
    player2 = RandomTTTPlayer()
