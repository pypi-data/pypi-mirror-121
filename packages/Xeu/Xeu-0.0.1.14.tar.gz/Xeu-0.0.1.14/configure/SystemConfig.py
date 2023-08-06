# -*- coding: utf-8 -*-
import os


__all__ = [
    'EXPIRE_TIME_SECONDS', 'BASE_DIR', 'SET_DEFAULT_HEADER', 'COOKIE_SECRET',
    'TEMPLATES_URL', 'STATIC_URL', 'STATIC_URL_PREFIX', 'INDEX_FILE'
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COOKIE_SECRET = 'ulb7bEIZmwpV545Z'
EXPIRE_TIME_SECONDS = 60 * 30


ROUTER_MAP = {

    # r'/CashEpayService/transaction/(?P<trans_number>.*)/merchant_code/(?P<merchant_code>.*)': 'Transaction',
    # r'/CashEpayService/transaction/(?P<trans_number>.*)': 'Transaction',
}

STATIC_RELATIVE = 'static'
STATIC_URL = os.path.join(BASE_DIR, STATIC_RELATIVE)
STATIC_URL_PREFIX_RAW = 'Front'
STATIC_URL_PREFIX = '/' + STATIC_URL_PREFIX_RAW + '/'
INDEX_FILE = "admin.html"
TEMPLATES_RELATIVE = 'templates'
TEMPLATES_URL = os.path.join(BASE_DIR, TEMPLATES_RELATIVE)


SET_DEFAULT_HEADER = {
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
    "Access-Control-Allow-Methods": "POST, GET, PUT, PATCH",
    "Access-Control-Allow-Headers": "Origin,Content-Type,Accept,token,X-Requested-With"
}


""" 系统共用字体 """
SYSTEM_FONTS_URL = os.path.join(BASE_DIR, 'Config', 'share_files', 'fonts')
""" 临时验证码图片 """
SYSTEM_VER_CODE_URL = os.path.join(BASE_DIR, 'temp', 'vercode')
""" 上传文件包存放路径 """
UPLOAD_PACKAGE_URL = os.path.join(BASE_DIR, 'upload_package')
""" 上传 报告相关文件包 存放路径 """
UPLOAD_REPORT_PACKAGE_URL = os.path.join(BASE_DIR, 'upload_package', 'report')




