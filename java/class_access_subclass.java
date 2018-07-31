class Parent {
  static int field1 = Child.method();
  static int foo2 = Child.foo;
}

class Child extends Parent {
  static int foo = 33;
  static int method() { return 42; }
}

