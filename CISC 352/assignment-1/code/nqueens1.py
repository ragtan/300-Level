
import random
import time
import math
from datetime import timedelta


def solve(board_size):
    num_repairs = 0
    time_out = 0
    fails = 0

    answer = initial_board(board_size)
    conflicts_x, conflicts_o = build_confliction_table(answer, board_size)
    conflicts = get_conflicts(answer, board_size, conflicts_x, conflicts_o)
    randChoose = random.choice
    indices = [0] * board_size

    while conflicts[0] != -1:  # This checks to see if we found any conflicts in the last confliction check
        # Simple loading icon
        print(' ' * 100, end="\r")  # Remove any residue from the loading animation
        print(''.join(("Determining Queens placements for n=", str(board_size), " ", (
            "|" if time_out % 12 <= 3 else "/" if time_out % 12 <= 6 else "-" if time_out % 12 <= 9 else "\\"),
                       " Failed Attempts: ", str(fails), " Timeout: ", str(time_out))), end='\r')
        if time_out < board_size + (board_size * 0.1):
            mini = min(conflicts[1])  # The minimum conflicts we're looking for
            indices = [x for x in range(board_size) if conflicts[1][x] == mini]
            temp = randChoose(indices)  # Randomly select one of the lowest conflict zones to replace the conflict with

            # Remove conflict influence
            pos_sum = answer[temp] + temp
            conflicts_x[pos_sum] -= 1
            conflicts_o[(board_size + 1 - answer[temp]) + temp] -= 1

            pos_sum = answer[conflicts[0]] + conflicts[0]
            conflicts_x[pos_sum] -= 1
            conflicts_o[(board_size + 1 - answer[conflicts[0]]) + conflicts[0]] -= 1

            # Swap the conflict to where it needs to be to minimize conflicts
            answer[temp], answer[conflicts[0]] = answer[conflicts[0]], answer[temp]

            # Add new conflict influence
            pos_sum = answer[temp] + temp
            conflicts_x[pos_sum] += 1
            conflicts_o[(board_size + 1 - answer[temp]) + temp] += 1

            pos_sum = answer[conflicts[0]] + conflicts[0]
            conflicts_x[pos_sum] += 1
            conflicts_o[(board_size + 1 - answer[conflicts[0]]) + conflicts[0]] += 1

            time_out += 1
        else:  # If we've been attempting to solve for too long
            fails += 1
            time_out = 0

            # Reset the board
            random.shuffle(answer)
            conflicts_x, conflicts_o = build_confliction_table(answer, board_size)

        conflicts = get_conflicts(answer, board_size, conflicts_x, conflicts_o)

        return answer

def initial_board(boardSize):
    """Initializes the representation of the chess board.
    Args:
        boardSize (int): The size of the n*n board

    Returns:
        board (int[]): The representation of the chess board
        conflictList (int[(int, int)]): A list of tuples of type (int, int),
                                        this gets passed on to the minConflicts() function.
    """

    # board list is initialized
    board = []

    # The list of Queens that conflict with each other.
    conflictList = []
    integerList = list(range(1, boardSize + 1))
    integerList2 = list(range(boardSize))

    # variable to represent half the size of the board (if the size is odd, it takes the floor as it should)
    halfSize = int(boardSize / 2)

    """
    The general idea is reducing the problem to a knight's problem. Two knights could take over each other on a 3*2 or 
    2*3 board on the corner, if we switch the knights to queens, it will show that the queens are not conflicting with 
    each other on row/column/diagonal. The purpose of this part of algorithm is to repeat this process until the board 
    has enough queens. The situation will change according to the size of the board, each branch of the if statement 
    shows a different case.
    """
    if boardSize % 6 == 2:
        board = [0] * (boardSize)
        for i in range(1, halfSize + 1):
            index1 = (2 * (i - 1) + halfSize - 1) % boardSize
            index2 = boardSize - (index1 + 1)
            board[index1] = i
            board[index2] = boardSize + 1 - i
    elif (boardSize - 1) % 6 == 2:
        board = [0] * (boardSize)
        for i in range(1, halfSize + 1):
            index1 = (2 * (i - 1) + halfSize - 1) % (boardSize - 1)
            index2 = boardSize - (index1 + 2)
            board[index1] = i
            board[index2] = boardSize - i
        board[boardSize - 1] = boardSize
    else:
        for i in range(1, halfSize + 1):
            board.append(halfSize + i)
            board.append(i)
        if boardSize % 2 == 1:
            board.append(boardSize)

    """
    Randomly picks x Queens to shuffle, creating conflicts. 
    This shows that our algorithm works, and it works well.
    The higher the value of x, the more our algorithm has to work.
    We decided to let x = 8 in honour of "the eight queens problem"
    """
    for i in range(8):
        randomInt = r.choice(integerList)
        randomIndex = r.choice(integerList2)
        board[randomIndex] = randomInt
        conflictList.append((randomInt, randomIndex))

    # the board and conflict list are returned
    return board, conflictList

def build_confliction_table(board, board_size):
    '''
    returns:
            conflicts_x - the conflicts for left-to-right diagonal conflicts
            conflicts_o - the conflicts for right-to-left diagonal conflicts
    '''
    # It should be noted the first indices will always be 0 because no two coordinates sum to 1
    conflicts_x = [0] * board_size * 2
    conflicts_o = [0] * board_size * 2

    # Build the confliction tables.
    for row, column in enumerate(board):
        conflicts_x[row + column] += 1
        conflicts_o[(board_size + 1 - column) + row] += 1

    return (conflicts_x, conflicts_o)

def get_conflicts(board, board_size, conflicts_x, conflicts_o):
    '''
    returns:
            index_d - the index of the queen that has the most
            index - A list of all possible positions to move the most conflicting queen, along with the number of conflicts per position

    This function obtains a bunch of conflict information that is needed to determine
    what to swap, and where.
    '''
    disturbed = 0
    index_d = -1
    index = []
    # Scan through the confliction tables for the most conflicting piece

    for row, column in enumerate(board):
        temp = conflicts_x[row + column] - 1 + conflicts_o[
            (board_size + 1 - column) + row] - 1  # Total amount of conflicts

        if temp > disturbed:
            # A conflicting piece was found
            disturbed = temp
            index_d = row

    if disturbed > 0:  # If a conflicting piece was found, record its local confliction column
        temp1 = board[index_d]
        index = [a + b for a, b in zip(conflicts_x[temp1:temp1 + board_size],
                                       conflicts_o[board_size + 1 - temp1:2 * board_size + 1 - temp1])]
        index[index_d] -= 2  # We subtract the amount of conflicts the piece would have contributed to its own table.

    return (index_d, index)

def readInput(file):
    with open(file) as f:
        data = f.readlines()
    data = [int(x.strip()) for x in data]
    return data

'''
def writeOutput(solutionLists):
    with open("nqueens_output.txt", 'w') as out:
        for solution in solutionLists:
            startAtOne = [row+1 for row in solution]
            sol = str(startAtOne) + "\n\n"
            out.write(sol)
'''

def verifyStats(listSizes):
    solved = []
    for size in listSizes:
        print("Starting Size:\t\t" + str(size))
        start = time.time()
        queen = solve(size)
        solved.append(queen.positions)
        elapsedTime = time.time() - start
        print("Number of Repairs:\t" + str(queen.num_repairs))
        print("Time Elapsed:\t\t" + str(timedelta(seconds=elapsedTime)))
        print("-----")
    return solved

if __name__ == '__main__':
    sizes = readInput('./nqueens.txt')
    verification = verifyStats(sizes)
    'writeOutput(verification)'