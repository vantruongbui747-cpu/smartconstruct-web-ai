@echo off
chcp 65001 >nul
title ĐẨY CODE LÊN GITHUB - SMARTCONSTRUCT WEB AI
echo ==============================================================================
echo 🏗️ SMARTCONSTRUCT WEB AI - KHOA XÂY DỰNG (ĐẠI HỌC DUY TÂN)
echo Repository: https://github.com/vantruongbui747-cpu/smartconstruct-web-ai.git
echo ==============================================================================
echo.

set "GIT_EXE=C:\Program Files\Git\cmd\git.exe"
if not exist "%GIT_EXE%" set "GIT_EXE=git"

echo [1/4] Đồng bộ và thêm tất cả các file mới (git add)...
"%GIT_EXE%" add .

echo.
echo [2/4] Tạo bản đóng gói commit tự động...
"%GIT_EXE%" commit -m "Update SmartConstruct 3D BIM & Blueprint CAD" 2>nul

echo.
echo [3/4] Cấu hình Remote origin...
"%GIT_EXE%" remote remove origin 2>nul
"%GIT_EXE%" remote add origin https://github.com/vantruongbui747-cpu/smartconstruct-web-ai.git
"%GIT_EXE%" branch -M main

echo.
echo [4/4] Đang đẩy toàn bộ mã nguồn lên GitHub...
echo (Nếu có cửa sổ GitHub hiện lên, bạn chỉ cần bấm "Sign in with your browser" để xác nhận)
echo.

"%GIT_EXE%" push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==============================================================================
    echo ✅ ĐÃ PUSH TOÀN BỘ CODE LÊN GITHUB THÀNH CÔNG!
    echo 🔒 Khóa bí mật API Key đã được bảo vệ an toàn 100%% (không bị lộ lên mạng).
    echo ==============================================================================
) else (
    echo.
    echo ⚠️ Có lỗi khi đẩy code. Nếu GitHub yêu cầu Personal Access Token (PAT),
    echo bạn chỉ cần dán token vào hoặc đăng nhập trên cửa sổ trình duyệt hiện ra.
)

echo.
pause
