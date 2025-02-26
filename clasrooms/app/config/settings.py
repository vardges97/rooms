# from pym

# client = MongoClient("mongodb+srv://arsenyanvardges:DbsSuck8Al1s@cluster0.8yb8n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# db = client.classrooms

# collection_name = db["todo_collection"]

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str

    model_config = ConfigDict(env_file = ".env", env_file_encoding = "utf-8")

settings = Settings()