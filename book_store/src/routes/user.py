from src import APIRouter, Depends, Session, status, HTTPException, JSONResponse, get_db, List, AuthJWT
from src.schemas.main import UserSchemas, LoginUser
from src.handler.user import *
from src.handler.utils import check_pw, check_role, authtenticate_check
from src.models.main import Member

route = APIRouter(
    prefix="/user", tags=["user"], include_in_schema=True, responses={404: {"description": "Not found"}}
)  # define user router


@route.get("/", response_model=List[UserSchemas], dependencies=[Depends(authtenticate_check)])  # define root path
def get_all_user(db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    user = get_all(db)  # get all user
    data: list = []
    for i in user:
        data.append(
            {
                "id": i.id,
                "name": i.name,
                "username": i.username,
                "is_admin": i.is_admin,
                "is_staff": i.is_staff,
            }
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success", "data": data})


@route.get("/member", dependencies=[Depends(authtenticate_check)])  # define root path
def get_member(db: Session = Depends(get_db)):
    member = get_all_member(db)
    data: list = []
    for x in member:
        data.append(
            {
                "id": str(x.id),
            }
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success", "data": data})


@route.post("/login")  # define login path
def login(items: LoginUser, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    user = check_user_by_username(items.username, db)  # check user by username
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if check_pw(items.password, user.password) is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    token = auth.create_access_token(
        subject=user.id, expires_time=False, fresh=True, user_claims={"is_admin": user.is_admin}
    )  # create token
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success", "token": token})


@route.post("/", dependencies=[Depends(authtenticate_check), Depends(check_role)])  # define create user path
async def create_user(items: UserSchemas, db: Session = Depends(get_db)):
    user = check_user_by_username(items.username, db)  # check user by username
    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    await create_new_user(db, items)  # create new user
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "success"})


@route.post("/member", dependencies=[Depends(authtenticate_check)])  # define create member path
async def create_member(items: UserSchemas, db: Session = Depends(get_db)):
    user = Member()
    db.add(user)
    db.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "success"})


@route.delete("/{id}", dependencies=[Depends(authtenticate_check), Depends(check_role)])  # define delete user path
async def delete_user(id: int, db: Session = Depends(get_db)):
    user = check_user_by_id(id, db)  # check user by id
    if user:
        await delete_user_id(id, db)  # delete user
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success"})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@route.put("/{id}", dependencies=[Depends(authtenticate_check), Depends(check_role)])  # define update user path
async def update_user_route(id: int, items: CreateUser, db: Session = Depends(get_db)):
    user = check_user_by_id(id, db)  # check user by id
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")  # update user
    await update_user(db, items, id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success"})
