public class Fruit implements Serializable {
  private static final long serialVersionUID = 1;
  private Object readResolve() throws ObjectStreamException {}
}
