from sqlalchemy import inspect
from sqlalchemy.orm.session import Session
from ..db import Base


def add_to_db(session: Session, obj: Base) -> None:
    session.add(obj)
    session.commit()
    session.refresh(obj)


def object_as_dict(obj) -> dict:
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
