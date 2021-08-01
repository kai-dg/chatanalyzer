@echo off
IF EXIST "venv\" (
  cd %CD%
  start cmd.exe /k "venv\scripts\activate.bat"^
    "&&echo Chat Analyzer: python chatanal.py [livestream_url]"
) ELSE (
  cd %CD%
  start cmd.exe /k "echo Setting up environment...please wait..."^
    "&&python -m venv venv"^
    "&&venv\Scripts\activate.bat"^
    "&&pip install -r requirements.txt"^
    "&&echo Chat Analyzer: python chatanal.py [livestream_url]"
)

