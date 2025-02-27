import re


password = input("请输入你的密码：")

# pattern1 = re.compile(r"[a-zA-Z0-9]{7,}\S{1,}")
# pattern2 = re.compile(r"[a-zA-Z0-9]{8,}")
# pattern3 = re.compile(r"\d{1,8}")
Uperword_pattern = re.compile(r"[A-Z]+")
lowerword_pattern = re.compile(r"[a-z]+")
number_pattern = re.compile(r"\d+")
specialchar_pattern = re.compile(r"[!@#$%^&*()_+-=<>?]")

if len(password) > 8:
    if Uperword_pattern.search(password) and lowerword_pattern.search(password) and number_pattern.search(password) and specialchar_pattern.search(password):
        print("密码强度高")
    elif Uperword_pattern.search(password) and lowerword_pattern.search(password) and number_pattern.search(password):
        print("密码强度中")

else:
    print("密码强度低")