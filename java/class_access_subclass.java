class Parent {
  static int field1 = Child.method();
}

class Child extends Parent {
  static int method() { return 42; }
}
