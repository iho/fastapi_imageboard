import databases
import sqlalchemy
from typing import List, Tuple
from pydantic import BaseModel, root_validator, validator, ValidationError, FilePath, SecretStr, ByteSize
from starlette.config import Config
from utils import *
from datetime import datetime
from ipaddress import IPv4Address
# load env variables
config = Config('.env')
# db url
DATABASE_URL = config('DATABASE_URL')

# db variable
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# header image
class Banner(BaseModel):
    id: int
    url: FilePath


# boards aka forums model
class Board(BaseModel):
    id: int
    short: str
    long_name: str
    info: str
    postcount: int = 0
    # created_by: User
    # moderators: List[User]
    created_at: datetime
    updated_at: datetime
    postlimit: int = 150 # number of posts after which posts get locked
    bumplimit: int = 100 # number of posts after which posts dont get served up top
    boardlimit: int = 50 # number of threads alive
    page_size: int = 10 # number of threads per page
    banners: List[Banner]
    is_global: bool = True
    is_located: bool = False # whether to use country/city flags

    @classmethod
    @validator('short')
    def short_validation(cls, v: str) -> str:
        assert 1 <= len(v) <= 5, 'Board handler must be between 1 and 5 characters long'

    @classmethod
    @validator('long_name')
    def long_validation(cls, v: str) -> str:
        assert 5 <= len(v) <= 50, 'Board name must be between 5 and 50 characters long'


class Attachment(BaseModel):
    id: int
    original_filename: str
    url: FilePath
    resolution: Tuple[int, int]
    size: ByteSize
    filetype: str
    is_spoilered: bool = False
    @property
    def filesize(self) -> str:
        return self.size.human_readable()


class User(BaseModel):
    id: int
    username: str
    password: SecretStr
    info: str
    created_at: datetime
    last_login: datetime
    edited_at: datetime
    boards_created: List[Board] # boards user has created
    boards_moderated: List[Board] # boards user is a moderator of

    # some basic validation - no idea whether it works at the moment
    @classmethod
    @root_validator
    def validation(cls, values: dict) -> dict:
        username, password = values.get('username', None), values.get('password', None)
        password = cleanse(password.get_secret_value())
        username = cleanse(username)
        if not password and not username:
            raise ValidationError("No username and password")
        if not password:
            raise ValidationError("Empty passwords not allowed")
        if not username:
            raise ValidationError('Empty username not allowed')
    
    @classmethod
    @validator('username')
    def username_validation(cls, v: str) -> str:
        assert v.isalpha(), 'Username must be alphanumeric'
        assert 3 < len(v) <= 50, 'Username must be between 4 and 50 characters'
        return v

    @classmethod
    @validator('password')
    def password_validation(cls, v: str) -> str:
        assert 6 <= len(v) <= 50, 'Password must be between 6 and 50 characters'
        return v


# idk if this hack will work
Board.created_by: User
Board.moderators: List[User]


class Location(BaseModel):
    coordinates: Tuple[float, float] # lat / long coords
    country: str
    city: str
    short: str # need a way to generate stuff like UA or UA-12 idk
    IP: IPv4Address 


# generic post and thread model
class Post(BaseModel):
    id: int # global post count
    local_id: int # local (board) post count
    is_op: bool # determines whether post is a threadstarter
    IP: IPv4Address
    header: str
    body: str
    is_locked: bool = False
    is_pinned: bool = False
    is_infinite: bool = False
    is_banned: bool = False
    location: Location
    files: List[Attachment]


class Ban(BaseModel):
    post: Post
    reason: str
    is_infinite: bool = False
    start: datetime = datetime.now()
    end: datetime # use timedelta to determine end time from start time

    def has_ended(self) -> bool:
        return end < datetime.now()

# posts = sqlalchemy.Table(
#     "posts",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("text", sqlalchemy.String),
#     sqlalchemy.Column("completed", sqlalchemy.Boolean),
# )

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={}
)
metadata.create_all(engine)