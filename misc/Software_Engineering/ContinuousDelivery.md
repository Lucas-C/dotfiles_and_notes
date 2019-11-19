Continuous Delivery
===================

::: toc
[[toc]]
:::

## References
- [Immutable Server](http://martinfowler.com/bliki/ImmutableServer.html) pattern
- [Best practices for writing Dockerfiles](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)
- [Continuous Delivery with Containers](http://www.slideshare.net/dbryant_uk/oreillynginx-2016-continuous-delivery-with-containers-the-trials-and-tribulations)
- [Building a Functional Puppet Workflow](http://garylarizza.com/blog/2014/02/17/puppet-workflow-part-1/)
- [AnsibleVSSaltVSStackStorm](https://medium.com/@anthonypjshaw/ansible-v-s-salt-saltstack-v-s-stackstorm-3d8f57149368)
- [Containers patterns](https://l0rd.github.io/containerspatterns/#1)
- [Using curl and the UNIX socket to talk to the Docker API](https://nathanleclaire.com/blog/2015/11/12/using-curl-and-the-unix-socket-to-talk-to-the-docker-api/)
- [Inspecting docker activity with socat](https://developers.redhat.com/blog/2015/02/25/inspecting-docker-activity-with-socat/)
- [How To Write Excellent Dockerfiles](https://rock-it.pl/how-to-write-excellent-dockerfiles/)
- [Container Training](https://github.com/jpetazzo/container.training)
- [Multi-stages Docker images](https://blog.hasura.io/how-to-write-dockerfiles-for-python-web-apps-6d173842ae1d#d0a8)

## general tips & tricks
Waiting on a HTTP service to be up:

    wget --waitretry=5 --retry-connrefused -T 60 -O - $ENDPOINT

## Git workflow
- [TrunkBasedDevelopment](https://trunkbaseddevelopment.com) > Gitflow
- very similar to [OneFlow](http://endoflineblog.com/oneflow-a-git-branching-model-and-workflow)

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

API JSON: `$JENKINS_URL/api/json?depth=1&pretty=true`

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

### Credentials
Retrieving an encrypted secret value from `credentials.xml` -> in Groovy script window: (tip from https://stackoverflow.com/a/37683492/636849 )

    println( hudson.util.Secret.decrypt("${ENCRYPTED_PASSPHRASE_OR_PASSWORD}") )

Revealing a crendential in a pipeline:

    withCredentials([string(credentialsId: 'credentialsId', variable: 'TOKEN_ID')]) {
        sh "bash -c 'echo \${TOKEN_ID:0:1}\${TOKEN_ID:1:-1}'"
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


## Docker
- cf. [Best practices for writing Dockerfiles], [How To Write Excellent Dockerfiles], [Containers patterns]:
  * No update instructions alone in the Dockerfile + Download packages securely using GPG
  * Use gosu instead of sudo wherever possible
- [Multi-stages Docker images]: use standard image for build, but alpine on for exec: `COPY --from=dependencies`
- [`clair`](https://github.com/coreos/clair) : Vulnerability Static Analysis for Containers - Also: [Anchore](https://github.com/anchore/anchore-engine)
- use the Calico network plugin for Docker instead of the native Docker "overlay" : https://www.percona.com/blog/2016/08/03/testing-docker-multi-host-network-performance/
- [Docker image dissection](http://blog.jeduncan.com/docker-image-dissection.html=) : its tarballs all the way down !
- http://blog.michaelhamrah.com/2014/06/accessing-the-docker-host-server-within-a-container/ - Alt: `docker.for.win.localhost` builtin DNS CNAME (or `host.docker.internal`)
- [dive](https://github.com/wagoodman/dive) : A tool for exploring a docker image, layer contents, and discovering ways to shrink your Docker image size.

```
docker run --read-only ... # CONTAINERS ARE NOT IMMUTABLE BY DEFAULT ! If you need tmp files, use --tmpfs /tmp (since 1.10)
```

`daemon.json`: defaults to `/etc/docker/daemon.json`

Docker daemon healthcheck: curl http://localhost:2375/v1.25/info

### Container build best practices

_cf._ Hesperides & VBoard

- 2-stages builds
- `envsubst` from package `gettext` - Alt with jinja2: https://stackoverflow.com/a/35009576/636849
- support `$JAVA_OPTS`
- `HEALTHCHECK`
- Maven dependencies caching : [`mvn dependency:go-offline`](https://medium.com/@nieldw/caching-maven-dependencies-in-a-docker-build-dca6ca7ad612)

### Inspecting Docker labels / image hashes / secrets

    docker inspect --format $'{{ range $k, $v := .Config.Labels }}{{$k}}={{$v}}\n{{ end }}' $container_id  # Unix-only because of $'...' format
    docker container inspect --format '{{.NetworkSettings.IPAddress}}' $container_id
    docker container inspect --format '{{json .NetworkSettings.Networks}}' $container_id

Listing running containers with their labels:

    docker ps --format "table {{.ID}}\t{{.Labels}}"

Listing labels of an image:

    docker inspect --format "{{.ContainerConfig.Labels}}" $img_name

Listing secrets used by services:

    docker service inspect $service_name --format="{{ range .Spec.TaskTemplate.ContainerSpec.Secrets }}{{ json . }}{{ println }}{{ end }}"
    docker service inspect $service_name --format="{{ range .PreviousSpec.TaskTemplate.ContainerSpec.Secrets }}{{ json . }}{{ println }}{{ end }}"

Getting Docker images used by a service, with its sha256 hash :

    docker service inspect $service_name --format="{{ .Spec.TaskTemplate.ContainerSpec.Image }}"

Display full error message with `docker service` : `--no-trunc`

### Docker remote REST API
- through `dockerd` CLI option: `-H tcp://0.0.0.0:2375` (takes priority over 2nd option below)
- through `daemon.json` list entry `hosts` (not tested)
- [Using curl and the UNIX socket to talk to the Docker API]
- [Inspecting docker activity with socat]
- [Connecting to the secure Docker port using curl](https://docs.docker.com/engine/security/https/#connecting-to-the-secure-docker-port-using-curl) with certificates

cf. [bin/docker_api.sh](https://github.com/Lucas-C/dotfiles_and_notes/blob/master/bin/docker_api.sh) :

    export DOCKER_HOST=...
    docker_api.sh /tasks?filters=$(echo '{"id": ["'$task_id'"]}' | urlencode) | jq '.[]|{ID,Status,CreatedAt,UpdatedAt}'
    docker_api.sh "/events?since=$(date -d 2018-06-26T15:38:00 +%s)&until=$(date +%s)" > events.log

### Docker containers health

Container health status log:

    docker inspect $container_id | jq '.[].State.Health'
    docker events --filter event=health_status

### Docker for Windows
`daemon.json`: defaults to `%programdata%\docker\config\daemon.json`

Logs: `%programdata%\docker\service*.txt`

Windows services:
```
sc query vmms
sc query com.docker.service
sc start com.docker.service
sc stop  com.docker.service
```

Command executed by the Docker For Windows installer to add the current user to the `docker-users` group:
```
net.exe localgroup docker-users GROUPEVSC\lucas_cimonn /add
```

Checking if Hyper-V is enabled:
```
dism /Online /Get-FeatureInfo /FeatureName:Microsoft-Hyper-V-All
```

Exploring the host VM (e.g. MobyLinuxVM) - Using privileged Alpine chroot (cf. https://github.com/gbraad/hostenter ) :
```
docker run --net=host --ipc=host --uts=host --pid=host -it --security-opt=seccomp=unconfined --privileged --rm -v /:/host alpine /bin/sh
```


#### Docker for Windows current quirks / major limitations / known bugs

- convert paths to unix "slash" format with a `/host_mnt` prefix
- ["." shorthand directory mounted volumes are not supported](https://github.com/docker/for-win/issues/1080)
- fail silently to mount volume if there is an [existing non empty directory](https://github.com/moby/moby/issues/20127)
The [docs](https://docs.docker.com/engine/reference/builder/#usage) explicitely mentions it:
> When using Windows-based containers, the destination of a volume inside the container must be one of: a non-existing or empty directory & a drive other than C
- whenever you change your password (at least when using an AD account), you **must** re-share your drives in Docker settings
- [Docker does not release disk space after deleting all images and containers](https://github.com/docker/for-win/issues/244#issuecomment-432242993):
to shrink `MobyLinuxVM.vhdx`, move the "Disk image location" to another location in Docker settings "Advanced menu".

### docker stack

    # Workaround, cf. https://github.com/moby/moby/issues/31101#issuecomment-365316698
    python yaml_merge.py docker-stack.yml docker-stack.branch.yml > docker-stack.${BRANCH_NAME}.yml
    docker --debug stack deploy -c docker-stack.${BRANCH_NAME}.yml api-system-${BRANCH_NAME}
    # service update --force required -> cf. https://github.com/moby/moby/issues/31357#issuecomment-359363903
    docker --debug service update api-system-${BRANCH_NAME}_web --force

#### Current major limitations / known bugs

- sometimes: `Error response from daemon: rpc error: code = 2 desc = update out of sequence`
Solution: redepoy - cf. https://github.com/moby/moby/issues/30794
- ~~no support for YAML files merging: https://github.com/moby/moby/issues/31101~~
  * implemented since 17.11.0-dev : https://github.com/docker/cli/commit/1872bd8
- does not support relative paths (under Windows at least), contrary to `docker-compose`
- does not currently support `host` network, e.g. giving access to localhost to services, cf. https://github.com/docker/swarmkit/issues/989

### Docker exec shell

    curl https://raw.githubusercontent.com/Lucas-C/dotfiles_and_notes/master/.inputrc > ~/.inputrc
    curl https://raw.githubusercontent.com/Lucas-C/dotfiles_and_notes/master/.vimrc > ~/.vimrc
    alias vim='TERM= vim'  # explanation: https://github.com/moby/moby/issues/13817#issuecomment-254088147

### FAQ

#### mounting <Windows path> to rootfs .../merged at ... caused "not a directory"

If you have recently changed your Windows password, this is very likely the reason.
Then you need to "Reset credentials" in Docker Settings "Shared Drives" tab, cf. https://github.com/moby/moby/issues/26822#issuecomment-340354240

Egalement utile : FAQ sur la gestion des permissions avec les _shared drives_ : https://docs.docker.com/docker-for-windows/troubleshoot/#verify-domain-user-has-permissions-for-shared-drives-volumes

#### Failed to connect to the database open \\.\pipe\dockerDataBase: The system cannot find the file specified.

Docker restarted

#### [SambaShare][Error] Unable to mount D drive: W.X.Y.Z open

Appears in `%programdata%\docker\service*.txt`

Open ticket: https://github.com/docker/for-win/issues/1555

#### Thin pool issues

    docker rm $(docker ps -qf status=exited)
    docker rmi $(docker images -qf dangling=true)  # dangling == untagged images that are the leaves of the images tree
    docker volume rm $(docker volume ls -qf dangling=true)  # dangling == untagged images that are the leaves of the images tree

    docker info  # -> provide thin pool ID, e.g. docker-thinpool
    sudo dmsetup status docker-thinpool
    sudo dmsetup info docker-thinpool
    lsblk
    lvs -a  # for direct-lvm thin pool

    # Will only work id disk supports TRIM: hdparm -I /dev/...
    docker ps -qa | xargs docker inspect --format='{{ .State.Pid }}' | grep -v '^0$' | xargs -IZ fstrim /proc/Z/root/

    # Since v1.13.0
    docker system prune -a
    docker container prune -f
    docker image prune -a -f

In case of:

> Non existing device docker-thinpool

Then:

    vgchange -Kay

#### FileNotFoundError: [WinError 3] Le chemin d’accès spécifié est introuvable: - Failed to execute script docker-compose

If the file in question has a very long path, you are very likely hitting the Windows limit of 260 characters in filepaths.

Curiously, this only happens with `docker-compose`, not with the `docker` command


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
