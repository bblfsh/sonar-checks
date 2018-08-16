class NonlockWaitNotify {
    void test() {
        synchronized(NonlockWaitNotify.class) {
            wait();
        }
    }

    synchronized void testSync() {
        wait();
    }

    void test2() {
        wait(); // Noncompliant
    }
}
