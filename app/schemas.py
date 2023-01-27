from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    gender: str
    email_id: str
    country_code: str
    mobile_number: str
    passcode: str = Field(max_length=4)
    profile_picture: str
    # tags = Column(ARRAY, blank=True, null=True)y

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email_id: str
    password: str


class UserSerialiser(BaseModel):
    first_name: str
    last_name: str
    gender: str
    email_id: str
    country_code: str
    mobile_number: str
    passcode: str
    profile_picture: str
