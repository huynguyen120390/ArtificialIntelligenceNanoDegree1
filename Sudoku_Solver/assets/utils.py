rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

def diagonalList(rows):
    i = 0
    lista = []
    listb = []
    for c in rows:
        lista += [c+str(i + 1)] 
        listb += [c+str(9-i)] 
        i += 1
    theList = [lista,listb]
    return theList 

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = diagonalList(rows)
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def findNakedTwinsinOneUnit(values,unit):
    potentialPair = []
    pairs = []
    for box in unit:
        if len(values[box]) == 2:
            potentialPair.append(box)

    #print(potentialPair)
    for box in potentialPair:
        for box2 in potentialPair:
            if (box != box2) and (values[box] == values[box2]) and (box not in pairs) :
                twin = box, box2
                pairs.append(twin);
               
    #print(pairs)
    return pairs 

def eliminateCandidates(values,pairs,unit):
    for twinPair in pairs:
        pair = list(twinPair)
        for box in pair:
            twinDigit = values[box]
            for digit in twinDigit:
                for unitPeer in unit:
                    #if (peer not in allPairs) and (peer not in pairs) and (digit in values[peer] and( len(values[peer]) > 1)) and (peer in unit):
                    if (unitPeer not in pair) and (digit in values[unitPeer]):
                        values[unitPeer] = values[unitPeer].replace(digit,'')   # remember not to replace one of the twins
    return values

def naked_twins(values):
    for unit in unitlist:
        pairs = findNakedTwinsinOneUnit(values,unit)
        values = eliminateCandidates(values,pairs,unit)
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))
    
def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
                values[peer] = values[peer].replace(digit,'')
                #print("Take out {} at {} with eliminate".format (digit, peer))
                

    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
                #print("Take out {} at {} with only_choice ".format (digit, dplaces[0]))
    return values
    
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        values = naked_twins(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)  
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    # then return one pair of 2 things : length & box name, 
    # not a list of such pairs after min()
    # ???? What if pairs have more than one same min(different boxes), which one min() returns
    #the one in side min() is a list of tuples (length , box name)
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
  
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:              # take a char/ digit in value of the box 
        new_sudoku = values.copy()       # copy dict of values 
        new_sudoku[s] = value            # assign value boxName ( as s )  
        attempt = search(new_sudoku)
        if attempt:
            return attempt
