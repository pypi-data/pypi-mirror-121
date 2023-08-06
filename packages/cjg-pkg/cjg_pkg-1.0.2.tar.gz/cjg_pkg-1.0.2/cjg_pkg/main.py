# coding: utf-8
# @Author: jigang.chen
# @Email: 1275479178@qq.com
# @Project: common_auto_test_frame
# @File: main.py
# @Date: 2021/9/17
import itertools


def auto_create_test_case(iterable_1, iterable_2):
    """自动生成测试用例"""
    count = 1
    # 通过itertools.product获取指定迭代对象的笛卡尔积
    for case in itertools.product(iterable_1, iterable_2):
        print(f"case {count}-{case}")
        count += 1
    print(f"自动生成用例完成，共{count - 1}条测试用例")
