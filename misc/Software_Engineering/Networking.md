Networking
==========

::: toc
[[toc]]
:::

101 : https://github.com/espadrine/Solve-Data-In-Code/blob/master/misc/network.md

## Windows

SmartSniff : http://www.nirsoft.net/utils/smsniff.html

Example, to watch Elasticsearch native Java protocol traffic:

    include:both:tcp:9300

## HTTP
- to check if a page exists without downloading it: use an HEAD request OR use an Etag + "If-None-Match" request -> HTTP 404 Not modified
- [URI Templates](http://www.rfcreader.com/#rfc6570) : http://example.com/{term:3}/search{?q,lang}
- HTTP server push solutions (cf. RFC 6202 " Known Issues and Best Practices for the Use of Long Polling and Streaming in Bidirectional HTTP") :
    * HTTP Long-Polling: Tte connection is held open until the server has new information
    * Streaming: the connection is held open and new pieces of information can be pushed over that existing connection, from server to client, without the connection being closed and re-opened as it is with HTTP Long-Polling
    * HTTP/2 Server Push: these are known as "pushed responses" and the browser may cache these
    * WebSockets: Full bi-directional and full duplex communication over a single TCP connection within a web browser (or any web client)
- [Timing HTTP requests with curl & ab](http://overloaded.io/timing-http-requests-curl)
    $ ab -n 10 http://my.json/service | grep -F 'Time per request:'
    Time per request:       0.861 [ms] (mean)
    $ boom -n 10 http://my.json/service # Python package

### SOP

Techniques for Bypassing the Single Origin Policy
- CORS : beware of the wildcard !
- JSONP (JSON with Padding) : either (1) ensure that a JSONP request never returns sensitive data, or (2) use another mechanism in place of cookies (e.g., secret tokens) to authorize the request
- The document.domain property relaxation:  2 documents from distinct origins communicate by setting their domain properties to a common value
- PostMessage/ReceiveMessage browser API : "it is the responsibility of the receiving document to additionally check the srcOrigin parameter to ensure that the message is coming from a trustworthy document."

## TCP
- reception acknowledged, packets ordered
- TCP's congestion avoidance algorithm causes the sender to reduce its sending rate by a factor of two when it sees a packet loss.
- Symetrically, it tries to improve the rate by performing, on packets ACK, addititive increases of the number of unacknowledged packets that are sent over the network.
- TCP starts with a slow rate, but ramp up quickly. It also sleeps for Xms between sends.

Pb de latence rencontré -> dû au TCP Segementation offload: https://forum.ivorde.com/linux-tso-tcp-segmentation-offload-what-it-means-and-how-to-enable-disable-it-t19721.html
    /sbin/ethtool -K eth0 tso off

John Nagle, author of the tinigram prevention aka Nagle algorithm, recommendation: always set TCP_QUICKACK (from: https://news.ycombinator.com/item?id=10608356) _

> For 'send`, although the documentation for the call indicates that the return value (if positive) is the "number of [bytes] sent", this is just plain wrong.
> All that the return value tells you is the number of bytes that the TCP stack in your underlying OS accepted into its outgoing buffer.
> After this point, the OS will try its best to deliver those bytes to the recipient that you initially made a connection with. But this may never happen,
> so it does not mean you can count on those bytes being sent!
FROM: http://stackoverflow.com/a/10269715/636849

## UDP
- no reception check, packets unordered, faster
- faster than TCP, better for voice over IP, video streaming

## DNS
- use UDP protocol, but can fall back to TCP

Also cf. **software_defined_networking.md**

## Other protocols
- [SCTP](http://en.wikipedia.org/wiki/Stream_Control_Transmission_Protocol)
- [Tsunami](http://tsunami-udp.sourceforge.net) : A fast user-space file transfer protocol that uses TCP control and UDP data
for transfer over very high speed long distance networks (≥ 1 Gbps and even 10 GE), designed to provide more throughput than possible with TCP over the same networks.
Includes FTP-like client and server command line applications for normal file transfers.
[Used at AWS](https://aws.amazon.com/fr/blogs/big-data/moving-big-data-into-the-cloud-with-tsunami-udp/)

## Monitoring tools
Cacti, Smokeping
