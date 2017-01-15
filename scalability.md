# Notes on scalability

* The first golden rule for scalability: every server contains exactly the
  same codebase and does not store any user-related data, like sessions or
  profile pictures, on local disc or memory. [lecloud1]
* Sessions need to be stored in a centralized data store which is accessible
  to all your application servers. It can be an external database or an
  external persistent cache, like Redis. An external persistent cache will
  have better performance than an external database.


## What to do when your database is the bottleneck?

There are two options [lecloud2]:

1. Go with your current relational database:

   - master-slave replication (read from slaves, write to master)
   - upgrade your master server by adding RAM
   - sharding
   - denormalization
   - SQL tuning
2. Search for alternative database systems depending on your use case. Be
   aware that you might end up to do inner joins in your application code and
   that would make your application slower. You can solve this problem by
   introducing a cache layer.


## Caching

[lecloud3]

* A cache is a simple key-value store and it should reside as a buffering
  layer between your application and your data storage.
* Never do file-based caching, it makes cloning and auto-scaling of your
  servers just a pain.


### Caching techniques

#### Caching database queries

* Whenever you do a query to your database, you store the result dataset in
  cache. A hashed version of your query is the cache key.
* This pattern has several issues: The main issue is the expiration.

#### Caching objects

* Let your class assemble a dataset from your database and then store the
  complete instance of the class or the assembed dataset in the cache.
* Some ideas of objects to cache:
  - user sessions (never use the database!)
  - fully rendered blog articles
  - activity streams
  - user<->friend relationships

---

#### Resources

* [lecloud1] http://www.lecloud.net/post/7295452622/scalability-for-dummies-part-1-clones
* [lecloud2] http://www.lecloud.net/post/7994751381/scalability-for-dummies-part-2-database
* [lecloud3] http://www.lecloud.net/post/9246290032/scalability-for-dummies-part-3-cache
