import uuid
from flask import render_template, request, redirect, url_for, flash, g, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from abalone import app, db, bcrypt, login_manager
from .logic import Game, Board
from .logic.User import User
from .logic.Utils import is_safe_url, check_for_existence, check_for_guest

games = dict()
board = Board.Board()

login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    registered_user = User.query.filter_by(username=username).first()

    if registered_user is None or not bcrypt.check_password_hash(registered_user.password, request.form['password']):
        flash('Username or password is invalid', 'error')
        return redirect(url_for('login'))

    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    login_user(registered_user, remember=remember_me)
    flash('Logged in successfully!', 'success')

    next = request.args.get('next')
    if not is_safe_url(next):
        return abort(400)
    return redirect(next or url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        error = dict()
        if request.form['username'] and request.form['password'] and request.form['repeat-password']:
            if len(request.form['password']) < 6:
                error['password-short'] = 'Password must be at least 6 characters long.'
                flash(error['password-short'], 'error')
            if request.form['password'] != request.form['repeat-password']:
                error['password-different'] = 'Passwords do not match.'
                flash(error['password-different'], 'error')

            password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            user = User(request.form['username'], password)
            try:
                db.session.add(user)
                db.session.commit()
                flash('Registered in successfully.', 'success')
                return redirect(url_for('index'))
            except IntegrityError:
                db.session.rollback()
                error['username-taken'] = 'This username is already taken.'
                flash(error['username-taken'], 'error')

            return render_template('register.html', error=error)
        else:
            flash('Fill all the inputs, please.', 'error')
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route('/start', methods=['POST', 'GET']) # new_game
@login_required
def start():

    if request.method == 'POST':
        name = request.form['name']
        creator = current_user.id
        game_id = str(uuid.uuid4())
        games[game_id] = (Game.Game(game_id, name, creator))
        if not games[game_id].save_game():
            flash('Error occurred while saving the game!', 'error')
        return redirect(url_for('game', game_id=game_id))
    return render_template('start.html')


@app.route('/o-grze')
def about():
    return render_template('about.html')


@app.route('/active_games')
@login_required
def active_games():
    join_games = dict()
    for single_game in games:
        if games[single_game].guest is False and current_user.id != games[single_game].creator:
            join_games[single_game] = games[single_game]
    return render_template('games.html', games=join_games)


@app.route('/my_games')
@login_required
def my_games():
    own_games = dict()
    for single_game in games:
        if current_user.id == games[single_game].creator or current_user.id == games[single_game].guest:
            own_games[single_game] = games[single_game]
    return render_template('my_games.html', games=own_games)


@app.route('/game/<string:game_id>')
@login_required
def game(game_id):
    """
    A basic view that just generates the board.
    :return render_template():
    """

    if games.get(game_id):
        games[game_id].check_end_of_game(games[game_id].points_for_black, games[game_id].points_for_white)
        if games[game_id].finish == 1:
            flash('Uzytkownik grający czarnymi kulkami wygrał', 'success')
        elif games[game_id].finish == 2:
            flash('Uzytkownik grający białymi kulkami wygrał', 'success')
        elif games[game_id].finish == 3:
            flash('Remis', 'success')
        return render_template('board.html', game_id=game_id)
    elif not check_for_existence(games, game_id):
        flash('Gra nie istnieje', 'error')
    return redirect(url_for('index'))


@app.route('/game/<string:game_id>/join')
@login_required
def join(game_id):
    if check_for_existence(games, game_id):
        # No guest and current_user is not creator. All is OK.
        if games[game_id].guest is False and current_user.id != games[game_id].creator:
            games[game_id].set_guest(current_user.id)
            games[game_id].save_timestamp()
            if not games[game_id].save_game():
                flash('Error occurred while saving the game!', 'error')
            return redirect(url_for('game', game_id=game_id))
        # There is a guest, or no guest and current_user is creator. Not OK to join.
        elif games[game_id].guest is True or current_user.id == games[game_id].creator:
            flash('Nie możesz dołączyć do tej gry!', 'error')
            return redirect(url_for('game', game_id=game_id))
    else:
        flash('Podana gra nie istnieje', 'error')
    return redirect(url_for('index'))


@app.route('/game/<string:game_id>/select/<int:coordinate_x>/<int:coordinate_y>/<int:coordinate_z>')
@login_required
def select(game_id, coordinate_x, coordinate_y, coordinate_z):
    """
    A view that handles player selecting one of his pieces.
    :param int game_id: This is an id of a game.
    :param int coordinate_x: This is a x coordinate of the piece that player selected.
    :param int coordinate_y: This is a y coordinate of the piece that player selected.
    :param int coordinate_z: This is a z coordinate of the piece that player selected.
    :return render_template():{{ url_for('index') }}"
    """
    if not check_for_guest(games[game_id]):
        flash('You must first have an opponent to play with!', 'error')
    else:
        games[game_id].check_end_of_game(games[game_id].points_for_black, games[game_id].points_for_white)
        if games[game_id].finish == 0:
            if games[game_id].select(coordinate_x, coordinate_y, coordinate_z, current_user.id):
                return render_template('board.html', game_id=game_id, coordinate_x=coordinate_x, coordinate_y=coordinate_y,
                                        coordinate_z=coordinate_z)
        elif games[game_id].finish == 1:
            flash('Uzytkownik grający czarnymi kulkami wygrał', 'success')
        elif games[game_id].finish == 2:
            flash('Uzytkownik grający białymi kulkami wygrał', 'success')
        elif games[game_id].finish == 3:
            flash('Remis', 'success')
    return redirect(url_for('game', game_id=game_id))


@app.route('/game/<string:game_id>/select/<int:coordinate_x>/<int:coordinate_y>/<int:coordinate_z>/'
           '<int:second_x>/<int:second_y>/<int:second_z>')
@login_required
def select_multiple(game_id, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z):
    """
    A view that handles player selecting one of his pieces.
    :param int coordinate_x: This is a x coordinate of the piece that player selected.
    :param int coordinate_y: This is a y coordinate of the piece that player selected.
    :return render_template():
    """
    if not check_for_guest(games[game_id]):
        flash('You must first have an opponent to play with!', 'error')

    else:
        games[game_id].check_end_of_game(games[game_id].points_for_black, games[game_id].points_for_white)
        if games[game_id].finish == 0:
            if games[game_id].select_multiple(coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, current_user.id):
                return render_template('board.html', game_id=game_id, coordinate_x=coordinate_x, coordinate_y=coordinate_y,
                                       coordinate_z=coordinate_z, second_x=second_x, second_y=second_y, second_z=second_z)
            else:
                flash('Zły select', 'error')
        elif games[game_id].finish == 1:
            flash('Uzytkownik grający czarnymi kulkami wygrał', 'success')
            return redirect(url_for('game', game_id=game_id))
        elif games[game_id].finish == 2:
            flash('Uzytkownik grający białymi kulkami wygrał', 'success')
            return redirect(url_for('game', game_id=game_id))
        elif games[game_id].finish == 3:
            flash('Remis', 'success')
            return redirect(url_for('game', game_id=game_id))
        return redirect(url_for('select', game_id=game_id, coordinate_x=coordinate_x, coordinate_y=coordinate_y,
                                coordinate_z=coordinate_z))
    return redirect(url_for('game', game_id=game_id))


@app.route('/game/<string:game_id>/select/<int:coordinate_x>/<int:coordinate_y>/<int:coordinate_z>/move/<int:to_x>/'
           '<int:to_y>/<int:to_z>')
@login_required
def move(game_id, coordinate_x, coordinate_y, coordinate_z, to_x, to_y, to_z):
    if not check_for_guest(games[game_id]):
        flash('You must first have an opponent to play with!', 'error')
    else:
        games[game_id].check_end_of_game(games[game_id].points_for_black, games[game_id].points_for_white)
        if games[game_id].finish == 0:
            if games[game_id].move(coordinate_x, coordinate_y, coordinate_z, to_x, to_y, to_z):
                games[game_id].change_turn()
            else:
                flash('Zły ruch', 'error')
        elif games[game_id].finish == 1:
            flash('Uzytkownik grający czarnymi kulkami wygrał')
        elif games[game_id].finish == 2:
            flash('Uzytkownik grający białymi kulkami wygrał')
        elif games[game_id].finish == 3:
            flash('Remis', 'success')
    return redirect(url_for('game', game_id=game_id))


@app.route('/game/<string:game_id>/select/<int:coordinate_x>/<int:coordinate_y>/<int:coordinate_z>/<int:second_x>/'
           '<int:second_y>/<int:second_z>/move/<int:to_x>/<int:to_y>/<int:to_z>')
@login_required
def move_multiple(game_id, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x, to_y, to_z):
    if not check_for_guest(games[game_id]):
        flash('You must first have an opponent to play with!', 'error')
    else:
        games[game_id].check_end_of_game(games[game_id].points_for_black, games[game_id].points_for_white)
        if games[game_id].finish == 0:
            if games[game_id].move_multiple(coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                            to_y, to_z):
                games[game_id].change_turn()
            else:
                flash('Zły ruch', 'error')
        elif games[game_id].finish == 1:
            flash('Uzytkownik grający czarnymi kulkami wygrał','success')
        elif games[game_id].finish == 2:
            flash('Uzytkownik grający białymi kulkami wygrał', 'success')
        elif games[game_id].finish == 3:
            flash('Remis', 'success')
    return redirect(url_for('game', game_id=game_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/_check_timestamp')
def check_timestamp():
    game_id = request.args.get('game_id', '0', type=str)
    if game_id in games:
        return jsonify(timestamp=games[game_id].get_timestamp())

    return jsonify(timestamp=0, error='Could not get the timestamp!')


@app.before_request
def before_request():
    g.user = current_user


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
            game_id=game_id,
            url=request.url,
            count_yz=count_yz,
            rule=rule,
            name=games[game_id].name,
            board={'rows': games[game_id].rows, 'columns': games[game_id].columns},
            player_black=games[game_id].player_black,
            player_white=games[game_id].player_white,
            turn=games[game_id].turn,
            points_for_black=games[game_id].points_for_black,
            points_for_white=games[game_id].points_for_white,
            finish=games[game_id].finish,
            creator=User.query.filter_by(id=games[game_id].creator).first(),
            guest=User.query.filter_by(id=games[game_id].guest).first(),
            game=games[game_id]

            )
    else:
        return dict(
            rule=rule
        )


