class UnusedPrivateClass {
    private class Useless {}
    private class Used {}
    void test() {
        Used u = new Used();
    }
}
