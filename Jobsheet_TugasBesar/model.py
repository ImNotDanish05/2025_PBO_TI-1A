from datetime import datetime
from typing import Optional

class User:
    def __init__(
        self,
        id: Optional[int] = None,
        google_id: str = '',
        email: str = '',
        name: Optional[str] = 'NotName',
        picture: Optional[str] = 'https://placehold.co/400x400?text=?',
        token: str = '',
        refresh_token: str = '',
        token_uri: str = '',
        client_id: str = '',
        client_secret: str = '',
        scopes: str = '',
        expiry: str = ''
    ):
        self.id = id
        self.google_id = google_id.strip()
        self.email = email.strip()
        self.name = name.strip()
        self.picture = picture.strip() or "https://placehold.co/400x400?text=?"
        self.token = token
        self.refresh_token = refresh_token
        self.token_uri = token_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.expiry = expiry

    def __repr__(self):
        return f"<User email={self.email}>"


class Channel:
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 0,
        channel_id: str = '',
        title: Optional[str] = 'Unknown',
        subscribers: int = 0,
        created_at: Optional[str] = None,
        is_active: int = 1
    ):
        self.id = id
        self.user_id = user_id
        self.channel_id = channel_id.strip()
        self.title = title
        self.subscribers = subscribers
        self.created_at = created_at or datetime.now().isoformat()
        self.is_active = is_active

    def __repr__(self):
        return f"<Channel id={self.channel_id} title='{self.title}'>"


class Video:
    def __init__(
        self,
        id: Optional[int] = None,
        channel_id: str = '',
        video_id: str = '',
        title: Optional[str] = 'Unknown',
        description: Optional[str] = '',
        published_at: Optional[str] = None,
        comment_count: int = 0
    ):
        self.id = id
        self.channel_id = channel_id.strip()
        self.video_id = video_id.strip()
        self.title = title
        self.description = description
        self.published_at = published_at or datetime.now().isoformat()
        self.comment_count = comment_count

    def __repr__(self):
        return f"<Video id={self.video_id} title='{self.title}'>"


class Comment:
    def __init__(
        self,
        id: Optional[int] = None,
        video_id: str = '',
        comment_id: str = '',
        author: Optional[str] = '',
        comment: str = '',
        published_at: Optional[str] = None
    ):
        self.id = id
        self.video_id = video_id.strip()
        self.comment_id = comment_id.strip()
        self.author = author.strip() if author else None
        self.comment = comment.strip()
        self.published_at = published_at or datetime.now().isoformat()

    def __repr__(self):
        return f"<Comment id={self.comment_id} author={self.author}>"
