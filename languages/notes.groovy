
/***********
* Jenkins 2
************/

    import groovy.transform.Field
    @Field  // module constant
    String REPO_PATH = new File(getClass().protectionDomain.codeSource.location.path).parentFile.parent


/*******************************
* Linter with Gradle + CodeNarc
********************************/

    apply plugin: 'groovy'
    apply plugin: 'codenarc'

    repositories {
        jcenter()
    }

    codenarc {
        configFile = new File('codenarc_rules.groovy')
    }

    dependencies {
        compile 'org.codehaus.groovy:groovy-all:2.4.7'
        compile 'org.eclipse.hudson.main:hudson-core:3.0.0-M2'
        // Currently broken; cf. https://issues.jenkins-ci.org/browse/JENKINS-41441
        //compile 'org.jenkins-ci.plugins.workflow:workflow-step-api:2.7'
    }

    sourceSets {
        main {
            groovy {
                srcDirs = ['.']
            }
        }
    }
