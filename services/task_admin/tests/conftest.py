import pytest
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from task_admin.db.tables import metadata

DATABASE_URL = "postgresql://postgres:postgrespw@localhost:55000/test-db"


@pytest.fixture(scope='session')
def db_engine():
    """Yields a SQLAlchemy engine which is suppressed after the test session."""
    engine_ = create_engine(DATABASE_URL, echo=True)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope="session")
def tables(db_engine):
    metadata.create_all(db_engine)
    yield
    metadata.drop_all(db_engine)


@pytest.fixture(scope='session')
def db_session_factory(db_engine, tables):
    """Returns a SQLAlchemy scoped session factory."""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope='function')
def db_session(db_session_factory):
    """Yields a SQLAlchemy connection which is rollbacked after the test."""
    session_ = db_session_factory()
    session_.begin_nested()

    yield session_

    session_.rollback()
    session_.close()
