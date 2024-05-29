from sqlalchemy import ForeignKey, Table, Column, Integer, String, TIMESTAMP, MetaData, Boolean

from auth.models import user
from laboratory.models import laboratory
metadata = MetaData()

student_laboratory = Table(
    "student_laboratory",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_lab", Integer, ForeignKey(laboratory.c.id)),
    Column("id_student", Integer, ForeignKey(user.c.id)),
    Column("loading_time", TIMESTAMP),
    Column("url", String),
    Column("status", Boolean),
    Column("score", String),
    Column("count_try", Integer),
)