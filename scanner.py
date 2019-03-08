#coding: utf8
__author__ = "郭 璞"
__email__ = "marksinoberg@gmail.com"

import redis
import time
import random

class Scanner(object):

    def __init__(self, host, port, db):
        self.host = host
        self.port = port
        self.db = db
        self.redisclient = redis.StrictRedis(host=host, port=port, db=db)

    def scan_keys(self, count=1000, output="./scankeys.txt"):
        with open(output, "a") as file:
            offset, sequence = self.redisclient.scan(0, count=count)
            print(offset, sequence)
            file.writelines([item.decode("utf8") + str("\n") for item in sequence])
            while offset != 0:
                print(offset, sequence)
                offset, sequence = self.redisclient.scan(offset, count=count)
            file.close()

    def _get_size(self, key):
        # try ... catch No Such Key.
        ret = self.redisclient.execute_command("DEBUG OBJECT", key)
        print(ret)

    def _get_ttls(self, keys=[]):
        # 此应该为较为底层的方法，输入输出无关
        ret = []
        if keys is not []:
            pipe = self.redisclient.pipeline()
            for key in keys:
                pipe.ttl(key)
            ret = pipe.execute()
        return ret

    def merge(self, input="./scankeys.txt", output="./without_ttl.txt"):
        with open(input, "r") as rfile:
            # 即便是成千上万个key，也不会占过多内存，直接读所有的即可
            keys = rfile.readlines()
            rfile.close()
        if keys is not []:
            with open(output, "a") as wfile:
                offset, length = 0, 1000
                while offset < len(keys):
                    keyslice = keys[offset:length]
                    wfile.writelines([str(item) + "\n" for item in self._get_ttls(keyslice)])
                    offset += length
                wfile.close()
        print("merge done.")

if __name__ == "__main__":
    scanner = Scanner("localhost", 6379, 0)
    # scanner.scan_keys(10)
    # scanner._get_size("set")
    # scanner._get_ttls(["name", "set", "age"])
    scanner.merge()



