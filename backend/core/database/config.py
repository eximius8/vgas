from sqlmodel import SQLModel, Session, create_engine

from backend.settings import SQLALCHEMY_DATABASE_URI


engine = create_engine(SQLALCHEMY_DATABASE_URI)


def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(engine)

