# -*- coding: utf-8 -*-
# @Time    : 2019/11/10 下午11:10
# @Author  : apecode
# @Email   : 1473018671@qq.com
# @File    : Login.py
# @Software: PyCharm

try:
    import Register
    import sql
except ModuleNotFoundError:
    from . import Register
    from . import sql

class LoginSystem():

    def __init__(self):
        self.sql = sql.AdminSQL()

    def searchSqlUsername(self,username):
        search_username = self.sql.searchAloneUsernameDB(username)
        if search_username == None:
            return None
        else:
            return search_username[0]

    def searchSqlPassword(self, username):
        search_password = self.sql.searchAlonePasswordDB(username)
        if search_password == None:
            return None
        else:
            return search_password


# l = LoginSystem()
# print(l.searchSqlUsername("aaaeeeq"))
# print(l.checkInput())