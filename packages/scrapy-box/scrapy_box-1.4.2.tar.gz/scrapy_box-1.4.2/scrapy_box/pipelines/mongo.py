"""
@Description: 
@Usage: 
@Author: liuxianglong
@Date: 2021/9/2 下午4:12
"""
import logging
from pymongo import MongoClient
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)


class MongoBatchInsertPipeline:
    def __init__(self, mongo_client, mongo_db, mongo_collection, mongo_insert_size):
        self.data = list()
        self.insert_size = mongo_insert_size
        self.mongo_cli = mongo_client
        self.mongo_table = self.mongo_cli[mongo_db][mongo_collection]

    @classmethod
    def from_crawler(cls, crawler):
        addr = crawler.settings.get('MONGO_ADDR')
        username = crawler.settings.get('MONGO_USERNAME')
        password = crawler.settings.get('MONGO_PASSWORD')
        db = crawler.settings.get('MONGO_DB')
        collection = crawler.settings.get('MONGO_COLLECTION')
        insert_size = crawler.settings.get('MONGO_INSERT_SIZE', 100)

        if db is None or collection is None or addr is None:
            raise NotConfigured

        client = MongoClient(addr)
        client.admin.authenticate(username, password)

        return cls(client, db, collection, insert_size)

    def _process_item(self, item):
        """return item or None"""
        return dict(item)

    def process_item(self, item, spider):
        """ 批量插入数据库 """
        if self._process_item(item):
            self.data.append(item)

        if len(self.data) >= self.insert_size:
            logger.info(f'批量插入 {len(self.data)}条 数据到MongoDB')
            self.mongo_table.insert_many(self.data)
            logger.info('批量插入成功')
            self.data.clear()

        return item

    def close_spider(self, spider):
        """ 关闭爬虫，处理最后的数据 """
        if len(self.data) > 0:
            logger.info(f'批量插入 {len(self.data)}条 数据到MongoDB')
            self.mongo_table.insert_many(self.data)
            logger.info('批量插入成功')
            self.data.clear()

        self.mongo_cli.close()

