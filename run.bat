@echo off 
cd /d C:\Users\Dell\pptgenrator\pptx-generator 
call .venv\Scripts\activate.bat 
py -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload 
pause 
