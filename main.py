from flask import Flask, request
import requests, json, os
from requests.auth import HTTPBasicAuth

app = Flask(__name__, static_url_path="/static")

def get_token():
  clientID = os.environ["CLIENT_ID"]
  clientSecret = os.environ["CLIENT_SECRET"]

  url = "https://accounts.spotify.com/api/token"
  data = {"grant_type":"client_credentials"}
  auth = HTTPBasicAuth(clientID, clientSecret)

  response = requests.post(url, data=data, auth=auth)
  accessToken = response.json()["access_token"]

  headers = {"Authorization": f"Bearer {accessToken}"}
  return headers

@app.route("/")
def index():
  page = ""
  with open("index.html", "r") as f:
    page = f.read()
  return page

@app.route("/year", methods=["GET", "POST"])
def year():
  form = request.form
  page = ""
  res = ""
  songs = ""
  with open("template.html", "r") as f:
    page += f.read()
    page = page.replace("{blank}", "Year")
    page = page.replace("{where}", "/year")
    page = page.replace("{form}", '<input type="text" name="year" placeholder="Enter a Year" pattern="\d{4}" maxlength="4">')
  with open("songs.html", "r") as f:
    songs += f.read()
  if len(form)==0:
    page = page.replace('{{year}}', "")
  else:
    year = form["year"]
    page = page.replace('{{year}}', f"<span class='cyear'><h3>Most Popular Songs in <span class='red'>{year}</span></h3></span>")
    search_url = f"https://api.spotify.com/v1/search?q=year:{year}&type=track&limit=10"
    headers = get_token()
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
      raise ValueError("Failed to search songs")
    data = json.loads(response.text)
    tracks = data["tracks"]["items"]
    for track in tracks:
      song = songs
      song = song.replace("{year}", year)
      song = song.replace("{artist}", track["artists"][0]["name"])
      song = song.replace("{track}", track['name'])
      song = song.replace("{preview}", track['preview_url'])
      song = song.replace("{album}", track['album']['name'])
      res += song
  page = page.replace("{content}", res)
  return page

@app.route("/artists", methods=["GET", "POST"]) 
def artists():
  pass
  form = request.form
  page = ""
  res = ""
  songs = ""
  with open("template.html", "r") as f:
    page += f.read()
    page = page.replace("{blank}", "Artist")
    page = page.replace("{where}", "/artists")
    page = page.replace("{form}", '<input type="text" name="artist" placeholder="Enter an Artist">')
  with open("songs.html", "r") as f:
    songs += f.read()
  if len(form)==0:
    page = page.replace('{{year}}', "")
  else:
    artist = form["artist"].title()
    page = page.replace('{{year}}', f"<span class='cyear'><h3>Most Popular Songs by <span class='red'>{artist}</span></h3></span>")
    search_url = f"https://api.spotify.com/v1/search?q=artist:{artist}&type=track&limit=10"
    headers = get_token()
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
      raise ValueError("Failed to search songs")
    data = json.loads(response.text)
    tracks = data["tracks"]["items"]
    for track in tracks:
      song = songs
      song = song.replace("{artist}", track["artists"][0]["name"])
      song = song.replace("{track}", track['name'])
      song = song.replace("{preview}", track['preview_url'])
      song = song.replace("{album}", track['album']['name'])
      res += song
  page = page.replace("{content}", res)
  return page
  
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)