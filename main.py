from fastapi import FastAPI, HTTPException, Depends
import models
from database import SessionLocal, engine
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import List


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name: str
    surname: str
    password: str
    email: EmailStr
    age: int

class UserUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    password: str | None = None
    age: int | None = None

class UserPatch(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    age: int


#connect to the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




#get all of the users from the database
@app.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


#add an user
@app.post("/users/")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.Users(
        name = user.name,
        surname = user.surname,
        email = user.email,
        password = user.password,
        age = user.age
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#change the existing user
@app.patch("/users/{user_id}")
def patch_user(user_id: int, user_update: UserPatch, db: Session = Depends(get_db)):
    # Query the user by ID
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    
    # Check if user exists
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields if provided in the request body
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    # Commit the changes to the database
    db.commit()
    db.refresh(user)
    return user



#Change value of existing user
@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserPatch, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    
    if not user: 
        raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")
    
    user.name = user_update.name
    user.surname = user_update.surname
    user.email = user_update.email
    user.password = user_update.password
    user.age = user_update.age

    db.commit()
    db.refresh(user)

    return user



#delete an user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Your id is not matching the database")
    
    db.delete(user)
    db.commit()

    return {"detail": "Użytkownik został pomyślnie usunięty"}