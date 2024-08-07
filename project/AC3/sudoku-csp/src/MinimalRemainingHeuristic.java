public class MinimalRemainingHeuristic implements ArcComparator {
    @Override
    public int compare(Arc o1, Arc o2) {
        return Integer.compare(o1.getX().getDomainSize(), o2.getX().getDomainSize());
    }
}

