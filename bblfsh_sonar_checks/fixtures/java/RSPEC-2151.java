class Finalizers {
    public static void main(String [] args) {
        System.runFinalizersOnExit(true);
    }

    protected void finalize() {
    }
}
