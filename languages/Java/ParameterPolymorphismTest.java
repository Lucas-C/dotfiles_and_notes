/*
 * This test illustrate that Java only resolve parameter type
 * at COMPILATION TIME, not during RUNTIME 
*/
class ParameterPolymorphismTest
{
    public static void main(String[] argv) {
        B obj = new C();
        String str = stringify(obj);
        System.out.println(str);
        assert str.startsWith("ArgType=B");
    }

    static class A {}
    static class B extends A {}
    static class C extends B {}
    public static String stringify(A a) {
        return "ArgType=A : " + a;
    }
    public static String stringify(B b) {
        return "ArgType=B: " + b;
    }
    public static String stringify(C c) {
        return "ArgType=C: " + c;
    }
}
