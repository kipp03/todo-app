import random
import string
from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_userName(db: Session, userName: str):
    return db.query(models.User).filter(models.User.userName == userName).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()



def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(email=user.userName, userName=user.userName, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, user_id: int):
    return db.query(models.Item).filter(models.Item.owner_id == user_id).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(title=item.title, owner_id=user_id, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def verify_token(user_id: int, token: str,db: Session):
    user_token = db.query(models.User).filter(models.User.id == user_id, models.User.loginToken == token).first()
    return user_token



def delete_item(item_id: int, db: Session):
    db_item=db.query(models.Item).filter(models.Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    


def verify_user(db: Session, userName: str, password: str) -> models.User:
    user = db.query(models.User).filter(models.User.userName == userName ,models.User.password == password).first()
    return user

def generate_token(db: Session, userName: str) -> str:
    db_user = get_user_by_userName(db, userName=userName)
    db_user.loginToken = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    db.commit()
    return db_user.loginToken
