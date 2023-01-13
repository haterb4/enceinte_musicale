import os

from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.utils import secure_filename

from recogition.recordCommandVoice import recordVoice
from recogition.translateAudio import translateSpeechToText
from player.player import MusicIndexer, MusicPlayer
import time
from constant import AUDIO_FOLDER

Indexer = MusicIndexer(AUDIO_FOLDER)
player = MusicPlayer(Indexer)


app = Flask(__name__)

app.config['MAX_CONTENT_PATH'] = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = "worker/musics"
app.config["SECRET_KEY"] = '571ebf8e13ca209536c29be68d435c00'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///registration.db'
db = SQLAlchemy(app)
app.app_context().push()

db.create_all()


# create user table with required field
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)
    user_password = db.Column(db.String(150), nullable=False)

    def __iter__(self):
        yield from {
            "id": self.id,
            "username": self.username,
            "user_email": self.user_email
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def toJson(self):
        return {"id": id, "username": self.username, "email": self.user_email}


# create user table with required field
class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(150), nullable=False)
    filename = db.Column(db.String(150), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    play_lists = relationship('Playlist', secondary='music_playlist')

    def toJson(self):
        return {"id": id, "name": self.name, "author": self.author, "album": self.album, "user_id": self.user_id}


class music_playlist(db.Model):
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'), primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), primary_key=True)


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    musics = db.relationship('Music', secondary='music_playlist')

    def toJson(self):
        return {"id": id, "title": self.title, "user_id": self.user_id}

    def __repr__(self):
        return f'<Playlist "{self.title}">'


@app.route('/add-to-playlist/<int:music_id>/<int:playlist_id>/', methods=['POST'])
def add_music_in_playlist(music_id, playlist_id):
    music = Music.query.get_or_404(music_id)
    playlist = Playlist.query.get_or_404(playlist_id)
    playlist.musics.append(music)

    db.session.add(playlist)
    db.session.commit()

    response = app.response_class(
        response=json.dumps("added"),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/remove-to-playlist/<int:music_id>/<int:playlist_id>/', methods=['PUT'])
def remove_music_in_playlist(music_id, playlist_id):

    link = music_playlist.query.filter_by((music_id, playlist_id))
    db.session.delete(link)
    db.session.commit()

    response = app.response_class(
        response=json.dumps("removed"),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/musics')
def musics():
    musics = Music.query.order_by(Music.id.desc()).all()
    res = []

    for music in musics:
        res.append({"id": music.id, "name": music.name, "author": music.author, "album": music.album,
                    "filename": music.filename}
                   )

    return app.response_class(
        response=json.dumps(res),
        status=200,
        mimetype='application/json'
    )


@app.route('/users')
def users():
    users = User.query.all()
    res = []

    for user in users:
        res.append({"id": user.id, "username": user.username, "email": user.user_email})

    return app.response_class(
        response=json.dumps(res),
        status=200,
        mimetype='application/json'
    )


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return app.response_class(
        status=200,
        mimetype='application/json'
    )


@app.route("/register", methods=["POST"])
def register():
    # check the request method to ensure the handling of POST request only

    data = request.get_json()
    # store the form value
    user_name = data["username"]
    email = data["email"]
    password = data["password"]

    # create an instance of the user table
    user = User(username=user_name, user_email=email, user_password=password)

    # add the user object to the database
    db.session.add(user)

    # commit changes to the database
    db.session.commit()

    response = app.response_class(
        response=json.dumps("created"),
        status=201,
        mimetype='application/json'
    )
    return response


@app.route("/create-playlist/<int:user_id>", methods=["POST"])
def create_playlist(user_id):
    # check the request method to ensure the handling of POST request only
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    # store the form value
    title = data["title"]

    # create an instance of the user table
    pl = Playlist(title=title, user_id=user.id)

    # add the user object to the database
    db.session.add(pl)

    # commit changes to the database
    db.session.commit()

    res = {"id": pl.id, "title": pl.title, "user_id": pl.user_id}

    return app.response_class(
        response=json.dumps(res),
        status=201,
        mimetype='application/json'
    )


@app.route("/create-music/<int:user_id>", methods=["POST"])
def create_music(user_id):
    # check the request method to ensure the handling of POST request only

    user = User.query.get_or_404(user_id)
    # data = request.form()
    # store the form value
    name = request.form["name"]
    author = request.form["author"]
    album = request.form["album"]

    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # create an instance of the user table
    music = Music(name=name, author=author, album=album, filename=filename)
    music.user_id = user.id

    # add the user object to the database
    db.session.add(music)

    # commit changes to the database
    db.session.commit()

    res = {"id": music.id, "name": music.name, "author": music.author, "album": music.album, "filename": music.filename}

    response = app.response_class(
        response=json.dumps(res),
        status=201,
        mimetype='application/json'
    )
    return response


@app.route("/login", methods=["POST"])
def login():
    # check the request method to ensure the handling of POST request only

    data = request.get_json()
    # store the form value
    user_name = data["username"]
    password = data["password"]

    # create an instance of the user table
    user = User.query.filter_by(username=user_name, user_password=password).first()
    res_data = {"id": user.id, "username": user.username, "email": user.user_email, }

    response = app.response_class(
        response=json.dumps(res_data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    # check the request method to ensure the handling of POST request only
    user = User.query.get_or_404(user_id)
    res = {"id": user.id, "username": user.username, "email": user.user_email}

    response = app.response_class(
        response=json.dumps(res),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/musics/<int:music_id>", methods=["GET"])
def get_music_by_id(music_id):
    # check the request method to ensure the handling of POST request only
    music = Music.query.get_or_404(music_id)
    res = {"id": music.id, "name": music.name, "author": music.author, "album": music.album, "filename": music.filename}

    response = app.response_class(
        response=json.dumps(res),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/search-musics", methods=["POST"])
def get_search_music_by_id():
    # check the request method to ensure the handling of POST request only

    data = request.get_json()
    # store the form value
    name = data["name"]

    musics =  db.session.query(Music).filter(Music.filename.contains(name + '%')).all()
    #Music.query.filter_by(name=name).all()
    res = []

    for music in musics:
        res.append({"id": music.id, "name": music.name, "author": music.author, "album": music.album,
                    "filename": music.filename})

    response = app.response_class(
        response=json.dumps(res),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/playlist/<int:playlist_id>", methods=["GET"])
def get_playlist_by_id(playlist_id):
    # check the request method to ensure the handling of POST request only
    pl = Playlist.query.get_or_404(playlist_id)

    musics = db.session.query(Music).filter(music_playlist.playlist_id == playlist_id).order_by(music_playlist.music_id).all()

    res_musics = []

    for music in musics:
        res_musics.append({"id": music.id, "name": music.name, "author": music.author, "album": music.album,
                           "filename": music.filename}
                          )

    res = {"id": pl.id, "title": pl.title, "user_id": pl.user_id, "musics": res_musics}
    response = app.response_class(
        response=json.dumps(res),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/users-musics/<int:user_id>", methods=["GET"])
def all_user_music(user_id):
    # check the request method to ensure the handling of POST request only
    musics = Music.query.filter_by(user_id=user_id).all()

    res = []

    for music in musics:
        res.append({"id": music.id, "name": music.name, "author": music.author, "album": music.album,
                    "filename": music.filename})

    return app.response_class(
        response=json.dumps(res),
        status=200,
        mimetype='application/json'
    )


@app.route("/users-playlists/<int:user_id>", methods=["GET"])
def all_user_playlist(user_id):
    # check the request method to ensure the handling of POST request only
    playlists = Playlist.query.filter_by(user_id=user_id).all()

    res = []

    for pl in playlists:
        res.append({"id": pl.id, "title": pl.title, "user_id": pl.user_id})

    return app.response_class(
        response=json.dumps(res),
        status=200,
        mimetype='application/json'
    )

#jouer une musique
@app.route("/musics/play_music", methods=["GET"])
def play_music():
    player.next_song()
    return {
        "status": "success"
    }
#mettre en pause
@app.route("/musics/pause_music", methods=["GET"])
def pause_music():
    player.pause_song()
    return {
        "status": "success"
    }

#reprendre la musique en pause
@app.route("/musics/resume_music", methods=["GET"])
def resume_music():
    player.resume_song()
    return {
        "status": "success"
    } 
    
#morceau suivant
@app.route("/musics/next_music", methods=["GET"])
def next_music():
    player.next_song()
    return {
        "status": "success"
    }
#morceau precedent
@app.route("/musics/prev_music", methods=["GET"])
def prev_music():
    player.prev_song()
    return {
        "status": "success"
    }

#morceau precedent
@app.route("/musics/prev_music", methods=["GET"])
def prev_music(file_list):
    random.shuffle(file_list)
    pygame.mixer.music.load(file_list[songNumber])
    pygame.mixer.music.play(1)

    for num, song in enumerate(file_list):
        if num == songNumber:
            continue # already playing
        pygame.mixer.music.queue(song)
    return {
        "status": "success"
    }    

def init_db():
    db.create_all()

    # Create a test user
    new_user = User(username="isis", user_email="isis", user_password="isis")
    db.session.add(new_user)
    db.session.commit()


if __name__ == '__main__':
    db.init_app(app)
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)


