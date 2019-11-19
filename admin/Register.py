# -*- coding: utf-8 -*-
# @Time    : 2019/11/10 下午11:10
# @Author  : apecode
# @Email   : 1473018671@qq.com
# @File    : Register.py
# @Software: PyCharm

import hashlib
import re
import sql

# md5加密)
def get_md5(key):
    return hashlib.md5(key.encode("utf-8")).hexdigest()

class HashMd5():

    def __init__(self,username, password):
        self.salt = "".join([str(ord(i)) for i in username])  # 遍历username并且获取对应的ascii，没学算法，随机生成的没办法保存
        self.password = get_md5(password+self.salt)  # 加盐

class Register():

    def __init__(self):
        self.db = {}
        self.user_date = []
        self.sql = sql.AdminSQL()
        self.re_username = re.compile(r'^[a-zA-Z]+[a-zA-Z0-9]+$')  # 输入的格式只能包含字母和数字,且字母开头
        self.re_password = re.compile(r'^[a-zA-Z]+[0-9!@#$%^&*()_+>}<{;\'\]\[\\|]+$')  # 匹配所有
        self.re_mail = re.compile(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}')  # 匹配邮箱

    def checkUsrname(self):
        flag = True
        print("-----------------注册-----------------")
        print("######################################")
        print("-----------输入`q`退出注册!-----------")
        while flag:
            username = input("用户名: ")
            len_username = len(username)  #获取长度
            re_username = self.re_username.findall(username)  # 输入的格式只能包含字母和数字,且字母开头
            if username == "q" or username == "Q":
                return username
            if username == "":  # 不得为空
                print("用户名不能为空，请重新输入!")
                continue
            elif len_username < 6 or len_username > 15:
                print("用户名太长或太短，请重新输入6-15个字符以内")
                continue
            elif re_username == [] or len_username != len("".join(username.split())):  # 如果为空list说明匹配失败，输入的有误
                print("用户名格式有误，只能包含字母和数字,且字母开头,不能有空格")
                continue
            elif self.sql.readAloneUsernameDB(username) != None:
                print("用户名已存在，请重新输入")
                continue
            else:
                flag = False
                self.db["username"] = username

    def checkAge(self):
        flag = True
        while flag:
            try:
                age = int(input("年龄: "))
                if age >= 150:
                    print("你是魔鬼吗？活这么久")
                    continue
                else:
                    flag = False
                    self.db["age"] = age
            except ValueError:
                print("请输入正确的年龄!")

    def checkGender(self):
        flag = True
        while flag:
            gender = input("性别 (男=0/女=1): ")
            if gender == "0" or gender == "1":
                flag = False
                self.db["gender"] = gender
            else:
                print("请输入性别,男输入0,女输入1")
                continue

    def checkPassword(self, username):
        flag = True
        while flag:
            password = input("密码: ")
            again_password = input("确认密码: ")
            len_password = len(password)  # 获取长度
            re_password = self.re_password.findall(password)
            if password == "":
                print("密码不能为空!")
                continue
            elif again_password != password:  # 判断第二次输入的和第一次输入的是不是一样的
                print("两次密码不相同!")
                continue
            elif len_password < 6:
                print("密码太弱，请输入6位数以上，且字母+数字或特殊符合")
                continue
            elif re_password == []:  # 如果为空说明匹配失败，输入不符合要求
                print("密码格式有误，字母+数字或特殊符号")
                continue
            else:
                flag = False
                self.db["password"] = HashMd5(username, password).password  # 调用HashMd5对象进行加盐

    def checkMail(self):
        flag = True
        while flag:
            mail = input("邮箱: ")
            re_mail = self.re_mail.findall(mail)
            if re_mail == []:  # 如果为空,则匹配失败，说明输入有误
                print("邮箱格式有误!")
                continue
            elif self.sql.readAloneMailDB(mail) != None:
                print("此邮箱已存在!")
            else:
                flag = False
                self.db["mail"] = mail

    def main(self):
        username_data = str(self.checkUsrname())  # 判断用户是否输入了q
        if username_data == "q":
            print("-----------已退出!---------")
        else:
            self.checkAge()
            self.checkGender()
            self.checkPassword(username_data)
            self.checkMail()
            self.sql.saveUserDB(self.db)
            print("注册成功！")


r = Register()
r.main()