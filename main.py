#Python
from queue import Empty
import pymysql
from uuid import UUID
from datetime import datetime
from typing import List, Optional

# Pydantic
from pydantic import Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Form, Path, Query

#Files
from models import *

app = FastAPI()

# ----------------------------------------
#                DataBase
#-----------------------------------------
myConexion = pymysql.connect( host='localhost', user= 'root', passwd= "root", db='project_iot' )
cur = myConexion.cursor()

# ----------------------------------------
#            Path Operations
#-----------------------------------------

## Users

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(user : UserRegister = Body(...)):
    """
    Signup

    This path operations register a user in the app

    Parameters:
    - Request body parameter
        - user: UserRegister

    Return a json with the basic user information:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - company: str
    - things : List[str]
    """
    user_dict = user.dict()
    cur.execute(
        "INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (str(user_dict["user_id"]),user_dict["first_name"],user_dict["last_name"],user_dict["password"],user_dict["company"],user_dict["type_user"],user_dict["email"], str(user_dict["things"])[1:-1]))
    myConexion.commit()
    return user

### Login a user
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
    )
def login(email: EmailStr  = Form(...), password: str = Form(...)):
    """
    Login

    This path operation login a Person in the app

    Parameters:
    - Request body parameters:
        - email: EmailStr
        - password: str

    Returns a LoginOut model with username and message
    """
    cur.execute(
        f"SELECT * FROM project_iot.users WHERE email =  '{str(email)}' AND password = '{password}';"
    )
    row = cur.fetchone()
    myConexion.commit()
    if row is None:
        return LoginOut(email=email, message="Login Unsuccessfully!")
    else:
        return LoginOut(email=email)

### Show all user
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    This path operation shows all users in the app

    Parameters:
    -

    Returns a json list with all users in the app, with the following keys:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: datetime
    """
    cur.execute(
        "SELECT * FROM project_iot.users;"
    )
    reply = [{ "user_id":list(i)[0], 
    "email": list(i)[6], 
    "first_name": list(i)[1], 
    "last_name": list(i)[2], 
    "company": list(i)[4], 
    "things" : list(i)[7].replace("'","").split(",") } for i in cur.fetchall()]
    myConexion.commit()
    return reply

## Show a user by his ID
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="show a User by ID",
    tags=["Users"]
)
def show_a_user_id(user_id : UUID = Path(
        None,
        title = "User ID",
        example = "3fa85f64-5717-4562-b3fc-2c966f66afa6"
    )):
    """
    Show a user by his id

    This path operation Show a User in the app.

    Parameters:
    - Request path parameter
        - user_id: UUID

    Returns a json with the basic user information:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: datetime
    """
    cur.execute(
        f"SELECT * FROM project_iot.users WHERE user_id =  '{str(user_id)}';"
    )
    i = cur.fetchall()
    if i is ():
        myConexion.commit()
        return None
    else:
        i = i[0]
        reply = { "user_id":list(i)[0], 
        "email": list(i)[6], 
        "first_name": list(i)[1], 
        "last_name": list(i)[2], 
        "company": list(i)[4], 
        "things" : list(i)[7].replace("'","").split(",") }
        myConexion.commit()
        return reply

## Show a user by his First Name or Last Name
@app.get(
    path="/users/{first_or_last_name_or_thing}/search",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="show a User by his first name or his last name",
    tags=["Users"]
)
def show_a_user_name(
    first_name : Optional[str] = Query(
    None,
    min_length = 1, 
    max_length=50,
    title = "First Name User",
    ), 
    last_name : Optional[str] = Query(
    None,
    min_length = 1, 
    max_length=50,
    title = "Last Name User",
    ),
    company : Optional[str] = Query(
    None,
    min_length = 1, 
    max_length=50,
    title = "First Name User",
    ),
    thing : Optional[str] = Query(
    None,
    min_length = 1, 
    max_length=50,
    title = "First Name User",
    ),
    ):
    """
    Show a user by first or last name

    This path operation show a User in the app

    Parameters:
    - Request Query parameters:
        - first_name: Optional[str]
        - last_name : Optional[str]
        - company : Optional[str]
        - thing : Optional[str]

    Returns a List of all users that meet the search values
    """
    cur.execute(
        f"SELECT * FROM project_iot.users WHERE first_name like '%{str(first_name)}%' or last_name like '%{str(last_name)}%' or things like '%{str(thing)}%' or company like '%{str(company)}%';"
    )
    set = cur.fetchall()
    if set is ():
        myConexion.commit()
        return None
    else:
        search = []
        for i in set:
            reply = { "user_id":list(i)[0], 
            "email": list(i)[6], 
            "first_name": list(i)[1], 
            "last_name": list(i)[2], 
            "company": list(i)[4], 
            "things" : list(i)[7].replace("'","").split(",") }
            search.append(reply)
        myConexion.commit()
        return search

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user(user_id : UUID = Path(...)):
    """
    Delete a User

    This path operation delete a user in the app

    Parameters:
        - user_id: UUID

    Returns a json with deleted user data:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    answerd = show_a_user_id(user_id)
    cur.execute(
    f"DELETE FROM `project_iot`.`users` WHERE (`user_id` = '{str(user_id)}');"
    )
    myConexion.commit()
    return answerd

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user(user_update : UserRegister = Body(...)):
    user_dict = user_update.dict()
    base_reply = show_a_user_id(user_dict['user_id'])
    base = [ base_reply[key] if value == "" else value for (key,value) in user_dict.items() ]
    cur.execute(
        f"UPDATE `project_iot`.`users` SET `first_name` = '{base[2]}', `last_name` = '{base[3]}', `company` = '{base[4]}', `type_person` = '{base[7]}', `email` = '{base[1]}', `things` = {str(base[5])[1:-1]} WHERE (`user_id` = '{base[0]}' and `password` = '{base[6]}');"
    )
    myConexion.commit()
    return show_a_user_id(base[0])


## Things

## Show a thing by his ID
@app.get(
    path="/thing/{thing_id}",
    response_model=ThingReply,
    status_code=status.HTTP_200_OK,
    summary="show a Thing by ID",
    tags=["Things"]
)
def show_a_thing_id(thing_id : UUID = Path(
        None,
        title = "Thing ID",
        example = "3fa85f64-5717-4562-b3fc-2c966f66afa6"
    )):
    """
    Show a Thing by his id

    This path operation Show a Thing in the app.

    Parameters:
    - Request path parameter
        - thing_id: UUID

    Returns a json with the basic user information:
    - thing_id: UUID
    - name_id: str
    - model: float
    - last_update: datetime
    - status: Status
    - message : str
    """
    cur.execute(
        f"SELECT * FROM project_iot.things WHERE thing_id =  '{str(thing_id)}';"
    )
    i = cur.fetchall()
    if i is ():
        myConexion.commit()
        return None
    else:
        i = i[0]
        reply = { "thing_id":list(i)[0], 
        "name_id": list(i)[1], 
        "model": list(i)[2], 
        "last_update": str(list(i)[3]), 
        "status": list(i)[4], 
        "message" : list(i)[5]}
        myConexion.commit()
        return reply

### Post a thing
@app.post(
    path="/thing/create",
    response_model=ThingReply,
    status_code=status.HTTP_201_CREATED,
    summary="Created a thing",
    tags=["Things"]
)
def create_a_thing(thing : Thing = Body(...)):
    """
    Create a Thing

    This path operations register a user in the app

    Parameters:
    - Request body parameter
        - thing: Thing

    Return a json with the basic user information:
    - thing_id: UUID
    - name_id: str
    - model: float
    - last_update: datetime
    - status: Status
    - message : str
    """
    thing_dict = thing.dict()
    cur.execute(
        "INSERT INTO things VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (str(thing_dict["thing_id"]),thing_dict["name_id"],thing_dict["model"],datetime.today(),"shutdown",'Successful Creation!!!', "No data yet to analyze", datetime.today()))
    myConexion.commit()
    return show_a_thing_id(thing_dict["thing_id"])

### Show all thigns
@app.get(
    path="/things",
    response_model=List[ThingReply],
    status_code=status.HTTP_200_OK,
    summary="Show all things",
    tags=["Things"]
)
def show_all_thing():
    """
    This path operation shows all things in the app

    Returns a json list with all things in the app:
    - thing_id: UUID
    - name_id: str
    - model: float
    - last_update: datetime
    - status: Status
    - message : str
    """
    cur.execute(
        "SELECT * FROM project_iot.things;"
    )
    reply = [{ "thing_id":list(i)[0], 
        "name_id": list(i)[1], 
        "model": list(i)[2], 
        "last_update": str(list(i)[3]), 
        "status": list(i)[4], 
        "message" : list(i)[5]} for i in cur.fetchall()]
    myConexion.commit()
    return reply

## Show a Thing by his Modification Dates
@app.get(
    path="/things/{date_modification}/search",
    response_model=List[ThingReply],
    status_code=status.HTTP_200_OK,
    summary="Show a Thing by his Modification Dates",
    tags=["Things"]
)
def show_a_thing_date(date_search : str = Query(..., example = "2022-02-13")):
    """
    Show a Thing by his Modification Dates

    This path operation Show a Thing in the app.

    Parameters:
    - Request path parameter
        - data_search: str

    Returns a json with the basic user information:
    - thing_id: UUID
    - name_id: str
    - model: float
    - last_update: datetime
    - status: Status
    - message : str
    """
    cur.execute(
        f"SELECT * FROM project_iot.things WHERE modification_dates like '%{date_search}%';"
    )
    set = cur.fetchall()
    if set is ():
        myConexion.commit()
        return None
    else:
        reply = [show_a_thing_id(j[0]) for j in set]
        myConexion.commit()
        return reply

### Analysis
@app.get(
    path = "/things/analysis/{thing_id}",
    response_model= Analysis,
    status_code=status.HTTP_200_OK,
    summary="One thing Analysis ",
    tags=["Things"]
)
def analysis():
    pass

### Update a thing
@app.put(
    path="/things/{thing_id}/update",
    response_model=ThingReply,
    status_code=status.HTTP_200_OK,
    summary="Update a thing",
    tags=["Things"]
)
def update_a_tweet():
    pass

### Delete a thing
@app.delete(
    path="/things/{thing_id}/delete",
    response_model=ThingReply,
    status_code=status.HTTP_200_OK,
    summary="Delete a thing",
    tags=["Things"]
)
def delete_a_thing(thing_id : UUID = Path(
        None,
        title = "Thing ID",
        example = "3fa85f64-5717-4562-b3fc-2c966f66afa6"
    )):
    """
    Delete a thing

    This path operation delete a thing in the app

    Parameters:
        - thing_id: UUID

    Returns a json with deleted thing data:
    - thing_id: UUID
    - name_id: str
    - model: float
    - last_update: datetime
    - status: Status
    - message : str
    """
    answerd = show_a_thing_id(thing_id)
    cur.execute(
    f"DELETE FROM `project_iot`.`things` WHERE (`thing_id` = '{str(thing_id)}');"
    )
    myConexion.commit()
    return answerd


