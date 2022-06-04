# Peer to peer system
Starting off with a contrast with client-server systems.

## Looking up Data in a p2p system

Naive is a **central index**, (centralized directory model). Has the standard pros (efficiency, low bandwidth, low client storage requirements etc..) and cons (central point of failure, scalability focused problems).

Naively too is a **flooded request model**...
	Summary, peer emits resource request to neighbours, which therego continue to emit the resource request until met with a peer that has said resource.
Pros (peers to only know immediate neighbours, no single point of failure), cons (inneficient search, generating lots of traffic, limited scalability).

**Document routing model**
	Summary, each peer is associated an id. There is a hashing function that takes in file bytes and returns a number in the codomain that inludes the identifiers distributed to the peers. The hashing function essentially maps files to which peer, peer when locating, sends request to peer with least distance to hashed file.
Pros(efficient search, routing information is simplified, some fault tolerance), cons (more convuluted)

## We are going to look at two DRM's
Problems:
- name nodes & objects
- find other nodes 
- split data between nodes
- prevent data from being lost

### CAN (content-addressable network)
- d-dimensional space (cartesian)
- space divided by nodes
- all nodes cover entire space (by partitioning)

- there is a hashing function, that takes in a node identifier and spits out a point for that node to live
- that node **just knows** it's direct neighbours. Defined by which as the nodes that lords the space that overlaps on d-1 dimensions and abuts (lol) on one.
- each node simply polls it's neighbours, and requests it's neighbours to return to it it's neighbours too (this is for fault tolerance)
- each file is hashed onto this d-dimensional space, if `f` is used, we can also use `f'` for increased file redundancy in case of failures.

- now suppose a client connects to a random node, the node checks if it has it, if not it hashes some file identifier which spits out some cartesian vector. We list all neighbours, and we forward the resource request to the neighbour with the smallest euclidian distance to the cartesian vector of the requested resource.

Notes: controlled node leaving, lets some neighbour take liberty of it's space, transfers files etc...
