# -*- coding:utf-8 -*-
 
import MySQLdb
import time

class Mysql:

    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))
    
    #数据库初始化
    def __init__(self):
        try:
            print('开始连接数据库')
            self.db = MySQLdb.connect('localhost','root','james890526','AHDB')
            self.db.set_character_set('utf8')
            self.cur = self.db.cursor()
            print('连接数据库成功')
        except MySQLdb.Error,e:
             print self.getCurrentTime(),"连接数据库错误，原因%d: %s" % (e.args[0], e.args[1])

    def createTable(self, tableName, columnList):
        titleStr = ''
        for item in columnList:
            titleStr += (item+' varchar(128),')

        titleStr += '店铺的名称'+' varchar(40)'

        sql = 'create table if not exists ' + tableName + ('(%s)' % titleStr) + ' ENGINE=InnoDB  DEFAULT CHARSET=utf8'

        try:
            result = self.cur.execute(sql)
            self.db.commit()

            if result:
                print('执行成功')
            else:
                print(result)
                return 0
        except MySQLdb.Error,e:
            print(e)
            pass
 
    #插入数据
    def insertData(self, table, columns, my_list):
         try:

             # self.db.set_character_set('utf8')
             cols = ', '.join(columns)
             # sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, '"'+values+'"')
             s = '' 
             for i, v in enumerate(columns):
                if i == len(columns)-1:
                    s += '%s'
                else: 
                    s += '%s,'
             sql = "INSERT INTO %s VALUES (%s)" % (table, s)
            
             try:
                insert2db = []
                for i in my_list:
                    t = tuple(i)
                    insert2db.append(t)

                print(len(columns))

                print(len(insert2db[0]))
                result = self.cur.executemany(sql, insert2db)
                self.db.commit()
                if result:
                    print('执行成功')
                else:
                    print('执行失败')

                print(result)
                return 0
             except MySQLdb.Error,e:
                #发生错误时回滚
                self.db.rollback()
                #主键唯一，无法插入
                if "key 'PRIMARY'" in e.args[1]:
                    print self.getCurrentTime(),"数据已存在，未插入数据"
                else:
                    print self.getCurrentTime(),"插入数据失败，原因 %d: %s" % (e.args[0], e.args[1])
         except MySQLdb.Error,e:
             print self.getCurrentTime(),"数据库错误，原因%d: %s" % (e.args[0], e.args[1])



 