import re
from flask import Flask, render_template, request
import api_integration

with open("app_info.txt", "r") as info_txt:
    lines = info_txt.readlines()
    CLIENT_ID = re.split(r'\W',lines[0])[1]
    CLIENT_SECRET = re.split(r'\W',lines[1])[1]

spotify = api_integration.Client(CLIENT_ID, CLIENT_SECRET)
app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        artist_info = spotify.get_random_artist()
        return render_template('result.html', artist_name=artist_info['artists']['items'][0]['name'],
         spotify_link=artist_info['artists']['items'][0]['external_urls']['spotify'])
    else:
        return render_template('index.html')
    

if __name__ == "__main__":
    app.run(debug=True)
