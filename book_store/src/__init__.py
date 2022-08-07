# import all the module
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException, JWTDecodeError
from bcrypt import gensalt, hashpw, checkpw
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, func, Boolean, TEXT
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from dotenv import load_dotenv
import os


load_dotenv()  # load .env file


Base = declarative_base()  # Base is defined in declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")  # postgres://user:password@host:port/database
engine = create_engine(DATABASE_URL)  # DATABASE_URL is defined in .env

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # bind=engine is defined in engine

salt = gensalt(12)  # salt is defined in gensalt


def get_db():  # get_db is defined in SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Setting(BaseModel):
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY")


@AuthJWT.load_config  # Load config is defined in AuthJWT
def get_config():
    return Setting()
