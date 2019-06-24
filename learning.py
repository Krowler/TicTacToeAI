from board import BoxState, TTTBoardDecision
import json
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import plot_model
import numpy as np

class GenericLearning(object):
    def getBoardStateValue(self, player, board, boardState):
        raise NotImplementedError

    def learnFromMove(self, player, board, prevBoardState):
        raise NotImplementedError

    def saveModel(self, filename):
        raise NotImplementedError

    def loadModel(self, filename):
        raise NotImplementedError

    def resetForNewGame(self):
        pass

    def gameOver(self):
        pass

class TableLearning(GenericLearning):
    def __init__(self, DecisionClass=TTTBoardDecision):
        self.values = {}
        self.DecisionClass = DecisionClass

    def getBoardStateValue(self, player, board, boardState):
        decision = board.getBoardDecision()
        if decision == self.DecisionClass.WON_X:
            self.values[boardState] = 1.0 if player == BoxState.PLAYER_X else -1.0
        if decision == self.DecisionClass.WON_O:
            self.values[boardState] = 1.0 if player == BoxState.PLAYER_O else -1.0
        if decision == self.DecisionClass.DRAW or boardState not in self.values:
            self.values[boardState] = 0
        return self.values[boardState]

    def learnFromMove(self, player, board, prevBoardState):
        curBoardState = board.getBoardState()
        curBoardStateValue = self.getBoardStateValue(player, board, curBoardState)
        if prevBoardState not in self.values:
            self.getBoardStateValue(player, board, prevBoardState)
        self.values[prevBoardState] = self.values[prevBoardState] + 0.2*(curBoardStateValue - self.values[prevBoardState])

    def printValues(self):
        print(self.values)
        print('Total number of states: %s' % (len(self.values)))
        print('Total number of knowledgeable states: %s' % (len(filter(lambda x: x!=0.5, self.values.values()))))

    def saveLearning(self, filename):
        json.dump(self.values, open(filename,'w'))

    def loadLearning(self, filename):
        self.values = json.load(open(filename, 'r'))


class NNLearning(GenericLearning):
    STATE_TO_NUMBER_MAP = {BoxState.EMPTY: 0, BoxState.PLAYER_O: -1, BoxState.PLAYER_X: 1}

    def __init__(self, DecisionClass=TTTBoardDecision):
        self.DecisionClass = DecisionClass
        self.values = {}
        self.initializeModel()

    def initializeModel(self):
        self.model = Sequential()
        self.model.add(Dense(9, input_dim=1, activation='relu'))
        self.model.add(Dense(27, activation='relu'))
        self.model.add(Dense(27, activation='relu'))
        self.model.add(Dense(1, activation='linear', kernel_initializer='glorot_uniform'))
        self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

    def initialModelTraining(self, jsonFile):
        import os
        if os.path.isfile(jsonFile):
            self.values = json.load(open(jsonFile, 'r'))
            self.gameOver()

    def resetForNewGame(self):
        self.values = {}

    def gameOver(self):
        boardStates, predYs = [], []
        for (k,v) in self.values.iteritems():
            boardStates.append(self.convertBoardStateToInput(k))
            predYs.append(v)
        self.trainModel(boardStates, predYs)

    def convertBoardStateToInput(self, boardState):
        return map(lambda x: self.STATE_TO_NUMBER_MAP.get(x), boardState)

    def trainModel(self, boardStates, y):
        self.model.fit(list(boardStates), list(y), verbose=0)

    def getPrediction(self, boardState):
        return self.model.predict(list(self.convertBoardStateToInput(boardState)))[0]

    def getBoardStateValue(self, player, board, boardState):
        decision = board.getBoardDecision()
        predY = self.getPrediction(boardState)[0]
        if decision == self.DecisionClass.WON_X:
            predY = 1.0 if player == BoxState.PLAYER_X else 0.0
            self.values[boardState] = predY
        if decision == self.DecisionClass.WON_O:
            predY = 1.0 if player == BoxState.PLAYER_O else 0.0
            self.values[boardState] = predY
        if decision == self.DecisionClass.DRAW:
            predY = 0.5
            self.values[boardState] = predY
        return predY

    def learnFromMove(self, player, board, prevBoardState):
        curBoardState = board.getBoardState()
        curBoardStateValue = self.getBoardStateValue(player, board, curBoardState)
        prevBoardStateValue = self.getPrediction(prevBoardState)[0]
        self.values[prevBoardState] = prevBoardStateValue + 0.2 * (curBoardStateValue - prevBoardStateValue)

    def printValues(self):
        pass

    def saveLearning(self, filename):
        self.model.save(filename)

    def loadLearning(self, filename):
        self.model = load_model(filename)
