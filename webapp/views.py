"""
.. module:: views.py

HTTP server views
"""
import json
from aiohttp import web
import aiohttp_jinja2
from webapp import spotify


@aiohttp_jinja2.template("index.html")
async def index(request):
    """
    Index page and Spotify search

    :param: q
      Spotify API "q" paramer, a search string, from GET
    :param: types
      Spotify API "types" parameter, array-like parameter from GET
    """
    data = []
    error_message = None
    counter = -1
    q = request.GET.get('q')
    types = request.GET.getall('types', [])
    if q:
        if types:
            try:
                data = await spotify.search(q, types)
                data = spotify.aggregate(data)
                counter = len(data)
            except spotify.SpotifyError as e:
                error_message = e.message
        else:
            error_message = "Please select a type"
    return {"data": data,
            "q": q,
            "types": types,
            "error_message": error_message,
            "counter": counter}


async def search(request):
    """
    API endpoint to search against Spotify

    :param: q
      Spotify API "q" paramer, a search string
    :param: types
      Spotify API "types" paramer, a comma-separated list of types
    """
    q = request.GET.get('q')
    types = request.GET.get('types')
    if types:
        types = types.split(",")
    data = []
    try:
        data = await spotify.search(q, types)
    except spotify.SpotifyError as e:
        raise web.HTTPBadRequest(text=json.dumps({"error": e.message}),
                                 content_type="application/json")
    return web.Response(text=json.dumps({'data': data}),
                        content_type="application/json")
