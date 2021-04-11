import os
from typing import List
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.datastructures import UploadFile
from fastapi.params import File
from pathlib import Path
from sqlalchemy.sql.expression import false, text
from starlette.requests import Request
from file import md5sum
from fastapi.responses import FileResponse, HTMLResponse
import handleUpload
from sqlalchemy import create_engine
import uvicorn


app = FastAPI()

engine = create_engine("sqlite:///db/test.db", echo=True)


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        if os.path.exists("temp") is false:
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


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    templates = Jinja2Templates(directory="templates")
    files = []
    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT FILENAME,
                DIRECTORY,
                MD5,
                VERSION,
                MESSAGE,
                UPLOADER
                FROM TEST1
                """
            )
        )
        for FILENAME, DIRECTORY, MD5, VERSION, MESSAGE, UPLOADER in result:
            files.append((FILENAME, DIRECTORY, MD5, VERSION, MESSAGE, UPLOADER))
    return templates.TemplateResponse("item.html", {"request": request, "files": files})


@app.get("/serve/{file_path:path}")
async def get_files(file_path: str):

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT FILENAME FROM TEST1 WHERE MD5 == '%s' " % (file_path))
        ).first()
    return FileResponse("./.serve/" + file_path, filename=result[0])


@app.delete("/serve/{file_md5}")
async def delete_files(file_md5: str):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM TEST1 WHERE MD5 == '%s' " % (file_md5)))
    handleUpload.delete_file("./.serve/" + file_md5)
    return {"message": "Post has been deleted succesfully"}


def start():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
