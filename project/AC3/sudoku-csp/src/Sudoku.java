import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.*;

public class Sudoku {
  private final Field[][] board;

  Sudoku(String filename) {
    this.board = readsudoku(filename);
  }

  @Override
  public String toString() {
    String output = "╔═══════╦═══════╦═══════╗\n";
		for(int i=0;i<9;i++){
      if(i == 3 || i == 6) {
		  	output += "╠═══════╬═══════╬═══════╣\n";
		  }
      output += "║ ";
		  for(int j=0;j<9;j++){
		   	if(j == 3 || j == 6) {
          output += "║ ";
		   	}
         output += board[i][j] + " ";
		  }
		  
      output += "║\n";
	  }
    output += "╚═══════╩═══════╩═══════╝\n";
    return output;
  }

  /**
	 * Reads sudoku from file
	 * @param filename
	 * @return 2d int array of the sudoku
	 */
	public static Field[][] readsudoku(String filename) {
		assert filename != null && !"".equals(filename) : "Invalid filename";
		String line = "";
		Field[][] grid = new Field[9][9];
		try {
		FileInputStream inputStream = new FileInputStream(filename);
        Scanner scanner = new Scanner(inputStream);
        for(int i = 0; i < 9; i++) {
        	if(scanner.hasNext()) {
        		line = scanner.nextLine();
        		for(int j = 0; j < 9; j++) {
              int numValue = Character.getNumericValue(line.charAt(j));
              if(numValue == 0) {
                grid[i][j] = new Field();
              } else if (numValue != -1) {
                grid[i][j] = new Field(numValue);
        			}
        		}
        	}
        }
        scanner.close();
		}
		catch (FileNotFoundException e) {
			System.out.println("error opening file: "+filename);
		}
    addNeighbours(grid);
		return grid;
	}

  /**
   * Adds a list of neighbours to each field, i.e., arcs to be satisfied
   * @param grid
   */
  private static void addNeighbours(Field[][] grid) {
      for(int i = 0; i < 9; i++){
          for(int j = 0; j < 9; j++){
              LinkedList<Field> neighbours = new LinkedList<>();

              // Vertical neighbours
              int vertX = i;
              for(int vertY = 0; vertY < 9; vertY++){
                  if(vertX == i && vertY == j) continue;
                  else {
                      if (neighbours.contains(grid[vertX][vertY])) continue;
                      else neighbours.add(grid[vertX][vertY]);
                  }
              }

              // Horizontal neighbours
              int horY = j;
              for(int horX = 0; horX < 9; horX++){
                  if(horX == i && horY == j) continue;
                  else {
                      if (neighbours.contains(grid[horX][horY])) continue;
                      else neighbours.add(grid[horX][horY]);
                  }
              }
              
              /**
               * We make use of the fact that integer division is a floor division
               * i / 3 calculates which position in a 3x3 grid the field occupies
               * and the * 3 ensures that we are in the correct 3x3 grid 
               */
              int startX = (i / 3) * 3;  
              int startY = (j / 3) * 3;

              // 'Box' neighbours
              for (int boxX = startX; boxX < startX+3; boxX++){
                  for (int boxY = startY; boxY < startY+3; boxY++){
                      if (boxX == i && boxY == j) continue;
                      else{
                          if (neighbours.contains(grid[boxX][boxY])) continue;
                          else neighbours.add(grid[boxX][boxY]);
                      }
                  }

              }
              grid[i][j].setNeighbours(neighbours);
          }
      }
  }

    /**
	 * Generates fileformat output
	 */
	public String toFileString(){
    String output = "";
    for (int i = 0; i < board.length; i++) {
      for (int j = 0; j < board[0].length; j++) {
        output += board[i][j].getValue();
      }
      output += "\n";
    }
    return output;
	}

  public Field[][] getBoard(){
    return board;
  }

}
