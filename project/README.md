Within this directory, there are a few important files and folders:

- The sudokus folder contains all sudoku's that were used to generate the results. Note that they are all of the form sudoku1_Nv.txt, where
N indicates the number of missing values. All these Sudoku's were generated from the same solution, which is stored as sudoku1_solution.txt
- The sudoku_evolution.py file contains the main logic for the AE and the helper functions needed
- sudoku.py contains all functionality related to working with the Sudoku
- sudoku_solver.py is the main file, and is used to run the experiments
- AC3 is a folder that contains a Java implementation of the AC3 algorithm which was used as a baseline

# Running the experiments
To run the experiments, you need to run sudoku_solver.py. You can decide which Sudoku to use by modifying line 5, simply give the path to your Sudoku
Then, there are two possible outcomes:

- Either the program does not find a solution in 10k generations, in which case it will output: "No solution found after 10.000 generations" in the terminal.
In this case, it will also create a plot (and save it to disk) called results.png, which show the best fitness over time.
- Otherwise, the program will output that it has found a solution in the terminal, and after how many generations. Additionally, it will output the solution to the Sudoku.

