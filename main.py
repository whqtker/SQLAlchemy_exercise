from sqlalchemy import create_engine, text
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from sqlalchemy import insert, delete
from sqlalchemy.exc import SQLAlchemyError

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

def Insert(db):
    table_name = input("삽입할 테이블 이름을 입력하세요: ")
    
    try:
        # 메타데이터 객체 생성 및 테이블 정보 가져오기
        metadata_obj.reflect(bind=db.bind)
        
        table = Table(table_name, metadata_obj, autoload_with=db.bind)

        print(f"'{table_name}' 테이블의 컬럼: {[column.name for column in table.columns]}")
        
        # 사용자로부터 각 속성의 값을 입력받기
        values = {}
        for column in table.columns:
            user_input = input(f"{column.name}의 값: (타입: {column.type}): ")
            values[column.name] = user_input

        insert_statement = table.insert().values(**values)

        db.execute(insert_statement)
        db.commit()

        print(f"'{table_name}' 테이블에 데이터가 성공적으로 삽입되었습니다.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"삽입 오류: {str(e)}")
    except Exception as e:
        print(f"오류: {str(e)}")

def Select(db):
    table_name = input("조회할 테이블 이름을 입력하세요: ")
    
    try:
        # 메타데이터 객체 생성 및 테이블 정보 가져오기
        metadata_obj.reflect(bind=db.bind)
        
        table = Table(table_name, metadata_obj, autoload_with=db.bind)

        # 테이블의 모든 데이터 조회
        select_statement = table.select()
        result = db.execute(select_statement)

        # 결과 출력
        rows = result.fetchall()
        if rows:
            print(f"'{table_name}' 테이블의 데이터:")
            for row in rows:
                print(dict(row._mapping))
        else:
            print(f"'{table_name}' 테이블에는 데이터가 없습니다.")
    except SQLAlchemyError as e:
        print(f"조회 오류: {str(e)}")
    except Exception as e:
        print(f"오류: {str(e)}")

def Update(db):
    table_name = input("업데이트할 테이블 이름을 입력하세요: ")
    
    try:
        # 메타데이터 객체 생성 및 테이블 정보 가져오기
        metadata_obj.reflect(bind=db.bind)
        
        table = Table(table_name, metadata_obj, autoload_with=db.bind)

        print(f"'{table_name}' 테이블의 컬럼: {[column.name for column in table.columns]}")

        # 조건 입력받기
        condition_column = input("조건으로 사용할 컬럼 이름: ")
        condition_value = input(f"{condition_column}의 값: ")

        # 업데이트할 값 입력받기
        update_values = {}
        for column in table.columns:
            user_input = input(f"{column.name}의 새로운 값 입력(업데이트하지 않으려면 Enter): ")
            if user_input:
                update_values[column.name] = user_input

        # 업데이트 쿼리 생성
        update_statement = table.update().where(getattr(table.c, condition_column) == condition_value).values(**update_values)

        result = db.execute(update_statement)
        db.commit()

        print(f"'{table_name}' 테이블의 데이터가 성공적으로 업데이트되었습니다. 업데이트된 행 수: {result.rowcount}")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"업데이트 오류: {str(e)}")
    except Exception as e:
        print(f"오류: {str(e)}")

def Delete(db):
    table_name = input("삭제할 테이블 이름을 입력하세요: ")
    
    try:
        # 메타데이터 객체 생성 및 테이블 정보 가져오기
        metadata_obj.reflect(bind=db.bind)
        
        table = Table(table_name, metadata_obj, autoload_with=db.bind)
        
        print(f"'{table_name}' 테이블의 컬럼: {[column.name for column in table.columns]}")

        # 삭제할 조건 입력받기
        condition_column = input("삭제할 조건으로 사용할 컬럼 이름: ")
        condition_value = input(f"{condition_column}의 값: ")

        delete_statement = table.delete().where(getattr(table.c, condition_column) == condition_value)

        result = db.execute(delete_statement)
        db.commit()

        print(f"'{table_name}' 테이블에서 {result.rowcount}개의 행이 삭제되었습니다.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"삭제 오류: {str(e)}")
    except Exception as e:
        print(f"오류: {str(e)}")

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
    # create_table()

    # drop_table('users')

    # Insert(db)

    # Select(db)

    # Update(db)

    Delete(db)

if __name__ == '__main__':
    main()