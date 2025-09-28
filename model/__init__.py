import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

# Importando os modelos
from model.base import Base
from model.client import Client
from model.card import Card

# Caminho do banco de dados
DB_DIR = "database"
DB_FILE = "db.sqlite3"
DB_PATH = os.path.join(DB_DIR, DB_FILE)
DB_URL = f"sqlite:///{DB_PATH}"

# Garante que o diretório do banco existe
os.makedirs(DB_DIR, exist_ok=True)

# Cria a engine de conexão
engine = create_engine(DB_URL, echo=False)

# Cria o banco se necessário
if not database_exists(engine.url):
    create_database(engine.url)

# Cria as tabelas se não existirem
Base.metadata.create_all(engine)

# Instancia o criador de sessão
Session = sessionmaker(bind=engine)