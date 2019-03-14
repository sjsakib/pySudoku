import random
import copy
import time

N = 2


class Cell:
    def __init__(self, pos):
        # A cell initially can have N*N possible answers
        self.possibleAnswers = list(range(1, N*N+1))
        # The answer is initially None
        self.ans = None
        # the position of ca cell is a tuple of three integer
        # first and second number represents row and column
        # the third number represents in which `box` the cell is in
        self.pos = pos
        # a cell also has an index, that is, the index of the cell if the board is a 1D array
        # it can be obtained from row and column
        self.i = pos[0]*N*N + pos[1]

    def __str__(self):
        return f'({self.ans} {self.possibleAnswers})'

    def show(self):
        # return self.ans or f'({self.possibleLen()})'
        return self.ans or 0

    def solved(self):
        return self.ans != None

    def remove(self, num):
        # if `num` in the list of possibleAnswers, remove it from there
        if num not in self.possibleAnswers:
            return False
        self.possibleAnswers.remove(num)
        # if after removing it, the possibleAnswers contain only one element, the cell is solved
        if len(self.possibleAnswers) == 1:
            self.ans = self.possibleAnswers[0]
            return True
        return False

    def setRandomAns(self):
        # select a random element from the possibleAnswers and set it as the answer
        x = random.choice(self.possibleAnswers)
        self.ans = x
        return x

    def reset(self):
        # rest the cell, set answer to None and possible answer to N*N number
        self.ans = None
        self.possibleAnswers = list(range(1, N*N+1))

    def possibleLen(self):
        # returns length of the possible answers array
        return len(self.possibleAnswers)

    def sameDomain(self, other):
        # checks if two cells is in the same domain, that is if they are in the same row, column or `box`
        p1 = self.pos
        p2 = other.pos
        return p1[0] == p2[0] or p1[1] == p2[1] or p1[2] == p2[2]


def emptyBoard():
    # returns and empty board of size N*N as an 1D array
    return [Cell((i, j, (i//N)*N+j//N)) for i in range(N*N) for j in range(N*N)]


def printBoard(b):
    # prints a board
    for i in range(N):
        for k in range(N):
            for j in range(N):
                start = ((i*N)+k)*N*N + j*N
                print([c.show() for c in b[start:start+N]], end=' ')
            print('')
        print('')


def check(board):
    # Checks if a board is completed and correct
    for c1 in board:
        if not c1.solved():
            # A cell is not solved. So, not complete
            return False
        for c2 in board:
            if c1 is c2:
                continue
            if c1.sameDomain(c2) and c1.ans == c2.ans:
                # Two cells in same domain but have same answer. So, not correct
                return False
    return True


def checkEqual(b1, b2):
    # checks if two boards are exactly same
    for c in b1:
        if c.ans != b2[c.i].ans:
            return False
    return True


def genCompleted():
    # generates and returns a completed board

    # first take an empty board
    board = emptyBoard()
    # make a `shallow` copy of all the cells, these cells are unfinished
    cells = board.copy()
    while cells:  # until the list of unifinshed cells is empty,
        # see which unfinished cells have the minimum number of possible answers
        # then select a random one from them, set a random answer to it from it's possible answers, let it be x
        # remove this cell from the list of unfinished cells
        # now go to every cell of the board, if a cell is in the same domain as the cell we just set a random
        # answer to, remove x from it's possible answer

        mn = min(c.possibleLen() for c in cells)
        lowestCells = []
        for c in cells:
            if c.possibleLen() == mn:
                lowestCells.append(c)
        choiceCell = random.choice(lowestCells)
        cells.remove(choiceCell)

        # if the cell is already solved, no need to set random answer
        if not choiceCell.solved():
            choiceCell.setRandomAns()
        x = choiceCell.ans
        for c in board:
            if c is choiceCell:
                continue
            if choiceCell.sameDomain(c):
                c.remove(x)

    # if the algorithm is finished, but we dont get a completed board, we have to try again
    if not check(board):
        return genCompleted()
    return board


def solve(board, t=0):
    # takes a board and number of previous attempts `t`
    # returns number of guesses (which we assume as difficulty) and the solved board

    # if the number of previous attempts is more than 900, we assume the board is unsolvable
    if t > 900:
        return (-1, None)

    # make a deep copy of the board, the copy has to be deep because we would want to try different solutions
    # without changing the original board first
    board_copy = copy.deepcopy(board)
    # number of guesses is zero at start
    guesses = 0

    # take the solved and unsolved cells in different lists
    solvedCells = []
    unsolvedCells = []
    for c in board_copy:
        if c.possibleLen() == 1:
            solvedCells.append(c)
        else:
            unsolvedCells.append(c)

    # for each solved cell, remove it's ans from the list of possibleAnswers of all the unsolved cells in it's domain
    while solvedCells:  # do this until the list of solved cells is empty
        # doing so, might solve some cells, keep them in this list
        newlySolved = []
        for c1 in solvedCells:
            for c2 in unsolvedCells:
                if c1.sameDomain(c2):
                    c2.remove(c1.ans)
                if c2.possibleLen() == 1:
                    # removing the number solved this cell, now set it's ans
                    # this will merely set the only element of it's possibleAnswers as it's ans
                    c2.setRandomAns()
                    # now that the cell is solved, remove it from unsolved cells
                    unsolvedCells.remove(c2)
                    # add it to the newly solved cells
                    newlySolved.append(c2)
        # the new list of solved cells would be the newlySolved cells
        solvedCells = newlySolved
        if solvedCells == [] and unsolvedCells != []:
            # we have done the above process for all the solved cells (the solvedCells list is empty)
            # but still some cells are unsolved
            # now we take the cells with minimum number of unsolved cells
            # select a random one and set a random answer to it

            mn = min(c.possibleLen() for c in unsolvedCells)
            choice = random.choice(
                list(filter(lambda c: c.possibleLen() == mn, unsolvedCells)))
            choice.setRandomAns()
            # add it to the solved cells and remove it from the unsolved cells
            solvedCells.append(choice)
            unsolvedCells.remove(choice)
            # now we have made a guess here, so increase a `guesses`
            guesses += 1
    if check(board_copy):
        # the board is solved, return guesses and the solved board
        return (guesses, board_copy)
    else:
        # the board is not solved, try again with number of previous attempt increased by one
        return solve(board, t+1)


def genPuzzle():
    # generates a puzzle and returns it's difficulty, the puzzle itself and it's solution as a tuple
    # generate a completed board first, then we will reset a random cell from a `deep copy` of the board
    # if the board still has a unique solution, we will reset the same cell in the original board and continue
    # doing this
    # otherwise, we return the original board in it's current state
    board = genCompleted()
    board_copy = copy.deepcopy(board)

    # list of all the solved cells
    cells = board_copy.copy()
    while cells:  # obviously, `cells` will never be empty, we will find a puzzle before that
        # choose a random cell and reset it
        choice = random.choice(cells)
        cells.remove(choice)
        choice.reset()
        # solve the board_copy to see if it still has a unique solution
        r0, s0 = solve(board_copy)
        if r0 == -1:
            # it doesn't have a solution, so we can't reset this or any other cell from the original board
            r, solution = solve(board)
            return r, board, solution
        elif checkEqual(s0, solve(board_copy)[1]):
            # the board_copy still has a unique solution, so reset the cell in the original board
            board[choice.i].reset()
        else:
            # it has a solution, but the solution is not unique, so we have to return
            r, solution = solve(board)
            return r, board, solution


def genPuzzleWithDifficulty(d):
    # generates a puzzle with a desired difficulty `d`.
    while True:  # keep generating puzzles until we find a puzzle with our desired difficulty
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
