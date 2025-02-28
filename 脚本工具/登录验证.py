import re

users = {
    "admin": "123456",
    "user1": "Password@123",
    "user2": "qwerty",
    "user3": "abc123",
}

def regex_compile():
    upper = re.compile(r"[A-Z]+")
    lower = re.compile(r"[a-z]+")
    number = re.compile(r"\d+")
    special = re.compile(r"[!@#$%^&*()_+-=<>?]")
    return upper, lower, number, special

def validate_username(username):
    if len(username.strip()) < 5:
        print("用户名必须大于5个字符")
        return False
    return True

def validate_password(password):
    password = password.strip()
    upper, lower, number, special = regex_compile()
    if not upper.search(password):
        print("密码必须包含大写字母")
        return False
    if not lower.search(password):
        print("密码必须包含小写字符")
        return False
    if not number.search(password):
        print("密码必须包含数字")
    if not special.search(password):
        print("密码必须包含特殊字符")
        return False
    return True



def main():
    username = input("请输入用户名：")
    if not validate_username(username):
        return
    password = input("请输入密码：")
    if not validate_password(password):
        return
    if username in users and users[username] == password:
        print("登录成功")
    else:
        print("用户名或密码错误")



if __name__ == '__main__':
    main()