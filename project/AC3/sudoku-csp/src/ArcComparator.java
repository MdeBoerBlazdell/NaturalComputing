import java.util.Comparator;

/**
 * Interface to simplify process of adding additional heuristics to sort the queue with. 
 * Additionally, it makes it slightly easier to work with PriorityQueues by using something which implements this interface.
 * Hence, we left it in, even though it may feel a bit redundant.
 */
public interface ArcComparator extends Comparator<Arc> {
    @Override
    int compare(Arc o1, Arc o2);
}
