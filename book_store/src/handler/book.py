from unittest import async_case
from src import Session
from src.schemas.main import CreateBook
from src.models.main import Book


def get_all_book(db: Session): # get_all_book
    return db.query(Book).all()


async def create_new_book(db: Session, book: CreateBook): # CreateBook
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    return new_book


def get_book_by_id(db: Session, id: int): # get_book_by_id
    return db.query(Book).filter(Book.id == id).first()


async def delete_book_by_id(db: Session, id: int): # delete_book_by_id
    book = get_book_by_id(db, id)
    db.delete(book)
    db.commit()
    return book

async def update_book_by_id(db: Session, id: int, book: CreateBook): # update_book_by_id
    book_to_update = get_book_by_id(db, id)
    if book.name:
        book_to_update.name = book.name
    if book.author:
        book_to_update.author = book.author
    if book.year_release:
        book_to_update.year_release = book.year_release
    if book.year_create:
        book_to_update.year_create = book.year_create
    if book.genre:
        book_to_update.genre = book.genre
    db.merge(book_to_update)
    db.commit()
    db.refresh(book_to_update)
    return book_to_update