from sqlalchemy import INTEGER,Column,String

from app.database import Base


class User(Base):
    
    __tablename__="users"
    
    id=Column(String,primary_key=True,index=True,unique=True)
    name=Column(String)
    email=Column(String,unique=True)