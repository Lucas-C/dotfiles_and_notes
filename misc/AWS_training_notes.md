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
