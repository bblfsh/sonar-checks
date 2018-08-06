class JavaIOFileDelete {
    static private File f1 = new File("/foo/bar.txt");

    void test() {
        File f2 = new File("/bar/baz.txt");
        f1.delete();
        f2.delete();
        Files.delete(f1);
        Files.delete(2);
    }
}
