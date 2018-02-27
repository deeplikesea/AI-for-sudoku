# AI-for-suduku
Here I give three search algorithms to solve 9 * 9 incomplete suduku
code that I upload includes some tests to show the differences among depth first, breadth first and depth first iterative deepening searches.

The goal of the game is to fill in completely the table with digits from 1 to 9 such that each row and column contains each of the digits from 1 to 9 appearing once and only once and at the same time each sub block 3x3 will also contain every 1 to 9 digit once and only once.

Create the structure of search tree
1)Determine the depth of search tree:
the number of layer is the number of empty box in a specific incomplete sudoku; 
2)Determine the searching order:
This means which empty box we should go first and which should be search later.(at each layer, we should choose a empty box with most likelihood under the sudoku rules.)
3)Determine the number of branch at each step:
number of branch from a specific node is available values in the next empty box under the sudoku rules.
