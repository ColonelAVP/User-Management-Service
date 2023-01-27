# Required Imports

import databases, sqlalchemy
from fastapi import FastAPI, Response
from sqlalchemy.orm import Session
import models
from typing import List
from database import SessionLocal, engine, Base
from repositories.user_manager import UserRepository

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, Header, HTTPException, Body
from schemas import UserSchema, UserLoginSchema


# FastAPI app config
app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    get_db() initiates a db session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/get-user-data")
async def get_user_details(
    mobile_number: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
    db: Session = Depends(get_db),
):
    """
    get_user_details() -> GET method -> Endpoint to retrieve a user/users
    params -> firstname | lastname | email_id | mobile_number
    """
    # NOTE : Revisit Query Params
    success, response = UserRepository.get_user_data(
        db=db,
        mobile_number=mobile_number,
        email_id=email,
        first_name=first_name,
        last_name=last_name,
    )
    if not success:
        bad_response = {"code": 400, "message": response}
        return JSONResponse(status_code=400, content=bad_response)
    data = jsonable_encoder(response)
    final_response = {"code": 200, "user_data": data}
    return JSONResponse(status_code=200, content=final_response)


# return response
@app.post("/create-user")
async def create_user(user: UserSchema, db: Session = Depends(get_db)):
    """
    create_user() -> POST method -> Endpoint to create user
    params -> user, db
    """
    success, response = UserRepository.create_user(user=user, db=db)
    if not success:
        bad_response = {"code": 400, "message": response}
        return JSONResponse(status_code=400, content=bad_response)
    final_response = {"code": 200, "message": response}
    return JSONResponse(status_code=200, content=final_response)


@app.delete("/delete-user")
async def delete_user(
    email_id: str = None, mobile_number: str = None, db: Session = Depends(get_db)
):
    """
    delete_user() -> DELETE method -> Endpoint to delete a specific user
    params -> email_id | mobile_number
    """
    success, response = UserRepository.delete_user(
        db=db, email_id=email_id, mobile_number=mobile_number
    )
    if not success:
        bad_response = {"code": 400, "message": response}
        return JSONResponse(status_code=400, content=bad_response)
    final_response = {"code": 200, "message": response}
    return JSONResponse(status_code=200, content=final_response)


@app.patch("/update-user-data/")
async def update_user_data(
    user_data: dict,
    db: Session = Depends(get_db),
):
    """
    update_user_data() -> PATCH method -> Endpoint to update user in DB
    params -> user_data: str, db
    """
    valid_user_data = user_data.get("user_data")
    print(user_data)
    mobile_number = user_data.get("mobile_number")
    email_id = user_data.get("email_id")
    print(mobile_number)
    success, response = UserRepository.update_user(
        user_data=valid_user_data, db=db, email_id=email_id, mobile_number=mobile_number
    )
    if not success:
        bad_response = {"code": 400, "message": response}
        return JSONResponse(status_code=400, content=bad_response)
    final_response = {"code": 200, "message": response}
    return JSONResponse(status_code=200, content=final_response)


@app.post("/login-user")
async def user_login(creds: UserLoginSchema, db: Session = Depends(get_db)):
    """
    user_login() -> POST method -> Endpoint to login a user in system
    params -> credentials, db
    """
    success, response = UserRepository.login_user_token(
        password=creds.password, email_id=creds.email_id, db=db
    )
    if not success:
        bad_response = {"code": 400, "message": response}
        return JSONResponse(status_code=400, content=bad_response)
    final_response = {"code": 200, "tokens": response}
    return JSONResponse(status_code=200, content=final_response)
