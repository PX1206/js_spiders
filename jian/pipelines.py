# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class JianPipeline:
#     def process_item(self, item, spider):
#         return item

import pymysql
from pymysql import cursors
from twisted.enterprise import adbapi


class JSPipeLine(object):
    def __init__(self):
        dbparams = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "px123456",
            "database": "jianshu",
            "charset": "utf8",
            "cursorclass": cursors.DictCursor
        }
        # self.conn = pymysql.connect(**dbparams)
        # self.cursor = self.conn.cursor()  # 这里要记住
        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparams)
        self._sql = None

    # def process_item(self, item, spider):
    #     self.cursor.execute(self.sql, (item["title"], item["auther"], item["article"], item["avatar"], item["article_id"], item["time_out"], item["read_number"]))
    #     # self.conn.commit()
    #     return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            replace into js(id, title, auther, article, avatar, article_id, time_out, read_number, meta_title, meta_keywords, meta_description) values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            return self._sql
        return self._sql

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (
        item["title"], item["auther"], item["article"], item["avatar"], item["article_id"], item["time_out"],
        item["read_number"], item["meta_title"], item["meta_keywords"], item["meta_description"]))

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def handle_error(self, error, item, spider):
        print("*"*60)
        print("出错啦")
        print(item)
        print(error)
        print("*"*60)
