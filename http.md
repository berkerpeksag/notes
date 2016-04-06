HTTP is an application layer protocol over TCP, which is over IP.

Establishing a connection between two endpoints is a multi-step process and
involves the following:

1. resolve IP address from host name via DNS
2. establish a connection with the server
3. send a request
4. wait for a response
5. close connection

In HTTP/1.0, all connections were closed after a single transaction. So, if a
client wanted to request three separate images from the same server, it made
three separate connections to the remote host. To reduce
connection-establishment delays, HTTP/1.1 introduced persistent connections,
long-lived connections that stay open until the client closes them.

Persistent connections are default in HTTP/1.1, and making a single transaction
connection requires the client to set the `Connection: close` request header.
This tells the server to close the connection after sending the response.

In addition to persistent connections, browsers/clients also employ
a technique, called parallel connections, to minimize network delays. The
age-old concept of parallel connections involves creating a pool of connections
(generally capped at six connections). If there are six assets that the client
needs to download from a website, the client makes six parallel connections to
download those assets, resulting in a faster turnaround.

The server mostly listens for incoming connections and processes them when it
receives a request. The operations involve:

1. establishing a socket to start listening on port 80 (or some other port)
2. receiving the request and parsing the message
3. processing the response
4. setting response headers
5. sending the response to the client
6. close the connection if a `Connection: close` request header was found

Cookies allow the server to attach arbitrary information for outgoing responses
via the `Set-Cookie` response header.

HTTP does support a rudimentary form of authentication called Basic
Authentication, as well as the more secure Digest Authentication.

In Basic Authentication,

1. The server initially denies the client's request with a `WWW-Authenticate`
   response header and a `401 Unauthorized` status code.
2. On seeing this header, the browser displays a login dialog, prompting for a
   username and password.
3. This information is sent in a base-64 encoded format in the `Authentication`
   request header.
4. The server can now validate the request and allow access if the credentials
   are valid.

Digest Authentication is similar to Basic and uses the same handshake technique
with the `WWW-Authenticate` and `Authorization` headers, but Digest uses a more
secure hashing function to encrypt the username and password (commonly with MD5
or KD digest functions).

Just as you need ID cards to show your identity, a web server needs a digital
certificate to identify itself. Certificates (or "certs") are issued by
a Certificate Authority (CA) and vouch for your identity on the web. The CAs
are the guardians of the PKI (Public-Key Infrastructure).

The most common form of certificates is the X.509 v3 standard, which contains
information, such as:

* the certificate issuer
* the algorithm used for the certificate
* the subject name or organization for whom this cert is created
* the public key information for the subject
* the Certification Authority Signature, using the specified signing algorithm

When a client makes a request over HTTPS, it first tries to locate
a certificate on the server. If the cert is found, it attempts to verfiy it
against its known list of CAs. If its not one of the listed CAs, it might show
a dialog to the user warning about the website's certficate.

Once the certificate is verified, the SSL handshake is complete and secure
transmission is in effect.

Caches are used at several places in the network infrastructure, from the
browser to the origin server. Depending on where it is located, a cache can be
categorized as:

Private: within a browser, caches usernames, passwords, URLs, browsing history
and web content. They are generally small and specific to a user.  Public:
deployed as caching proxies between the server and client. These are much
larger because they serve multiple users. A common practice is to keep multiple
caching proxies between the client and the origin-server. This helps to serve
frequently accessed content, while still allowing a trip to the server for
infrequently needed content.

Regardless of where a cache is located, the process of maintaining a cache is
quite similar:

1. Receive request message.
2. Parse the URL and headers.
3. Lookup a local copy; otherwise, fetch and store locally
4. Do a freshness check to determine the age of the content in the cache; make
   a request to refresh the content only if necessary.
5. Create the response from the cached body and updated headers.
6. Send the response back to client.
7. Optionally, log the transaction.

If a document hasn't changed, the server should respond with a
`304 Not Modified`.

If the cached copy has expired, it should generate a new response with updated
response headers and return with a `200 OK`.

If the resource is deleted, it should come back with `404 Not Found`.

To keep the cached copy consistent with the server, HTTP provides some simple
mechanisms, namely Document Expiration and Server Revalidation.

HTTP allows an origin-server to attach an expiration date to each document
using the `Cache-Control` and `Expires` response headers. This helps the client
and other cache servers know how long a document is valid and fresh.

`Expires` is an older HTTP/1.0 response header that specifies the value as an
absolute date. This is only useful if the server clocks are in sync with the
client, which is a terrible assumption to make.

`Expires` is less useful compared to the newer `Cache-Control: max-age=<s>`
header introduced in HTTP/1.1. Here, max-age is a relative age, specified in
seconds, from the time the response was created.

Once a cached document expires, the cache must revalidate with the server to
check if the document has changed. This is called server revalidation and
serves as a querying mechanism for the stale-ness of a document.

The revalidation step can be accomplished with two kinds of request-headers:

1. `If-Modified-Since`
2. `If-None-Match`

The former is for date-based validation while the latter uses Entity-Tags
(ETags), a hash of the content.

These headers use date or ETag values obtained from a previous server response.

In case of `If-Modified-Since`, the `Last-Modified` response header is used;
for `If-None-Match`, it is the `ETag` response header.

The validity period for a document should be defined by the server generating
the document. If it's a newspaper website, the homepage should expire after
a day (or sometimes even every hour!). HTTP provides the `Cache-Control` and
`Expires` response headers to set the expiration on documents.

The `Cache-Control` header is far more useful than the `Expires` header and has
a few different values to constrain how clients should be caching the response:

* `Cache-Control: no-cache`: the client is allowed to store the document;
  however, it must revalidate with the server on every request. There is
  a HTTP/1.0 compatibility header called `Pragma: no-cache`, which works the
  same way.
* `Cache-Control: no-store`: this is a stronger directive to the client to not
  store the document at all.
* `Cache-Control: must-revalidate`: this tells the client to bypass its
  freshness calculation and always revalidate with the server. It is not
  allowed to serve the cached response in case the server is unavailaible.
* `Cache-Control: max-age`: this sets a relative expiration time (in seconds)
  from the time the response is generated.

As an aside, if the server does not send any `Cache-Control` headers, the
client is free to use its own heuristic expiration algorithm to determine
freshness.

Cachability is not just limited to the server. It can also be specified from
the client. This allows the client to impose constraints on what it is willing
to accept. This is possible via the same `Cache-Control` header, albeit with
a few different values:

* `Cache-Control: min-fresh=<s>`: the document must be fresh for at least `<s>`
  seconds.
* `Cache-Control: max-stale` or `Cache-Control: max-stale=<s>`: the document
  cannot be served from the cache if it has been stale for longer than `<s>`
  seconds.
* `Cache-Control: max-age=<s>`: the cache cannot return a document that has
  been cached longer than `<s>` seconds.
* `Cache-Control: no-cache` or `Pragma: no-cache`: the client will not accept
  a cached resource unless it has been revalidated.

**Reference:** http://code.tutsplus.com/tutorials/http-the-protocol-every-web-developer-must-know-part-2--net-31155
