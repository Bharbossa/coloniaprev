@echo off
color 0C
echo ==========================================================
echo    FORCE PUSH - CORRIGINDO PONTO DE ENTRADA VERCEL
echo ==========================================================
echo.
echo 1. Limpando cache do Git...
git rm -r --cached . >nul 2>&1
echo 2. Adicionando todos os arquivos (incluindo app.py)...
git add -A
echo 3. Criando commit de correção...
git commit -m "Fix: Adicionando ponto de entrada app.py e vercel.json corrigido"
echo 4. Enviando para o servidor...
git push origin main --force
echo.
echo ==========================================================
echo PRONTO! O Vercel deve detectar o app.py agora.
echo Verifique o painel do Vercel e o "Building" novamente.
echo ==========================================================
pause
