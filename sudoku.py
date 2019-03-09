import random
import copy

N = 3


class Cell:
    def __init__(self, pos):
        self.possibleAnswers = list(range(1, N*N+1))
        self.ans = None
        self.pos = pos
        self.i = pos[0]*N*N + pos[1]

    def __str__(self):
        return f'({self.ans} {self.possibleAnswers})'

    def show(self):
        # return self.ans or f'({self.possibleLen()})'
        return self.ans or 0

    def solved(self):
        return self.ans != None

    def remove(self, num):
        if num not in self.possibleAnswers:
            return False
        self.possibleAnswers.remove(num)
        if len(self.possibleAnswers) == 1:
            self.ans = self.possibleAnswers[0]
            return True
        return False

    def setRandomAns(self):
        x = random.choice(self.possibleAnswers)
        self.ans = x
        return x

    def reset(self):
        self.ans = None
        self.possibleAnswers = list(range(1, N*N+1))

    def possibleLen(self):
        return len(self.possibleAnswers)

    def sameDomain(self, other):
        p1 = self.pos
        p2 = other.pos
        return p1[0] == p2[0] or p1[1] == p2[1] or p1[2] == p2[2]


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
    board = emptyBoard()
    cells = board.copy()
    while cells:

        mn = min(c.possibleLen() for c in cells)
        lowestCells = []
        for c in cells:
            if c.possibleLen() == mn:
                lowestCells.append(c)
        choiceCell = random.choice(lowestCells)
        cells.remove(choiceCell)
        if not choiceCell.solved():
            choiceCell.setRandomAns()
        x = choiceCell.ans
        for c in board:
            if c is choiceCell:
                continue
            if choiceCell.sameDomain(c):
                c.remove(x)
    if not check(board):
        return genCompleted()
    return board


def check(board):
    for c1 in board:
        if not c1.solved():
            return False
        for c2 in board:
            if c1 is c2:
                continue
            if c1.sameDomain(c2) and c1.ans == c2.ans:
                return False
    return True


def checkEqual(b1, b2):
    for c in b1:
        if c.ans != b2[c.i].ans:
            return False
    return True


def solve(board, t=0):
    if t > 900:
        return (-1, None)
    solvedCells = []
    unsolvedCells = []
    board_copy = copy.deepcopy(board)
    guesses = 0
    for c in board_copy:
        if c.possibleLen() == 1:
            solvedCells.append(c)
        else:
            unsolvedCells.append(c)
    # for each solved cells remove it's value from all the unsolved cells in it's domain
    removed = 0
    while len(solvedCells) != 0:
        newlySolved = []
        for c1 in solvedCells:
            for c2 in unsolvedCells:
                if c1.sameDomain(c2):
                    c2.remove(c1.ans)
                if c2.possibleLen() == 1:
                    removed += 1
                    c2.setRandomAns()
                    unsolvedCells.remove(c2)
                    newlySolved.append(c2)
        solvedCells = newlySolved
        if solvedCells == [] and unsolvedCells != []:
            mn = min(c.possibleLen() for c in unsolvedCells)
            choice = random.choice(
                list(filter(lambda c: c.possibleLen() == mn, unsolvedCells)))
            try:
                choice.setRandomAns()
            except Exception as e:
                solve(board, t+1)
            solvedCells.append(choice)
            unsolvedCells.remove(choice)
            guesses += 1
    if check(board_copy):
        return (guesses, board_copy)
    else:
        return solve(board, t+1)


def genPuzzle():
    board = genCompleted()
    board_copy = copy.deepcopy(board)
    cells = board_copy.copy()
    while cells:
        choice = random.choice(cells)
        cells.remove(choice)
        choice.reset()
        r0, s0 = solve(board_copy)
        if r0 == -1:
            r, solution = solve(board)
            return r, board, solution
        elif checkEqual(s0, solve(board_copy)[1]):
            board[choice.i].reset()
        else:
            r, solution = solve(board)
            return r, board, solution


def genPuzzleWithDifficulty(d):
    while True:
        r, puzzle, solution = genPuzzle()
        print('Found puzzle with difficulty: ', r+1)
        if r == d-1 or (d == 5 and r >= 5):
            return puzzle, solution

def main():
    global N
    N = int(input('Enter value of N (>1): '))
    d = int(input('Enter difficulty (1-5): '))

    puzzle, solution = genPuzzleWithDifficulty(d)
    print('Puzzle:')
    printBoard(puzzle)
    print('Solution:')
    printBoard(solution)

if __name__ == '__main__':
    main()
    # genCompleted()