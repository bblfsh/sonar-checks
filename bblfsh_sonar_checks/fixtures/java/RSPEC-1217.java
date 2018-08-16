class AvoidThreadrun {
    void test() {
        Thread myThread = new Thread(runnable);
        myThread.run();
    }
}
