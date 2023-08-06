# -*- coding: utf-8 -*-
"""
    常用异常字段
"""
from tornado.web import MissingArgumentError
from pymysql.err import DataError # as pymysql
__all__ = ['TokenRefreshError', 'ParameterError', 'DataBaseOperationalError', 'ModuleAuthError', 'MissValueError',
           'SettlementError', 'ConstError', 'ConstCaseError', 'MissingArgumentError', 'DataError']


class TokenRefreshError(Exception):
    """
    token 刷新异常
    """
    def __init__(self, errmsg=None, errcode=None):
        Exception.__init__(self)
        self.message = errmsg
        self.code = errcode

    def __str__(self):
        return self.message, self.code


class FormError(Exception):
    """
    参数错误
    """
    def __init__(self, errmsg=None, errcode=None):
        Exception.__init__(self)
        self.message = errmsg
        self.code = errcode

    def __str__(self):
        return self.message, self.code


class ParameterError(Exception):
    """
    参数错误
    """
    def __init__(self, errmsg=None, errcode=None):
        Exception.__init__(self)
        self.message = errmsg
        self.code = errcode

    def __str__(self):
        return self.message, self.code


class DataBaseOperationalError(Exception):
    """
    数据库操作错误
    """
    def __init__(self, errmsg=None, errcode=None):
        Exception.__init__(self)
        self.message = errmsg
        self.code = errcode

    def __str__(self):
        return self.message, self.code


class ModuleAuthError(Exception):
    """
    模块访问权限
    """
    def __init__(self, error_info):
        Exception.__init__(self)
        self.message = error_info

    def __str__(self):
        return self.message


class MissValueError(Exception):
    """
    请求参数丢失
    """
    def __init__(self, error_info):
        Exception.__init__(self)
        self.message = error_info

    def __str__(self):
        return self.message


class SettlementError(Exception):
    """
    请求参数丢失
    """
    def __init__(self, error_info):
        Exception.__init__(self)
        self.message = error_info

    def __str__(self):
        return self.message


class ConstError(TypeError):
    """
    请求参数丢失
    """
    def __init__(self, error_info):
        Exception.__init__(self)
        self.message = error_info

    def __str__(self):
        return self.message


class ConstCaseError(ConstError):
    """
    请求参数丢失
    """
    def __init__(self, error_info):
        Exception.__init__(self)
        self.message = error_info

    def __str__(self):
        return self.message