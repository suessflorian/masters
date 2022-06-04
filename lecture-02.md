# CDN (content delivery/distribution network)
Network of _edge servers_ (said to be physically located at edges, different locations). Each server is supposedly close to.

Forward proxy, decides which is the closest edge server to forward incoming request.

## Potential Problems
- stale data relative to origin server (not ideal if origin resource changes a lot)
- edge server inconsistency
- appealing when cache hits occur, gravely slower when cache miss
- cannot accomodate all resources

_lecturer sites sensitive resources should not be stored in caches._

# Dynamic Data Page (aka Dynamic content)
Supposedly what we're going to be looking at for a bit.

- generated output depends on data
- generated on demand
- considered volatile, frequent change between client w/ some variation + changes are unpredictable. 
- considered expensive to create relative to static page

I think this is quite dependant on focusing on server side rendering. Has this lecturer thought about client side rendering

### Proxy-based dynamic page caching
Three tiers
1. page level
2. fragment level
3. data-centric level

**Page level** - each page, simply cached

Pros: Clearly this reduces page generation time the most of all methods, reduces packet filter(?!) and firewall-related delays (compared to others). Opportunity to reduce bandwidth required for transmission (how?! By depending on downstream cache servers?, this specific for origin servers?).

Cons: Often inapplicable due to data dependant page generation. One users page cannot be reused for another user. (Re-usability problem). If a particular item in a page, the entire page gets invalidated.

**Fragment level** - each page, factored into fragments
Requires a _template file_ for each dynamic page. Each fragment it's own cacheable resource. Web page is assembled on proxy caching server. Akamai as part of Edge Side Includes (ESI) initiative.

# Describing the template (ESI implementation)
Extension to HTML - ESI is a markup language that is used to describe how different cached fragments should fit together to rebuild the requested page.

[Lecture gave additional resource](https://docs.oracle.com/cd/B14099_19/caching.1012/b14046/esi.htm)

```
<html>
	<body>
		<esi:include src=http://example.com/weather.jsp />
		<esi:include src=http://example.com/weather.jsp />
		<esi:include src=http://example.com/weather.jsp />
	</body>
</html>
```

Pros: Obviously fragments have a tendency to be more re-usable (improves hit rate). Granular cache-ability tuning of fragments (expiring and cache-ability). 

Cons: Who tf uses ESI. Additional work incorporating this into template files. 

## Data-centric caching
Focuses on the contents of the data being transmitted. Usually carried out of underlying mechanism not requiring concious cooperation with page authors.

Two methods:
# 1. Value-based web caching
Breaks up a page in blocks (how?), diffs previously served pages with current served pages and diffs them to see the changes that are required to be sent to the client.

## Sub concept: Message Digest
Some sort of hashing function? Used as salts to compare messages, ie, different messages have different digests.

So each page is broken into blocks, ~2KB, each block is digested (MD5) and it's fingerprint is determined by that message digest.

- blocks are identical IFF fingerprints match

_lecture stops around here, missed delta encoding, lecturer explains we will using this set of principals in the first assignment!! Next lecture we will look a little more at implementations..._

2. Delta encoding
