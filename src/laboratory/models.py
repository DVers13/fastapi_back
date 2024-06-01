from sqlalchemy import ForeignKey, Sequence, Table, Column, Integer, String, TIMESTAMP, MetaData

from auth.models import user, group
metadata = MetaData()

subject = Table(
    "subject",
    metadata,
    Column("id", Integer, Sequence('subject_id_seq', start=0, increment=1), primary_key=True),
    Column("name", String, nullable=False),
)


discipline = Table(
    "discipline",
    metadata,
    Column("id", Integer, Sequence('discipline_id_seq', start=0, increment=1), primary_key=True),
    Column("subject_id", Integer, ForeignKey(subject.c.id, ondelete="CASCADE")),
)

discipline_groups = Table(
    "discipline_groups",
    metadata,
    Column("id", Integer, Sequence('discipline_groups_id_seq', start=0, increment=1), primary_key=True),
    Column("group_id", Integer, ForeignKey(group.c.id, ondelete="CASCADE")),
    Column("discipline_id", Integer, ForeignKey(discipline.c.id, ondelete="CASCADE")),
)

discipline_teacher = Table(
    "discipline_teacher",
    metadata,
    Column("id", Integer, Sequence('discipline_teacher_id_seq', start=0, increment=1), primary_key=True),
    Column("teacher_id", Integer, ForeignKey(user.c.id, ondelete="CASCADE")),
    Column("discipline_id", Integer, ForeignKey(discipline.c.id, ondelete="CASCADE")),
)

laboratory = Table(
    "laboratory",
    metadata,
    Column("id", Integer, Sequence('laboratory_id_seq', start=0, increment=1), primary_key=True),
    Column("name", String),
    Column("url", String, nullable=True),
    Column("discipline_id", Integer, ForeignKey(discipline.c.id, ondelete="CASCADE")),
    Column("deadline", TIMESTAMP),
)