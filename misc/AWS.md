Limite de roles dans interface web => plugins Chrome / Firefox pour plus de contrôle

## AWS cli snippets

    vim ~/.aws/credentials
    export AWS_PROFILE=
    aws sts get-caller-identity # whoami

    aws codecommit list-repositories
    aws codecommit get-repository --repository-name $repo

    aws ec2 describe-instances --filter Name=tag:Name,Values=$name \
        | jq -r '.Reservations[].Instances[]|.InstanceId,.NetworkInterfaces[].Association.PublicDnsName'

    pip install ssmh  # alt: ssm-sh (Go)
    aws ssm describe-sessions --state Active
    smsh $instance_id

    aws codepipeline get-pipeline-state --name $pipeline | jq ".stageStates[]|select(.stageName=='$stage').actionStates"

    aws s3 ls $bucket
    s3_zip_list () {
        aws s3api get-object --bucket $1 --key $2 tmp.zip
        unzip -l tmp.zip
        rm tmp.zip
    }
    aws s3 cp --recursive $dir s3://$bucket/$path

    aws logs describe-log-groups --log-group-name-prefix /aws/elasticbeanstalk/
    for logStream in $(aws logs describe-log-streams --log-group-name $logGroup | jq -r .logStreams[].logStreamName | dos2unix); do \
        echo $(aws logs get-log-events --log-group-name $logGroup --log-stream-name $logStream | jq -r .events[].message) \
    done > $logGroup-events.log

    aws cognito-identity list-identity-pools --max-results 10
    aws cognito-idp list-user-pools --max-results 10

    lucagrulla/cw: The best way to tail AWS CloudWatch Logs from your terminal

## Architecturing on AWS class notes

AWS Technical Essentials: https://aws.amazon.com/fr/training/course-descriptions/essentials/

AWS Cloud Practionner Essentials: https://aws.amazon.com/fr/training/course-descriptions/cloud-practitioner-essentials/

Architecturing on AWS class slides: https://bookshelf.vitalsource.com

Qwiklabs AWS: https://run.qwiklab.com/catalog?cloud=AWS (1 credit == 1 dollar)

AWS trainings: https://www.aws.training/Training

- architecture Simple (sans SLA -> Best Effort)
- architecture H/A (High Availability) : pas de SLA de run, SLA de retour de service
- architecture F/T (Fault Tolerance) : avec SLA
- architecture scalaire
- architecture transactionnelle (sans serveurs)

TO READ: [AWS Cloud Adoption Framework](https://d1.awsstatic.com/whitepapers/aws_cloud_adoption_framework.pdf)

**Day One with AWS**:
1. stop using the root access
2. require multi-factor auth
3. enable AWS CloudTrail
4. enable full billing report

Then: https://aws.amazon.com/trustedadvisor/

### Module 3: Designing Your Environment
- How do you choose a region ?
- How many AZs should you use ?
- Only-one-VPC, multi-VPC or multi-accounts ?

#### AWS NAT (Network Address TRanslation) 101
VPC = Virtual Private Cloud
- To make a subnet public, it must be routed through an Internet gateway.
- If instances in your private subnets need to send data out to the Internet, you'll need to route traffic to something like a NAT instance (or NAT gateway).
- We further tighten security using security groups.

### Module 4: Making Your Environment Highly Available
> High availability is about ensuring that your application's downtime is minimized as much as possible, without the need for human intervention.

- RTO = Recovery Time Objective (system full recovery time)
- RPO = Recovery Point Objective (acceptable data loss)

### Module 6: Automating Your Infrastructure
Utilisent cloud-init: https://cloudinit.readthedocs.io

Infrastructure As Code = techniques, practices and tools from software development applied to creating reusable, maintainable, extensible and testable infrastructure.

Note on EC2 instances Network Performance: it's always possible to get dedicated, more performant resources
- low / moderate / high -> indicates how close to the underlying switch hotspot is the instance
- multi-tenant VPC
- dedicated host
- dedicated ec2

server vs VM vs instance
CPU vs VCPU vs ECU


## Other notes

There are 4 types of load balancers :

* The old ELB Classic, the historic one, capable of both HTTP(S) and TCP forwarding
* The Network Load Balancer, capable of TCP transparent forwarding and really really really fast…
* The Application Load Balancer, capable of HTTP(S) forwarding.
  If used for HTTPS, always act as a TLS termination proxy/bridge
* The Gateway Load Balancer (end of 2020), works on Layer 3 (IP), capable of deploy, scale, and manage virtual appliances, such as Firewalls, IDS, IPS and DPI systems.

Can perform health checks and decide which backend server can receive traffic

