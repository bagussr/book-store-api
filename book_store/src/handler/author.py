from src import Session
from src.models.main import Author
from src.schemas.main import CreateAuthor


def get_all_authors(db: Session): # get_all_authors
    user = db.query(Author).all()
    return user


async def create_new_author(db: Session, author: CreateAuthor): # CreateAuthor
    new_author = Author(**author.dict())
    db.add(new_author)
    db.commit()
    return new_author


def get_author_by_id(db: Session, author_id: int): # get_author_by_id
    return db.query(Author).filter(Author.id == author_id).first()


async def delete_author_by_id(db: Session, author_id: int): # delete_author_by_id
    author = db.query(Author).filter(Author.id == author_id).first()
    db.delete(author)
    db.commit()
    return author


async def update_author_by_id(db: Session, author_id: int, author_: CreateAuthor): # update_author_by_id
    author = db.query(Author).filter(Author.id == author_id).first()
    if author_.name:
        author.name = author_.name
        print(author_.name)
    if author_.date_of_birth:
        author.date_of_birth = author_.date_of_birth
    db.merge(author)
    db.commit()
    db.refresh(author)
    return author
