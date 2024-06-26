from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Sequence, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
from sqlalchemy.dialects.postgresql import ARRAY
from database import Base

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, Sequence('role_id_seq', start=0, increment=1), primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", ARRAY(String)),
)

group = Table(
    "group",
    metadata,
    Column("id", Integer, Sequence('group_id_seq', start=0, increment=1), primary_key=True),
    Column("name", String, nullable=False),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, Sequence('user_id_seq', start=0, increment=1), primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id, ondelete="CASCADE")),
    Column("group_id", Integer, ForeignKey(group.c.id, ondelete="CASCADE"), nullable=True),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, Sequence('user_id_seq', start=0, increment=1), primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey(role.c.id, ondelete="CASCADE"))
    group_id = Column(Integer, ForeignKey(group.c.id, ondelete="CASCADE"), nullable=True)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)