# app/schemas.py

from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class PhoneBase(BaseModel):
    identifier: str

    model_config = ConfigDict(from_attributes=True)

class Phone(PhoneBase):
    phoneId: int

    model_config = ConfigDict(from_attributes=True)

class VoicemailBase(BaseModel):
    identifier: str

    model_config = ConfigDict(from_attributes=True)

class Voicemail(VoicemailBase):
    vmId: int

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    id: int  # Changed from str to int
    userId: str  # Adjust if necessary
    originationTime: int
    clusterId: str

    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    phones: List[Phone] = []
    voicemails: List[Voicemail] = []

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
