@echo off
chcp 65001 >nul
title ĐẨY CODE LÊN GITHUB - SMARTCONSTRUCT WEB AI
echo ==============================================================================
echo 🏗️ SMARTCONSTRUCT WEB AI - KHOA XÂY DỰNG - ĐẠI HỌC DUY TÂN
echo Repository: https://github.com/vantruongbui747-cpu/smartconstruct-web-ai.git
echo ==============================================================================
echo.

set "GIT_EXE=C:\Program Files\Git\cmd\git.exe"
if not exist "%GIT_EXE%" set "GIT_EXE=git"

echo [1/4] Đang quét và thêm các file mới (git add)...
"%GIT_EXE%" add .

echo.
echo [2/4] Đang đóng gói commit...
"%GIT_EXE%" commit -m "Cap nhat ban ve 3D BIM va CAD Blueprint" 2>nul

echo.
echo [3/4] Cấu hình nhánh chính main...
"%GIT_EXE%" remote remove origin 2>nul
"%GIT_EXE%" remote add origin https://github.com/vantruongbui747-cpu/smartconstruct-web-ai.git
"%GIT_EXE%" branch -M main

echo.
echo [4/4] Đang kết nối và đẩy mã nguồn lên GitHub...
echo (Nếu có cửa sổ GitHub bật lên, bạn bấm nút xanh 'Sign in with your browser')
echo.

"%GIT_EXE%" push -u origin main

if errorlevel 1 goto :loi_push

echo.
echo ==============================================================================
echo ✅ THÀNH CÔNG: Đã đẩy toàn bộ mã nguồn lên GitHub!
echo 🔒 Toàn bộ dữ liệu và file index.html đã sẵn sàng cho GitHub Pages.
echo ==============================================================================
goto :ket_thuc

:loi_push
echo.
echo ==============================================================================
echo ⚠️ CHƯA THÀNH CÔNG: Vui lòng xác thực tài khoản GitHub trong trình duyệt
echo hoặc kiểm tra lại quyền truy cập repository.
echo ==============================================================================

:ket_thuc
echo.
pause
