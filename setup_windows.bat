@echo off
python -m venv .venv --without-pip
if errorlevel 1 goto ERROR
.\.venv\Scripts\python.exe -m ensurepip --upgrade
if errorlevel 1 goto ERROR
.\.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto ERROR
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto ERROR
echo SETUP SELESAI.
pause
exit /b 0
:ERROR
echo SETUP GAGAL.
pause
exit /b 1
