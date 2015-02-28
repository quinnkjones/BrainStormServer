from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


DecBase = declarative_base()


def sql_init(dsn):
    engine = create_engine(dsn, pool_size=12)
    DecBase.metadata.create_all(engine)
    global _session
    _session = scoped_session(sessionmaker(bind=engine))