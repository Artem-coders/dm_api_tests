from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class UserMustBeAuthenticated(BaseModel):
    message: Optional[str] = None