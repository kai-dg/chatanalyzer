@echo off
IF EXIST "venv\" (
  cd %CD%
  start cmd.exe /k "venv\scripts\activate.bat"^
    "&&python chatcmd.py"
) ELSE (
  cd %CD%
  start cmd.exe /k "echo Setting up environment...please wait..."^
    "&&python -m venv venv"^
    "&&venv\Scripts\activate.bat"^
    "&&echo Installing python packages...please wait..."^
    "&&pip install -r requirements.txt"^
    "&&echo ...done"^
    "&&python chatcmd.py"
)

