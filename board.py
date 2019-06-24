class BoxState():
    EMPTY = ' '
    PLAYER_X = 'X'
    PLAYER_O = 'O'

class TTTBoardDecision():
    ACTIVE = 0
    DRAW = 1
    WON_X = 2
    WON_O = 3

class TTTBoard():
    def __init__(self):
        self.board = self.emptyState()
        self.decision = TTTBoardDecision.ACTIVE

    def emptyState(self):
        return [BoxState.EMPTY]*9

    def determineBoardState(self):
        winlines = [[self.board[0], self.board[1], self.board[2]],
        [self.board[3], self.board[4], self.board[5]],
        [self.board[6], self.board[7], self.board[8]],
        [self.board[0], self.board[3], self.board[6]],
        [self.board[1], self.board[4], self.board[7]],
        [self.board[2], self.board[5], self.board[8]],
        [self.board[0], self.board[4], self.board[8]],
        [self.board[2], self.board[4], self.board[6]]]

        if BoxState.EMPTY not in self.board:
            self.decision = TTTBoardDecision.DRAW
        else:
            self.decision = TTTBoardDecision.ACTIVE

        for line in winlines:
            if len(set(line)) == 1 and BoxState.EMPTY not in line:
                if BoxState.PLAYER_O in line:
                    self.decision = TTTBoardDecision.WON_O
                else:
                    self.decision = TTTBoardDecision.WON_X
                    
    def setMoves(self, boardList):
        self.board = boardList
        self.determineBoardState()

    def makeMove(self, who, i, verbose=False):
        if self.board[i] != BoxState.EMPTY:
            print('That location is not empty')
            return
        self.board[i] = who
        self.determineBoardState()
        if self.decision == TTTBoardDecision.DRAW and verbose is True:
            print('This TTT game was drawn!')
        elif self.decision != TTTBoardDecision.ACTIVE and verbose is True:
            print('This TTT game was won by %s'%(BoxState.PLAYER_X if self.decision == TTTBoardDecision.WON_X else BoxState.PLAYER_O))

    def printBoard(self):
        delimiter = "-------------"
        BOARD_FORMAT = "%s\n%s\n%s\n"%(delimiter, self.getBoardString(), delimiter)
        cells = []
        for i in range(9):
            cells.append(self.board[i])
        print(BOARD_FORMAT.format(*cells))

    def getBoardString(self):
        return "| {0} | {1} | {2} | \n| {3} | {4} | {5} | \n| {6} | {7} | {8} |".format(*self.board[0:9])

    def getGrid(self, i):
        return self.board[i]

    def getEmptyBoardPlaces(self):
        return [i for i,x in enumerate(self.board) if x==BoxState.EMPTY]

    def getBoardState(self):
        return ''.join(self.board)

    def getDoesBoardHaveEmptyCell(self):
        for i in range(9):
            if self.board[i] == BoxState.EMPTY:
                return True
        return False

    def getBoardDecision(self):
        return self.decision

if __name__ == '__main__':
    b = TTTBoard()
    b.makeMove(BoxState.PLAYER_X, 0)
    b.makeMove(BoxState.PLAYER_O, 8)
    b.makeMove(BoxState.PLAYER_X, 1)
    b.makeMove(BoxState.PLAYER_O, 7)
    b.makeMove(BoxState.PLAYER_X, 2)
    print(b.getBoardState())
    print(b.getEmptyBoardPlaces())
    """b.makeMove(BoxState.PLAYER_O, 6)
    b.makeMove(BoxState.PLAYER_X, 5)
    b.makeMove(BoxState.PLAYER_O, 3)
    b.makeMove(BoxState.PLAYER_X, 4)"""
