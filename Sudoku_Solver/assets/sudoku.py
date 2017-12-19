from utils import *
diagonalSudokuString1 = '49.....8...3...........62..5...8..9.....4.61.6.1.2.5..256...3..1....2........78..'
diagonalSudokuString2 = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
theGrid = grid_values(diagonalSudokuString1)
val = search(theGrid)
print(val)
display(val)
