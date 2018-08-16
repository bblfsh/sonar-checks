class IllegalMonitorCatch {
    void test() {
        try {
            this.notify();
        } catch(IllegalMonitorStateException e) {
        }
    }
}
