import java.util.concurrent.locks;

class MultiLocksWait {
    private Lock mon1;
    private Lock mon2;

    void test() {
        synchronized (this.mon1) {  // threadB can't enter this block to request this.mon2 lock & release threadA
            synchronized (this.mon2) {
                this.mon2.wait();  // Noncompliant; threadA is stuck here holding lock on this.mon1
            }
        }
    }
}
