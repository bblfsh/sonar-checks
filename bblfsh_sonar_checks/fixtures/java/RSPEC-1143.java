class ThrowInFinally {
    void test() {
        try {
        } finally {
            throw new RuntimeException();
            return;
        }
    }
    void test2() {
        throw new RuntimeException();
    }
}
