from urllib.parse import urlparse, urljoin
from flask import request


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def check_for_existence(games, game_id):
    """
    This function checks whether a game of particular UUID exists.
    Thanks to using get() method we avoid exceptions here.
    :param dict games: This is a dictionary of games, where UUID is the key and Game object is a value.
    :param string game_id: UUID of a game to check for its existence.
    :return boolean: Returns True if the game exists and False otherwise.
    """
    if not games.get(game_id):
        return False
    return True


def check_for_guest(game):
    """
    This simple function checks whether there's a guest set for a particular game.
    :param Game game: A single Game object instance.
    :return boolean: Returns True if there's a guest and False otherwise.
    """
    if not game.guest:
        return False
    return True
