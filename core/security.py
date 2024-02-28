import json
from fastapi import Depends, HTTPException, status
from core.config import settings
from jose  import JWTError, jwt
from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi.security.oauth2 import OAuth2PasswordBearer
from db.models import Collection
from bson import ObjectId

password_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
ld_collection = Collection()

auth_scheme =OAuth2PasswordBearer(tokenUrl = "login")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.SECRET_ALGORITHM
EXPIRY_TIME = settings.TOKEN_EXPIRY_DAYS

async def create_access_token(data:dict):
    data_encode = data.copy()
    expiry_time = datetime.utcnow() + timedelta(days = EXPIRY_TIME)
    data_encode.update({"expiry time": json.dumps(expiry_time, default = str)})
    access_token =jwt.encode(data_encode, SECRET_KEY, algorithm = ALGORITHM)
    return access_token

async def verify_access_token(token: str, credentials_exception):
    try:
        # decoding the access token to retrieve the decoded dictionary from it
        data_decode = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

        # getting the username that is encoded in access token and storing in user_name
        id: int = data_decode.get("id")

        if not id:
            raise credentials_exception
        token_data = id
    except JWTError:
        raise credentials_exception
    return token_data

async def get_current_user(token:str = Depends(auth_scheme)):
    db = ld_collection.load_collection()
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalidate Credentials",
        headers = { "WWW-Authenticate": "Bearer" }
    )
    id = await verify_access_token(token, credentials_exception)
    user = await db.find_one({"_id":ObjectId(id)})
    return user

# for hashing the password
async def get_hash_password(password:str):
    return password_context.hash(password)

# for verifying the password
async def verify_password(hash_password: str, password:str):
    return password_context.verify(password,hash_password)