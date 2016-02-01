Networking
==========

## REST
(taken from http://spring.io/guides/tutorials/bookmarks/)

![](http://martinfowler.com/articles/images/richardsonMaturityModel/overview.png)

Dr. Leonard Richardson put together a maturity model that interprets various levels of compliance with RESTful principles, and grades them. It describes 4 levels, starting at level 0. Martin Fowler has a very good write-up on the maturity model

- Level 0: the Swamp of POX - at this level, we’re just using HTTP as a transport. You could call SOAP a Level 0 technology. It uses HTTP, but as a transport. It’s worth mentioning that you could also use SOAP on top of something like JMS with no HTTP at all. SOAP, thus, is not RESTful. It’s only just HTTP-aware.
- Level 1: Resources - at this level, a service might use HTTP URIs to distinguish between nouns, or entities, in the system. For example, you might route requests to /customers, /users, etc. XML-RPC is an example of a Level 1 technology: it uses HTTP, and it can use URIs to distinguish endpoints. Ultimately, though, XML-RPC is not RESTful: it’s using HTTP as a transport for something else (remote procedure calls).
- Level 2: HTTP Verbs - this is the level you want to be at. If you do everything wrong with Spring MVC, you’ll probably still end up here. At this level, services take advantage of native HTTP qualities like headers, status codes, distinct URIs, and more. This is where we’ll start our journey.
- Level 3: Hypermedia Controls - This final level is where we’ll strive to be. Hypermedia, as practiced using the HATEOAS ("HATEOAS" is a truly welcome acronym for the mouthful, "Hypermedia as the Engine of Application State") design pattern. Hypermedia promotes service longevity by decoupling the consumer of a service from intimate knowledge of that service’s surface area and topology. It describes REST services. The service can answer questions about what to call, and when. We’ll look at this in depth later.

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

## TCP
- reception acknowledged, packets ordered
- TCP's congestion avoidance algorithm causes the sender to reduce its sending rate by a factor of two when it sees a packet loss.
- Symetrically, it tries to improve the rate by performing, on packets ACK, addititive increases of the number of unacknowledged packets that are sent over the network.
- TCP starts with a slow rate, but ramp up quickly. It also sleeps for Xms between sends.

Pb de latence rencontré -> dû au TCP Segementation offload: https://forum.ivorde.com/linux-tso-tcp-segmentation-offload-what-it-means-and-how-to-enable-disable-it-t19721.html
    /sbin/ethtool -K eth0 tso off

John Nagle, author of the tinigram prevention aka Nagle algorithm, recommendation: always set TCP_QUICKACK (from: https://news.ycombinator.com/item?id=10608356) _

## UDP
- no reception check, packets unordered, faster
- faster than TCP, better for voice over IP, video streaming

## DNS
- use UDP protocol, but can fall back to TCP

Also cf. **software_defined_networking.md**

## Other protocols
- [SCTP](http://en.wikipedia.org/wiki/Stream_Control_Transmission_Protocol)
- [UDP](http://en.wikipedia.org/wiki/UDP-based_Data_Transfer_Protocol)

## Monitoring tools
Cacti, Smokeping
