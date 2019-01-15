# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from datetime import datetime


class HackernewsPipeline(object):
    def process_item(self, item, spider):
        author=item['author'].replace('"','')
        title=item['title'].replace('"','')
        content=item['content'].replace('"','')
        times=item['time'].replace('"','')
        url=item['url'].replace('"','').replace('\\','')

        atime=datetime.strptime(times, "%Y-%m-%d")
        sf = self.is_repeat('fbart',url)
        if not sf:
            self.insertModel('fbart', [author, title, content, atime, url])

    # 注释为静态方法
    @staticmethod
    def connect():
        return pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='hnnt',
            charset="utf8mb4"
        )

    # 根据表名和插入值，插入单条到数据库
    def insertModel(self, table, article):
        con = self.connect()
        cur = con.cursor()
        try:
            rowlist = self.getTableRows(table)
            sql = 'insert into ' + table + '(' + rowlist + ')'
            sql = sql + ' values(%s,%s,%s,%s,%s)'
            cur.execute(sql, article)
        except Exception as e:
            con.rollback()
            print(u'执行'+sql+'\n'+article+'\n'+u'语句时报错，%s'%(e))
            raise
        finally:
            cur.close()
            con.commit()
            con.close()

    # 根据表名和值获取singe数据,有值返回真，无返回假
    def is_repeat(self,table,value):
        result=False
        con = self.connect()
        cur = con.cursor()
        rowsql = "select * from %s  where url='%s'" % (table,value)
        cur.execute(rowsql)
        rows = cur.fetchall()
        cur.close()
        con.close()
        if rows:
            result=True

        return result

    # 获取表中字段名
    def getTableRows(self, table):
        con = self.connect()
        # 通过获取到的数据库连接con下的cursor()方法来创建游标
        cur = con.cursor()
        rowsql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'" % (table)
        cur.execute(rowsql)
        rows = cur.fetchall()
        cur.close()
        con.close()
        ro = ','.join((row[0] for row in rows))
        key = self.get_key(table)
        # 表主键存在则截掉主键
        if key:
            sj = ro.replace(key+',', '')
        return sj

    # 获取表的主键
    def get_key(self, table):
        con = self.connect()
        # 通过获取到的数据库连接con下的cursor()方法来创建游标
        cur = con.cursor()
        rowsql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME='%s'" % (table)
        cur.execute(rowsql)
        rows = cur.fetchall()
        cur.close()
        con.close()
        ro = ','.join((row[0] for row in rows))
        return ro
