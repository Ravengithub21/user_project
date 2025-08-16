from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    age: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/", response_model=List[UserCreate])
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()  # Pobieramy wszystkie rekordy z tabeli
    return users

@app.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.Users(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=user.password,
        age=user.age 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user