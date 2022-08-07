# import all the modules from the book_store package
from src import *
from src.routes import user, author, book, order
from src.handler.utils import *
from src.models.main import *
from src.handler.user import *

# import all module for main apps
from fastapi import FastAPI, status, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import uvicorn

app = FastAPI(title="Book Store Api", description="Book Store Api", version="1.0.0")  # define fastapi application

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)  # Add CORS middleware

app.include_router(user.route, dependencies=[Depends(authenticate_optional)])  # Include user router
app.include_router(author.route, dependencies=[Depends(authtenticate_check)])  # Include author router
app.include_router(book.route, dependencies=[Depends(authtenticate_check)])  # Include book router
app.include_router(order.route, dependencies=[Depends(authtenticate_check)])  # Include order router
