class ArraysAsList {
    void test() {
        Arrays.asList("a1", "a2", "b1", "c2", "c1"); // this is fine (Object)
        Arrays.asList(1, 2, 3, 4);
        Arrays.asList(01, 02);
        Arrays.asList(0x1, 0x2);
        Arrays.asList(0b11, 0b10);
        Arrays.asList(123.456);
        Arrays.asList('a', 'b');
        Arrays.asList(true, false);
    }
}
