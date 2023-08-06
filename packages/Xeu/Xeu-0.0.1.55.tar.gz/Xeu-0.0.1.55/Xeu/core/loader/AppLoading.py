# _*_ coding:utf-8 _*_
import os
import tornado.ioloop
import tornado.httpserver
from colorama import init
from Xeu.utils.DevConsole import StdoutColors

init(autoreset=True)
from Xeu.core.route.RouterCore import router_map_pool, api_doc
from Xeu.configure.init import Setup, BASE_DIR, LISTEN, APP_ROOT, INSTALL_APP, SETUP_MAIN_ROUTERS, RUNTIME
from Xeu.logger.conf import Logger, OK, FAIL

"""
    The load file for the App
"""
app = None

apps_root = os.path.join(BASE_DIR, APP_ROOT)

_compile_lis = []


# todo INstall 与 路由映射的检查一致性
def is_app_consistence():
    app_consis = set(SETUP_MAIN_ROUTERS.keys()) ^ set(INSTALL_APP)
    if app_consis:
        return False, app_consis
    return True, None


def loading(root, app_root):
    """ 遍历目录下所有要导入的应用文件 """
    for app_file in os.listdir(root):
        app_file_path = os.path.join(root, app_file)
        if os.path.isdir(app_file_path) and not app_file.startswith('_'):
            """ dir """
            loading(app_file_path, app_root+'.'+app_file)
        elif not os.path.isdir(app_file_path):
            """ file """
            app_name = app_file.split('.')[0]
            if app_name in INSTALL_APP:

                # 一致性判断
                state, arg = is_app_consistence()
                if not state:
                    raise ValueError('Inconsistency between RouterMap and INSTALL_APP %s ' % str(arg))

                # todo 预加载 应用目录下的模块 此处 后面可以进行接口模块校验
                _compile_lis.append("from "+app_root + "."+str(app_name)+" import *")
            else:
                pass


"""
    Load the application in the App directory and load the routing map
"""
try:
    Logger.sys_info(f'{StdoutColors.OKBLUE}[system]{StdoutColors.ENDC} {StdoutColors.TXTGRAY}loading component class of handler ......')
    loading(apps_root, app_root=APP_ROOT)
    for source in _compile_lis:
        try:
            eval(compile(source, '', 'exec'))
        except Exception as e:
            Logger.error(f'[system] loading component class of handler <{source}> [Fail] when {e} occurs as {source}')

    Logger.sys_info(f'{StdoutColors.OKBLUE}[system]{StdoutColors.ENDC} {StdoutColors.TXTGRAY}loading component class of handler {OK}')
except ModuleNotFoundError as e:
    Logger.error(f'[system] loading component class of handler {FAIL} {e}')
except ValueError as e:
    Logger.error(f'[system] loading component class of handler {FAIL} {e}')
else:
    # sort router_map_pool
    router_map_pool.sort(key=lambda tup: tup[0], reverse=True)
    for router_map in router_map_pool:
        app.add_handlers(".*$", [router_map])
        Logger.sys_info(f'{StdoutColors.OKBLUE}[system]{StdoutColors.ENDC} {StdoutColors.TXTGRAY}routing map loading <{router_map}> {OK}')

# def gen_pia_doc(api_doc_dic):
#     # print(api_doc_dic)
#     for full_class, api_doc in api_doc_dic.items():
#         # print(full_class, api_doc)
#         for method, method_doc in api_doc.items():
#             if method_doc is not None:
#
#                 print(method, method_doc.strip())
#
#
# gen_pia_doc(api_doc)

Setup(
    base_config=('base.toml', )
)


def run():
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(LISTEN.port, address=LISTEN.ipv4)
    http_server.start(1)
    Logger.sys_info(f"""{StdoutColors.OKBLUE}[system]{StdoutColors.ENDC} {StdoutColors.TXTGRAY}* current environment -> {StdoutColors.WARNING}{RUNTIME.env}
                                                                             * listen -> http://{LISTEN.ipv4}:{LISTEN.port}""")
    tornado.ioloop.IOLoop.instance().start()