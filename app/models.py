# Required Imports
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    CHAR,
    ARRAY,
    DateTime,
    Date,
)
from sqlalchemy_utils import URLType
from pydantic import Field
from database import Base


class User(Base):
    """
    Class User() -> User Model with respective fields
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(CHAR)
    email_id = Column(String, unique=True, index=True)
    country_code = Column(Integer)
    mobile_number = Column(String, unique=True)
    hashed_passcode = Column(String)
    profile_picture = Column(URLType)
    # tags = Column(ARRAY, blank=True, null=True)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)
