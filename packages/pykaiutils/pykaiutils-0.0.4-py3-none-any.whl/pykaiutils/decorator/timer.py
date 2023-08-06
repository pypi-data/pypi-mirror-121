# -*- coding: utf-8 -*-
# @time    ： 2021/9/24 17:35
# author   ： 贾志凯 15716539228@163.com
# filename ： timer.py
# @software： win10 python3.6.5 PyCharm
import time
from functools import wraps
'''
r如果有多个装饰器，会先执行最下面，例如
@timethis2
@timethis
def prin(n):
timethis2（timethis（prin））


你写了一个装饰器作用在某个函数上，但是这个函数的重要的元信息比如名字、文档字符串、注解和参数签名都丢失了。
任何时候你定义装饰器的时候，都应该使用 functools 库中的 @wraps 装饰器来注解底层包装函数

在这里原始的函数的信息就不会丢失

'''


def run_time(func):
    '''
    该方法消耗时间
    使用方法:
    from pykaiutils.decorator.timer import run_time
    @run_time
    def dome():
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"**装饰器输出** 函数名称：{func.__name__}, 消耗时间：{end - start}s**")
        return result
    return wrapper
