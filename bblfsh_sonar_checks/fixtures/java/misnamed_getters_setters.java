class MisnamedGettersSetters {
    private int x, y;
    public int getX() {
        return this.y;
    }

    public int getZ() {
        return y;
    }

    public void setY(int y) {
        this.x = y;
    }

    public void setZ(int y) {
        x = y;
    }
}
