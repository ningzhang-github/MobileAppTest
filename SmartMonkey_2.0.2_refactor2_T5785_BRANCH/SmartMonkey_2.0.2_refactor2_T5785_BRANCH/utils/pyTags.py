# -*- coding: utf8 -*-
'''
Created on 2014-10-27
@author: zen
'''


def singleton(cls, *args, **kw):
    '''实现单例模式方法'''
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton