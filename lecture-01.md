# Setup C-Sharp Dev Env

- %15(c#)/%15(c#,c++,js,java)/%70 essay style (all open books, walk in the park...)
- Assignments seem to be quite programming heavy! Yay! 
- 2 lecturers, Xingfeng and Manu, first six weeks purely online.

## Steps on accessing a web site
*RTT, Rount Trip Time*
- RT for client to establish a connection, service creates a connection and responds via "you can use this connection".
- RT for client to send a HTTP request, server to generate HTTP response.

The entire process involves times spent
= DNS resolving web server's name to IP (if necessary??)
- Client to setup TCP connection
- Request transmitted from client to server
- Web server to parse request and generate response
- Response transmitted from server to client
	- All response data
- Client to then react to request response

### How to reduce time
- Network latency, physical proximity
- Smaller payloads, given bandwidth...
- Reduce load on web server
	- generate response faster
- Proxy server / caching server
	- a proxy server normally caches web content. But web content can be cached on other types of servers as well (??)

_First assignment to implement some of these techniques_

#### Web Cache
Server that sits between client and pure server. Client strictly requests from caching server, which forwards any requests for resources it doesn't have.

Note, client agnostic, cache warming simply depends on generalised traffic. Physical location of caching server obviously important.

Ooooh seems to be generalised locale wise, can be completely local. (client side caching). Albeit then loosing generalised traffic caching.

~double check what network latency actually is, idle time of requests?~ [Nice 5min video here comparing bandwidth and latency](https://www.youtube.com/watch?v=YgBOT3bWukg). Simply how long it takes for a message to reach it's destination.

TODO
- [ ] C-Sharp crash course
[crash course, progress is 0%](https://www.youtube.com/watch?v=GhQdlIFylQ8)
- [ ] C-Sharp dev env 

Update, we could try to use some sort of codegen tool, like go2cs 😁😇...

Second covered benefit is reduced server load, obvious.

#### Categories of web caching
- client side caching, calls to question valid cache

_need to look at the difference here!_

from point of view of server, forward meaning closer to the client
- forward proxy servers (improve request serving speed, also for authorization)
- reverse proxy servers (reduce server load)

Interesting, so lecturer describes the reality of the web, where we'd actually have may different layers of caching, this phenomenon is called hierarchical caching. Each cache servers many clients, or other caches.

Heirarchical because if a request at each stage is not met before, in such a fashion the request would be escalated. Until handled by the origin server.

Cooperative caching, being that of asking peers, rather than parents for resources.

cons: suffers from a lot of increased inter-cache comms
pros: further reduce origin server retrievals
