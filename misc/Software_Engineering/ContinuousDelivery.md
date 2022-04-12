Continuous Delivery
===================

::: toc
[[toc]]
:::

## References
- [AWS: Going faster with continuous delivery](https://aws.amazon.com/fr/builders-library/going-faster-with-continuous-delivery/)
- [Reproducible builds](https://reproducible-builds.org)
- [Immutable Server by Martin Fowler](http://martinfowler.com/bliki/ImmutableServer.html) pattern
- [Continuous Delivery with Containers](http://www.slideshare.net/dbryant_uk/oreillynginx-2016-continuous-delivery-with-containers-the-trials-and-tribulations) (2016)
- [Building a Functional Puppet Workflow](http://garylarizza.com/blog/2014/02/17/puppet-workflow-part-1/)
- [AnsibleVSSaltVSStackStorm](https://medium.com/@anthonypjshaw/ansible-v-s-salt-saltstack-v-s-stackstorm-3d8f57149368)
- [PhoenixServer](https://martinfowler.com/bliki/PhoenixServer.html)

## Principles
* [PhoenixServer] by Martin Fowler:
> The primary advantage of using phoenix servers is to avoid **configuration drift**: ad hoc changes to a systems configuration that go unrecorded.

## General tips & tricks
Waiting on a HTTP service to be up:

    wget --waitretry=5 --retry-connrefused -T 60 -O - $ENDPOINT

## Deployment automation & orchestration
From __fle__ @ AFPY barcamp, Ansible is a good compromise between Fabric, Salt & Puppet: simple & configurable enough + not to "dev-oriented" (cf. also omniti-labs/ansible-dk)
[AnsibleVSSaltVSStackStorm]:
- "Ansible is simple, which is a major strength", it "works by connecting to a server using SSH, copies the Python code over, executes it and then removes itself".
"Ansible Tower is the Enterprise version, it turns the command line Ansible into a service, with a web interface, scheduler and notification system."
"you can’t have long-running tasks."
- "StackStorm is designed as a highly-configurable if-this-then-that service. it can react to events and then run a simple command or a complex workflow."
"MongoDB can be scaled using well-documented patterns." "StackStorm extensibility system is a key strength." "If StackStorm were a programming language, it would be strongly typed."
- "Salt was born as a distributed remote execution system used to execute commands and query data on remote nodes."
"Ultra high-performance for large deployments." (LinkedIn use it)

## Travis
- `travis_retry`: https://github.com/travis-ci/travis-build/tree/master/lib/travis/build/bash
- a build script example using wine: https://github.com/spesmilo/electrum/blob/master/contrib/build-wine/prepare-wine.sh

## Buildbot
Jenkins alternative, in Python: https://buildbot.net

## Jenkins
History:
- 2004 : Projet Hudson
- 2011 : Fork Jenkins
- 2013 :Jenkins is victorious
- 2016 : Jenkins v2 (by Cloudbees) with Jenkinsfile

Notes:
- fan-in / fan-out pattern: [Using Workflow to Deliver a Multi-Component/App Pipeline](https://www.cloudbees.com/blog/using-workflow-deliver-multi-componentapp-pipeline)
- Best practice: write a simple documentation page for your pipeline, indicating steps already working fine and the ones you wish
- Plugins: AnsiColor, ChuckNorris, InternetMeme, Pipeline, ShiningPanda, jenkins.sitespeed.io, ThinBackup
- Global Security Authorization: special user "authenticated"
- [Top 10 Best Practices for Jenkins Pipeline Plugin ](https://www.cloudbees.com/blog/top-10-best-practices-jenkins-pipeline-plugin) by CloudBees. Includes:
  * Do: All material work within a `node`
  * Do: Work you can within a parallel step & Acquire nodes within parallel steps
  * Don’t: Use input within a node block & Wrap your inputs in a timeout

```
cd ~/.jenkins/jobs/$job/workspace  # Also useful to backup/check: ~/.jenkins/jobs/$job/config.xml
PATH=$PATH:~/.jenkins/tools/jenkins.plugins.nodejs.tools.NodeJSInstallation/NodeJs_6.2.1/bin/
PATH=$PATH:~/.jenkins/tools/hudson.tasks.Maven_MavenInstallation/maven3/bin/
source /appl/usljksu1/.jenkins/shiningpanda/jobs/17bf94c9/virtualenvs/d41d8cd9/bin/activate
export LD_LIBRARY_PATH=/appl/usljksu1/.jenkins/shiningpanda/jobs/17bf94c9/virtualenvs/d41d8cd9/lib
```

Get plugins versions from `/script` console:
```
Jenkins.instance.pluginManager.plugins.each{
  plugin ->
    println ("${plugin.getDisplayName()} (${plugin.getShortName()}): ${plugin.getVersion()}")
}
```

Jenkinsfile linter (`$API_TOKEN` can be retrieved from `$JENKINS_URL/user/$USER_NAME/configure`):
```
curl --verbose $JENKINS_URL/job/$JOB_NAME/1/replay/checkScriptCompile --user "$USER_NAME:$API_TOKEN" --data-urlencode value@Jenkinsfile
```

Equivalent of `docker.image($img).inside($args) {}` in CLI: (cf. https://github.com/jenkinsci/docker-workflow-plugin/blob/master/src/main/resources/org/jenkinsci/plugins/docker/workflow/Docker.groovy )
```
docker run -it -w $PWD -v $PWD:$PWD $args $img sh script.sh
```

### HTTP API
* described at `$JENKINS_URL/api/` - Example in JSON: `$JENKINS_URL/api/json?depth=1&pretty=true`
* permissions details: https://www.jenkins.io/doc/book/security/access-control/permissions/
* basic curl to display version as HTTP header: `curl -vL --user $USERNAME:$TOKEN $JENKINS_URL -o /dev/null`
* Java CLI: `java -jar jenkins-cli.jar -s $JENKINS_URL -auth $USERNAME:$TOKEN -webSocket` (download JAR from `$JENKINS_URL/jnlpJars/jenkins-cli.jar`)
* Python lib: https://jenkinsapi.readthedocs.io/en/latest/index.html
  Example usage: https://github.com/Lucas-C/dotfiles_and_notes/blob/master/languages/python/jenkins.py
  Tuto to crawl jobs: https://chezsoi.org/lucas/blog/using-python-requests-futures-to-crawl-all-jobs-on-a-jenkins-4-times-faster.html


### Credentials
Retrieving an encrypted secret value from `credentials.xml` -> in Groovy script window: (tip from https://stackoverflow.com/a/37683492/636849 )

    println( hudson.util.Secret.decrypt("${ENCRYPTED_PASSPHRASE_OR_PASSWORD}") )

Revealing a credential in a pipeline:

    withCredentials([string(credentialsId: 'credentialsId', variable: 'TOKEN_ID')]) {
        sh "bash -c 'echo \${TOKEN_ID:0:1} \${TOKEN_ID:1}'"
    }
    withCredentials([usernamePassword(credentialsId: 'credentialsId', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
        sh "bash -c 'echo \${USERNAME:0:1} \${USERNAME:1}'"
        sh "bash -c 'echo \${PASSWORD:0:1} \${PASSWORD:1}'"
    }

Listing all credentials:

    import com.cloudbees.plugins.credentials.common.StandardUsernameCredentials
    import com.cloudbees.plugins.credentials.CredentialsProvider
    def creds = CredentialsProvider.lookupCredentials(StandardUsernameCredentials.class, Jenkins.instance, null, null)
    for (c in creds) {
        println(String.format("id=%s desc=%s scope=%s", c.id, c.description, c.scope))
    }

### Pipeline Shared Libs

https://github.com/jenkinsci/workflow-cps-global-lib-plugin
Uni testing with Spock: https://github.com/macg33zr/pipelineUnit

    import org.jenkinsci.plugins.workflow.steps.FlowInterruptedException
    import hudson.AbortException


    def call(Map args=[:], Closure closure) {
        def abortResult = args.get('abortResult', 'ABORTED')
        try {
            closure()
        } catch (org.jenkinsci.plugins.workflow.steps.FlowInterruptedException fie) {
            // this ambiguous condition means a user probably aborted
            if (fie.causes.size() == 0 || fie.causes[0].shortDescription.contains('Rejected by')) {
                echo fie.causes[0].shortDescription
                currentBuild.result = abortResult
            } else {
                fail(fie, args.hipchatRoomName, args.notificationEmail)
            }
        } catch (hudson.AbortException ae) {
            // this ambiguous condition means during a shell step, user probably aborted
            if (ae.message.contains('script returned exit code 143')) {
                currentBuild.result = abortResult
            } else {
                fail(ae, args.hipchatRoomName, args.notificationEmail)
            }
        } catch (Exception e) {
            fail(e, args.hipchatRoomName, args.notificationEmail)
        }
    }

    def fail(Exception exception, hipchatRoomName, notificationEmail) {
        echo 'Build FAILED'
        currentBuild.result = 'FAILED'
        node {
            if (hipchatRoomName) {
                hipchatSend(color: 'RED',
                            message: "Build ${currentBuild.result}: Job <a href=\"${env.BUILD_URL}\">${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>",
                            room: hipchatRoomName,
                            notify: true)
            }
            if (notificationEmail) {
                sendMail(notificationEmail)
            }
        }
        throw exception
    }

    def sendMail(notificationEmail=null) {
        def subject = "${currentBuild.result}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
        def details = """<p>${currentBuild.result}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
        <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>"""
        emailext(to: notificationEmail, subject: subject, body: details, recipientProviders: [[$class: 'DevelopersRecipientProvider']])
    }


## Puppet
> "Puppet runs completely synchronously, but the order in which it applies resources is essentially unpredictable in the absence of declared resource relationships.  That's very different from asynchronous operation, which would mean that Puppet applies multiple resources concurrently (i.e. via threads or multiple child processes), which it absolutely does not do"

cf. [Building a Functional Puppet Workflow]

```
puppet apply --debug --verbose [--graph]  # graphs are generated in /var/lib/puppet/state/graphs by default
dot -Tsvg $dot_graph -o ${dot_graph%*.dot}.svg  # >>> PNG-export, as it did not handle fonts correctly under Cygwin - Alt: dot -Tx11 $dot_graph for a terminal display
!! future parser
puppetlabs-stdlib
$content = inline_template("...Hurrah ! Ruby code !...")
notify { "var: ${var}": }
```

["Evaluation Error: Error while evaluating a Function Call, Cannot allocate memory" when executing external Ruby commands in Puppet](https://support.puppet.com/hc/en-us/articles/360005992274--Evaluation-Error-Error-while-evaluating-a-Function-Call-Cannot-allocate-memory-when-executing-external-Ruby-commands-in-Puppet-Enterprise-2018-1-0-and-later)
> If you're getting a Cannot allocate memory error in puppetserver.log or in the output of a Puppet run, you might need to remove backticks from external commands in your Ruby functions.


## OpenStack
```
neutron subnet-list

/var/lib/heat-config/hooks/puppet < cd59c0ef-4929-40d5-a30f-5c3ab7cdc660.json
facter # -> all variables available
rm /var/run/heat-config/deployed/* && os-refresh-config # -> redownload & re-execute Puppet hooks
/var/log/cloud-init-output.log

# History of executed JSONs
cd /var/run/heat-config/deployed && grep -F '(heat-config) [DEBUG] Running /var/lib/heat-config/hooks/' /var/log/messages | sed 's/^.\+\[\([ 0-9,:-]\+\)\].\+deployed\/\([0-9a-f-]\+\)\.json$/\1 \2/' | while read date time id; do echo -n "$date $time $id "; jq -r .name $id.json; done

os-collect-config
os-apply-config
os-refresh-config
dib-run-parts --list /usr/libexec/os-refresh-config/configure.d
```

## GitHub Actions

Sample pipelines:
- [fpdf2](https://github.com/PyFPDF/fpdf2/blob/master/.github/workflows/continuous-integration-workflow.yml)
- Hesperides [backend](https://github.com/voyages-sncf-technologies/hesperides/blob/master/.github/workflows/ci.yml) & [frontend](https://github.com/voyages-sncf-technologies/hesperides-gui/blob/master/.github/workflows/ci.yml) -> runs 25 BDD scenarios using a browser in 5min!
