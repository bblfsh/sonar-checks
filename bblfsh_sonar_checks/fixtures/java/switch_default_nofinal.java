class SwitchDefaultNoFinal {
    void test() {
        switch (myVariable) {
            default:
                doSomethingElse();
                break;
            case 1:
                foo();
                break;
            case 2:
                doSomething();
                break;
        }
    }
}
