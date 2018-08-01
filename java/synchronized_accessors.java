public class Person {
  String name;
  int age;

  public synchronized void setName(String name) {
    this.name = name;
  }

  public String getName() {
    return this.name;
  }

  public void setAge(int age) {
    this.age = age;
  }

  public synchronized int getAge() {
    synchronized (this) {
      return this.age;
    }
  }
}
