@echo off
title DAY CODE LEN GITHUB - SMARTCONSTRUCT WEB AI
echo ==============================================================================
echo SMARTCONSTRUCT WEB AI - KHOA XAY DUNG - DAI HOC DUY TAN
echo Repository: https://github.com/vantruongbui747-cpu/smartconstruct-web-ai.git
echo ==============================================================================
echo.

set "GIT_EXE=C:\Program Files\Git\cmd\git.exe"
if not exist "%GIT_EXE%" set "GIT_EXE=git"

echo [1/3] Adding all files to git...
"%GIT_EXE%" add .

echo.
echo [2/3] Committing changes...
"%GIT_EXE%" commit -m "Update SmartConstruct 3D BIM and CAD Blueprint"

echo.
echo [3/3] Pushing to GitHub main branch...
echo (Neu co cua so dang nhap hien ra, hay dang nhap tren trinh duyet)
echo.

"%GIT_EXE%" push -u origin main

if errorlevel 1 goto :loi_push

echo.
echo ==============================================================================
echo [THANH CONG] Da day toan bo ma nguon len GitHub!
echo File index.html da san sang cho GitHub Pages.
echo ==============================================================================
goto :ket_thuc

:loi_push
echo.
echo ==============================================================================
echo [THONG BAO] Vui long kiem tra dang nhap hoac xac thuc GitHub.
echo ==============================================================================

:ket_thuc
echo.
pause
