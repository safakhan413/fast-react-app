# app/schemas.py

from pydantic import BaseModel
from typing import List, Optional

class PhoneBase(BaseModel):
    identifier: str

class Phone(PhoneBase):
    phoneId: int

    class Config:
        orm_mode = True

class VoicemailBase(BaseModel):
    identifier: str

class Voicemail(VoicemailBase):
    vmId: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    id: str
    userId: str
    originationTime: int
    clusterId: str

class User(UserBase):
    phones: List[Phone] = []
    voicemails: List[Voicemail] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
