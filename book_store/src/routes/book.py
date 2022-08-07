from src import APIRouter, Depends, Session, status, HTTPException, JSONResponse, get_db, List
from src.schemas.main import BookSchemas
from src.handler.book import *
from src.handler.author import get_author_by_id

route = APIRouter(
    prefix="/book", tags=["book"], include_in_schema=True, responses={404: {"description": "Not found"}}
)  # define book router


@route.get("/", response_model=List[BookSchemas]) # define get all book route
def get_all_books(db: Session = Depends(get_db)):
    books = get_all_book(db)
    data: list = []
    for x in books:
        author = get_author_by_id(db, x.author)
        data.append(
            {
                "id": x.id,
                "name": x.name,
                "author": author.name,
                "year_created": str(x.year_create),
                "year_release": str(x.year_release),
                "genre": x.genre,
            }
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success", "data": data})


@route.post("/", response_model=BookSchemas) # define create new book route
async def create_book(book: CreateBook, db: Session = Depends(get_db)):
    await create_new_book(db, book)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success"})


@route.get("/{id}", response_model=BookSchemas) # define get book by id route
def get_book(id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(db, id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    author = get_author_by_id(db, book.author)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "success",
            "data": {
                "id": book.id,
                "name": book.name,
                "author": author.name,
                "year_created": str(book.year_create),
                "year_release": str(book.year_release),
                "genre": book.genre,
            },
        },
    )


@route.delete("/{id}", response_model=BookSchemas) # define delete book by id route
async def delete_book(id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(db, id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    await delete_book_by_id(db, id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success"})


@route.put("/{id}", response_model=BookSchemas) # define update book by id route
async def update_book(id: int, book: CreateBook, db: Session = Depends(get_db)):
    book_to_update = get_book_by_id(db, id)
    if not book_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    await update_book_by_id(db, id, book)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success"})
