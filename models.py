#Python
from uuid import UUID
from datetime import datetime
from typing import List
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# ----------------------------------------
#                 Models
#-----------------------------------------

class TypeUser(Enum):
    administrator = "administrator"
    administrator_client = "administrator_client"
    customer_employee = "customer_employee"
    absent = "absent"

class Status(Enum):
    shutdown = "shutdown"
    processing = "processing"
    analyzing = "analyzing"
    running = "running"

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class LoginOut(BaseModel): 
    email: EmailStr = Field(...)
    message: str = Field(default="Login Successfully!")

class User(UserBase):
    first_name: str = Field(
        ...,
        min_lenght=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_lenght=1,
        max_length=50
    )
    company : str = Field(
        ...,
        min_lenght=1,
        max_length=50
    )
    things : List[str] = Field(...)

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )
    type_user : TypeUser = Field(default = "absent")

class Thing(BaseModel):
    thing_id : UUID = Field(...)
    name_id : str = Field(
        ...,
        min_length=8,
        max_length=64
    )
    model   : float = Field(...)

class ThingReply(Thing):
    last_update : datetime = Field(...)
    status: Status = Field(default = "shutdown")
    message: str = Field(default= 'Successful Creation!!!')

class Analysis(Thing):
    tables_analyzed : List[str] = Field(...)
    message : str = Field(default ="Analysis Successful ")