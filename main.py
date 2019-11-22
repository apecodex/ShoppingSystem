# -*- coding: utf-8 -*-
# @Time    : 2019/11/10 下午11:09
# @Author  : apecode
# @Email   : 1473018671@qq.com
# @File    : main.py.py
# @Software: PyCharm

from admin import Register
from admin import sql
from random import randint
import getpass
import re

class_sql = sql.AdminSQL() # 实例化

def login():
    flag = True
    print(" *********************** ")
    print("|~~~~~~~~~~登录~~~~~~~~~|")
    print("|#######################|")
    print("|~~~输入 `q` 退出登录~~~|")
    print(" *********************** ")
    num = 1
    while flag:
        username = input("用户名: ")
        if username == "q" or username == "Q":
            flag = False
            return "exit"
        password = getpass.getpass("密  码:")
        if username.strip() == "":
            print("用户名不能为空!")
            continue
        elif password.strip() == "":
            print("密码不能为空!")
            continue
        else:
            search_username = class_sql.searchAloneUsernameDB(username)     # 查询用户名
            if search_username != None:    # 判断查询的结果是否为None,如果为None,则用户名不存在数据库
                search_password = class_sql.searchAlonePasswordDB(search_username)    # 判断不为None时,开始查询密码
                hashpassword = Register.HashMd5(username ,password).password    # 利用用户输入的生成新的hash
                print(search_username, hashpassword, search_password)
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
                num += 1
                if num == 3 or num == 6 or num == 9:
                    return "None"

class RegisterMain():

    def __init__(self):
        print(" ************************* ")
        print("|~~~~~~~~~~注 册~~~~~~~~~~|")
        print("|#########################|")
        print("|~~~~输入 `q` 退出登录~~~~|")
        print(" ************************* ")
        self.re_username = re.compile(r'^[a-zA-Z]+[a-zA-Z0-9]+$')  # 输入的格式只能包含字母和数字,且字母开头
        self.re_password = re.compile(r'^[0-9a-zA-Z]+[0-9a-zA-Z!@#$%^&*()_+>}<{;\'\]\[\\|]+$')  # 匹配所有
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
            elif class_sql.searchAloneUsernameDB(username) != None:
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
                print("密码格式有误，需包含字母、数字或特殊符号")
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
        is_exit = self.checkUsername()
        if is_exit == "q" or is_exit == "Q":
            print("已退出!")
            return None
        else:
            self.checkAge()
            self.checkGender()
            self.checkPassword()
            self.checkMail()
            username, age, gender, password, mail = self.db['username'], self.db['age'], self.db['gender'], self.db['password'], self.db['mail']
            print(self.db)
            class_register = Register.RegisterSystem(username, age, gender, password, mail)
            class_register.save()
            print("注册成功!")


class FindPassword():

    def __init__(self):
        print(" *********************** ")
        print("|~~~~~~~~找回密码~~~~~~~|")
        print("|#######################|")
        print("|~~~输入 `q` 退出登录~~~|")
        print(" *********************** ")
        self.db = {}
        self.re_mail = re.compile(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}')  # 匹配邮箱
        self.re_password = re.compile(r'^[0-9a-zA-Z]+[0-9a-zA-Z!@#$%^&*()_+>}<{;\'\]\[\\|]+$')  # 匹配所有
        self.code = "".join([str(randint(0, 122)) for i in range(5)])

    def checkUsername(self):
        flag = True
        while flag:
            username = input("用户名: ")
            if username == "q" or username == "Q":
                flag = False
                return "exit"
            elif username.strip() == "":
                print("请输入用户名!")
                continue
            else:
                search_username = class_sql.searchAloneUsernameDB(username)
                if search_username == None:
                    print("用户名不存在!")
                    continue
                else:
                    self.db["username"] = username
                    flag = False

    def checkMail(self):
        flag = True
        while flag:
            mail = input("邮  箱: ")
            if mail.strip() == "" or self.re_mail.findall(mail) == []:
                print("邮箱格式有误!")
                continue
            else:
                search_mail = class_sql.searchFindPassword(self.db['username'] ,mail)
                if search_mail == None:
                    print("邮箱地址有误,请核查!")
                    continue
                else:
                    flag = False
                    self.db['mail'] = mail
                    return None   # 表示格式正确，且存在

    def checkNewPassword(self):
        flag = True
        while flag:
            new_password = getpass.getpass("密  码: ")
            again_password = getpass.getpass("确认密码: ")
            if new_password == "" or again_password == "":
                print("密码不得为空!")
                continue
            elif again_password != new_password:
                print("两次密码不相同!")
                continue
            elif len(again_password) < 6:
                print("密码太弱，请输入6位数以上，且字母+数字或特殊符合")
                continue
            elif self.re_password.findall(new_password) == []:  # 如果为空说明匹配失败，输入不符合要求
                print("密码格式有误，需包含字母、数字或特殊符号")
                continue
            else:
                self.db["password"] = Register.HashMd5(self.db["username"], new_password).password  # 调用HashMd5对象进行加盐
                flag = False

    def codeRecord(self, code):
        print("按 `q` 退出验证")
        flag = True
        num = 0
        while flag:
            codeInput = input("code: ")
            if codeInput == "q" or codeInput == "Q":
                flag = False
                return None
            if codeInput != code:
                print("验证码错误!")
                num += 1
                if num == 3 or num == 6 or num == 9:
                    re_code_input = input("需要重新获取验证码吗？(y/n): ")
                    if re_code_input == "y" or re_code_input == "Y":
                        code = "".join([str(randint(0, 122)) for i in range(5)])
                        print(code)
                        continue
                    else:
                        if re_code_input == "n" or re_code_input == "N":
                            continue
            else:
                flag = False
                return "ok"

    def main(self):
        record_username = self.checkUsername()
        if record_username == "exit":
            print("已退出找回密码!")
        else:
            if self.checkMail() == None:
                code = self.code
                print(code)
                code_record = self.codeRecord(code)
                if code_record == None:
                    print("已退出！")
                else:
                    if code_record == "ok":
                        self.checkNewPassword()
                        username = self.db["username"]
                        mail = self.db['mail']
                        new_password = self.db["password"]
                        s = class_sql.updateUserPasswordDB(username, mail, new_password)
                        print(s)
                        print("密码已重新设置!")

if __name__ == '__main__':
    flag = True
    while flag:
        print(" 一一一一一一一一一一一一一一一一一一一一一一一一一一一 ")
        print("|-------------Welcome To apecode Shopping!--------------|")
        print("|#######################################################|")
        print("|-------------在这里你可以购买你需要的东西!-------------|")
        print("|#######################################################|")
        print("|-----------------在此之前，您得先登录!-----------------|")
        print("|#######################################################|")
        print("|---------------------输入 `1` 登录---------------------|")
        print("|---------------------输入 `2` 注册---------------------|")
        print("|---------------------输入 `3` 找回密码-----------------|")
        print("|---------------------输入 `4` 退出---------------------|")
        print(" 一一一一一一一一一一一一一一一一一一一一一一一一一一一 ")
        user_select = input("请选择: ")
        if user_select == "1":
            login_record = login()
            if login_record == "exit":
                print("已经退出！")
                continue
            else:
                if login_record == "None":
                    is_register = input("是否注册?(y/n)")
                    if is_register == "y" or is_register == "Y":
                        register_init = RegisterMain()
                        record = register_init.main()
                        if record == None:
                            continue
        elif user_select == "2":
            register_init = RegisterMain()
            record = register_init.main()
            if record == None:
                continue
        elif user_select == "3":
            find_password = FindPassword()
            find_password.main()
        elif user_select == "4":
            flag = False
            class_sql.close()
            print("已退出!")