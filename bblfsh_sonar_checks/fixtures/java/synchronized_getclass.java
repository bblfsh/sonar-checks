class SyncGetClass {
    void test() {
        synchronized (this.getClass()) {}
    }
}
