# -*- coding: utf-8 -*-
# @time    ： 2021/9/24 17:46
# author   ： 贾志凯 15716539228@163.com
# filename ： check.py
# @software： win10 python3.6.5 PyCharm
from inspect import signature
from functools import wraps


def check_parameter(*ty_args, **ty_kwargs):
    '''
    参数类型检察，如果属性类型不符合则无法通过
    用法：
        from pykaiutils.decorator.check import check_parameter
        @check_parameter(x=str, y=str, z=int)
        def dome(x, y, z):
    '''
    def decorator(func):
        if not __debug__:
            return func
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments
        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            for name,value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('参数：{} 必须是：{}，您输入的参数类型错误！'.format(name, bound_types[name]))
            return func(*args, **kwargs)
        return wrapper
    return decorator
