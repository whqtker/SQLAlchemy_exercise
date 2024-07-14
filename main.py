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

metadata_obj = MetaData()
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
db = SessionLocal()

def insert(table_name, data):
    table = Table(table_name, metadata_obj, autoload_with=engine)
    ins = table.insert().values(data)
    db.execute(ins)
    db.commit()
    db.close()

def main():
    insert('student', {'id': 96541, 'name': 'Alice', 'dept_name': 'Comp. Sci.', 'tot_cred': 5})

if __name__ == '__main__':
    main()