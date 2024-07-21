from fastapi import Depends, FastAPI, HTTPException, Header
from sqlalchemy.orm import Session
import uvicorn

import crud, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def is_valid_token():
    accept_language = Header(None)
    print("header", accept_language)
    return True

@app.post("/login/")
def login(loginRequestDetails: schemas.LoginRequestDetails, db: Session = Depends(get_db)):
    user = crud.verify_user(db, loginRequestDetails.userName, loginRequestDetails.password)
    if user:
        return {
            "details": "logged in",
            "user_id": user.id,
            "token": crud.generate_token(db, loginRequestDetails.userName)
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/signup/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_userName(db, userName=user.userName)
    if db_user:
        raise HTTPException(status_code=400, detail="UserName already registered")
    else:
        return crud.create_user(db, user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}/", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db), token:str=Header(None)
):
    user_token=crud.verify_token(user_id,token,db)
    if user_token is None:
        raise HTTPException(status_code=401, detail="unauthorized")
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/users/{user_id}/items/", response_model=list[schemas.Item])
def read_items(user_id: int, db: Session = Depends(get_db),token:str=Header(None)
):
    user_token=crud.verify_token(user_id,token,db)
    if user_token is None:
        raise HTTPException(status_code=401, detail="unauthorized")
    items = crud.get_items(db, user_id)
    return items

@app.delete("/{user_id}/items/{item_id}/")
def remove_item(user_id: int, item_id: int, db: Session = Depends(get_db),token:str=Header(None)
):
    user_token=crud.verify_token(user_id,token,db)
    if user_token is None:
        raise HTTPException(status_code=401, detail="unauthorized")
    crud.delete_item(item_id ,db)
    return {
        "status":"item deleted"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
