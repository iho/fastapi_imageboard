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



class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return "Hello " + name


app = FastAPI()
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))


# default database events
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
