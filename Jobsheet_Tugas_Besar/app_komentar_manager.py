import os
import csv
import datetime
import re
import uuid
import unicodedata

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

import database
import config
from model import User, Channel, Video, Comment

# Constants
PREFIX = "[App_Komentar_Manager]"
SCOPES = config.SCOPES
CREDENTIALS_PATH = config.CREDENTIALS_PATH
LOGIN_SESSION = config.LOGIN_SESSION
TIME_SESSION = config.TIME_SESSION
DB_COMMENT_DELETEAFTERFINISHEXECUTE = config.DB_COMMENT_DELETEAFTERFINISHEXECUTE

fetch_query = database.fetch_query
execute_query = database.execute_query


import uuid
from model import Comment
from database import execute_query

PREFIX = "[App_Youtube_Commenter]"

def load_user_and_youtube():
    with open(LOGIN_SESSION, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
    email = rows[1][0]

    user_data = fetch_query("SELECT * FROM user WHERE email = ?", (email,), fetch_all=False)
    if not user_data:
        raise ValueError("User tidak ditemukan.")

    user = User(**user_data)
    creds = Credentials(
        token=user.token,
        refresh_token=user.refresh_token,
        token_uri=user.token_uri,
        client_id=user.client_id,
        client_secret=user.client_secret,
        scopes=user.scopes.split()
    )
    youtube = build("youtube", "v3", credentials=creds)
    return user, youtube

def get_youtube_channels():
    user, youtube = load_user_and_youtube()
    response = youtube.channels().list(part="id,snippet,statistics", mine=True).execute()
    channels = []
    if not response.get("items"):
        print(f"{PREFIX} Tidak ada channel ditemukan.")
        return user, []
    for item in response.get("items", []):
        # channels.append({
        #     "id": item["id"],
        #     "title": item["snippet"]["title"],
        #     "subscribers": int(item["statistics"].get("subscriberCount", "0"))
        # })
        ch = Channel(
            id=None,
            user_id=user.id,
            channel_id=item["id"],
            title=item["snippet"]["title"],
            subscribers=int(item["statistics"].get("subscriberCount", "0")),
            created_at=item["snippet"]["publishedAt"],
            is_active=0
        )
        channels.append(ch)
        execute_query("INSERT OR IGNORE INTO channel (user_id, channel_id, title, subscribers, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?)", (
            ch.user_id,
            ch.channel_id,
            ch.title,
            ch.subscribers,
            ch.created_at,
            ch.is_active
        ))
    return user, channels

def activate_channel(user, selected_channel_id):
    execute_query("UPDATE channel SET is_active = 0 WHERE user_id = ?", (user.id,))
    execute_query("UPDATE channel SET is_active = 1 WHERE user_id = ? AND channel_id = ?", (user.id, selected_channel_id))
    with open(LOGIN_SESSION, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["email", "created_at", "channel_id"])
        writer.writerow([user.email, datetime.datetime.now().isoformat(), selected_channel_id])


def is_weird_text(text: str) -> bool:
    normalized_text = unicodedata.normalize("NFKD", text)
    if text != normalized_text:
        return True
    non_ascii_count = 0
    total_count = 0
    for char in text:
        if not char.isprintable():
            continue
        category = unicodedata.category(char)
        name = unicodedata.name(char, '')
        if category in ('Ll', 'Lu', 'Nd', 'Zs', 'Po'):
            continue
        if any(keyword in name for keyword in [
            "EMOJI", "HEART", "SMILING", "FACE", "HAND",
            "MUSIC", "NOTE", "SYMBOL", "STAR", "FIRE", "HUNDRED POINTS",
            "EMOTICON", "PARTY", "ANIMAL", "FOOD", "EYES", "DRAGON",
            "SQUARED", "CIRCLED", "ENCLOSED", "NEGATIVE"]):
            continue
        if ord(char) > 0x2E80:
            non_ascii_count += 1
        total_count += 1
    return total_count > 0 and (non_ascii_count / len(text)) > 0.3

def get_suspicious_comments(video_id: str):
    user, youtube = load_user_and_youtube()
    video_response = youtube.videos().list(part="snippet,statistics", id=video_id).execute()
    owner_channel_id = video_response.get("items", [{}])[0].get("snippet", {}).get("channelId", "")
    is_owner = False
    active_channel = fetch_query("SELECT * FROM channel WHERE user_id = ? AND is_active = 1", (user.id,), fetch_all=False)
    if not video_response.get("items"):
        return None, None, None
    if active_channel and active_channel["channel_id"] == owner_channel_id:
        is_owner = True
    suspicious = []
    next_page_token = None

    # Identitas video
    video_data = video_response["items"][0]
    snippet_video = video_data["snippet"]
    statistics = video_data["statistics"]

    channel_id = snippet_video.get("channelId", "")
    title = snippet_video.get("title", "")
    description = snippet_video.get("description", "")
    published_at = snippet_video.get("publishedAt", datetime.datetime.now().isoformat())
    comment_count = int(statistics.get("commentCount", 0))
    vd = Video(
        id=None,
        channel_id=channel_id,
        video_id=video_id,
        title=title,
        description=description,
        published_at=published_at,
        comment_count=comment_count
    )
    execute_query("INSERT OR IGNORE INTO video (channel_id, video_id, title, description, published_at, comment_count) VALUES (?, ?, ?, ?, ?, ?)", (
        vd.channel_id,
        vd.video_id,
        vd.title,
        vd.description,
        vd.published_at,
        vd.comment_count
    ))
    # Identitas komentar
    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText",
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comment_id = item["id"]
            author = snippet.get("authorDisplayName", "Unknown")
            author_channel_id = snippet.get("authorChannelId", {}).get("value", "")
            text = snippet.get("textDisplay", "")
            published_at = snippet.get("publishedAt", "")
            if author_channel_id == owner_channel_id:
                continue
            if is_weird_text(text):
                suspicious.append({
                    "unique_code": str(uuid.uuid4())[:8],
                    "comment_id": comment_id,
                    "author": author,
                    "text": text,
                    "published_at": published_at
                })
                cmt = Comment(
                    id=None,
                    video_id=video_id,
                    comment_id=comment_id,
                    author=author,
                    comment = text,
                    published_at=published_at
                )
                execute_query("INSERT OR IGNORE INTO comment (video_id, comment_id, author, comment, published_at) VALUES (?, ?, ?, ?, ?)", (
                    cmt.video_id,
                    cmt.comment_id,
                    cmt.author,
                    cmt.comment,
                    cmt.published_at
                ))
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return suspicious, youtube, is_owner

def handle_selected_comments(youtube, selected_comments, is_owner):
    results = []
    for selected in selected_comments:
        try:
            youtube.comments().markAsSpam(id=selected["comment_id"]).execute()
            if is_owner:
                youtube.comments().setModerationStatus(
                    id=selected["comment_id"], moderationStatus="rejected").execute()
                # youtube.comments().delete(id=selected["comment_id"]).execute()
            results.append((selected["comment_id"], True))
            if DB_COMMENT_DELETEAFTERFINISHEXECUTE:
                execute_query("DELETE FROM comment")
        except Exception as e:
            results.append((selected["comment_id"], False))
    return results


def extract_video_id(url: str):
    # Accept both full and short YouTube URLs
    patterns = [
        r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
        r"(?:https?://)?youtu\.be/([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            return match.group(1)
    return None 


def get_user_info(credentials):
    try:
        oauth2 = build('oauth2', 'v2', credentials=credentials)
        return oauth2.userinfo().get().execute()
    except Exception as e:
        print(f"{PREFIX} Error get_user_info: {e}")
        return None


def login_session_is_valid():
    if not os.path.exists(LOGIN_SESSION):
        return False
    try:
        with open(LOGIN_SESSION, mode="r") as file:
            reader = csv.DictReader(file)
            row = next(reader)
            created_at = datetime.datetime.fromisoformat(row["created_at"])
            limit = created_at + datetime.timedelta(minutes=TIME_SESSION)
        return datetime.datetime.now() <= limit
    except Exception as e:
        print(f"{PREFIX} Error reading login session: {e}")
        return False


def login_user():
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"{PREFIX} Credentials not found! {CREDENTIALS_PATH}")
        return

    if login_session_is_valid():
        print(f"{PREFIX} User already logged in!")
        return
    if os.path.exists(LOGIN_SESSION):
        os.remove(LOGIN_SESSION)
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    credentials = flow.run_local_server(port=0)
    user_info = get_user_info(credentials)

    if not user_info:
        print(f"{PREFIX} Failed Login. Cannot save user info!")
        return

    user = User(
        id=None,
        google_id=user_info["id"],
        email=user_info["email"],
        name=user_info.get("name", ""),
        picture=user_info.get("picture", ""),
        token=credentials.token,
        refresh_token=credentials.refresh_token,
        token_uri=credentials.token_uri,
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        scopes=" ".join(credentials.scopes),
        expiry=credentials.expiry.isoformat()
    )

    existing = fetch_query("SELECT id FROM user WHERE google_id = ?", (user.google_id,), fetch_all=False)

    if existing:
        user.id = existing["id"]
        query = """
        UPDATE user SET email=?, name=?, picture=?, token=?, refresh_token=?,
        token_uri=?, client_id=?, client_secret=?, scopes=?, expiry=?
        WHERE google_id=?;
        """
        params = (
            user.email, user.name, user.picture, user.token,
            user.refresh_token, user.token_uri, user.client_id,
            user.client_secret, user.scopes, user.expiry, user.google_id
        )
    else:
        query = """
        INSERT INTO user (google_id, email, name, picture, token, refresh_token,
        token_uri, client_id, client_secret, scopes, expiry)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            user.google_id, user.email, user.name, user.picture,
            user.token, user.refresh_token, user.token_uri,
            user.client_id, user.client_secret, user.scopes, user.expiry
        )

    success = execute_query(query, params)

    if success:
        with open(LOGIN_SESSION, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["email", "created_at"])
            writer.writerow([user.email, datetime.datetime.now().isoformat()])
        print(f"{PREFIX} ✅ User {user.email} berhasil login dan disimpan.")
    else:
        print(f"{PREFIX} ❌ Gagal menyimpan user ke database.")

#
# Choose Channel
#

# def get_youtube_channels():
#     with open(LOGIN_SESSION, newline='', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         rows = list(reader)
#     email = rows[1][0]

#     user_data = fetch_query("SELECT * FROM user WHERE email = ?", (email,), fetch_all=False)
#     if not user_data:
#         print(f"{PREFIX} User tidak ditemukan.")
#         return None, None

#     user = User(**user_data)

#     creds = Credentials(
#         token=user.token,
#         refresh_token=user.refresh_token,
#         token_uri=user.token_uri,
#         client_id=user.client_id,
#         client_secret=user.client_secret,
#         scopes=user.scopes.split()
#     )

#     youtube = build("youtube", "v3", credentials=creds)
#     request = youtube.channels().list(part="id,snippet,statistics", mine=True)
#     response = request.execute()

#     channels = []
#     for item in response.get("items", []):
#         ch = Channel(
#             id=None,
#             user_id=user.id,
#             channel_id=item["id"],
#             title=item["snippet"]["title"],
#             subscribers=int(item["statistics"].get("subscriberCount", "0")),
#             created_at=item["snippet"]["publishedAt"],
#             is_active=0
#         )
#         channels.append(ch)
    
#     return channels, user

def clear_database():
    input2 = input("Are you sure you want to clear all data ? (type 'yes' if you agree)")
    if input2 == 'yes':
        execute_query("DELETE FROM comment")
        execute_query("DELETE FROM channel")
        execute_query("DELETE FROM user")
        execute_query("DELETE FROM video")
    else:
        print(f"Oke, gk dihapus ya xD")

if __name__ == "__main__":
    clear_database()
    # database.setup_database_initial()
    # if DB_COMMENT_DELETEAFTERFINISHEXECUTE:
    #     execute_query("DELETE FROM comment")  # ← Komentar aja kalau mau nyimpen histori~
    # login_user()