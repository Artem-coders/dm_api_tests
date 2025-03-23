from __future__ import annotations
from dm_api_account.models.user_envelope import UserRole, Rating
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict



class Info(BaseModel):
    value: str = Field(None, alias='value')
    parseMode: str


class Paging(BaseModel):
    postsPerPage: int
    commentsPerPage: int
    topicsPerPage: int
    messagesPerPage: int
    entitiesPerPage: int


class Settings(BaseModel):
    colorSchema: str
    nannyGreetingsMessage: str = Field(None, alias='nannyGreetingsMessage')
    paging: Paging


class Resource(BaseModel):
    login: str
    roles: List[UserRole]
    mediumPictureUrl: str = Field(None, alias='mediumPictureUrl')
    smallPictureUrl: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None, alias='status')
    rating: Rating
    online: str
    name: str = Field(None, alias='name')
    location: str = Field(None, alias='location')
    registration: str = Field(None, alias='registration')
    icq: str = Field(None, alias='icq')
    skype: str = Field(None, alias='skype')
    originalPictureUrl: str = Field(None, alias='originalPictureUrl')
    info: str = None
    settings: Settings


class GetUser(BaseModel):
    model_config = ConfigDict(extra='forbid')
    resource: Resource
    metadata: str = Field(None, alias='originalPictureUrl')