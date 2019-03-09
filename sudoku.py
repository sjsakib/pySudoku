import random

N = 2


class Cell:
    def __init__(self, pos):
        self.possibleAnswers = list(range(1, N*N+1))
        self.ans = None
        self.pos = pos
        self.i = pos[0]*N*N + pos[1]
        # self.solved = False

    def __str__(self):
        return f'{self.ans} {self.possibleAnswers}'

    def show(self):
        return self.ans or f'({self.possibleLen()})'

    def solved(self):
        return self.ans != None

    def remove(self, num):
        if num not in self.possibleAnswers:
            return
        self.possibleAnswers.remove(num)

    def setAns(self, num):
        if num > N*N:
            raise(ValueError)
        self.possibleAnswers = [num]

    def setRandomAns(self):
        x = random.choice(self.possibleAnswers)
        # print(x, self.possibleAnswers)
        self.ans = x
        return x

    def reset(self):
        self.possibleAnswers = list(range(1, pow(N, 4)+1))

    def possibleLen(self):
        return len(self.possibleAnswers)


def emptyBoard():
    return [Cell((i, j, (i//N)*N+j//N)) for i in range(N*N) for j in range(N*N)]


def printBoard(b):
    for i in range(N):
        for k in range(N):
            for j in range(N):
                start = ((i*N)+k)*N*N + j*N
                print([c.show() for c in b[start:start+N]], end=' ')
            print('')
        print('')


def genCompleted():
    # unfinished cells
    cells = list(range(pow(N, 4)))
    board = emptyBoard()
    while len(cells):
        mn = min(board[i].possibleLen() for i in cells)
        lowestCells = []
        for i in cells:
            if board[i].possibleLen() == mn:
                lowestCells.append(board[i])
        choiceCell = random.choice(lowestCells)
        cells.remove(choiceCell.i)
        if not choiceCell.solved():
            x = choiceCell.setRandomAns()
        else:
            continue
        p1 = choiceCell.pos
        for c in board:
            if c is choiceCell:
                continue
            p2 = c.pos
            if p1[0] == p2[0] or p1[1] == p2[1] or p1[2] == p2[2]:
                c.remove(x)
    return board


def check(board):
    for c1 in board:
        for c2 in board:
            if c1 is c2:
                continue
            p1 = c1.pos
            p2 = c2.pos
            if (p1[0] == p2[0] or p1[1] == p2[1] or p1[2] == p2[2]) and c1.ans == c2.ans:
                return False
    return True

def checkEqual(b1, b2):
    for c in b1:
        if c.ans != b2[c.i].ans:
            return False
    return True



try:
    printBoard(genCompleted())
except:
    pass
