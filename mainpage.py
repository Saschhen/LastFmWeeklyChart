from flask import Flask, render_template
import requests


app = Flask(__name__)
app.debug = True

def get_data():
    url = "http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=6c08b2f4e48e2262e18b4e1829dabb86&format=json"
    r = requests.get(url)
    return r.json()

def get_track_list(json):
    track_dict = {}
    for i in range(len(json["tracks"]["track"])):
        track_name = json["tracks"]["track"][i]["name"]
        listener_name = json["tracks"]["track"][i]["listeners"]
        artist_name = json["tracks"]["track"][i]["artist"]
        track_dict[track_name] = [listener_name, artist_name]
    return track_dict


def new_data():
    url = "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=rj&api_key=6c08b2f4e48e2262e18b4e1829dabb86&format=json"
    a = requests.get(url)
    return a.json()


def get_artist_list(json):
    artist_list = []
    playcount_list = []
    for i in range(len(json["topartists"]["artist"])):
        artist_name = json["topartists"]["artist"][i]["name"]
        playcount_name = json["topartists"]["artist"][i]["playcount"]
        artist_list.append(artist_name)
        playcount_list.append(playcount_name)
    return zip(artist_list, playcount_list)


@app.route('/')
def main_page():
    return render_template("main_page.html")

@app.route('/chart')
def my_page():
    data=get_data()
    track_list=get_track_list(data)
    return render_template("my_page.html",
                           data=track_list)


@app.route('/song/<int:n>')
def show_song(n):
    track_list = get_track_list(get_data())
    data = track_list
    return render_template("show_song.html",
                           data=data)


@app.route('/topartist')
def show_artist():
    return render_template("show_artist.html",
                           data=get_artist_list(new_data()))






if __name__ == '__main__':
    app.run()