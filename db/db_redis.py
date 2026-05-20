import redis
#from utils.log import Logger

#LOG = Logger("RedisDB")

class RedisDB:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def hset_one(self, db, key, value):
        self.client.hset(db, key, value)
        
    def hset_dict(self, db, dicts, subDB=None):
        for k, v in dicts.items():
            if subDB:
                k = f"{subDB}.{k}"
            self.hset_one(db, k, v)

    def hset_all(self, db, data):
        self.client.hset(db, mapping=data)

    def hget_all(self, db):
        byte_data = self.client.hgetall(db)
        return {k.decode(): v.decode() for k,v in byte_data.items()}
    
    def hget_one(self, db, feild):
        return self.client.hget(db, feild).decode()

    def hscan_section(self, db, section):
        cursor, byte_data = self.client.hscan(db, match=f"{section}.*")
        return {k.decode(): v.decode() for k,v in byte_data.items()}

    def db_size(self):
        return self.client.dbsize()
