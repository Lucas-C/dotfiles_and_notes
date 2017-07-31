Continuous Delivery
===================

## References
- [Immutable Server](http://martinfowler.com/bliki/ImmutableServer.html) pattern
- [Best practices for writing Dockerfiles](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)
- [Continuous Delivery with Containers](http://www.slideshare.net/dbryant_uk/oreillynginx-2016-continuous-delivery-with-containers-the-trials-and-tribulations)
- [Building a Functional Puppet Workflow](http://garylarizza.com/blog/2014/02/17/puppet-workflow-part-1/)
- [AnsibleVSSaltVSStackStorm](https://medium.com/@anthonypjshaw/ansible-v-s-salt-saltstack-v-s-stackstorm-3d8f57149368)

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

## Jenkins
- Jenkins 2 with Jenkinsfile & Docker compose
- Best practice: write a simple documentation page for your pipeline, indicating steps already working fine and the ones you wish
- Plugins: AnsiColor, ChuckNorris, InternetMeme, Pipeline, ShiningPanda, jenkins.sitespeed.io, ThinBackup
- Global Security Authorization: special user "authenticated"

```
cd ~/.jenkins/jobs/$job/workspace  # Also useful to backup/check: ~/.jenkins/jobs/$job/config.xml
PATH=$PATH:~/.jenkins/tools/jenkins.plugins.nodejs.tools.NodeJSInstallation/NodeJs_6.2.1/bin/
PATH=$PATH:~/.jenkins/tools/hudson.tasks.Maven_MavenInstallation/maven3/bin/
source /appl/usljksu1/.jenkins/shiningpanda/jobs/17bf94c9/virtualenvs/d41d8cd9/bin/activate
export LD_LIBRARY_PATH=/appl/usljksu1/.jenkins/shiningpanda/jobs/17bf94c9/virtualenvs/d41d8cd9/lib
```

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


## Docker
- cf. [Best practices for writing Dockerfiles]
- [`clair`](https://github.com/coreos/clair) : Vulnerability Static Analysis for Containers
- use the Calico network plugin for Docker instead of the native Docker "overlay" : https://www.percona.com/blog/2016/08/03/testing-docker-multi-host-network-performance/
- [Docker image dissection](http://blog.jeduncan.com/docker-image-dissection.html=) : its tarballs all the way down !

```
docker run --read-only ... # CONTAINERS ARE NOT IMMUTABLE BY DEFAULT ! If you need tmp files, use --tmpfs /tmp (since 1.10)
if [ -n "$DOCKER_MACHINE_NAME" ]; then  # %HOME%\.bashrc for Docker Toolbox which source it twice: the following is only evaluated on the 2nd pass
    source .../.bashrc
    PATH="$PATH:/.../Docker Toolbox"  # required in case of a custom installation path
    cd ...
fi
<INSERT> # paste under MinGW / Git Bash
```

`daemon.json`: defaults to `%programdata%\docker\config\daemon.json` / `/etc/docker/daemon.json`

### Security
https://www.nccgroup.trust/us/our-research/understanding-and-hardening-linux-containers/
https://benchmarks.cisecurity.org/tools2/docker/CIS_Docker_1.12.0_Benchmark_v1.0.0.pdf

### Cygwin support
winpty: https://github.com/rprichard/winpty/issues/64

    winpty docker exec -i -t 11e68e488021 /bin/bash


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
