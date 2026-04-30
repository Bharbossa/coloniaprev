@echo off
title Iniciando o COLONIAPREV
echo ========================================================
echo        SISTEMA DE INICIALIZACAO - COLONIAPREV
echo ========================================================
echo.
echo [1/3] Instalando os modulos do MySQL e do Python...
venv_new\Scripts\pip.exe install -r requirements.txt
echo.
echo ========================================================
echo AVISO IMPORTANTE SOBRE O BANCO DE DADOS:
echo O seu MySQL (ex: XAMPP, Workbench) precisa estar LIGADO!
echo E voce precisa ter criado um banco vazio chamado: coloniaprev
echo ========================================================
echo.
echo [2/3] Criando a estrutura das tabelas no MySQL...
venv_new\Scripts\python.exe setup_db.py
echo.
echo [3/3] Ligando o servidor web do site...
echo.
echo Pode acessar no seu navegador o link: http://localhost:5000
echo.
venv_new\Scripts\python.exe run.py


pause
