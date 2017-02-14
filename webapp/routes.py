"""
.. module:: routes.py

Routes setup for HTTP server
"""


def setup_routes(app, views, project_root):
    """
    Setting up HTTP routes

    :param: app
      Aiohttp app object to add routes to

    :param: views
      A module or a class instance which contains actual views to route to

    :param: project_root
      A directory containing project root, for static files if needed
    """
    app.router.add_route('GET', '/', views.index)
    app.router.add_route('GET', '/search', views.search)
    app.router.add_static('/static/',
                          path=project_root/'static',
                          name='static')
