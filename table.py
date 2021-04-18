from sqlalchemy import create_engine
from sqlalchemy import text
import os
import shutil
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


def delete():
    engine = create_engine("postgresql+psycopg2://billy:1111@localhost:5432/xdb")
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS TEST1"))


def removeFolder():
    if os.path.exists("./.temp") is True:
        shutil.rmtree("./.temp")
    if os.path.exists("./.serve") is True:
        shutil.rmtree("./.serve")


Base = declarative_base()


class file_list(Base):
    __tablename__ = "test1"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    directory = Column(String, nullable=False)
    md5 = Column(String, nullable=False, unique=True)
    version = Column(Integer, nullable=False)
    message = Column(String)
    uploader = Column(String, nullable=False)


def create():
    if os.path.exists("./.temp") is False:
        os.mkdir("./.temp")
    if os.path.exists("./.serve") is False:
        os.mkdir("./.serve")
    engine = create_engine("postgresql+psycopg2://billy:1111@localhost:5432/xdb")
    Base.metadata.create_all(engine)
    # with engine.connect() as conn:
    #     conn.execute(
    #         text(
    #             """
    #             CREATE TABLE IF NOT EXISTS TEST1
    #             (ID SERIAL PRIMARY KEY, FILENAME TEXT NOT NULL,
    #             DIRECTORY TEXT NOT NULL,MD5 TEXT NOT NULL UNIQUE,
    #             VERSION INT NOT NULL,
    #             MESSAGE TEXT, UPLOADER TEXT NOT NULL)
    #             """
    #         )
    #     )


if __name__ == "__main__":
    delete()
    removeFolder()
    create()
