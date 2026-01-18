import os

class Config:
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre_cle_secrete' 
    basedir = os.path.abspath(os.path.dirname(__file__))  
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "systra_platform.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

