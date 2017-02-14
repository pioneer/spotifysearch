"""
.. module:: spotify.py

A small wrapper around Spotify API, to reuse in asyncio-based applications
"""
import urllib.parse
import asyncio
import aiohttp


SPOTIFY_URL = "https://api.spotify.com/v1/search"
SPOTIFY_SEARCH_TYPES = ("album", "artist", "playlist", "track")


class SpotifyError(Exception):
    message = "A Spotify API call error occured"

    def __init__(self, data=None, *args, **kwargs):
        super(SpotifyError, self).__init__(*args, **kwargs)
        self.data = data


class SpotifyEmptyQueryError(SpotifyError):
    message = "Spotify search query shoudn't be empty"


class SpotifyIncorrectTypesError(SpotifyError):
    message = "Spotify types should be ones from a list of: {}"\
                                                .format(SPOTIFY_SEARCH_TYPES)


async def search(q, types):
    """
    Spotify search API endpoint wrapper

    :param: q
      Spotify API "q" paramer, a search string
    :param: types
      Spotify API "types" paramer, a comma-separated list of types
    """
    if not q:
        raise SpotifyEmptyQueryError
    if not types:
        raise SpotifyIncorrectTypesError(types)
    for t in types:
        if t not in SPOTIFY_SEARCH_TYPES:
            raise SpotifyIncorrectTypesError(t)
    response = await aiohttp.get(SPOTIFY_URL,
                                 params={"q": urllib.parse.quote(q),
                                         "type": ",".join(types)})
    if not response.status == 200:
        raise SpotifyError(await response.text())
    return await response.json()


def aggregate(data):
    """
    Aggregate Spotify search results

    :param: data
      data from a Spotify search
    """
    def extract_item(item):
        KEYS = ("id", "name", "type")
        data = {k: item[k] for k in KEYS}
        data["href"] = item['external_urls']['spotify']
        image_url = None
        for img in item["images"]:
            image_url = img["url"]
            if img["width"] == 64:  # we focus just on that size currently
                break
        if image_url:
            data["image_url"] = image_url
        return data

    return [extract_item(item)
            for t in SPOTIFY_SEARCH_TYPES
            for item in data.get(t + "s", {"items": []})["items"]]


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        content = loop.run_until_complete(search("Bob Dylan",
                                                 ["artist", "album"]))
        import pprint
        pprint.pprint(content)
    except Exception as e:
        print(type(e), e.message, e.data)
