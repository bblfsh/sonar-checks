class ForLoopVarModify {
    void test() {
        for (i = 0; i < 10; i++) {
            --i;
            i++;
            i+=1;
            i=10;
        }
    }
}
