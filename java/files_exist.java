class FilesExists {
    void test() {
        Files.exists("foo");
        Files.notExists("foo");
        Files.isDirectory("/foo");
        Files.isRegularFile("foo");
    }
}
