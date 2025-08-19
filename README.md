# MongoDB-sharding-demo

This project shows how to do setup a local MongoDB cluster using Docker.
I will be using MongoDB version 5.0.31, but of course you can use a newer one.
Just make sure that you use the correct documentation version.
At the time of writing this MongoDB version 8 is the latest.

## Important note

To make our lives easier, I added a configuration files where you can have the
different configurations for each server without having to do much in each
Docker compose file. Changes to the Docker files are minimal.

> Sadly, when testing it, Docker compose did not recognized the config files,
> forcing me to set the config in the commands.
> I've left the files for reference. 

## Config servers

1. Start config servers (3 member replica set)

```bash
docker compose -f config/docker-compose.yaml up -d
```

2. Connect to mongod

```bash
mongosh mongodb://localhost:40000
```

3. Initiate replica set

```js
rs.initiate({
    _id: "cfgrs",
    configsvr: true,
    members: [
      { _id : 0, host : "cfgsvr1:27019" },
      { _id : 1, host : "cfgsvr2:27019" },
      { _id : 2, host : "cfgsvr3:27019" }
    ]
  }
)

rs.status()
```

## Shard 1 servers

1. Start shard 1 servers (3 member replicas set)

```bash
docker compose -f shard1/docker-compose.yaml up -d
```

2. Connect mongod in shard1

```bash
mongo mongodb://localhost:50000
```

3. Initiate replica set

```js
rs.initiate(
  {
    _id: "shard1rs",
    members: [
      { _id : 0, host : "shard1svr1:27018" },
      { _id : 1, host : "shard1svr2:27018" },
      { _id : 2, host : "shard1svr3:27018" }
    ]
  }
)

rs.status()
```

## Shard 2 servers

This second shard is optional but it shows how a second replica set can be
configured and added as well.

1. Start shard 2 servers (3 member replicas set)

```bash
docker compose -f shard2/docker-compose.yaml up -d
```

2. Connect mongod in shard2

```bash
mongo mongodb://localhost:50003
```

3. Initiate replica set

```js
rs.initiate(
  {
    _id: "shard2rs",
    members: [
      { _id : 0, host : "shard2svr1:27018" },
      { _id : 1, host : "shard2svr2:27018" },
      { _id : 2, host : "shard2svr3:27018" }
    ]
  }
)

rs.status()
```

## Add shards to the cluster

Adding the shards to a cluster is the last thing you do.

1. Start mongos server

```bash
docker compose -f mongos/docker-compose.yaml up -d
```

2. Connect to mongos

```bash
mongo mongodb://localhost:60000
```

3. Add shards

```bash
mongos> sh.addShard("shard1rs/localhost:50000,localhost:50001,localhost:50002")
mongos> sh.addShard("shard2rs/localhost:50003,localhost:50004,localhost:50005")
mongos> sh.status()
```

## Testing

1. Run `python3 mongo-test.py` to insert, read and delete data from the
   configured cluster.

## Resources

* [Sharding a MongoDB Collection](https://www.youtube.com/watch?v=Rwg26U0Zs1o)
* [MongoDB Sharding on Ubuntu](https://www.youtube.com/watch?v=aBaD0qHK1as&list=PLIRAZAlr4cfY1gugVw2enf6uVXyJaWwwv)
* [Github sharing demo](https://github.com/justmeandopensource/learn-mongodb/blob/master/sharding/)
* [MongoDB restart cluster](https://www.mongodb.com/docs/v5.0/tutorial/restart-sharded-cluster/)
* [Expiring Data in MongoDB](https://www.mongodb.com/docs/v5.0/tutorial/expire-data/)
* [MongoDB docs - Deploy shard cluster](https://www.mongodb.com/docs/v5.0/tutorial/deploy-shard-cluster/)
* [Adding keyfile to a sharded cluster](https://www.mongodb.com/docs/v5.0/tutorial/deploy-sharded-cluster-with-keyfile-access-control/)
* [Configuring TLS/SSL](https://www.mongodb.com/docs/v5.0/tutorial/configure-ssl/)
* [FIPS mode setup](https://www.mongodb.com/docs/v5.0/tutorial/configure-fips/)
