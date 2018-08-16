class BinaryInsteadOfBoolean {
    void test() {
        int a = true;
        int b = false;
        if(a | b) {}
        if(a & b) {}
    }
}
