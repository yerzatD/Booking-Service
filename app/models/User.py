from ...database import Base
from sqlalchemy import Column,String,Integer,Float,ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,index=True,primary_key=True)
    username = Column(String, index=True)
    email = Column(String,index=True,unique=True)
    hashed_password = Column(String)
    role = Column(String,default="user")

    