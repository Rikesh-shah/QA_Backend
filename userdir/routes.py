from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from db.models import UserModel
from db.schemas import LoginSchema
from userdir.usercrud import User
from db import get_db


class UserRoutes:
    def __init__(self):
        self.router = APIRouter()
        self.user = User()

    def setup_routes(self):
        self.router.post("/register/", tags = ['User Creation'])(self.create_user)
        self.router.post("/login/", tags = ['User Authentication'])(self.login_user)

    async def create_user(self, user:UserModel = Body(...), db = Depends(get_db)):
        #converting the pydantic model into json compatible dictionary
        user = jsonable_encoder(user)
        response = await self.user.create_user(user = user)
        return response

    async def login_user(self, credentials: LoginSchema = Body(...), db = Depends(get_db)):
        access_token = await self.user.authenticate(email = credentials.email, password = credentials.password)
        return access_token