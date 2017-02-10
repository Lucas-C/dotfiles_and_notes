obj.properties.collect{it}.join('\n') // debug dump props

ob.@property // direct access to Java property

@GrabResolver(name='nexus', root='http://nexus/content/repositories/central/')
@GrabExclude('org.codehaus.groovy:groovy-all')
@Grab(group='org.codehaus.groovy.modules.http-builder', module='http-builder', version='0.7.2')

@groovy.transform.Immutable


def getHttpClient() {
    // Ignores certificate issues for SSL connections. Cert does not have to be from a trusted authority and the hostname does not need to be verified.
    def trustStrategy = new TrustStrategy() {
        @Override
        public boolean isTrusted(X509Certificate[] chain, String authtype) { true }
    }
    def sslSocketFactory = new SSLSocketFactory(trustStrategy, SSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER)
    HttpClients.custom().setSSLSocketFactory(sslSocketFactory).build()
}
def httpGet(url) { // using Apache Java httpclient, basic GET
    (new JsonSlurper()).parseText((new Executor(httpClient)).execute(Request.Get(url)).returnContent().asString())
}
static final COLOR_RED = '\033[31m'
static final COLOR_END = '\033[0m'
def httpGetJson(Map args) { // using Apache Java httpclient, with query-params, auth header, and parse returned JSON
    def uriBuilder = new URIBuilder(apiRootUrl)
    uriBuilder.path = args.path
    if (args.query) {
        args.query.each{ k, v -> uriBuilder.addParameter(k, v) }
    }
    def request = new HttpGet(uriBuilder.build())
    request.addHeader('Authorization', authHeader)
    def response = httpClient.execute(request)
    try {
        def responseContent = responseAsString(response)
        def parsedResponse = tryParseJSON(responseContent)
        if (response.statusLine.statusCode != 200) {
            errLog COLOR_RED + tryPrettyPrintJSON(parsedResponse) + COLOR_END
            throw new HttpResponseException(response.statusLine.statusCode, response.statusLine.reasonPhrase)
        }
        parsedResponse
    } finally {
        response.close()
    }
}
def responseAsString(response) {
    def outputStream = new ByteArrayOutputStream()
    response.entity.writeTo(outputStream)
    outputStream.toString('utf8')
}
def tryParseJSON(text) {
    try {
        new JsonSlurper().parseText(text)
    } catch (JsonException) {
        text
    } catch (IllegalArgumentException) {
        text
    }
}
def tryPrettyPrintJSON(obj) {
    try {
        prettyPrint obj
    } catch (JsonException) {
        obj.toString()
    }
}
def httpGetJson(Map args) { // using Groovy HTTPBuilder
    def parsedResponse
    httpClient.request(GET, JSON) { req ->
        uri.path = args.path
        uri.query = args.query
        headers.Authorization = authHeader
        response.success = { resp, json ->
            parsedResponse = json
        }
        response.failure = { resp ->
            System.err.println COLOR_RED + prettyPrint(responseAsString(resp)) + COLOR_END
            throw new HttpResponseException(resp.statusLine.statusCode, resp.statusLine.reasonPhrase)
        }
    }
    parsedResponse
}


/***********
* Jenkins 2
************/

    import groovy.transform.Field
    @Field  // module constant
    String REPO_PATH = new File(getClass().protectionDomain.codeSource.location.path).parentFile.parent

    def outLog (msg) {
        if (jenkinsWorkflowScript) {
            jenkinsWorkflowScript.invokeMethod 'echo', [msg] as Object[]
        } else {
            System.out.println msg
        }
    }

    javax.net.ssl.SSLException: java.lang.RuntimeException: Could not generate DH keypair.
    -> passer en Java 8


/*******************************
* Linter with Gradle + CodeNarc
********************************/

    apply plugin: 'groovy'
    apply plugin: 'codenarc'

    repositories {
        jcenter()
        maven {
            name = 'repo.jenkins-ci.org'
            url = 'http://repo.jenkins-ci.org/public/'
        }
    }

    codenarc {
        configFile = file('codenarc_rules.groovy')
    }

    dependencies {
        compile 'org.codehaus.groovy:groovy-all:2.4.7'
        compile 'org.eclipse.hudson.main:hudson-core:3.0.0-M2'
        compile group: 'org.jenkins-ci.plugins.workflow', name: 'workflow-step-api', version: '2.7', ext: 'jar'
    }

    sourceSets {
        main {
            groovy {
                srcDirs = ['src/', 'vars/']
            }
        }
    }
