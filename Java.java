jconsole
// http://docs.oracle.com/javase/6/docs/technotes/guides/management/jconsole.html

// Object-type histogram on a running jvm
jmap -histo:live <pid>

// String / ByteString correct conversion :
String asString = new String( byteString.getArray(), "UTF-8" );
ByteString asBytes = ByteString.wrap( string.getBytes( "UTF-8" );

// Built-in parallelism the easy way : ExecutorService

// Methods/attribute privacy only true at compile time : if one recompile a class into bytecode with all private, it will still work !

// Google Optional<> : Optional.of(...), Optional.absent(), opt.isPresent(), opt.get()

// Google public String toString() { Objects.toStringHelper(getClass()).add("Attr", attr).add(...); }

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
    1 /******/
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
    LOG.info("{} starting with args ", PROG_NAME, Array.toString(args));
    try {
        run(args);
    } catch (RuntimeException e) {
        StringWriter stackTrace = mew StringWriter();
        e.printStackTrace(new PrintWriter(stackTrace));
        LOG.error(errors.toString());
        throw e;
    }
    LOG.info("{} exited sucessfully", PROG_NAME);
}
