import os


class Config:
    APP_NAME = os.getenv("APP_NAME", "python-wsgi-sample")
    ENV = os.getenv("APP_ENV", "dev")
    DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"