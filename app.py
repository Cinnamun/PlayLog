from flask import Flask, render_template, jsonify, json, url_for, redirect, session, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
import datetime

# Enable CORS for all routes
app = Flask(__name__)
CORS(app)
app.secret_key = "your_secret_key"

# Database
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://cinnamun:fNr8KYsdYEMvECQwwidIXETheFKnDQTk@dpg-cmhlns7qd2ns73ft8os0-a.oregon-postgres.render.com/playlog"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://cinnamun:fNr8KYsdYEMvECQwwidIXETheFKnDQTk@dpg-cmhlns7qd2ns73ft8os0-a/playlog"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# User model for sql alchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    username = db.Column(db.Text)
    pfp = db.Column(db.Text)
    top_tracks = db.Column(db.Text)
    top_artists = db.Column(db.Text)
    recently_played = db.Column(db.Text)

# Store data in database
def store_data(email, username, pfp, top_tracks, top_artists, recently_played):
    # Check if user already exists
    user = User.query.filter_by(email=email).first()
    if user:
        # Update user data if user exists
        user.pfp = pfp
        user.top_tracks = top_tracks
        user.top_artists = top_artists
        user.recently_played = recently_played
    else:
        # Create new user data if user doesn't exist
        new_user = User(email=email, username=username, pfp=pfp, top_tracks=top_tracks, top_artists=top_artists, recently_played=recently_played)
        db.session.add(new_user)
    db.session.commit()

# Login or root
@app.route("/")
def index():
    return render_template("login.html")

# Get user data
@app.route("/callback")
def callback():
    # redirect_uri = "http://localhost:5000/callback"
    redirect_uri = "https://playlog.onrender.com/callback"

    # Spotify callback and get user data
    code = request.args.get("code")
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": "7351837820d04a438ea8fa4081178723",
        "client_secret": "34469924b9a24d6c82c60f2588fe973c",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    api_url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_data = requests.get(api_url, headers=headers).json()

    # Email, username and profile picture
    email = user_data["email"]
    username = user_data["display_name"]
    pfp = next((image["url"] for image in user_data.get("images", []) if image["height"] >= 200), None)

    # Top tracks
    top_tracks_response = requests.get(f"{api_url}/top/tracks?limit=20&time_range=short_term", headers={"Authorization": f"Bearer {access_token}"})
    top_tracks_data = top_tracks_response.json()
    top_tracks = json.dumps([
        {
            "name": track["name"],
            "artist": track["artists"][0]["name"], 
            "played_count": track["popularity"],
            "image_url": track["album"]["images"][0]["url"],
            "song_link": f'https://open.spotify.com/track/{track.get("id", "")}'
        }
        for track in top_tracks_data["items"]
    ])
    
    # Top artists
    top_artists_response = requests.get(f"{api_url}/top/artists?limit=20&time_range=short_term", headers={"Authorization": f"Bearer {access_token}"})
    top_artists_data = top_artists_response.json()
    top_artists = json.dumps([
        {
            "name": artist["name"],
            "image_url": artist["images"][0]["url"],
            "artist_link": f'https://open.spotify.com/artist/{artist.get("id", "")}'
        }
        for artist in top_artists_data["items"]
    ])
    
    # Recently played
    recently_played_response = requests.get(f"{api_url}/player/recently-played?limit=20", headers={"Authorization": f"Bearer {access_token}"})
    recently_played_data = recently_played_response.json()
    recently_played = json.dumps([
        {
            "name": track["track"]["name"],
            "artist": track["track"]["artists"][0]["name"],
            "image_url": track["track"]["album"]["images"][0]["url"],
            "played_datetime": datetime.datetime.fromisoformat(track["played_at"][:-1]),
            "song_link": f'https://open.spotify.com/track/{track["track"].get("id", "")}'
            }
            for track in recently_played_data["items"]
    ])
    
    # Store data in database
    store_data(email, username, pfp, top_tracks, top_artists, recently_played)

    # Set user session and redirect to profile
    session["user_email"] = email
    return redirect(url_for("profile"))

# Profile
@app.route("/profile")
def profile():
    # Get user data from database using session
    if "user_email" in session:
        user = User.query.filter_by(email=session["user_email"]).first()
        user_data = {
            "email": user.email,
            "username": user.username,
            "pfp": user.pfp
        }
        top_tracks = user.top_tracks
        top_artists = user.top_artists
        recently_played = user.recently_played

        # Pass data to profile
        return render_template("profile.html", user_data=user_data, top_tracks=top_tracks, top_artists=top_artists, recently_played=recently_played)
    else:
        print("NO DATA")
        return jsonify({"error": "User not found, no data"}), 404

if __name__ == "__main__":
    app.run()
