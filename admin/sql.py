# -*- coding: utf-8 -*-
# @Time    : 2019/11/18 下午4:54
# @Author  : apecode
# @Email   : 1473018671@qq.com
# @File    : sql.py
# @Software: PyCharm

import sqlite3
import os
from datetime import datetime

# 获取db的路径
def get_path():
    if os.path.abspath(".").split("/")[-1] == "ShoppingSystem":
        db_file = os.path.abspath(".")+"/admin"
    else:
        db_file = os.path.abspath(".")
    return db_file

def initSql():
    user_db_connect = sqlite3.connect(get_path()+"/db/userdata.db")
    record_db_connect = sqlite3.connect(get_path()+"/db/record.db")
    commodity_db_connect = sqlite3.connect(get_path()+"/db/commodity.db")
    print( "Opened database successfully")
    user_db_cursor = user_db_connect.cursor()
    record_db_cursor = record_db_connect.cursor()
    commodity_db_cursor = commodity_db_connect.cursor()
    user_db = """
        CREATE TABLE `user_data` (
            id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(16) UNIQUE NOT NULL,
            age INTEGER NOT NULL,
            gender VARHCAR(1) NOT NULL,
            password VARCHAR(35) NOT NULL,
            mail VARCHAR(25) UNIQUE NOT NULL,
            datetime VARCHAR(20)
        );"""

    record_db = """
        CREATE TABLE `record_data` (
            username VARCHAR(16) NOT NULL,
            buy_what TEXT NOT NULL,
            spend INTEGER NOT NULL,
            datetime VARCHAR(20)
        );"""

    commodity_db = """
        CREATE TABLE `commodity_information` (
            id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            name_of_a_commodity VARCHAR(30) UNIQUE NOT NULL,
            datetime TEXT,
            price VARCHAR(20),
            number VARCHAR(10)
        );
    """

    user_db_cursor.execute(user_db)
    user_db_cursor.close()
    user_db_connect.commit()
    user_db_connect.close()
    commodity_db_cursor.execute(commodity_db)
    commodity_db_cursor.close()
    commodity_db_connect.commit()
    record_db_cursor.execute(record_db)
    record_db_cursor.close()
    record_db_connect.commit()
    record_db_connect.close()


class AdminSQL():

    def __init__(self):
        self.user_db_connect = sqlite3.connect(get_path()+"/db/userdata.db")
        self.user_db_cursor = self.user_db_connect.cursor()
        self.record_db_connect = sqlite3.connect(get_path()+"/db/record.db")
        self.record_db_cursor = self.record_db_connect.cursor()
        self.commodity_db_connect = sqlite3.connect(get_path()+"/db/commodity.db")
        self.commodity_db_cursor = self.commodity_db_connect.cursor()

    # 获取时间
    def getTime(self):
        dtime = datetime.now().timestamp()
        # date = datetime.fromtimestamp(dtime)
        return dtime

    # 保存注册的信息
    def saveUserDB(self,db):
        username, age, gender, password, mail = db["username"], db["age"], db["gender"], db["password"], db["mail"]
        get_max_id = self.user_db_cursor.execute("SELECT MAX(id) FROM user_data;")
        max_id = [i for i in get_max_id][0][0]
        if max_id == None:
            max_id = 0
        into_data = """
            INSERT INTO user_data (id, username, age, gender, password, mail, datetime) VALUES ({}, '{}', {}, '{}', '{}', '{}', '{}')
        """.format(max_id+1, username, age, gender,password, mail, self.getTime())
        self.user_db_cursor.execute(into_data)
        self.user_db_cursor.close()
        self.user_db_connect.commit()
        self.user_db_connect.close()

    # 保存消费记录
    def saveRecordDB(self, record_db):
        into_db = """
            INSERT INTO record_db (username, buy_what, spend, datetime) VALUES ('{}', '{}', {}, '{}')
        """.format(username, buy_what, spend, self.getTime())

    # 查询用户名
    def searchAloneUsernameDB(self, username):
        search_db = """
            SELECT username FROM user_data WHERE username="{}"
        """.format(username)
        try:
            data = [i for i in self.user_db_cursor.execute(search_db)][0]
        except IndexError:
            return None
        return data

    # 查询密码
    def searchAlonePasswordDB(self, username):
        search_db = """
            SELECT password FROM user_data WHERE username="{}"
        """.format(username)
        try:
            data = [i for i in self.user_db_cursor.execute(search_db)][0]
        except IndexError:
            return None
        return data[0]

    # 查询邮箱
    def searchAloneMailDB(self, mail):
        search_db = """
            SELECT mail FROM user_data WHERE mail="{}" 
        """.format(mail)
        try:
            data = [i for i in self.user_db_cursor.execute(search_db)][0]
        except IndexError:
            return None
        return data

try:
    if os.listdir("db") == []:
        initSql()
except FileNotFoundError:
    pass

# a = AdminSQL()
# print(a.searchAloneMailDB("14@qq.com"))