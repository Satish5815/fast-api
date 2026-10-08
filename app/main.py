from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.database import engine,Base,get_db
from app.models import User as UserModel


app=FastAPI()
# # Random UUID4 generate karna
# user_id = uuid.uuid4()

#create database table
Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name:str
    email:str



@app.get('/')
def home(db:Session=Depends(get_db)):
    return {"message":'DB is Connected'}

@app.post('/user')
def create_user(user:UserCreate, db: Session = Depends(get_db)):
    existing_user=(
        db.query(UserModel)
        .filter(UserModel.email==user.email)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )
        
    user_id=str(uuid.uuid4())
    user_object=UserModel(
        id=user_id,
        name=user.name,
        email=user.email
    )
    db.add(user_object)
    db.commit()
    db.refresh(user_object)
    return user_object
    
    
@app.get('/user/{email}')
def get_user(email:str,db:Session=Depends(get_db)):
    user=(
        db.query(UserModel)
        .filter(UserModel.email==email)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )
    
    return {
        "status": "Ok",
        "user": user
    }   
    

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    
@app.patch("/user/{email}")
def update_user(
    email: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    # Find user by current email
    user = (
        db.query(UserModel)
        .filter(UserModel.email == email)
        .first()
    )

    # Check if user was found
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )

    # Update name if provided
    if user_data.name is not None:
        user.name = user_data.name

    # Update email if provided
    if user_data.email is not None:
        user.email = user_data.email

    # Save changes
    db.commit()

    # Refresh object
    db.refresh(user)

    # Return updated user
    return {
        "status": "Ok",
        "user": user
    } 

@app.delete('/user/{email}')
def delete_user(email:str,db:Session=Depends(get_db)):
    user=(db.query(UserModel)
          .filter(UserModel.email==email)
          .first()
          )      
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )  
    
    db.delete(user)
    db.commit()
    
    return {
        'status':'Ok',
        'message':"User deleted successfuly"
    }    