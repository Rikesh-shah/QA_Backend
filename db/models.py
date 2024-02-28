from pydantic import BaseModel, Field, EmailStr
from db import get_db

class UserModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length = 8, description = "Minimum length of 8 characters")

    class Config:
        json_schema_extra = {
            "example":{
                "name":"Test 1",
                "email":"test@gmail.com",
                "password":"test1@123"
            }
        }

class Collection:
    def __init__(self):
        self.db = get_db()

    def create_indexes(self):
        self.db["users"].create_index("email", unique = True)

    def load_collection(self):
        self.create_indexes()
        collection = self.db.get_collection("users")
        return collection