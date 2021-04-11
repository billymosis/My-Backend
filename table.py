from sqlalchemy import create_engine
from sqlalchemy import text

# import sqlite3
# conn = sqlite3.connect('./db/test.db')
# conn.execute('drop table TEST1')
# conn.execute('''CREATE TABLE TEST1
#          (ID INTEGER PRIMARY KEY,
#          FILENAME           TEXT    NOT NULL,
#          DIRECTORY            TEXT     NOT NULL,
#          MD5        TEXT    NOT NULL,
#          VERSION    INT     NOT NULL,
#          MESSAGE    TEXT,
#          UPLOADER   TEXT    NOT NULL
#          );''')
# conn.execute('''
#             INSERT INTO TEST1 (FILENAME DIRECTORY MD5 VERSION MESSAGE UPLOADER)
#             VALUES ('%s', 'temp', '%s', '%d', '%s', '%s')
#             ''' % ('woke', 'thismd5', 0, 'first commit', 'billy'))
# conn.close()

engine = create_engine("sqlite:///db/test.db", echo=True)

# with engine.connect() as conn:
#     conn.execute(
#         text(
#             """
#             INSERT INTO TEST1
#             (FILENAME, DIRECTORY, MD5, VERSION, MESSAGE, UPLOADER)
#             VALUES (:a, 'temp', :b, :c, :d, :e)
#             """
#         ),
#         [{"a": "ntva", "b": "mddx", "c": 0, "d": "first commit", "e": "billy"}],
#     )

#     print("done commiting")


with engine.connect() as conn:
    conn.execute(text("DROP TABLE TEST1"))
    conn.execute(
        text(
            """
            CREATE TABLE TEST1
            (ID INTEGER PRIMARY KEY NOT NULL, FILENAME TEXT NOT NULL,
            DIRECTORY TEXT NOT NULL,MD5 TEXT NOT NULL UNIQUE,
            VERSION INT NOT NULL,
            MESSAGE TEXT, UPLOADER TEXT NOT NULL)
            """
        )
    )
