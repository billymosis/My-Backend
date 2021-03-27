<p align="center">
  <img src="https://i.imgur.com/8SKteyR.png" />
</p>

# My Backend

My attempt to create file manager and versioning for non IT user.
The Idea is storing file trough local server http drag and drop files.
Each uploaded file will be given MD5 and auto versioning increment for the one with same file name.

## Motivation

As a Team in civil engineering project we often missused the newest update revision file. And we don't even track it. The files consist of drawing (.dwg), spreadsheet (.xlsx) and document (.docx). File diff is not needed the file mostly in binary or non readable. With lack of document controller in our team I inisiated this APP to help versioning the file.

## To Do

- Implement CRUD
- File per User basis
- Drag and Drop GUI
- Simple user Login

## Main Tools

- FastAPI
- SQLite
- SQLAlchemy