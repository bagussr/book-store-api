from src import APIRouter, Depends, Session, status, HTTPException, JSONResponse, get_db, List
from src.schemas.main import AuthorSchemas, CreateAuthor
from src.handler.author import *

route = APIRouter(
    prefix="/author", tags=["author"], include_in_schema=True, responses={404: {"description": "Not found"}}
)  # define author router


@route.get("/", response_model=List[AuthorSchemas]) # get all authors
def get_all_author(db: Session = Depends(get_db)):
    authors = get_all_authors(db)
    data: list = []
    for x in authors:
        data.append({"id": x.id, "name": x.name, "date_of_birth": str(x.date_of_birth)})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success", "data": data})


@route.post("/", response_model=AuthorSchemas) # create new author
async def create_author(author: CreateAuthor, db: Session = Depends(get_db)):
    await create_new_author(db, author)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success"})


@route.get("/{author_id}", response_model=AuthorSchemas) # get author by id
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = get_author_by_id(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "success",
            "data": {"id": author.id, "name": author.name, "date_of_birth": str(author.date_of_birth)},
        },
    )


@route.delete("/{author_id}", response_model=AuthorSchemas) # delete author by id
async def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = get_author_by_id(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    await delete_author_by_id(db, author_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success"})


@route.put("/{author_id}", response_model=AuthorSchemas) # update author by id
async def update_author(author_id: int, author: CreateAuthor, db: Session = Depends(get_db)):
    author_ = get_author_by_id(db, author_id)
    if author_ is None:
        raise HTTPException(status_code=404, detail="Author not found")
    await update_author_by_id(db, author_id, author)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success"})
