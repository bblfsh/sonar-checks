class ElifRepeatedCondition {
    void test() {
        int a = 1;

        if (a == 1) {}
        else if (a == 2) {}
        else if (a == 1) {}
        else if (1 == a) {}
        else {}
    }
}
