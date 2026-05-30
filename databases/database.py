from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from databases.models import Base

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/databases"

engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        conn.execute(text("""
                          SELECT create_hypertable(
                          'prices',
                          'time',
                          chunk_time_interval => INTERVAL '1 month',
                          if_not_exists => TRUE);
                          """))
        conn.commit()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()