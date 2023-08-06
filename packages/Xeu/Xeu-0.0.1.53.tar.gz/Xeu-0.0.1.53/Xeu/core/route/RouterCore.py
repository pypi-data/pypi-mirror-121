# _*_ coding:utf-8 _*_
import tornado.web
import copy
from Xeu.configure.init import SETUP_MAIN_ROUTERS
# from Config.LoggingConf import Logger, LFormatRSD, LFormatRS, LFormatR
from Xeu.configure.init import COOKIE_SECRET, TEMPLATES_URL, STATIC_URL, INDEX_FILE

__all__ = ['app', 'router_map_pool', 'api_doc']

from Xeu.logger.conf import Logger
from Xeu.utils.DevConsole import StdoutColors

router_map_pool = list()
api_doc = dict()


class __RouterConfig(tornado.web.Application):
    """ 重置Tornado自带的路有对象 """

    def route(self, url, name=None):
        """
        注册模块的路由映射关系
        :param url:
        :param name:
        :return:
        """

        def __register(handler):
            """
            :param handler: URL对应的Handler
            :return: Handler
            """
            #########################
            # 接口下的 http 方法文档 #
            #########################

            __main_url = SETUP_MAIN_ROUTERS.get(str(handler.__module__).split('.')[-1], None)
            api_doc.update({
                str(handler.__module__): dict(
                    get=handler.get.__doc__,
                    post=handler.post.__doc__,
                    patch=handler.patch.__doc__,
                    put=handler.put.__doc__,
                    delete=handler.delete.__doc__,
            )})
            ####################
            # 路由载入 排序 #
            ####################

            __route_url = __main_url is not None and __main_url + url or url
            __route_map = (__route_url, handler)
            router_map_pool.append(__route_map)
            Logger.sys_info(f'{StdoutColors.OKBLUE}[system]{StdoutColors.ENDC} {StdoutColors.TXTGRAY}routing map preloading {name} <{__route_url}> ')

            # self.add_handlers(".*$", [(main_url is not None and main_url+url or url, handler)])  # URL和Handler对应关系添加到路由表中
            return handler

        return __register


app = __RouterConfig(
    cookie_secret=COOKIE_SECRET,
    template_path=TEMPLATES_URL,
    static_path=STATIC_URL,
    static_handler_args={"default_filename": INDEX_FILE}
)  # 创建Tornado路由对象，默认路由表为空