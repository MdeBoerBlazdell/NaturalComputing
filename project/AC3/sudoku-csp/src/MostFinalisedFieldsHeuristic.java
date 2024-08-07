public class MostFinalisedFieldsHeuristic implements  ArcComparator {
    @Override
    public int compare(Arc o1, Arc o2) {
        if ((o1.getY().getDomainSize() == 1) && (o2.getY().getDomainSize() != 1)) {
            return -1;
        } else if (o1.getY().getDomainSize() != 1 && o2.getY().getDomainSize() == 1) {
            return 1;
        } else {
            return 0;
        }
    }
}
