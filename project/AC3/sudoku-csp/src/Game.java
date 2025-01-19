import java.util.*;

public class Game {
    private final Sudoku sudoku;
    private int counter = 0;

    Game(Sudoku sudoku) {
        this.sudoku = sudoku;
    }

    public void showSudoku() {
        System.out.println(sudoku);
    }

    /**
     * Implementation of the AC-3 algorithm
     *
     * @return true if the constraints can be satisfied, else false
     */
    public boolean solve() {
        // First, get the board and store all fields in a list
        Field[][] board = sudoku.getBoard();
        List<Field> variables = new LinkedList<>();
        for (int i = 0; i <= 8; i++) {
            for (int j = 0; j <= 8; j++) {
                Field field = board[i][j];
                if (board[i][j].getValue() < 0 || board[i][j].getValue() > 9) {
                    System.err.println("The sudoku contains a value outside of the domain, sudoku can't be solved");
                    return false;
                }
                if (field.getDomainSize() == 0) // For better representation, let no domain be empty
                    field.addDomainvalue(field.getValue());
                variables.add(field);
            }
        }

        // Next, create arcs across the board that will be used in the ac3 algorithm
        List<Arc> arcs = new LinkedList<>();
        for (Field variable : variables) {
            for (Field neighbour : variable.getNeighbours()) {
                Arc arc = new Arc(variable, neighbour);
                arcs.add(arc);
            }
        }
        // At this point, there should be 81*20 = 1620 Arcs created.
        // Finally, initialize the ac3 algorithm, passing all the arcs
        return ac3(arcs);
    }

    private boolean ac3(List<Arc> arcs) {
        // Create a queue, that will contain all initial arcs and future propagation arcs
        Queue<Arc> queue = new PriorityQueue<>(new MostFinalisedFieldsHeuristic());
        queue.addAll(arcs);
        do {
            // At each iteration, retrieve one Arc from the queue
            Arc nextArc = queue.remove();
            counter++;

            // Attempt to reduce each arc object with the revise function
            boolean isReduced = revise(nextArc.getX(), nextArc.getY());
            if (nextArc.getX().getDomainSize() == 0) {
                // If domain is empty there is no value possible for this Field, thus cannot satisfy all constraints
                System.out.println(this.counter);
                return false;
            }

            if (isReduced && nextArc.getX().hasValue()) { // Propagate the effect of arc reduction by creating arcs with neighbours
                for (Field neighbour : nextArc.getX().getNeighbours()) {
                    // only the first Field is reduced: only update those arcs. Arcs of second Field do not need to be updated
                    if (neighbour.hasValue()) continue; // If the neighbour already has a value, no need to propagate
                    Arc propArc = new Arc(neighbour, nextArc.getX());
                    if (!queue.contains(propArc)) {
                        queue.add(propArc);
                    }
                }
            }
            // If the current board is a feasible solution, stop and clear the queue
            if (this.validSolution()) {
                queue.clear();
            }
        }
        while (!queue.isEmpty());
        return true;
    }
    // This performs arc reduction when possible
    private boolean revise(Field x, Field y) {
        if (x.getDomainSize() == 1)
            return false;
        if (x.getDomain().contains(y.getValue())) {
            x.removeFromDomain(y.getValue());
            return true;
        }
        return false;
    }

    /**
     * Checks the validity of a sudoku solution
     *
     * @return true if the sudoku solution is correct
     */
    public boolean validSolution() {
        Field[][] board = sudoku.getBoard();
        for (int i = 0; i < 9; i++) {
            if (!checkRowCol(i, board, true) || !checkRowCol(i, board, false)) {
                return false;
            }
        }

        for (int i = 0; i <9; i +=3){
            for (int j = 0; j <9; j +=3){
                checkBoxes(i,j, board);
            }
        }
        return true;
    }

    private boolean checkBoxes(int i, int j, Field[][] board) {
        List<Integer> allowed = new LinkedList<>(Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9));
     
        for (int boxX = i; boxX < i + 3; boxX++) {
            for (int boxY = j; boxY < j + 3; boxY++) {
                int value = board[boxX][boxY].getValue();
                if (!allowed.contains(value))
                    return false;
                allowed.remove(Integer.valueOf(value));
            }
        }
        return true;
    }

    /**
     * @param index - which row or column we check
     * @param board - current state of sudoku
     * @param isRow - boolean flag to indicate if we check row or column
     * @return - whether the row/column is valid according to rules of sudoku
     */
    public boolean checkRowCol(int index, Field[][] board, boolean isRow) {
        List<Integer> allowed = new LinkedList<>(Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9));
        for (int i = 0; i < 9; i++) {
            int value = (isRow) ? board[index][i].getValue() : board[i][index].getValue();
            if (!allowed.contains(value))
                return false;
            allowed.remove(Integer.valueOf(value));
        }
        return true;
    }
}
