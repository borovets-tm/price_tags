@echo off
start microsoft-edge:http://localhost:8000/
cd C:\Users\t.m.borovets\Documents\my_django\price_tags
venv/Scripts/activate.ps1
python manage.py runserver
cmd /k