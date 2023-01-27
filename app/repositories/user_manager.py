# Required Imports

from sqlalchemy.orm import Session
from models import User
from schemas import UserSchema, UserSerialiser
from datetime import datetime
from utils.crypto import get_hashed_password, verify_password
from utils.tokeniser import create_access_token, create_refresh_token
from pydantic import parse_obj_as
from typing import List

from fastapi.security import OAuth2PasswordRequestForm


class UserRepository:
    """
    Class UserRepository contains repository functions for user
    """

    @staticmethod
    def get_user_data(
        db: Session, email_id=None, mobile_number=None, first_name=None, last_name=None
    ):
        """
        Function that retrieves a user or users
        params -> firstname | lastname | email_id | mobile_number
        There could be only one Param
        returns -> User/s
        """
        query = db.query(
            User.first_name,
            User.last_name,
            User.gender,
            User.email_id,
            User.country_code,
            User.mobile_number,
            User.profile_picture,
        )
        if not email_id and not mobile_number and not first_name and not last_name:
            users_data = query.all()
            if not users_data:
                return False, "No Users Exist"
            return True, users_data
        user_data = None
        if email_id:
            user_data = query.filter(User.email_id == email_id).all()
        if mobile_number:
            user_data = query.filter(User.mobile_number == mobile_number).all()
        if first_name:
            user_data = query.filter(User.first_name == first_name).all()
        if last_name:
            user_data = query.filter(User.last_name == last_name).all()
        if not user_data:
            return False, "User not found"
        return True, user_data

    @staticmethod
    def create_user(user: UserSchema, db: Session):
        """
        create_user() function creates user in database
        params -> user, db
        returns -> bool, str
        """
        instance = db.query(User).filter_by(mobile_number=user.mobile_number).first()
        if instance:
            return False, "user already Exists!"
        created_at = datetime.now()
        modified_at = datetime.now()
        hashed_passcode = get_hashed_password(user.passcode)
        if not hashed_passcode:
            return False, "Password should be 4 digit"
        user_kwargs = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "gender": user.gender,
            "email_id": user.email_id,
            "country_code": user.country_code,
            "mobile_number": user.mobile_number,
            "hashed_passcode": hashed_passcode,
            "profile_picture": user.profile_picture,
            "created_at": created_at,
            "modified_at": modified_at,
        }

        new_user = User(**user_kwargs)
        db.add(new_user)
        db.commit()
        return True, "User Created Successfully"

    @staticmethod
    def delete_user(db: Session, email_id: str = None, mobile_number: str = None):
        """
        delete_user() function deletes a user in database
        params -> email_id, db
        returns -> bool, str
        """
        if not email_id and not mobile_number:
            return False, "Invalid Params"
        if email_id:
            user = db.query(User).filter(User.email_id == email_id).first()
        else:
            user = db.query(User).filter(User.mobile_number == mobile_number).first()
        if not user:
            return False, "User Not Found"
        db.delete(user)
        db.commit()
        return True, "User Deleted Successfully"

    @staticmethod
    def update_user(
        user_data: dict, db: Session, email_id=None, mobile_number: str = None
    ):
        """
        update_user() function updates a specific user in db
        params -> user, db, email_id | mobile_number
        returns -> bool, str
        """
        if not email_id and not mobile_number:
            return False, "Invalid Params"
        if email_id:
            user = db.query(User).filter(User.email_id == email_id).first()
        if mobile_number:
            user = db.query(User).filter(User.mobile_number == mobile_number).first()
        if not user:
            return False, "User not Found"
        user_data["modified_at"] = datetime.now()
        for key, value in user_data.items():
            setattr(user, key, value)
        db.add(user)
        # db.query(User).update(user_data)
        db.commit()
        db.refresh(user)
        return True, "User Data updated Successfully"

    @staticmethod
    def login_user_token(
        db: Session, password: str, email_id: str = None, mobile_number: str = None
    ):
        """
        login_user_token() logins a user by creating a access and refresh token
        params -> db, password, email_id | mobile_number
        returns -> bool, dict
        """
        if not email_id and not mobile_number:
            return False, "Incorrect credentials"
        if email_id:
            verified_user = db.query(User).filter_by(email_id=email_id).first()
            if not verified_user:
                return False, "Incorrect Email!!!"
        else:
            verified_user = (
                db.query(User).filter_by(mobile_number=mobile_number).first()
            )
        hash_password = verified_user.hashed_passcode
        verified_password = verify_password(
            password=password, hashed_pass=hash_password
        )
        if not verified_password:
            return False, "Incorrect Password!!!"
        access_token = create_access_token(email_id)
        refresh_token = create_refresh_token(email_id)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return True, tokens
