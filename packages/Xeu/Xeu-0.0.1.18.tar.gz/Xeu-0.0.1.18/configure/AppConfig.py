# _*_ coding:utf-8 _*_

"""
    App loads the authentication record of the project
    The mapping of the main path of App
"""
from Xeu.core.route.RouterGroup import RouterGroup

""" App Register """

INSTALL_APP = [
    'AdminSystemIndexHtml',
    'BaseDemo',
    'AdminApi'
]

"""
    Prefix routing for App main routes、
"""

admin_route_group = RouterGroup(
    group='admin',
    route_map=dict(
        AdminSystemIndexHtml='index',
        AdminApi='api'
    )
)
example_route_group = RouterGroup(
    group='example',
    route_map=dict(
        BaseDemo='base',
    )
)

SETUP_MAIN_ROUTERS = (admin_route_group + example_route_group).to_dict()

"""
    APP ROOT DIR
"""

APP_ROOT = 'app'

