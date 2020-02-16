import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from starlette.config import Config
from typing import List
from pydantic import BaseModel
from db import *
from utils import *
# load env variables
config = Config('.env')
# db url
DATABASE_URL = config('DATABASE_URL')

import graphene
from graphene_pydantic import PydanticObjectType
import db

class Banner(PydanticObjectType):
    class Meta:
        model = db.Banner
        # only return specified fields
#         only_fields = ("name",)
#         # exclude specified fields
#         exclude_fields = ("id",)
#

class Board(PydanticObjectType):
    class Meta:
        model = db.Board

class Query(graphene.ObjectType):
    all_banners = graphene.List(Banner)
    all_boards = graphene.List(Board)

    board = graphene.Field(Board, board_id=graphene.Int())

    def resolve_all_banners(self, info):
        return [db.Banner(id=1, url='db.py')]

    def resolve_board(self, info, board_id):
        print(id)
        return [db.Board(id=1, short="b", long_name='lol', ...)]


app = FastAPI()
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))


# default database events
# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()
