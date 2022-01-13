Docker & orchestrators
======================

::: toc
[[toc]]
:::

## References
- [Container Training](https://github.com/jpetazzo/container.training) : workshops, tutorials, and training sessions around the themes of Docker, containers, and orchestration
- [Best practices for writing Dockerfiles](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)
- [Containers patterns](https://l0rd.github.io/containerspatterns/#1)
- [Using curl and the UNIX socket to talk to the Docker API](https://nathanleclaire.com/blog/2015/11/12/using-curl-and-the-unix-socket-to-talk-to-the-docker-api/)
- [Inspecting docker activity with socat](https://developers.redhat.com/blog/2015/02/25/inspecting-docker-activity-with-socat/)
- [How To Write Excellent Dockerfiles](https://rock-it.pl/how-to-write-excellent-dockerfiles/)
- [Multi-stages Docker images](https://blog.hasura.io/how-to-write-dockerfiles-for-python-web-apps-6d173842ae1d#d0a8)
- [Faster CI Builds with Docker Layer Caching and BuildKit](https://testdriven.io/blog/faster-ci-builds-with-docker-cache/)
- [GoogleContainerTools/distroless](https://github.com/GoogleContainerTools/distroless/)
- [Caching Maven dependencies in a Docker build](https://medium.com/@nieldw/caching-maven-dependencies-in-a-docker-build-dca6ca7ad612)
- [Creating Efficient Docker Images with Spring Boot 2.3](https://spring.io/blog/2020/08/14/creating-efficient-docker-images-with-spring-boot-2-3)
- [Checkov: cloud infrastructure configuration scanner](https://www.checkov.io): CLI to analyze IaC: Terraform, CloudFormation, Kubernetes, Helm, ARM Templates and Serverless framework


## Docker
- cf. [Best practices for writing Dockerfiles], [How To Write Excellent Dockerfiles], [Containers patterns]:
  * No update instructions alone in the Dockerfile + Download packages securely using GPG
  * Use gosu instead of sudo wherever possible
- [Multi-stages Docker images]: use standard image for build, but alpine on for exec: `COPY --from=dependencies`
- [`clair`](https://github.com/coreos/clair) : Vulnerability Static Analysis for Containers
  Also: [Anchore](https://github.com/anchore/anchore-engine) - [trivy](https://github.com/aquasecurity/trivy#comparison-with-other-scanners)
- use the Calico network plugin for Docker instead of the native Docker "overlay" : https://www.percona.com/blog/2016/08/03/testing-docker-multi-host-network-performance/
- [Docker image dissection](http://blog.jeduncan.com/docker-image-dissection.html=) : its tarballs all the way down !
- http://blog.michaelhamrah.com/2014/06/accessing-the-docker-host-server-within-a-container/ - Alt: `docker.for.win.localhost` builtin DNS CNAME (or `host.docker.internal`)
- [dive](https://github.com/wagoodman/dive) : A tool for exploring a docker image, layer contents, and discovering ways to shrink your Docker image size. Quick alternative to run in an image:

    wget https://dev.yorhel.nl/download/ncdu-linux-x86_64-1.15.1.tar.gz
    tar xzvf ncdu-linux-x86_64-1.15.1.tar.gz
    ./ncdu /

- [hadolint](https://github.com/hadolint/hadolint) : Dockerfile linter in Haskell
- [skopeo](https://github.com/containers/skopeo) : CLI to inspect images without pulling them, and also perform copy/delete/sync operations
- [google/cadvisor](https://github.com/google/cadvisor) : Container Advisor provides information on resource usage and performances of running containers. It is a running daemon that collects, aggregates & exports metrics.
- [LocalStack](https://github.com/localstack/localstack) : a fully functional local AWS cloud stack & easy-to-use test/mocking framework, using Docker & Python - Alt for lambdas: AWS SAM (Serverless Application Model)

```
docker run --read-only ... # CONTAINERS ARE NOT IMMUTABLE BY DEFAULT ! If you need tmp files, use --tmpfs /tmp (since 1.10)
```

`daemon.json`: defaults to `/etc/docker/daemon.json`

Docker daemon healthcheck: curl http://localhost:2375/v1.25/info

### Container build best practices

_cf._ Hesperides & VBoard

- [Multi-stages Docker images]
- `envsubst` from package `gettext` - Alt with jinja2: https://stackoverflow.com/a/35009576/636849
- `HEALTHCHECK`
- [GoogleContainerTools/distroless]
- [Faster CI Builds with Docker Layer Caching and BuildKit]

For Java apps:
- support `$JAVA_OPTS`
- Maven dependencies caching : `mvn dependency:go-offline` (_cf._ [Caching Maven dependencies in a Docker build])
- Spring Boot layered JARs, _cf._ [Creating Efficient Docker Images with Spring Boot 2.3]

#### Healthcheck without curl nor wget

    #!/bin/bash
    check_http() {
      set -e
      # Read and write to TCP socket through the 3rd file handle
      exec 3<> /dev/tcp/127.0.0.1/8081
      # HTTP 101: Send the tinyest correct HTTP Request
      printf "GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n" >&3
      read -r result <&3
      echo "${result}"|grep 200
    }
    # timeout http_check after 1 min
    if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
       timeout 60 bash -c "source ${0} && check_http"
    fi


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

    curl --unix-socket /var/run/docker.sock http://localhost/containers/json  # or http://localhost/v1.35/containers/json
    curl --unix-socket /var/run/docker.sock http://localhost/images/json
    curl --unix-socket /var/run/docker.sock http://localhost/events

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
sc query vmms &:: Hyper-V
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


#### Troubleshooting
_cf._ https://docs.docker.com/docker-for-windows/troubleshoot/

    docker-machine ls &:: if none found, you may want to: docker-machine create --driver hyperv default
    "C:\Program Files\Docker\Docker\resources\com.docker.diagnose.exe" gather

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

### Pulling a Docker image from AWS ECR

    export DEFAULT_AWS_REGION=eu-west-1
    export ECR_ENDPOINT=$AWS_ACCOUNT_ID.dkr.ecr.$DEFAULT_AWS_REGION.amazonaws.com
    export AWS_PROFILE=...
    export IMAGE=hesperides/hesperides
    aws ecr describe-images --repository-name $IMAGE --query "sort_by(imageDetails,& imagePushedAt)[*]"
    aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_ENDPOINT
    docker pull $ECR_ENDPOINT/$IMAGE:$TAG

Bonus, with `skopeo`:

    aws ecr get-login-password | skopeo login --username AWS --password-stdin $ECR_ENDPOINT
    skopeo inspect docker://$ECR_ENDPOINT/$IMAGE:$TAG

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

#### Cannot start service XXX: b'driver failed programming external connectivity on endpoint YYY: Error starting userland proxy: /forwards/expose/port returned unexpected status: 500'
_cf._ https://github.com/docker/for-win/issues/2722

Find the process using the blocking port with PowerShell: `Get-Process -Id (Get-NetTCPConnection -LocalPort <port>).OwningProcess`

If killing it fails, and also "Reset to factory defauls" and "sc stop/start com.docker.service/vmms" services, try:

     netcfg -d &:: then restart Windows


### Security
https://www.nccgroup.trust/us/our-research/understanding-and-hardening-linux-containers/
https://benchmarks.cisecurity.org/tools2/docker/CIS_Docker_1.12.0_Benchmark_v1.0.0.pdf

### Cygwin support
winpty: https://github.com/rprichard/winpty/issues/64

    winpty docker exec -i -t 11e68e488021 /bin/bash


## k8s

- [Kubernetes Cheat Sheet (PDF)](https://linuxacademy.com/site-content/uploads/2019/04/Kubernetes-Cheat-Sheet_07182019.pdf)
- [kubectl-neat](https://github.com/itaysk/kubectl-neat) : Remove clutter from Kubernetes manifests to make them more readable
- [Graceful shutdown and zero downtime deployments](https://learnk8s.io/graceful-shutdown)

> Instead of immediately shutting down your Pods, you should consider waiting a little bit longer in your application or set up a preStop hook.

    NS=...  # k8s namespace
    kubectl -n $NS api-resources
    kubectl -n $NS get deployments/event/pods/services          # liste les entités du cluster
    kubectl -n $NS get rs -o wide                               # liste les ReplicaSets
    kubectl -n $NS describe pod $pod                            # état détaillé d'un pod
    kubectl -n $NS describe deployment ...
    kubectl -n $NS logs -f $pod
    kubectl -n $NS exec -it $pod sh
    kubectl -n $NS rollout restart deployment/usl-demo-project  # relance un déploiement
    kubectl -n $NS scale deploy usl-demo-project --replicas=0   # supprime toutes les replicas d'un déploiement
    kubectl cluster-info
    # --debug -v9
    k8s-show-ns $NS
    # Quickly launching an interactive shell:
    kubectl run tmp-shell --restart=Never --rm -i --tty --image centos -- /bin/bash

Pour tester que l'appli est "UP", et qu'elle répond bien aux requêtes HTTP,
vous pouvez créer un proxy jusqu'à un pod et ainsi la requêter :

    kubectl -n $NS port-forward usl-demo-project-X-Y 80:8080  # $locallyExposedPort:$containerPort

La durée de vie du proxy est celle de cette commande `kubectl port-forward`.
Tant que ce processus s'exécute, vous pouvez accéder à votre appli :

    curl http://127.0.0.1:80/manage/health

Ce type de proxy sert uniquement à faire des tests.
En production, il faudra mettre en place [un NodePort ou un LoadBalancer](https://www.ovh.com/blog/getting-external-traffic-into-kubernetes-clusterip-nodeport-loadbalancer-and-ingress/).

[k9s](https://github.com/derailed/k9s) : CLI to make it easier to navigate, observe and manage your applications in the wild
Useful shortcuts:
- `CTRL+D` : delete a resource
- `SHIFT+F` : launch _port-forward_. `:pf` to list all active ones

With AWS:

    aws --profile $AWS_PROFILE sts get-caller-identity
    aws eks --profile $AWS_PROFILE --region=$AWS_REGION list-clusters
    aws eks --profile $AWS_PROFILE --region=$AWS_REGION update-kubeconfig --name $AWS_EKS_CLUSTER --alias $AWS_EKS_CONTEXT  # this cmd updates ~/.kube/config

With osprey:

    echo -e "${USERNAME}\n${PASSWORD}" | osprey user login --group $ONPREMS_EKS_CONTEXT # this cmd updates ~/.kube/config

- an app / container can write in `/dev/termination-log` on failure to help diagnosing the failure cause

Installing `ingress-nginx` with Docker for Windows:

* https://stackoverflow.com/a/65219093/636849
* https://stackoverflow.com/a/62713105/636849

Debugging `ingress-nginx`:

    nginx=$(kubectl get pods -n ingress-nginx | egrep -o '^ingress-nginx-controller-[a-zA-Z0-9]+-[a-zA-Z0-9]+ ')
    kubectl logs -n ingress-nginx $nginx --follow
    kubectl exec -n ingress-nginx $nginx -- cat /etc/nginx/nginx.conf

### Hands-on

https://github.com/nocquidant/hello-trainee

    kubectl config use-context docker-desktop
    kubectl run hello-trainee --image nocquidant/hello-trainee
    kubectl expose --port 80 --target-port 8488 pod/hello-trainee --type=NodePort --name hello-trainee-svc
    kubectl get all
    PORT=$(kubectl get service hello-trainee-svc -o jsonpath="{.spec.ports[0].nodePort}")
    curl localhost:$PORT/hello


## helm

    helm --kube-context $AWS_EKS_CONTEXT --namespace $AWS_EKS_NAMESPACE list
    helm --kube-context $AWS_EKS_CONTEXT --namespace $AWS_EKS_NAMESPACE upgrade --install --render-subchart-notes --atomic --timeout ${HELM_TIMEOUT} --values ./values/aws.yaml --set tag=$TAG $PROJECT --debug .
    helm --kube-context $AWS_EKS_CONTEXT --namespace $AWS_EKS_NAMESPACE list

