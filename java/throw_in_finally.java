class ThrowInFinally {
    void test() {
        try {
        } finally {
            throw new RuntimeException();
            return;
        }
    }
}
