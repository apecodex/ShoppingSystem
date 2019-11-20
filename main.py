# -*- coding: utf-8 -*-
# @Time    : 2019/11/10 下午11:09
# @Author  : apecode
# @Email   : 1473018671@qq.com
# @File    : main.py.py
# @Software: PyCharm

from admin import Login
from admin import Register
from admin import sql
import getpass
import re

class_Login = Login.LoginSystem()  # 实例化
class_sql = sql.AdminSQL()

def login():
    flag = True
    print(" *********************** ")
    print("|~~~~~~~~~~登录~~~~~~~~~|")
    print("|#######################|")
    print("|~~~输入 `q` 退出登录~~~|")
    print(" *********************** ")
    while flag:
        username = input("用户名: ")
        if username == "q" or username == "Q":
            flag = False
        password = getpass.getpass("密  码:")
        if username.strip() == "":
            print("用户名不能为空!")
            continue
        elif password.strip() == "":
            print("密码不能为空!")
            continue
        else:
            search_username = class_Login.searchSqlUsername(username)     # 查询用户名
            if search_username != None:    # 判断查询的结果是否为None,如果为None,则用户名不存在数据库
                search_password = class_Login.searchSqlPassword(search_username)    # 判断不为None时,开始查询密码
                hashpassword = Register.HashMd5(username ,password).password    # 利用用户输入的生成新的hash
                if hashpassword != search_password:    # 如果新生成的hash与数据库中的不同，则密码错误
                    print("用户名或密码有误!")
                else:
                    if hashpassword == search_password:
                        print("登录成功")
                        flag = False
                    else:
                        print("登录异常")
                        flag = False
            else:
                return "None"

class RegisterMain():

    def __init__(self):
        print(" ************************* ")
        print("|~~~~~~~~~~注 册~~~~~~~~~~|")
        print("|#########################|")
        print("|~~~~输入 `q` 退出登录~~~~|")
        print(" ************************* ")
        self.re_username = re.compile(r'^[a-zA-Z]+[a-zA-Z0-9]+$')  # 输入的格式只能包含字母和数字,且字母开头
        self.re_password = re.compile(r'^[a-zA-Z]+[0-9!@#$%^&*()_+>}<{;\'\]\[\\|]+$')  # 匹配所有
        self.re_mail = re.compile(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}')  # 匹配邮箱
        self.db = {}

    def checkUsername(self):
        flag = True
        while flag:
            username = input("用户名: ")
            len_usename = len(username)
            if username == "q" or username == "Q":
                flag = False
                return username
            if username.strip() == "":
                print("用户名不能为空!")
                continue
            elif len_usename < 6 or len_usename > 15:
                print("用户名太长或太短，请重新输入6-15个字符以内")
                continue
            elif self.re_username.findall(username) == [] or len_usename != len("".join(username.split())):
                print("用户名格式有误，只能包含字母和数字,且字母开头,不能含有空格")
                continue
            elif class_Login.searchSqlUsername(username) != None:
                print("用户名已存在!")
                continue
            else:
                self.db["username"] = username
                flag = False

    def checkAge(self):
        flag = True
        while flag:
            try:
                age = int(input("年  龄: "))
            except ValueError:
                print("请输入正确的年龄!")
                continue
            if age > 150 or age < 0:
                print("请输入正确的年龄!")
                continue
            else:
                self.db["age"] = age
                flag = False

    def checkGender(self):
        flag = True
        while flag:
            gender = input("性  别 (男=0 | 女=1): ")
            if gender.strip() == "":
                print("请输入性别 (男=0 | 女=1)")
                continue
            elif gender == "1" or gender == "0":
                self.db["gender"] = gender
                flag = False
            else:
                print("请输入正确的性别 (男=0 | 女=1)")

    def checkPassword(self):
        flag = True
        while flag:
            password = getpass.getpass("密  码: ")
            again_password = getpass.getpass("确认密码: ")
            if password == "":
                print("密码不能为空!")
                continue
            elif again_password != password:  # 判断第二次输入的和第一次输入的是不是一样的
                print("两次密码不相同!")
                continue
            elif len(again_password) < 6:
                print("密码太弱，请输入6位数以上，且字母+数字或特殊符合")
                continue
            elif self.re_password.findall(password) == []:  # 如果为空说明匹配失败，输入不符合要求
                print("密码格式有误，字母+数字或特殊符号")
                continue
            else:
                self.db["password"] = Register.HashMd5(self.db["username"], password).password  # 调用HashMd5对象进行加盐
                flag = False

    def checkMail(self):
        flag = True
        while flag:
            mail = input("邮箱: ")
            if self.re_mail.findall(mail) == []:  # 如果为空,则匹配失败，说明输入有误
                print("邮箱格式有误!")
                continue
            elif class_sql.searchAloneMailDB(mail) != None:
                print("此邮箱已存在!")
                continue
            else:
                flag = False
                self.db["mail"] = mail

    def main(self):
        no_exit = self.checkUsername()
        if no_exit == "q" or no_exit == "Q":
            print("已退出!")
        else:
            self.checkAge()
            self.checkGender()
            self.checkPassword()
            self.checkMail()
            class_sql.saveUserDB(self.db)
            print("注册成功!")


def findpassword():
    pass

if __name__ == '__main__':
    print(" 一一一一一一一一一一一一一一一一一一一一一一一一一一一 ")
    print("|-------------Welcome To apecode Shopping!--------------|")
    print("|#######################################################|")
    print("|-------------在这里你可以购买你需要的东西!-------------|")
    print("|#######################################################|")
    print("|-----------------在此之前，您得先登录!-----------------|")
    print("|#######################################################|")
    print("|---------------------输入 `1` 登录---------------------|")
    print("|---------------------输入 `2` 注册---------------------|")
    print("|---------------------输入 `3` 退出---------------------|")
    print(" 一一一一一一一一一一一一一一一一一一一一一一一一一一一 ")
    user_select = input("请选择: ")
    if user_select == "1":
        login_record = login()
        if login_record == "None":
            print("is no exists")
    elif user_select == "2":
        register_init = RegisterMain()
        register_init.main()