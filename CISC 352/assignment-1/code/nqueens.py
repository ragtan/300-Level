import random
import time
import math


def timing_val(func):
    def wrapper(*arg, **kw):
        '''source: http://www.daniweb.com/code/snippet368.html'''
        t1 = time.time()
        res = func(*arg, **kw)
        t2 = time.time()
        return res, (t2 - t1)

    return wrapper


@timing_val
def solve(board_size):
    '''
    Solves the n-queens problem
    '''

    answer = initial_board(board_size)
    conflicts_x, conflicts_o = build_confliction_table(answer, board_size)
    time_out = 0  # This will determine when we need to reshuffle and try again
    fails = 0
    conflicts = get_conflicts(answer, board_size, conflicts_x, conflicts_o)
    randchoose = random.choice
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
            temp = randchoose(indices)  # Randomly select one of the lowest conflict zones to replace the conflict with

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
            answer = initial_board(board_size)
            conflicts_x, conflicts_o = build_confliction_table(answer, board_size)

        conflicts = get_conflicts(answer, board_size, conflicts_x, conflicts_o)

    return answer

def initial_board(board_size):
    test = []
    first_half = []
    second_half = []
    initial_y = random.randrange(1, math.floor(board_size/2), 1)
    for i in range(1, math.floor(board_size/2) + 1):
        test.append(i-1)
        first_half.append((initial_y + (2*i)) % board_size)
    for i in range(math.floor(board_size/2) + 1, board_size + 1):
        test.append(i-1)
        second_half.append((initial_y + (2*i) - 1) % board_size)
    full_list = first_half + second_half
    print(full_list)
    return full_list

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
if __name__ == '__main__':
    print(solve(100000))