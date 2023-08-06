"""
@Description: 
@Usage: 
@Author: liuxianglong
@Date: 2021/9/3 下午11:49
"""
import traceback
import logging
import pymysql
from scrapy.exceptions import NotConfigured
from twisted.enterprise import adbapi
from twisted.internet import defer

logger = logging.getLogger(__name__)


class MysqlBasePipeline(object):
    def __init__(self, host, port, user, password, db, charset, table, update_fixed_fields):
        params = dict(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset=charset,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.table = table
        self.update_fixed_fields = update_fixed_fields
        self.dbpool = adbapi.ConnectionPool('pymysql', **params)

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get('MYSQL_HOST')
        port = crawler.settings.getint('MYSQL_PORT', 3306)
        user = crawler.settings.get('MYSQL_USERNAME')
        password = crawler.settings.get('MYSQL_PASSWORD')
        db = crawler.settings.get('MYSQL_DB')
        charset = crawler.settings.get('MYSQL_CHARSET', 'utf8')
        table = crawler.settings.get('MYSQL_TABLE')
        update_fixed_fields = crawler.settings.get('MYSQL_UPDATE_FIXED_FIELDS')

        if host is None or db is None or table is None:
            raise NotConfigured

        return cls(host, port, user, password, db, charset, table, update_fixed_fields)

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        try:
            yield self.dbpool.runInteraction(self.do_mysql, dict(item))
        except:
            logger.error(traceback.format_exc())

        defer.returnValue(item)

    def do_mysql(self, curson, item):
        """Insert operation or update operation"""


class MysqlInsertPipeline(MysqlBasePipeline):
    def do_mysql(self, cursor, item):
        fields = ','.join(item.keys())
        values = ','.join(('%({})s'.format(k) for k in item.keys()))
        sql = f'insert ignore into {self.table}({fields}) values({values})'
        cursor.execute(sql, item)


class MysqlUpdatePipeline(MysqlBasePipeline):
    def do_mysql(self, cursor, item):
        update_phrase = [f'{name}=%({name})s' for name in item.keys() if name not in self.update_fixed_fields]
        where_phrase = [f'{name}=%({name})s' for name in self.update_fixed_fields]
        update_sql = f'update {self.table} set {",".join(update_phrase)} where {" and ".join(where_phrase)}'
        cursor.execute(update_sql, item)
