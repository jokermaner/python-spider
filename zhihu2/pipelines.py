# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import binascii

from scrapy.conf import settings
import pymongo

from scrapy.conf import settings
import pymongo
import socket
import struct


class Zhihu2Pipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']

        # hosts = binascii.hexlify(host).decode()
        # hostss =int(socket.inet_aton(hosts).decode('hex'),16)
        # ports =int(socket.inet_aton(port).decode('hex'),16)
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host =host,port=int(port))
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        zhihu = dict(item)
        self.post.insert(zhihu)
        return item
