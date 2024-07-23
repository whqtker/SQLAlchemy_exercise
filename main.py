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

def insert_data(table_name, data):
    table = Table(table_name, metadata_obj, autoload_with=engine)
    ins = table.insert().values(data)
    db.execute(ins)
    db.commit()
    db.close()

def delete_data(table_name, data):
    table = Table(table_name, metadata_obj, autoload_with=engine)
    del_data = table.delete().where(table.c.id == data['id'])
    db.execute(del_data)
    db.commit()
    db.close()

def create_table():
    # 기본 클래스 생성
    Base = declarative_base()

    # User 테이블 정의
    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String, nullable=False)
        email = Column(String, nullable=False)

    # 데이터베이스에 테이블 생성
    Base.metadata.create_all(engine)

def drop_table(table_name):
    try:
        # 메타데이터에 테이블 로드
        metadata_obj.reflect(bind=engine)
        
        # 테이블 객체 가져오기
        table = metadata_obj.tables.get(table_name)

        if table is not None:
            # 테이블 삭제
            with engine.begin() as connection:
                connection.execute(text(f"DROP TABLE {table_name} CASCADE"))
            print(f"테이블 '{table_name}'이(가) 삭제되었습니다.")
        else:
            print(f"테이블 '{table_name}'이(가) 존재하지 않습니다.")
    except Exception as e:
        print(f"테이블 삭제 중 오류 발생: {str(e)}")

def main():
    # ins_data = [
    #     {'id': 96541, 'name': 'Alice', 'dept_name': 'Comp. Sci.', 'tot_cred': 5},
    #     {'id': 96542, 'name': 'Bob', 'dept_name': 'Comp. Sci.', 'tot_cred': 4},
    #     {'id': 96543, 'name': 'Charlie', 'dept_name': 'Comp. Sci.', 'tot_cred': 7},
    #     {'id': 96544, 'name': 'David', 'dept_name': 'Comp. Sci.', 'tot_cred': 10},
    #     {'id': 96545, 'name': 'Eve', 'dept_name': 'Comp. Sci.', 'tot_cred': 1}
    # ]
    # insert_data('student', ins_data)

    # del_data = {'id': 99999}
    # delete_data('student', del_data)

    # create_table()

    # drop_table('users')

if __name__ == '__main__':
    main()