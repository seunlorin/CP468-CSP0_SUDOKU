from collections import deque
from time import time
from unittest import result

rows = "ABCDEFGHI"
cols = "123456789"

def block_neighbors(square):
    r, c = square[0], square[1]
    row_index = rows.index(r) #convert row and col to 0 to 8 indexes
    col_index = int(c) - 1

    block_row = (row_index // 3) * 3 #converts it to either 0, 3, 6 so we know the starting index of the row and col of which block it belongs to
    block_col = (col_index // 3) * 3

    block_squares = [
        rows[block_row + r] + str(block_col + c + 1) #starting row of block + r to get specific row within that block +1 for columns since we were using 0-8 earlier
        for r in range(3) #each combination of r and c gives one square in the block
        for c in range(3)   
    ]

    block_squares.remove(square) #remove self square from neighbors
    return(block_squares)

# Revise domain of xi with respect to xj by removing values that don't meet the constraint xi != xj
def revise(domains, xi, xj):
    revised = False

    # If xj only has one value then remove it from xi's domain
    if len(domains[xj]) == 1:
        value = next(iter(domains[xj])) # Get the value
        # If xi has that value then remove because xi != xj
        if value in domains[xi]:
            domains[xi].remove(value)
            revised = True

    return revised # Will return true if any values are removed from the domain of xi

# Implement AC-3 Algorithm
def AC3(domains, neighbours):
    queue = deque((xi, xj) for xi in domains for xj in neighbours[xi]) # Make queue with all arcs for every variable and neighbours
    length_queue = [] # Track queue length

    print(f"Initial queue length: {len(queue)}")

    # Loop through queue until empty
    while queue:
        length_queue.append(len(queue)) # Update queue length before each pop
        xi, xj = queue.popleft() # Take an arc

        # Revise if needed
        if revise(domains, xi, xj):
            # If xi's domain is empty then the csp is inconsistent
            if len(domains[xi]) == 0:
                length_queue.append(len(queue))
                return domains, length_queue
            # If we revise then recheck all arcs for xk in xi's neighbors
            for xk in neighbours[xi]:
                if xk != xj: # Don't add the same arc back right away
                    queue.append((xk, xi))
        print(f"Current queue length: {len(queue)}")
    print(f"Lengths of queue: {length_queue}")

    return domains, length_queue # Return the domain and queue length

def is_complete(domains):
    return all(len(v) == 1 for v in domains.values())

def select_unassigned_variable(domains):
    # minimum remaining values
    return min((s for s in domains if len(domains[s]) > 1), key=lambda s: len(domains[s]))

def backtrack(domains, neighbours):
    if is_complete(domains):
        return domains
    var = select_unassigned_variable(domains)
    for value in sorted(domains[var]):
        temp = {v: set(domains[v]) for v in domains}  # deep copy domains
        temp[var] = {value}
        consistent = True
        # forward checking
        for n in neighbours[var]:
            if value in temp[n]:
                temp[n].remove(value)
                if not temp[n]:
                    consistent = False
                    break
        if consistent:
            result = backtrack(temp, neighbours)
            if result:
                return result
    return None

def main():
    start_time = time()
    result1, length_queue = csp_solver('sudoku_1.txt')
    end_time = time()
    time1 = end_time - start_time

    start_time = time()
    result2, length_queue = csp_solver('sudoku_2.txt')
    end_time = time()
    time2 = end_time - start_time
    
    start_time = time()
    result3, length_queue = csp_solver('sudoku_3.txt')
    end_time = time()
    time3 = end_time - start_time

    print("Results")
    print(f"Time taken for Sudoku 1: {time1:.4f} seconds.")
    print_sudoku(result1)
    print(f"Time taken for Sudoku 2: {time2:.4f} seconds.")
    print_sudoku(result2)
    print(f"Time taken for Sudoku 3: {time3:.4f} seconds.")
    print_sudoku(result3)

def csp_solver(filename):
    neighbors = {} #neighbors dictionary
    squares = [r + c for r in rows for c in cols] #create list of squares (A1, A2, etc..)

    domains = {s: {} for s in squares}

    for s in squares:
        r, c = s[0], s[1] #get the row letter and column number for the square
        row_neighbors = [r + col for col in cols if col != c] #A1, A2, for all numbers 1-9 except for current square s col number
        col_neighbors = [row + c for row in rows if row != r]
        b_neighbors = block_neighbors(s)

        #all row, col, and block neighbors together in a set
        neighbors[s] = set(row_neighbors + col_neighbors + b_neighbors) #use set to remove duplicates that come from block_neighbors

    file = open(filename, 'r')
    print(f"\nSolving Sudoku Puzzle from file: {filename}\n")

    for square in domains:
        char = file.read(1) #read 1 char from file at a time
        while char in '\n': #skip new lines and spaces
            char = file.read(1)
        if char == '0':
            domains[square] = {1,2,3,4,5,6,7,8,9} #if square is empty, then domain is {1,2,3,4,5,6,7,8,9}
        else:
            domains[square] = {int(char)} #if square has value, then domain is that value
        
    file.close()

    length_queue = 0

    domains, length_queue = AC3(domains, neighbors)
    if is_complete(domains):
        print("\nThe puzzle is solved by AC-3...")
        #print_sudoku(domains)
    else:
        #print("\nAC-3 could not solve the puzzle, proceeding to backtracking...")
        result = backtrack(domains, neighbors)
        if result:
            #print("\nThe puzzle is solved by Backtracking...")
            #print_sudoku(result)
            return result, length_queue
        else:
            print("No solution found.")

    return domains, length_queue

def print_sudoku(domains):
    for r in rows:
        row_str = ""
        for c in cols:
            square = r + c
            value = next(iter(domains[square])) #print domains of each square (assuming that it is comepleted each should have 1 value)
            row_str += f"[{value}]" #format for sudoku puzzle ex. [0] [1] [2]
        print(row_str)
if __name__ == '__main__':
    main()