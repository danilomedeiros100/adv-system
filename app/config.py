

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-padrao-segura')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = 3600  # 1 hora
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Altere para True em produção com HTTPS