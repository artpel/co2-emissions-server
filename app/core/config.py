import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.API_PORT = int(os.environ["PORT"])


config = Settings()
