class IdentExprBinary {
    void test() {
        int a = 1;
        int b = 2;
        if (a == a) {}
        if (a == b && a == b) {}
        if (a == b && b == a) {}
        this.equals(this);
        a = b + b;
        a = a * a;
        int c = 5/5;
        int d = 7-7;
    }
}
