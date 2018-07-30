import java.util.concurrent.locks;

class SleepInsideLock {
    void test() {
        Lock monitor;

        synchronized(monitor) {
            while(notReady()){
                Thread.sleep(200);
            }
        }
    }
}
