import os


current_path = os.path.dirname(os.path.realpath(__file__))
# - Путь к файлу БД в данной папке
db_path = "sqlite:///" + current_path + "\\enikeev_project4.db"
    
class Config:
    DEBUG = True
    SECRET_KEY= "Enikeev-project4-secret-phrase"
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False