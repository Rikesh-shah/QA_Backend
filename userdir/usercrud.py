from core.security import get_hash_password, verify_password, create_access_token
from db.models import Collection
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from pydantic import EmailStr
from db.schemas import UserParse
from pymongo.errors import DuplicateKeyError

collection = Collection()
usr_collection = collection.load_collection()

class User:
    async def raise_error(self):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
            headers = { "WWW-Authenticate": "Bearer" })


    async def create_user(self, user):
        try:
            # Hash the user's password
            user["password"] = await get_hash_password(user["password"])
            # Insert the new user into the database
            new_user = await usr_collection.insert_one(user)
            # Retrieve the created user's data
            created_user = await usr_collection.find_one({ "_id": new_user.inserted_id })
            # Parse the user data
            usr_parse = UserParse(user = created_user)
            data = await usr_parse.parsedata()  # Assuming parsedata is not an async function
            # Return a JSON response with the created user data
            return JSONResponse(status_code = status.HTTP_201_CREATED, content = data)
        except DuplicateKeyError:
            # Handle duplicate key error (e.g., email already exists)
            raise HTTPException(status_code = 400, detail = "Email already exists")
        except Exception as e:
            # Handle other unexpected errors
            raise HTTPException(status_code = 500, detail = str(e))

    async def authenticate(self, email: EmailStr, password: str):
        user = await usr_collection.find_one({ "email": email })
        if not user:
            # User not found
            raise HTTPException(status_code = 401, detail = "Incorrect email or password")

        if not await verify_password(hash_password = user["password"], password = password):
            # Password verification failed
            raise HTTPException(status_code = 401, detail = "Incorrect email or password")

        usr_parse = UserParse(user = user)
        parsed_data = await usr_parse.parsedata()
        token = await create_access_token(data = { "id": parsed_data["id"] })
        return { "access_token": token, "token_type": "bearer" }