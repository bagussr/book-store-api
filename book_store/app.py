from __init__ import *


@app.exception_handler(AuthJWTException)  # AuthJWTException is raised when the token is invalid
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.on_event("startup")  # on_event is a decorator that is called when the application starts
async def on_startup():
    ses = SessionLocal()
    admin = ses.query(Users).filter(Users.is_admin == True).first()
    if admin is None:
        await create_admin(ses)
    pass


@app.get("/")  # define root path
def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":  # run application
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
