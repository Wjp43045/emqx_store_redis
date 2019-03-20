# emqx_store_redis
Use redis to store emqx messages to mysql.

If you have a better solution, please write in the issues, thank you.

Subscribing to the stored message scheme requires two services to be enabled: emq_sub.py and emq_redis_store.py.

emq_redis_store.py turns on the timing service, periodically checks whether there is data writing in redis. If data has been written, switch the data table, retrieve the data and write it to mysql, and delete the data in this table.
