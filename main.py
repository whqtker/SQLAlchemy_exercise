from sqlalchemy import create_engine, text
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from sqlalchemy import insert, delete

# PostgreSQL 데이터베이스 연결 정보
username = 'postgres'
password = '1234'
host = 'localhost'
port = '5432'
database = 'exercise'

db_url = f'postgresql://{username}:{password}@{host}:{port}/{database}'

# 데이터베이스 엔진 생성
engine = create_engine(db_url, echo=False)

metadata_obj = MetaData(bind=engine)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
db = SessionLocal()

def create_table_and_insert():
    Base = declarative_base()

    class User(Base):
        __tablename__ = 'temp_table'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        email = Column(String)

    new_users = [
        {'name': 'John Doe', 'email': 'john.doe@example.com'},
        {'name': 'Jane Smith', 'email': 'jane.smith@example.com'},
        {'name': 'Bob Johnson', 'email': 'bob.johnson@example.com'}
    ]

    with engine.begin() as conn:
        conn.execute(User.__table__.insert(), new_users)

def main():
    create_table_and_insert()

if __name__ == '__main__':
    main()