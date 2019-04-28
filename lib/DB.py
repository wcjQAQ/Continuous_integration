import pymysql
import traceback
class MySQL(object):
    def __init__(self, host, port, user, passwd, db):
        self.__host = str(host)
        self.__port = int(port)
        self.__user = str(user)
        self.__passwd = str(passwd)
        self.__db = str(db)

    def insert(self, sql):
        connect = pymysql.connect(host=self.__host, port=self.__port, user=self.__user, passwd=self.__passwd, database=self.__db, charset='utf8')
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            connect.commit()
        except:
            connect.rollback()
        finally:
            connect.close()

    def update(self, sql):
        connect = pymysql.connect(host=self.__host, port=self.__port, user=self.__user, passwd=self.__passwd, database=self.__db, charset='utf8')
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            connect.commit()
        except:
            connect.rollback()
        finally:
            connect.close()

    def existence(self, sql):
        connect = pymysql.connect(host=self.__host, port=self.__port, user=self.__user, passwd=self.__passwd, database=self.__db, charset='utf8')
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                return True
            else:
                return False
        except:
            print('haha')

    def select(self, sql):
        connect = pymysql.connect(host=self.__host, port=self.__port, user=self.__user, passwd=self.__passwd, database=self.__db, charset='utf8')
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            restfuls = cursor.fetchall()
            return list(restfuls)
        except:
            return False