import os
import logging
# import logging.handlers
import logging.config
from Xeu.configure.init import BASE_DIR
from Xeu.utils.DevConsole import StdoutColors

__all__ = ['Logger', ]

""" Log file storage path """
LOG_DIR = os.path.join(BASE_DIR, 'log')

# FileName = {
#     'defaut': os.path.join(LOG_DIR, 'request.log'),
#     'info': os.path.join(LOG_DIR, 'info.log'),
#     'debug': os.path.join(LOG_DIR, 'debug.log'),
#     'error': os.path.join(LOG_DIR, 'error.log')
# }
# Handler = {
#     'defaut': logging.handlers.RotatingFileHandler(FileName['defaut'], maxBytes = 1024*1024*50, backupCount = 5),
#     'info': logging.handlers.RotatingFileHandler(FileName['info'], maxBytes = 1024*1024*50, backupCount = 5),
#     'info-console': logging.StreamHandler(),
#     'debug': logging.handlers.RotatingFileHandler(FileName['debug'], maxBytes = 1024*1024*50, backupCount = 5),
#     'error': logging.handlers.RotatingFileHandler(FileName['error'], maxBytes = 1024*1024*50, backupCount = 5)
# }
# format = {
#     'simple': '[%(asctime)s] %(levelname)s : %(message)s',
#     'verbose': '[%(asctime)s] %(levelname)s %(module)s %(process)d %(thread)d : %(message)s',
#     'standard': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]-%(message)s',
#     'detail-info': '[%(asctime)s] [%(levelname)s] [%(threadName)s:%(thread)d] [%(module)s:%(lineno)d] %(message)s',
#     'color-detail-info': StdoutColors.WARNING +'[%(asctime)s] [%(levelname)s] [%(threadName)s:%(thread)d] [%(module)s:%(lineno)d] %(message)s',
#     'simple-info': '[%(asctime)s] [%(levelname)s] %(message)s',
#     'color-simple-info': StdoutColors.WARNING +'[%(asctime)s] [%(levelname)s] %(message)s',
#     'error': '[%(asctime)s] [%(levelname)s] [%(threadName)s:%(thread)d] [%(module)s:%(lineno)d] %(message)s',
#     'color-error': StdoutColors.FAIL + '[%(asctime)s] [%(levelname)s] [%(threadName)s:%(thread)d] [%(module)s:%(lineno)d] %(message)s',
#     'error-http': '[%(asctime)s] [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s] %(message)s',
#     'user-defined': '[%(asctime)s] [%(processName)s:%(process)d] [%(filename)s:%(lineno)d] [%(levelname)s]: %(message)s'
# }
#
# info_formatter = logging.Formatter(format['user-defined'])
# console_info_formatter = logging.Formatter(format['user-defined'])
# Handler['info'].setFormatter(info_formatter)
# Handler['info-console'].setFormatter(console_info_formatter)
# Logger = logging.getLogger(__file__)
# # Logger.addHandler(Handler['info'])
# Logger.addHandler(Handler['info-console'])
# # Logger.setLevel(logging.DEBUG)
# Logger.setLevel(logging.INFO)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '[%(asctime)s] %(levelname)s : %(message)s'},
        'verbose': {'format': '[%(asctime)s] %(levelname)s %(module)s %(process)d %(thread)d : %(message)s'},
        'standard': {'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]-%(message)s'},
        'detail-info': {'format': '[%(asctime)s] [%(levelname)s] [%(threadName)s:%(thread)d] [%(module)s:%(lineno)d] %(message)s'},
        'color-detail-info': {
            'format': StdoutColors.WARNING +f'[%(asctime)s] [%(levelname)s] [%(threadName)s:%(thread)d] [%(module)s:%(lineno)d] %(message)s' + StdoutColors.ENDC
        },
        'simple-info': {'format': '[%(asctime)s] [%(levelname)s] %(message)s'},
        'color-simple-info': {'format': StdoutColors.WARNING +'[%(asctime)s] [%(levelname)s] %(message)s' + StdoutColors.ENDC},
        'error': {'format': '[%(asctime)s] [%(levelname)s] [%(threadName)s:%(thread)d] [%(module)s:%(lineno)d] %(message)s'},
        'color-error': {
            'format': StdoutColors.FAIL + '[%(asctime)s] [%(levelname)s] [%(threadName)s:%(thread)d] [%(module)s:%(lineno)d] %(message)s'},
        'error-http': {'format': '[%(asctime)s] [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s] %(message)s'},
    },
    'handlers': {
        'console-debug-default': {'level': 'DEBUG', 'formatter': 'standard', 'class': 'logging.StreamHandler'},
        'console-simple-info': {'level': 'INFO', 'formatter': 'color-simple-info', 'class': 'logging.StreamHandler'},
        'console-detail-info': {'level': 'INFO', 'formatter': 'color-detail-info', 'class': 'logging.StreamHandler'},
        'console_error': {'level': 'INFO', 'formatter': 'color-error', 'class': 'logging.StreamHandler'},
        'file-debug-default': {
            'level': 'DEBUG', 'formatter': 'standard', 'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'debug.log'), 'maxBytes': 1024 * 1024 * 50, 'backupCount': 3,
        },
        'request_handler': {
            'level': 'DEBUG', 'formatter': 'standard', 'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'request.log'), 'maxBytes': 1024 * 1024 * 50, 'backupCount': 3,
        },

        'file-error': {
            'level': 'ERROR', 'formatter': 'error', 'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'), 'maxBytes': 1024 * 1024 * 50, 'backupCount': 3, 'mode': 'a',
        },
        'file-simple-info': {
            'level': 'INFO', 'formatter': 'simple-info', 'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'info.log'), 'maxBytes': 1024 * 1024 * 50, 'backupCount': 3, 'mode': 'a',
        },
        'file-detail-info': {
            'level': 'INFO', 'formatter': 'detail-info', 'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'info.log'), 'maxBytes': 1024 * 1024 * 50, 'backupCount': 10, 'mode': 'a',
        },
        # 'request': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': os.path.join(LOG_DIR, 'request.log'),
        #     'maxBytes': 1024 * 1024 * 50,
        #     'backupCount': 5,
        #     'formatter': 'simple',
        # },
        # 'console_error_file': {
        #     'level': 'ERROR',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': os.path.join(LOG_DIR, 'console.log'),
        #     'formatter': 'standard',
        # },
        # 'file-http': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.HTTPHandler',
        #     'formatter': 'standard',
        #     "host": "127.0.0.1:8080",
        #     "url": "/log_server",
        #     "method": "POST",
        # },
    },

    'loggers': {
        'simple-info': {'handlers': ['file-simple-info', 'console-simple-info'], 'level': 'INFO', 'propagate': False},
        'detail-info': {'handlers': ['file-detail-info', 'console-detail-info'], 'level': 'INFO', 'propagate': False},
        'critical': {'handlers': ['file-detail-info', 'console-detail-info'], 'level': 'INFO', 'propagate': False},
        'error': {'handlers': ['file-error', 'console_error'], 'level': 'ERROR', 'propagate': False},
        'debug': {'handlers': ['console-debug-default', 'file-debug-default'], 'level': 'DEBUG', 'propagate': False},
        # 'request': {
        #     'handlers': ['request'],
        #     'level': 'INFO',
        #     'propagate': True,
        # },
        # 'http_request': {
        #     'handlers': ['console_error'],
        #     'level': 'ERROR',
        #     'propagate': True,
        # },
        # 'django.request': {
        #     'handlers': ['request_handler'],
        #     'level': 'ERROR',
        #     'propagate': False,
        # },
    }

}

logging.config.dictConfig(LOGGING)


class Logger(object):
    @classmethod
    def info(cls, *args, **kwargs):
        pass

    @classmethod
    def error(cls, *args, **kwargs):
        pass

""" 应用自定义的数据库模板的方法 """
Logger.applyTemp = logging.getLogger

""" 应用缺省的数据库模板的方法 """
Logger.getLogger = logging.getLogger
Logger.info = logging.getLogger('detail-info').info
Logger.error = logging.getLogger('error').error
Logger.critical = logging.getLogger('critical').critical

