import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from core.config import settings

mongodb_url = f"mongodb+srv://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(mongodb_url, server_api=ServerApi('1'))



async def ping_server():
    # Send a ping to confirm a successful connection
    try:
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

def get_db():
    return client.user_login