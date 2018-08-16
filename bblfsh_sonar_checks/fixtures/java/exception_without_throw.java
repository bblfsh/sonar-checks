class ExceptionWithoutThrow {
    void test() {
        new RuntimeException();
        throw new PokException();
    }
}
