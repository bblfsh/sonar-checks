import javax.crypto.KeyGenerator;

class CryptoKeysLength {
    void test1() {
        KeyGenerator keyGen = KeyGenerator.getInstance("Blowfish");
        keyGen.init(64); // Noncompliant
    }

    void test2() {
        KeyPairGenerator keyPairGen = KeyPairGenerator.getInstance("RSA");
        keyPairGen.initialize(512); // Noncompliant
    }
}
