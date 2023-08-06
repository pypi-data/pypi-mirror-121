# coding: utf-8
# @Author: jigang.chen
# @Email: 1275479178@qq.com
# @Project: common_auto_test_frame
# @File: main.py
# @Date: 2021/9/17
import itertools

username = ["正确的手机号", "错误的手机号", "手机号为空"]
password = ["正确的密码", "错误的密码", "密码为空", "密码过期"]


def auto_create_test_case(iterable_1, iterable_2):
    count = 1
    # 通过itertools.product获取指定迭代对象的笛卡尔积
    for case in itertools.product(iterable_1, iterable_2):
        print(f"case {count}-{case}")
        count += 1
    print(f"自动生成用例完成，共{count-1}条测试用例")


auto_create_test_case(username, password)
