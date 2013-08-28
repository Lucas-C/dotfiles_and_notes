/**EXPORT:
//1-Compile
rm -rf bin/*
libs="src/" ; for f in lib/*.jar; do libs="$libs:$f"; done
javac -cp $libs -d bin/ $(find src/ -name *.java)
//2-Pack
mkdir lib_extracted
for file in $(find ../lib/ -name *.jar | grep -v 'mockito\|junit'); do jar xf $file; done
cd ..
jar cmf MANIFEST.MF archive.jar -C bin/ com/ -C lib_extracted/ . data/
rm -rf lib_extracted
//3-Run!
java -jar archive.jar # Maybe -cp .
// To be sure you're using the correct Java : namei $(which java)
*/

// Debugger
jdb

jconsole
// http://docs.oracle.com/javase/6/docs/technotes/guides/management/jconsole.html

// Object-type histogram on a running jvm
jmap -histo:live <pid>

// String / ByteString correct conversion :
String asString = new String( byteString.getArray(), "UTF-8" );
ByteString asBytes = ByteString.wrap( string.getBytes( "UTF-8" );

import java.util.Arrays;
Arrays.toString(myCollection.toArray()) // nice collection stringification

assert *<condition>* : *<object>* // Don't forget to -enableassertions

"" == (new String("")).intern()

// Reflection
import java.lang.reflect.Field;
import java.lang.reflect.Method;

// Methods/attribute privacy only true at compile time : if one recompile a class into bytecode with all private, it will still work !

// Google Guava
Optional<> : Optional.of(...), Optional.absent(), opt.isPresent(), opt.get()
public String toString() { Objects.toStringHelper(getClass()).add("Attr", attr).add(...); }
ImmutableSet<V>
ImmutableMap.Builder<K,V>

// Enum
static enum Action {
    PUT(ClientPut.class),
    GET(ClientGet.class),
    LIST(ClientList.class);
    final Class< ? extends BackupClient > client;
    private Action(Class< ? extends BackupClient > client) { this.client = client; }
    public static Action fromString(String value) {
        for (Action action : Action.values()) {
            if (action.toString().equalsIgnoreCase(value)) {
                return action;
            }
        }
        throw new IllegalArgumentException("Value " + value + " can not be converted to Action. "
                + "Available values are: " + Arrays.toString(Action.values()));
    }
}
Client client = injector.getInstance(params.action.client);
Method action = Client.class.getMethod(params.action.toString().toLowerCase());
action.invoke(client);

// Jcommander
static Settings parseCommandLineArguments(String[] args) {
    Settings params = new Settings(); // with attributes commented with @Parameter
    JCommander parser = new JCommander(params);
    parser.setProgramName("whatever");
    try {
         parser.parse(args);
    } catch (ParameterException ex) {
        parser.usage();
        Throwables.propagate(ex);
    }
    if (params.help) {
        parser.usage();
    }
    return params;
}

// Java exception handling (use only RuntimeExceptions !!)
public static void main(String[] args) {
    LOG.info("{} starting with args ", PROG_NAME, Arrays.toString(args));
    try {
        run(args);
    } catch (InvocationTargetException e) {
        throw (RuntimeException)e.getTargetException();
    } catch (RuntimeException e) {
        StringWriter stackTrace = new StringWriter();
        e.printStackTrace(new PrintWriter(stackTrace));
        LOG.error(stackTrace.toString());
        throw e;
    }
    LOG.info("{} exited sucessfully", PROG_NAME);
}

/* Useful standard runtime exceptions:
 *  - IllegalArgumentException
 *  - NullPointerException
 *  - IllegalStateException => for class invariants
 *  - UnsupportedOperationException
 *  - NoSuchElementException
 *  - IndexOutOfBoundsException / ArrayIndexOutOfBoundsException
 *  - NumberFormatException
 *  - ProviderException / MissingResourceException(String s, String className, String key)
 *  - TypeNotPresentException / TypeConstraintException / UnknownEntityException
 *  - ClassCastException
 * Less useful but worth knowing:
 *  - BufferOverflowException / BufferUnderflowException
 *  - WrongMethodTypeException 
 *  - AnnotationTypeMismatchException(Method element, String foundType) / IncompleteAnnotationException(Class<? extends Annotation> annotationType, String elementName)
 *  - EnumConstantNotPresentException
 *  - ArrayStoreException
 *  - ArithmeticException
 *  - EmptyStackException
 *  - SystemException / SecurityException
 * Complete list : http://docs.oracle.com/javase/7/docs/api/java/lang/RuntimeException.html
 */
