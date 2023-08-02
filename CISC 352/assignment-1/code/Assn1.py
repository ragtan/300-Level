import random
import time
from datetime import timedelta

"""The n queens puzzle"""

class NQueens:
    """Generate all valid solutions for the n queens puzzle"""
    def __init__(self, size, showProgress=False):
        # Store the puzzle (problem) size and the number of valid solutions
        self.size = size
        self.numRepairs = 0
        self.positions = [None] * self.size # Represents the entire chessboard, positions[k] = i denotes a queen in the kth column and ith row.
        self.rowConflicts=[0]*size          # There are n rows, each queen needs to eventually reside in its own row. This list keeps track of queens that conflict on the same row.
        self.diag1Conflicts=[0]*(2*size-1)  # There are 2n-1 diagonals going in the /// direction, we have to account for possible conflicts on those diagonals
        self.diag2Conflicts=[0]*(2*size-1)  # There are 2n-1 diagonals going in the \\\ direction, we have to account for possible conflicts on those diagonals
        self.initializePositions()          
        self.solve(showProgress)

    def solve(self,showProgress):

        maxIters = 100
        currentIter = 0
        success = False
        while currentIter < maxIters:
            column = self.findConflictingCol()
            if column < 0:
                success = True
                self.numRepairs+=currentIter
                break
            rowToPut = self.minConflicts(column)
            if showProgress: print("Moved queen in column "+str(column)+" from row "+str(self.positions[column]) + " to row " + str(rowToPut)+".")
            self.removeQueen(self.positions[column], column)
            self.addQueen(rowToPut, column)
            currentIter+=1
        if not success:
            self.numRepairs+=currentIter
            self.restart(showProgress)

    def restart(self,showProgress):
        """
            If there have been a number of iterations without any progress made we reset the entire board, and conflict lists, then start
            over.
        """
        self.positions = [None] * self.size 
        self.rowConflicts=[0]*self.size
        self.diag1Conflicts=[0]*(2*self.size-1)
        self.diag2Conflicts=[0]*(2*self.size-1)
        self.initializePositions()
        self.solve(showProgress)

    def findConflictingCol(self):
    	num_vars_violated = 0
    	vio_col = []
    	num_vios = 0 # The number of violations for a row/column position.
    	for col in range(0, self.size):
    		row=self.positions[col]
    		num_vios = self.rowConflict(row, col)
    		if 3 != num_vios: #three = zero violations, means that one queen can reach that row/column position from either side or both diagonals. The only queen that fits that description is the one residing on that row/column position
    			vio_col.append(col)
    	num_vars_violated = len(vio_col)
    	if num_vars_violated == 0: # If the array of possible options is empty return -1
    		return -1
    	return random.choice(vio_col)

    def initializePositions(self):
        """
            Starting off with an empty board, place each queen in their respective column on the row that minimizes conflicts.
            Initializing the board in a way that's as close to optimal as we can get off the bat improves the speed of finding a solution. 
        """
        self.positions = [None] * self.size 
        for column in range(self.size):
            rowToPut = self.minConflicts(column) # See if we can put the queen along the diagonal
            self.addQueen(rowToPut, column)

    def addQueen(self, row, col):
        """
            Update the positions list to denote the queen 
        """
        self.positions[col] = row
        self.rowConflicts[row] = self.rowConflicts[row]+1
        self.diag1Conflicts[(self.size-1)+(col-row)] = self.diag1Conflicts[(self.size-1)+(col-row)]+1
        self.diag2Conflicts[row+col] = self.diag2Conflicts[row+col]+1

    def removeQueen(self, row, col):
        """
            Remove a queen from it's row/column position - updates the positions array and removes any conflicts that
            the queen originally had.
        """
        self.positions[col] = None
        self.rowConflicts[row] = self.rowConflicts[row]-1
        self.diag1Conflicts[(self.size-1)+(col-row)] = self.diag1Conflicts[(self.size-1)+(col-row)]-1
        self.diag2Conflicts[row+col] = self.diag2Conflicts[row+col]-1

    def minConflicts(self,col):
        """
            Takes in the column the queen is on.
            Returns the row for that Queen's column that minimizes conflict.
        """
        minn = float('inf')
        candidates = []
        for row in range(self.size):
            rowCons = self.rowConflict(row, col)
            if rowCons < minn:
                minn = rowCons
                candidates = [row]
            elif rowCons == minn:
                candidates.append(row)
        choice = random.choice(candidates) # Out of all all the best possible options, pick one randomly. 
        return choice

    def rowConflict(self, row, col):
        """
            Given a row and a column, return how many current queen's could reach that square.
        """
        return self.rowConflicts[row]+self.diag1Conflicts[(self.size-1)+(col-row)]+self.diag2Conflicts[col+row]

    def showFullBoard(self):
        """Show the full NxN board"""
        for row in range(self.size):
            line = ""
            for column in range(self.size):
                if self.positions[column] == row:
                    line += "Q "
                else:
                    line+=". "
            print(line)

def readText(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [int(x.strip()) for x in content]
    return content

def writeOutput(listOfAnswers):
    with open("nqueens_out.txt",'w') as out:
        for answer in listOfAnswers:
            makeOneBased = [row+1 for row in answer]
            line = str(makeOneBased)+"\n"
            out.write(line)

def solveQueens(listOfSizes):
    solved = []
    for size in listOfSizes:
        print("Starting Size:\t\t"+str(size))
        start = time.time()
        queen = NQueens(size)
        solved.append(queen.positions)
        timeTaken = time.time()-start
        print("Number of Repairs:\t"+str(queen.numRepairs))
        print("Time Taken:\t\t"+str(timedelta(seconds=timeTaken)))
        print("---")
    return solved

if __name__ == '__main__':
    # queen = NQueens(50,True)
    # queen.showFullBoard()
    sizes = readText('./nqueens.txt')
    solvedQueens = solveQueens(sizes)
    writeOutput(solvedQueens)



def test():
    initialConflictsSmall = []
    initialConflictsMed = []
    timesLong = []

    count = 0
    while count < 10:
        # print(count)
        count+=1
        # start = time.time()
        # queen = NQueens(100)
        # timesShort.append(time.time() - start)

        # start = time.time()
        # queen = NQueens(120)
        # timesMedium.append(time.time() - start)
        start = time.time()
        queen = NQueens(20000)
        timeTaken = time.time()-start
        print("Pass: "+str(count)+", time taken: "+str(timeTaken))
        timesLong.append(time.time() - start)
        

        # start = time.time()
        # queen = NQueens(64, True)
        # betaTimesShort.append(time.time() - start)
        # start = time.time()
        # queen = NQueens(120, True)
        # betaTimesMedium.append(time.time() - start)
        # start = time.time()
        # queen = NQueens(20000, True)
        # betaTimesLong.append(time.time() - start)

        print("---")
        # print(sum(initialConflictsSmall)/len(initialConflictsSmall), "avg initial conflicts small")
        # print(sum(initialConflictsMed)/len(initialConflictsMed), "avg initial conflicts medium")
        print(sum(timesLong)/len(timesLong), "avg time large")