University: Georgia Tech

### Overview Part 1: Preparing for SDN [5 mins]

###  Overview Part 2: Course Overview: Background, and what you will learn in this course [5 mins]

What is a SDN ?

- control network behaviour from single high-level control program
- separate infrastructure in 2 parts:
    * control plane: the network "brain", can be run separately from devices, compute logic of how traffic will be forwarded
    * data plane: typically programmable hardware

Distributed configuration can be buggy & unpredicatble.
Instead, we want to control the network from a logically centralized high-level program

- 2004: Routing Control Platforms
- 2005: 4D architecture: Decisions > Dissemination > Discovery > Data
- 2008: OpenFlow : communications protocol giving access to the forwarding plane of a network switch or router over the network.

Advantages -> easier to: coordinate behavior of network devices, evolve, reason about, apply conventional computer science approaches

Applications: data centers, wide-area backbone networks, enterprise & home networks, Internet exchange points

### Pre-Assesment Quiz takeaways
All the following are true about Classless Interdomain Routing (CIDR):

- CIDR slowed the rate of Internet routing table growth because prefixes no longer had to be allocated in fixed-size blocks.
- In an Internet forwarding table with CIDR, there can only be multiple matching entry for any given IP address.
- The prefix length for a CIDR prefix can be anywhere in the range from 0 to 32 bits.

All the following are true about how DNS lookups:

- An MX-record query for a DNS lookup will return a list of host names of mail exchange servers accepting incoming mail for that domain.
- A DNS A-record query for google.com can (and will) return multiple IP addresses at a time.
- An NS-record query for a DNS lookup will return the name(s) of the authoritative name server(s) for that domain.

All of the following are true about traffic control with BGP:

- A network operator can use the BGP local preference attribute to control outbound traffic from his or her AS to a destination.
- A network operator can use BGP AS path prepending to control inbound traffic from his or her AS to a destination.

The network layer has only a single protocol in widespread use today, representing what we call the narrow waist.

All of the following are not true about packet switching:

- Traffic running over a packet-switched network between two endpoints will never be dropped by intermediate nodes along the path.
- Traffic running over a packet-switched network between two endpoints will always experience predictable latency.
- A user of a packet switched network might occasionally get a busy signal if there are too many users on the network.
- Once a connection is established between two endpoints in a packet switched network, the end-to-end route cannot change, or the connection must be re-established.

All of the following are true about 802.11 wireless medium access control:

- Carrier sense multiple access with collision avoidance (CSMA/CA) is a network multiple access method in which carrier sensing is used, but nodes attempt to avoid collisions by transmitting only when the channel is sensed to be "idle". When they do transmit, nodes transmit their packet data in its entirety.
- It is particularly important for wireless networks, where the collision detection of the alternative CSMA/CD is unreliable due to the hidden node problem.
- CSMA/CA can optionally be supplemented by the exchange of a Request to Send (RTS) packet sent by the sender S, and a Clear to Send (CTS) packet sent by the intended receiver R. Thus alerting all nodes within range of the sender, receiver or both, to not transmit for the duration of the main transmission. This is known as the IEEE 802.11 RTS/CTS exchange. It reduces the overall achieveable throughput of the wireless network. Implementation of RTS/CTS helps to partially solve the hidden node problem that is often found in wireless networking

All of the  following are true about TCP:

- TCP's congestion avoidance algorithm causes the sender to reduce its sending rate by a factor of two when it sees a packet loss.
- A TCP sender controls its sending rate by adjusting the number of unacknowledged packets that can be sent over the network at any time.


### Module 2.0: Testing Mininet Setup [16:35]

    sudo mn --topo single,3 --mac --switch ovsk --controller remote
    sudo mn --test pingall --topo single,3
    sudo mn --topo minimal # 2 hosts + 1 switch
    sudo mn --topo linear,4
    sudo mn --topo tree,depth=2,fanout=2

    # Python
    mininet.cli.CLI(network) # to call before network.stop(), invoke the interactive CLI
    network.addLink(bw, delay, max_queue_size, loss)

