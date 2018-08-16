class Pear {}

class ClassCompareName {
  public void test() {
    item = new Pear();
    if ("Pear".equals(item.getClass().getSimpleName())) {}
    if ("Pear".equals(item.getClass().getName())) {}
  }
}
