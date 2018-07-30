import javax.naming.directory.SearchControls;

class LDAPDeserialization {
    void test() {
        SearchControls foo = new SearchControls(scope, countLimit, timeLimit, attributes,
                                    true, // Noncompliant; allows deserialization
                                    deref)
    }
}
