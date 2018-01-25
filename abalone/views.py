import math
import uuid
from abalone import app
from .logic import Game, Board
from flask import render_template, request, redirect, url_for, flash

app.secret_key = 'C~\xb2\x95\x00:\xca\xc8b\x83\x89\xee\xf7)w&\xed\x96\xbe\x13\xfd\x88\x92\x81'

games = dict()
board = Board.Board()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST', 'GET'])
def start():
    if request.method == 'POST':
        name = request.form['name']
        gametype = request.form['gametype']
        if name and gametype:
            return redirect(url_for('create', name=name))
    return render_template('start.html')


@app.route('/o-grze')
def about():
    return render_template('about.html')


@app.route('/create/<string:name>')
def create(name):
    game_id = str(uuid.uuid4())
    games[game_id] = (Game.Game(name))
    flash('Game started!', 'success')

    return redirect(url_for('game', game_id=game_id))


@app.route('/games')
def active_games():
    return render_template('games.html', games=games)


@app.route('/game/<string:game_id>')
def game(game_id):
    """
    A basic view that just generates the board.
    :return render_template():
    """
    if games.get(game_id):
        return render_template('board.html', game_id=game_id)
    else:
        flash('Such a game does not exist. It might have ended.', 'error')
    return redirect(url_for('index'))


@app.route('/game/<string:game_id>/select/<int:coordinate_x>/<int:coordinate_y>/<int:coordinate_z>')
def select(game_id, coordinate_x, coordinate_y, coordinate_z):
    """
    A view that handles player selecting one of his pieces.
    :param int game_id: This is an id of a game.
    :param int coordinate_x: This is a x coordinate of the piece that player selected.
    :param int coordinate_y: This is a y coordinate of the piece that player selected.
    :param int coordinate_z: This is a z coordinate of the piece that player selected.
    :return render_template():
    """

    return render_template('board.html', game_id=game_id, coordinate_x=coordinate_x, coordinate_y=coordinate_y,
                           coordinate_z=coordinate_z)


@app.route('/game/<string:game_id>/select/<int:coordinate_x>/<int:coordinate_y>/<int:coordinate_z>/'
           '<int:second_x>/<int:second_y>/<int:second_z>')
def select_multiple(game_id, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z):
    """
    A view that handles player selecting one of his pieces.
    :param int coordinate_x: This is a x coordinate of the piece that player selected.
    :param int coordinate_y: This is a y coordinate of the piece that player selected.
    :return render_template():
    """

    return render_template('board.html', game_id=game_id, coordinate_x=coordinate_x, coordinate_y=coordinate_y,
                           coordinate_z=coordinate_z, second_x=second_x, second_y=second_y, second_z=second_z)


@app.route('/game/<string:game_id>/select/<int:coordinate_x>/<int:coordinate_y>/<int:coordinate_z>/move/<int:to_x>/'
           '<int:to_y>/<int:to_z>')
def move(game_id, coordinate_x, coordinate_y, coordinate_z, to_x, to_y, to_z):

    if (coordinate_x, coordinate_y, coordinate_z) in games[game_id].player_white.positions:
        games[game_id].player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
        games[game_id].player_white.positions.add((to_x, to_y, to_z))
    elif (coordinate_x, coordinate_y, coordinate_z) in games[game_id].player_black.positions:
        games[game_id].player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
        games[game_id].player_black.positions.add((to_x, to_y, to_z))

    return redirect(url_for('game', game_id=game_id))


@app.route('/game/<string:game_id>/select/<int:coordinate_x>/<int:coordinate_y>/<int:coordinate_z>/<int:second_x>/'
           '<int:second_y>/<int:second_z>/move/<int:to_x>/<int:to_y>/<int:to_z>')
def move_double(game_id, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x, to_y, to_z):

    if (coordinate_x, coordinate_y, coordinate_z) in games[game_id].player_white.positions and \
            (second_x, second_y, second_z) in games[game_id].player_white.positions and\
            ((math.fabs(coordinate_x - second_x) == 2 and ((math.fabs(coordinate_y - second_y) == 2 or
                                                            math.fabs(coordinate_z - second_z) == 2)))) \
            or ((math.fabs(coordinate_y - second_y) == 2 and ((math.fabs(coordinate_x - second_x) == 2
                                                               or math.fabs(coordinate_z - second_z) == 2)))) \
            or ((math.fabs(coordinate_z - second_z) == 2 and ((math.fabs(coordinate_y - second_y) == 2
                                                               or math.fabs(coordinate_x - second_x) == 2)))):

        if math.fabs(to_y - coordinate_y) < math.fabs(to_y - second_y) or math.fabs(to_x - coordinate_x) < math.fabs(
                to_x - second_x):
            #player_white.positions.remove((second_x, second_y, second_z))
            games[game_id].player_white.positions.add((to_x, to_y, to_z))

        elif math.fabs(to_y - second_y) < math.fabs(to_y - coordinate_y) or math.fabs(to_x - second_x) < math.fabs(
                to_x - coordinate_x):
            #player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
            games[game_id].player_white.positions.add((to_x, to_y, to_z))

    elif (coordinate_x, coordinate_y, coordinate_z) in games[game_id].player_black.positions and \
            (second_x, second_y, second_z) in games[game_id].player_black.positions and \
            ((math.fabs(coordinate_x - second_x) == 2 and ((math.fabs(coordinate_y - second_y) == 2 or
                                                            math.fabs(coordinate_z - second_z) == 2)))) \
            or ((math.fabs(coordinate_y - second_y) == 2 and ((math.fabs(coordinate_x - second_x) == 2
                                                               or math.fabs(coordinate_z - second_z) == 2)))) \
            or ((math.fabs(coordinate_z - second_z) == 2 and ((math.fabs(coordinate_y - second_y) == 2
                                                               or math.fabs(coordinate_x - second_x) == 2)))):

        if math.fabs(to_y - coordinate_y) < math.fabs(to_y - second_y) or math.fabs(to_x - coordinate_x) < math.fabs(
                to_x - second_x):
            #player_black.positions.remove((second_x, second_y, second_z))
            games[game_id].player_black.positions.add((to_x, to_y, to_z))


        elif math.fabs(to_y - second_y) < math.fabs(to_y - coordinate_y) or math.fabs(to_x - second_x) < math.fabs(
                to_x - coordinate_x):
            #player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
            games[game_id].player_black.positions.add((to_x, to_y, to_z))

    elif (coordinate_x, coordinate_y, coordinate_z) in games[game_id].player_white.positions and (second_x, second_y, second_z) \
            in games[game_id].player_white.positions and math.fabs(coordinate_x - second_x) < 2 and \
            math.fabs(coordinate_y - second_y) < 2 and math.fabs(coordinate_z - second_z) < 2:

        if math.fabs(to_y - coordinate_y) < math.fabs(to_y - second_y) or math.fabs(to_x - coordinate_x) < math.fabs(to_x - second_x):
            games[game_id].player_white.positions.remove((second_x, second_y, second_z))
            games[game_id].player_white.positions.add((to_x, to_y, to_z))

        elif math.fabs(to_y - second_y) < math.fabs(to_y - coordinate_y) or math.fabs(to_x - second_x) < math.fabs(to_x - coordinate_x):
            games[game_id].player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
            games[game_id].player_white.positions.add((to_x, to_y, to_z))

    elif (coordinate_x, coordinate_y, coordinate_z) in games[game_id].player_black.positions and (second_x, second_y, second_z) \
            in games[game_id].player_black.positions and math.fabs(coordinate_x - second_x) < 2 and \
            math.fabs(coordinate_y - second_y) < 2 and math.fabs(coordinate_z - second_z) < 2:

        if math.fabs(to_y - coordinate_y) < math.fabs(to_y - second_y) or math.fabs(to_x - coordinate_x) < math.fabs(to_x - second_x):
            games[game_id].player_black.positions.remove((second_x, second_y, second_z))
            games[game_id].player_black.positions.add((to_x, to_y, to_z))

        elif math.fabs(to_y - second_y) < math.fabs(to_y - coordinate_y) or math.fabs(to_x - second_x) < math.fabs(to_x - coordinate_x):
            games[game_id].player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
            games[game_id].player_black.positions.add((to_x, to_y, to_z))

    return redirect(url_for('game', game_id=game_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.context_processor
def utility_processor():

    def count_yz(row, column, which):
        if row <= 4:
            coordinates = {'y': column, 'z': column + (4 - row)}
        else:
            coordinates = {'y': column + (row - 4), 'z': column}

        if which == 'y':
            return coordinates.get('y')
        elif which == 'z':
            return coordinates.get('z')

    rule = str(request.url_rule)

    if 'game/' in rule:
        s = request.url.split('/')
        game_id = s[s.index('game') + 1]
        return dict(
            count_yz=count_yz,
            rule=rule,
            name=games[game_id].name,
            board={'rows': games[game_id].rows, 'columns': games[game_id].columns},
            player_black=games[game_id].player_black,
            player_white=games[game_id].player_white,
            )
    else:
        return dict(
            rule=rule
        )


