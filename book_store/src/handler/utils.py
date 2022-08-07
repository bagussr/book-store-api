from src import salt, AuthJWT, Depends, hashpw, HTTPException, status, AuthJWTException, checkpw


def create_password(passowrd: str):  # create_password is defined in salt
    hashed_password = hashpw(passowrd.encode("utf-8"), salt)
    print(hashed_password)
    return hashed_password


def authtenticate_check(auth: AuthJWT = Depends()):  # authtenticate_check is defined in authenticate_optional
    try:
        auth.jwt_required()
        pass
    except AuthJWTException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


def authenticate_optional(auth: AuthJWT = Depends()):  # authenticate_optional is defined in authenticate_optional
    try:
        auth.jwt_optional()
        pass
    except AuthJWTException:
        pass


def check_pw(password: str, hashed_password: str):  # check_pw is defined in checkpw
    return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def check_role(auth: AuthJWT = Depends()):  # check_role is defined in check_role
    role = auth.get_raw_jwt()["is_admin"]
    if role:
        pass
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your role cannot access this resource")
