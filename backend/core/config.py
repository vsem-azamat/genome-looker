from decouple import config

class Config:
    HOST = config("HOST", default="localhost")
    PORT = config("PORT", default=8000, cast=int)

    DATASETS_DIR = "./datasets"

cnfg = Config()