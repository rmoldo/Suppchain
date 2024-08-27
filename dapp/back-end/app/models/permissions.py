from typing import List, Optional, Set
from sqlmodel import Field, ARRAY, SQLModel, Column, String, JSON
from sqlalchemy.dialects import postgresql


class PermissionBase(SQLModel):
    acl_group: str
    permissions: List[dict] = Field(default=None, sa_column=Column(ARRAY(JSON())))


class Permission(PermissionBase, table=True):
    id: int = Field(default=None, primary_key=True)
