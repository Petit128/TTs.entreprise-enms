@echo off
echo Nettoyage des fichiers temporaires...
del /s /q *.pyc 2>nul
del /s /q config\*.db 2>nul
del /s /q reports\*.md 2>nul
echo Nettoyage termin? !
pause
