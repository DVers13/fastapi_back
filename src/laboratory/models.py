from sqlalchemy import ForeignKey, Table, Column, Integer, String, TIMESTAMP, MetaData

from auth.models import user, group
metadata = MetaData()

subject = Table(
    "subject",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)


discipline = Table(
    "discipline",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("info", String, nullable=True),
    Column("subject_id", Integer, ForeignKey(subject.c.id)),
)

discipline_groups = Table(
    "discipline_groups",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("group_id", Integer, ForeignKey(group.c.id)),
    Column("discipline_id", Integer, ForeignKey(discipline.c.id)),
)

discipline_teacher = Table(
    "discipline_teacher",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("teacher_id", Integer, ForeignKey(user.c.id)),
    Column("discipline_id", Integer, ForeignKey(discipline.c.id)),
)

laboratory = Table(
    "laboratory",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("url", String, nullable=True),
    Column("discipline_id", Integer, ForeignKey(discipline.c.id)),
    Column("deadline", TIMESTAMP),
)