
import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;


public class App {
    public static void main(String[] args) throws Exception {
        var results = runAllTests();
        System.out.println("Printing all test results (execution time in ms)");
        for (String key : results.keySet()){
            System.out.println(key + ": " + Arrays.toString(results.get(key)));
        }
    }

    /**
     * Start AC-3 using the sudoku from the given filepath, and reports whether the
     * sudoku could be solved or not, and how many steps the algorithm performed
     * 
     * @param filePath
          * @return 
          */
        public static Map<String, long[]> runAllTests() {
        Map<String, long[]> results = new HashMap<>();
    
        File path = new File("sudokus/inputs");
        File[] testCases = path.listFiles();
        for (File f : testCases){
            String filePath = "sudokus/inputs/" + f.getName();
            var timings = runTest(filePath);
            results.put(f.getName(), timings);
        }
        
        return results;
    }

    public static long[] runTest(String filepath){
        long[] timings = new long[5];
        
        for (int i = 0; i < 5; i++) {
            Game game = new Game(new Sudoku(filepath));
            long start = System.currentTimeMillis();
            game.solve();
            timings[i] = System.currentTimeMillis() - start;
        }
        return timings;
    }

}

