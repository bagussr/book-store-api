from src import Session, status, HTTPException
from src.models.main import Users, Member
from .utils import create_password
from src.schemas.main import CreateUser


def get_all(db: Session):  # get_all user
    return db.query(Users).all()


async def create_admin(db: Session):  # create_admin
    user = Users(
        name="Admin", username="admin", password=create_password("admin").decode("utf-8"), is_admin=True, is_staff=True
    )
    db.add(user)
    db.commit()
    return


async def create_new_user(db: Session, items: CreateUser):  # CreateUser
    new_user = Users(
        name=items.name,
        username=items.username,
        password=create_password(items.password).decode("utf-8"),
        is_admin=items.is_admin,
        is_staff=items.is_staff,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def check_user_by_username(username: str, db: Session):  # check_user_by_username
    return db.query(Users).filter(Users.username == username).first()


def check_user_by_id(id: int, db: Session):  # check_user_by_id
    return db.query(Users).filter(Users.id == id).first()


def get_all_member(db: Session):  # get_all_member
    return db.query(Member).all()


async def delete_user_id(id: int, db: Session):  # delete_user_id
    user = check_user_by_id(id, db)
    db.delete(user)
    db.commit()
    return user


async def update_user(db: Session, items: CreateUser, id: int):
    user = check_user_by_id(id, db)
    if items.name:
        user.name = items.name
    if items.username:
        user.username = items.username
    if items.password:
        user.password = create_password(items.password).decode("utf-8")
    if items.is_admin:
        user.is_admin = items.is_admin
    if items.is_staff:
        user.is_staff = items.is_staff
    db.merge(user)
    db.commit()
    db.refresh(user)
    return user
