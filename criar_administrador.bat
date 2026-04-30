@echo off
color 0B
echo ==========================================================
echo    CRIANDO USUARIO ADMINISTRADOR NA NUVEM
echo ==========================================================
echo.
echo Conectando ao Vercel e configurando seu acesso...
venv_new\Scripts\python.exe setup_db.py
echo.
echo ==========================================================
echo ACESSO LIBERADO! 
echo O seu usuario administrativo ja esta disponivel!
echo ==========================================================
pause
