public class Arc{
    private final Field x;
    private final Field y;

    public Arc(Field x, Field y){
        this.x = x;
        this.y = y;
    }

    public boolean equals(Arc other){
        return this.x.equals(other.x) && this.y.equals(other.y);
    }

    public Field getX(){
        return this.x;
    }
    public Field getY(){
        return this.y;
    }

}
