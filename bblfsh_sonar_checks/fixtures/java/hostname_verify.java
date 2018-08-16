import javax.ws.rs.client.ClientBuilder;
import javax.net.ssl;
import javax.ws.rs.client

class HostnameVerify {
    void test() {
        Client client = ClientBuilder.newBuilder().sslContext(sslcontext).hostnameVerifier(new HostnameVerifier() {
            @Override
                public boolean verify(String requestedHost, SSLSession remoteServerSession) {
                    return true;  // Noncompliant
                }
        }).build();
    }
}
