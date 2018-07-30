class LDAPDeserialization {
    void test() {
        user = "foo";
        pass = "bar";
        String query = "SELECT * FROM users WHERE user = '" + user + "' AND pass = '" + pass + "'"; // Unsafe
    }
}
