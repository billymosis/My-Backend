import os
from typing import List
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.datastructures import UploadFile
from fastapi.params import File
from pathlib import Path
from sqlalchemy.sql.expression import text
from starlette.requests import Request
from file import md5sum
from fastapi.responses import FileResponse, HTMLResponse
import handleUpload
from sqlalchemy import create_engine


app = FastAPI()

engine = create_engine("sqlite:///db/test.db", echo=True)


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        os.mkdir("temp")
        y = Path("./temp/" + file.filename)
        if handleUpload.save_upload_file(file, y) is True:
            md5 = md5sum(y)
            z = Path("./.serve/" + md5)
            os.rename(y, z)
            with engine.connect() as conn:
                conn.execute(
                    text(
                        """
                        INSERT INTO TEST1
                        (FILENAME, DIRECTORY, MD5, VERSION, MESSAGE, UPLOADER)
                        VALUES (:a, 'serve', :b, :c, :d, :e)
                        """
                    ),
                    {
                        "a": file.filename,
                        "b": md5,
                        "c": 0,
                        "d": "first commit",
                        "e": "billy",
                    },
                )
                print("done commiting")
            return {"filenames": [file.filename for file in files]}


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    files = []
    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
        SELECT FILENAME,
        DIRECTORY,
        MD5
        FROM TEST1
        """
            )
        )
        for FILENAME, DIRECTORY, MD5 in result:
            files.append((FILENAME, DIRECTORY, MD5))
    return templates.TemplateResponse("item.html", {"request": request, "files": files})


@app.get("/serve/{file_path:path}")
async def get_files(file_path: str):

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT FILENAME FROM TEST1 WHERE MD5 == '%s' " % (file_path))
        ).first()
    return FileResponse("./.serve/" + file_path, filename=result[0])
