from __future__ import annotations
from dm_api_account.models.user_envelope import UserRole, Rating
from typing import List, Optional
from pydantic import BaseModel, Field, root_validator, ConfigDict


class DeleteUser(BaseModel):
    message: str