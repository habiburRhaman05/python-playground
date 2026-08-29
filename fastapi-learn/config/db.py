from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .env import envVariables


db_engine = create_engine(
    envVariables.DATABASE_URL,
    pool_pre_ping=True
)

sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=db_engine
)

Base = declarative_base()


def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()