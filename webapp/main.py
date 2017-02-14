"""
.. module:: main.py

Initialization and runner for the HTTP server
"""
import asyncio
import logging
import pathlib
import aiohttp_jinja2
import jinja2
from aiohttp import web

from webapp.routes import setup_routes
from webapp import settings
from webapp import views


PROJ_ROOT = pathlib.Path(__file__).parent.parent


async def init(loop):
    """
    Sets up aiohttp-based web application, views and routes

    :param: loop
      Asyncio's event loop to pass into aiohttp web application
    """
    # Setup application and extensions
    app = web.Application(loop=loop)

    # Setup templates
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(
                                                   str(PROJ_ROOT/'templates')))

    # Setup views and routes
    setup_routes(app, views, PROJ_ROOT)

    return app, settings.HOST, settings.PORT


def main():
    """
    Main HTTP server runner
    """
    # Init logging
    logging.basicConfig(level=logging.DEBUG,
                        format=settings.LOGGING_FORMAT)

    # Start event loop and web server
    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
