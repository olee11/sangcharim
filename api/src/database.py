from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://{username}:{password}@{host}:{port}/{db_name}".format(
    host=os.getenv('DB_SCR_HOST'),
    username=os.getenv('DB_SCR_USERNAME'),
    password=os.getenv('DB_SCR_PASSWORD'),
    port=os.getenv('DB_SCR_PORT'),
    db_name=os.getenv('DB_SCR_DATABASE')
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
