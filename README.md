# 🏗️ SMARTCONSTRUCT WEB AI
### Nền tảng Web Trợ lý Kỹ thuật, Tra cứu TCVN & Tính toán Kết cấu Thông minh
**Hạng mục:** BẢNG A – Sáng tạo Phần mềm, Website bằng AI  
**Đơn vị:** Khoa Xây Dựng • Trường Đại Học Duy Tân (DTU)

---

## 🌟 Giới Thiệu Dự Án
**SmartConstruct Web AI** là nền tảng số toàn diện hỗ trợ kỹ sư và sinh viên ngành Xây dựng giải quyết 3 bài toán lớn:
1. **Tra cứu nhanh quy chuẩn & pháp lý xây dựng:** TCVN 5574:2018 (Bê tông cốt thép), TCVN 2737:2023 (Tải trọng và tác động), TCVN 9362:2012 (Nền móng), TCVN 4453:1995 (Thi công bê tông) và Nghị định 206/2026/NĐ-CP (Lộ trình áp dụng BIM bắt buộc).
2. **Tính toán cơ học & mô phỏng trực quan:** Tính toán sơ bộ và kiểm tra điều kiện bền dầm, sàn, cột chịu nén lệch tâm (biểu đồ tương tác P-M), thí nghiệm đầm chặt đất Proctor, thiết kế móng đơn, tải trọng gió nhà cao tầng và trích xuất nội lực từ SAP2000/ETABS.
3. **Tự động hóa hồ sơ kỹ thuật:** Bóc tách khối lượng cốt thép (Auto-BOQ), định mức cấp phối bê tông, và tự động xuất bản thuyết minh đồ án chuẩn Microsoft Word (`.docx`).

---

## 🚀 06 Phân Hệ Chức Năng Cốt Lõi
- **Phân hệ 1: Kết cấu Bê tông Cốt thép (TCVN 5574:2018)**
  - 1.1 Bản sàn: Phân loại bản 1 phương / 2 phương, tính $M_{max}$ và bước thép $s$.
  - 1.2 Dầm chữ nhật: Kiểm tra $\alpha_m \le \alpha_R$, tự động chọn số thanh thép $n\Phi d$ và vẽ mặt cắt dầm trực quan.
  - 1.3 Cột chịu nén lệch tâm: Tính độ lệch tâm $e_1, e_a, \eta$ và vẽ biểu đồ bao tương tác $P - M$ bằng Plotly.
- **Phân hệ 2: Địa Kỹ Thuật, Cơ Học Đất & Nền Móng**
  - 2.1 Thí nghiệm đầm chặt đất: Hồi quy đa thức bậc 2 xác định độ ẩm tối ưu $W_{opt}$, $\gamma_{d,max}$ và đường bão hòa khí $S_r = 1.0$.
  - 2.2 Thiết kế Móng đơn dưới cột: Kiểm tra áp lực đáy móng $p_{tb}, p_{max}, p_{min}$ theo TCVN 9362:2012 và tính thép móng.
- **Phân hệ 3: Tải Trọng Gió & Cầu Nối SAP2000/ETABS**
  - 3.1 Tải trọng gió TCVN 2737:2023: Tính áp lực gió theo cao độ và vẽ biểu đồ lực gió tầng $W_i$.
  - 3.2 Lọc nội lực SAP2000: Đọc file Excel/CSV xuất từ SAP2000/ETABS và tự động trích xuất cặp nội lực nguy hiểm nhất.
- **Phân hệ 4: Chatbot Tra Cứu TCVN, Pháp Lý & BIM**
  - Tích hợp Google Gemini AI và bộ dữ liệu RAG chuyên ngành Xây dựng.
  - Kiểm tra nhanh điều kiện miễn Giấy phép xây dựng và lộ trình áp dụng BIM theo Nghị định 206/2026/NĐ-CP.
  - Ngân hàng câu hỏi trắc nghiệm ôn tập Pháp luật Xây dựng có chấm điểm và giải thích.
- **Phân hệ 5: Kỹ Thuật Thi Công & Bóc Tách Khối Lượng (Auto-BOQ)**
  - Tính cấp phối vật tư xi măng, cát, đá, nước cho $V\text{ m}^3$ bê tông và thời gian tháo ván khuôn theo TCVN 4453:1995.
  - Thống kê cốt thép tự động và xuất bảng tính Excel (`.xlsx`).
- **Phân hệ 6: Xuất Thuyết Minh Đồ Án (.docx)**
  - Tự động đồng bộ số liệu các phân hệ và xuất file Microsoft Word chuẩn chỉnh.

---

## 🛠️ Cài Đặt & Chạy Trực Tiếp Tại Local (Máy Tính Cá Nhân)

### 1. Yêu cầu môi trường
- Python 3.10 trở lên.
- Cài đặt các thư viện phụ thuộc:
```bash
pip install -r requirements.txt
```

### 2. Cấu hình API Key (Bảo mật máy chủ)
Tạo file `.env` tại thư mục gốc của dự án:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 3. Khởi chạy ứng dụng
```bash
streamlit run app.py
```
Hoặc bấm đúp chuột vào file `Chay_SmartConstruct.bat` trên Windows.

---

## 🌐 Hướng Dẫn Triển Khai Lên Web (Deploy Free Lên Streamlit Cloud)
Để mọi người có thể nhấn vào link trải nghiệm trực tiếp trên điện thoại/máy tính:

1. Đẩy mã nguồn này lên một GitHub Repository của bạn.
2. Truy cập [share.streamlit.io](https://share.streamlit.io/) và đăng nhập bằng tài khoản GitHub.
3. Bấm **"Create app"** $\rightarrow$ Chọn Repository vừa tạo $\rightarrow$ Main branch $\rightarrow$ Main file path: `app.py`.
4. **BƯỚC BẢO MẬT QUAN TRỌNG:**
   - Trong giao diện cài đặt ứng dụng (Advanced settings $\rightarrow$ Secrets), dán cấu hình API Key:
     ```toml
     GEMINI_API_KEY = "your_gemini_api_key_here"
     ```
   - Nhấn **Save**.
5. Bấm **Deploy!** Trong vòng 1 phút, bạn sẽ nhận được một đường link web chính thức (ví dụ: `https://smartconstruct-dtu.streamlit.app`) để chia sẻ cho mọi người cùng sử dụng!

---

## 📜 Bản Quyền & Tác Giả
- **Dự án:** SmartConstruct Web AI
- **Nhóm tác giả:** Khoa Xây Dựng • Trường Đại Học Duy Tân
- © 2026 Bản quyền thuộc về Nhóm Nghiên cứu & Ứng dụng AI trong Kỹ thuật Xây dựng.
