import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Department(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'department'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String)
    chief_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    chief = sa.orm.relationship('User')
    members = sa.Column(sa.String)
    email = sa.Column(sa.String)
