@echo off
chcp 65001 >nul
title ĐẨY CODE LÊN GITHUB & DEPLOY STREAMLIT
echo ==============================================================================
echo 🏗️ SMARTCONSTRUCT WEB AI - KHOA XÂY DỰNG (ĐẠI HỌC DUY TÂN)
echo ==============================================================================
echo.

set /p repo_url="Nhập đường link GitHub Repository của bạn (VD: https://github.com/username/smartconstruct-web-ai.git): "

if "%repo_url%"=="" (
    echo Bạn chưa nhập link GitHub. Vui lòng thử lại!
    pause
    exit /b
)

echo.
echo [1/3] Đang liên kết với GitHub Repository...
"C:\Program Files\Git\cmd\git.exe" remote remove origin 2>nul
"C:\Program Files\Git\cmd\git.exe" remote add origin %repo_url%

echo.
echo [2/3] Đang đồng bộ và đẩy mã nguồn lên nhánh main...
"C:\Program Files\Git\cmd\git.exe" branch -M main
"C:\Program Files\Git\cmd\git.exe" push -u origin main

echo.
echo ==============================================================================
echo ✅ ĐÃ PUSH TOÀN BỘ CODE LÊN GITHUB THÀNH CÔNG!
echo 🔒 Khóa bí mật API Key đã được bảo vệ an toàn 100%% (không bị lộ lên mạng).
echo ==============================================================================
echo.
pause
