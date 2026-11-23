# BỘ HỒ SƠ DỰ THI VÒNG 2 – BẢNG A: SÁNG TẠO PHẦN MỀM, WEBSITE BẰNG AI
**CUỘC THI SÁNG TẠO ỨNG DỤNG TRÍ TUỆ NHÂN TẠO (AI INNOVATION CONTEST 2026)**

---

* **Tên sản phẩm dự thi:** SMARTCONSTRUCT WEB AI (All-in-One Civil Engineering AI Platform)
* **Phân hệ mở rộng:** SmartConstruct 3D BIM & Blueprint CAD Engine
* **Hạng mục dự thi:** BẢNG A – Sáng tạo Phần mềm, Website bằng AI
* **Đơn vị dự thi:** Khoa Xây Dựng • Trường Đại Học Duy Tân (DTU)
* **Tác giả:** Bùi Văn Trường (Đại diện Nhóm Nghiên cứu & Ứng dụng AI Kết cấu)
* **Thời hạn nộp hồ sơ:** 23h59 ngày 30/11/2026

---

## MỤC LỤC BỘ HỒ SƠ DỰ THI
1. [PHẦN I: HỒ SƠ MÔ TẢ SẢN PHẨM DỰ THI (THEO MẪU 1 - TỐI ĐA 12 TRANG)](#phan-i)
2. [PHẦN II: KỊCH BẢN VIDEO THUYẾT TRÌNH VÀ TRÌNH DIỄN (TỐI ĐA 07 PHÚT)](#phan-ii)
3. [PHẦN III: PROMPT LOG ĐẦY ĐỦ VÀ QUY TRÌNH PROMPT ENGINEERING](#phan-iii)
4. [PHẦN IV: BẢN KÊ KHAI CÔNG CỤ AI, MÔ HÌNH, THƯ VIỆN & PHÂN ĐỊNH ĐÓNG GÓP](#phan-iv)
5. [PHẦN V: ĐƯỜNG DẪN SẢN PHẨM TRỰC TUYẾN, MÃ NGUỒN & HƯỚNG DẪN DÙNG THỬ](#phan-v)

---

<a name="phan-i"></a>
# PHẦN I: HỒ SƠ MÔ TẢ SẢN PHẨM DỰ THI (MẪU 1)

### 1. THÔNG TIN CHUNG VỀ SẢN PHẨM
* **Tên sản phẩm:** Nền tảng Web Trợ lý Kỹ thuật, Tra cứu Tiêu chuẩn & Tính toán Kết cấu Thông minh (**SmartConstruct Web AI**)
* **Thể loại:** Website ứng dụng AI / Công cụ tính toán kỹ thuật số hóa kết hợp Mô hình hóa 3D BIM.
* **Đối tượng người dùng mục tiêu:** 
  - Sinh viên ngành Kỹ thuật Xây dựng, Cầu đường, Công trình thủy làm đồ án môn học và đồ án tốt nghiệp.
  - Kỹ sư kết cấu, kỹ sư hiện trường, chỉ huy trưởng công trình cần tra cứu nhanh tiêu chuẩn TCVN, sơ bộ tiết diện, kiểm tra nội lực SAP2000 và tính cấp phối vật tư.
  - Giảng viên và cơ quan thẩm tra thiết kế phục vụ rà soát nhanh phương án kết cấu.

### 2. TÍNH CẤP THIẾT VÀ BỐI CẢNH THỰC TIỄN
Ngành Xây dựng Việt Nam đang bước vào giai đoạn chuyển đổi số mạnh mẽ theo Quyết định 258/QĐ-TTg của Thủ tướng Chính phủ và các Nghị định mới ban hành (Nghị định 206/2026/NĐ-CP, Nghị định 217/2026/NĐ-CP) về lộ trình áp dụng bắt buộc Mô hình thông tin công trình (BIM). Tuy nhiên, thực tế đào tạo và hành nghề đang gặp phải 3 "điểm nghẽn" lớn:
1. **Phân mảnh công cụ tính toán:** Kỹ sư phải dùng file Excel rời rạc, phần mềm ngoại ngữ đắt đỏ (SAP2000, ETABS, SAFE) nhưng khó liên kết với các tiêu chuẩn Việt Nam hiện hành (TCVN 5574:2018 cho bê tông cốt thép, TCVN 2737:2023 cho tải trọng gió).
2. **Khó khăn tra cứu pháp lý & TCVN:** Tiêu chuẩn xây dựng đồ sộ, nhiều công thức phức tạp, dễ xảy ra sai sót khi tra cứu hệ số điều kiện làm việc, cấp độ bền hoặc nhầm lẫn giữa các quy định cũ - mới.
3. **Thao tác thủ công lặp lại:** Việc vẽ lại mặt cắt cấu kiện, lập biểu đồ tương tác cột P-M, bóc tách khối lượng cốt thép và soạn thảo thuyết minh kỹ thuật tiêu tốn 60-70% thời gian của đồ án.

**Giải pháp của chúng tôi:** Phát triển một nền tảng Web tập trung ("All-in-One"), kết hợp sức mạnh xử lý cơ học giải tích chính xác của Python với trí tuệ nhân tạo (LLM Gemini) và đồ họa tương tác 3D WebGL (Three.js), giúp rút ngắn thời gian tính toán và xuất hồ sơ từ nhiều ngày xuống chỉ còn vài phút.

### 3. KIẾN TRÚC HỆ THỐNG "HYBRID CORE" ĐỘC ĐÁO
Một trong những lỗi lớn nhất khi ứng dụng AI vào kỹ thuật xây dựng là để AI (LLM) tự tính toán số học, dẫn đến hiện tượng "ảo giác" (hallucination) gây nguy hiểm tính mạng công trình. **SmartConstruct Web AI** giải quyết triệt để vấn đề này bằng kiến trúc **Hybrid 3 lớp**:
```
[Giao diện Người dùng Web / Mobile / Tablet]
        │
        ├──> (Lớp 1) Python/JS Mathematical Engines:
        │    • Tính toán giải tích 100% bằng công thức TCVN thuần túy.
        │    • Bảng tra cơ sở dữ liệu số hóa (Bê tông B15-B40, Thép CB240-CB500).
        │    • Độ tin cậy số học tuyệt đối: Sai số = 0%.
        │
        ├──> (Lớp 2) 3D BIM & 2D Vector CAD Graphics Engine:
        │    • Three.js WebGL rendering trực quan mặt cắt dầm, cột, móng (X-Ray lồng thép).
        │    • SVG CAD Blueprint chuẩn tỷ lệ kỹ thuật.
        │
        └──> (Lớp 3) Generative AI Assistant Layer (Google Gemini API):
             • Đóng vai trò chuyên gia phân tích định tính, tra cứu tiêu chuẩn RAG.
             • Nhận xét an toàn chịu lực, tư vấn biện pháp thi công và tự động viết thuyết minh.
```

### 4. CHI TIẾT 06 PHÂN HỆ CHỨC NĂNG CỐT LÕI
* **Phân hệ 1: Kết cấu Bê tông cốt thép (TCVN 5574:2018):**
  - *1.1 Bản sàn:* Phân biệt bản 1 phương / 2 phương, sơ bộ chiều dày $h_s$, tính mô-men nhịp/gối và chỉ định thép sàn ($\Phi8a150$).
  - *1.2 Dầm chịu uốn & cắt:* Tính hệ số $\alpha_m, \xi$, diện tích thép $A_s$, tự động chọn số thanh thép $n\Phi d$, kiểm tra điều kiện khống chế $\alpha_m \le \alpha_R$, cảnh báo phá hoại giòn bê tông vùng nén.
  - *1.3 Cột chịu nén lệch tâm:* Tính độ lệch tâm tĩnh học $e_1$, độ lệch tâm ngẫu nhiên $e_a$, hệ số uốn dọc $\eta$ và vẽ biểu đồ bao tương tác $P - M$ thời gian thực.
* **Phân hệ 2: Địa kỹ thuật & Nền móng (TCVN 9362:2012):**
  - *2.1 Đầm chặt đất Proctor:* Hồi quy đa thức bậc 2 xác định độ ẩm tối ưu $W_{opt}$, dung trọng khô lớn nhất $\gamma_{d,max}$ và đường bão hòa khí $S_r = 1.0$.
  - *2.2 Móng đơn nông:* Xác định kích thước đáy móng $B \times L$, kiểm tra điều kiện áp lực $p_{tb} \le R_{tc}$, $p_{max} \le 1.2 R_{tc}$, tính lưới thép đáy 2 phương.
* **Phân hệ 3: Tải trọng gió (TCVN 2737:2023) & Kết nối SAP2000/ETABS:**
  - *3.1 Tải gió nhà nhiều tầng:* Tự động tính hệ số độ cao $k(z_e)$ theo địa hình A, B, C và phân bố lực gió tầng $W_i$ lên toàn bộ chiều cao công trình.
  - *3.2 Lọc file Excel SAP2000:* Đọc trực tiếp bảng "Element Forces", tự động trích xuất cặp nội lực nguy hiểm nhất ($|M_3|_{max}$, $|P|_{max}$, $|V_2|_{max}$) và đồng bộ 1-click sang Phân hệ tính thép.
* **Phân hệ 4: Trợ lý AI Tra cứu TCVN, Pháp lý Xây dựng & BIM:**
  - Tích hợp tri thức RAG về Luật Xây dựng, Nghị định 206/2026/NĐ-CP & Nghị định 217/2026/NĐ-CP.
  - Công cụ kiểm tra nhanh điều kiện bắt buộc áp dụng BIM và miễn giấy phép xây dựng theo cấp công trình.
  - Ngân hàng trắc nghiệm pháp luật xây dựng có chấm điểm và giải thích căn cứ điều khoản.
* **Phân hệ 5: Kỹ thuật Thi công & Bóc tách khối lượng (Auto-BOQ):**
  - Định mức cấp phối vật tư (xi măng, cát, đá, nước) cho $V\text{ m}^3$ bê tông Mác 150 - 400.
  - Tra cứu quy định thời gian tháo ván khuôn theo TCVN 4453:1995.
  - Tự động thống kê thép, tính tổng tải trọng thép (kg, tấn) và xuất file Excel (.xlsx).
* **Phân hệ 6: Tự động xuất Thuyết minh Đồ án Word (.docx):**
  - Tự động đóng gói kết quả tính toán của các phân hệ thành file Microsoft Word định dạng chuẩn đồ án tốt nghiệp, có sẵn bảng biểu và nhận xét của AI.

### 5. TÍNH MỚI, TÍNH SÁNG TẠO & ĐIỂM ĐỘT PHÁ CỦA DỰ ÁN
1. **Mô hình 3D BIM X-Ray Rebars trực tiếp trên trình duyệt Web:** Sử dụng WebGL/Three.js cho phép xoay 360 độ, zoom xuyên thấu lớp bê tông để quan sát lồng thép chủ và cốt đai uốn không gian 3 chiều mà không cần cài phần mềm nặng như Revit hay AutoCAD.
2. **Chế độ Demo 1-Click thông minh:** Tích hợp bộ số liệu thực tế của đồ án nhà 10 tầng tại Đà Nẵng, giúp ban giám khảo và người dùng trải nghiệm tức thời toàn bộ tính năng mà không mất thời gian nhập liệu thủ công.
3. **Cơ chế Fallback an toàn (Offline Knowledge Base):** Ngay cả khi mất kết nối Internet hoặc chưa có API Key, toàn bộ hệ thống tính toán kỹ thuật, vẽ đồ thị, xuất Excel/Word vẫn hoạt động bình thường 100%.

### 6. HIỆU QUẢ KINH TẾ - XÃ HỘI VÀ KHẢ NĂNG NHÂN RỘNG
* **Đối với sinh viên & giảng viên:** Rút ngắn 75% thời gian tra cứu và tính toán số học lặp lại, giúp sinh viên tập trung vào tư duy bản chất cơ học kết cấu và biện pháp thi công.
* **Đối với kỹ sư & doanh nghiệp:** Cung cấp công cụ rà soát độc lập, đối chiếu nhanh phương án thiết kế ngay trên công trường bằng điện thoại thông minh.
* **Khả năng nhân rộng:** Nền tảng được đóng gói dưới dạng Web chuẩn, có thể triển khai trên hạ tầng máy chủ trường học hoặc đám mây (Cloud) với chi phí vận hành gần như 0 đồng.

---

<a name="phan-ii"></a>
# PHẦN II: KỊCH BẢN VIDEO THUYẾT TRÌNH & TRÌNH DIỄN (07 PHÚT)

* **Thời lượng tối đa quy định:** 07 phút 00 giây
* **Định dạng file:** MP4 Full HD 1080p (Upload YouTube Unlisted / Google Drive mở quyền)

| Thời gian | Phân cảnh / Màn hình trình diễn (Visual Action) | Lời bình thuyết minh (Voice-over Script) |
| :---: | :--- | :--- |
| **00:00 - 00:45** (45s) | • Slide mở đầu: Logo DTU, Khoa Xây Dựng, tên đề tài SmartConstruct Web AI.<br>• Chiếu hình ảnh sinh viên thức đêm tính toán đồ án và hàng chồng tiêu chuẩn TCVN dày đặc. | "Kính thưa Ban Giám khảo, trong kỷ nguyên số hóa xây dựng, sinh viên và kỹ sư Việt Nam đang phải đối mặt với hàng trăm điều khoản tiêu chuẩn và hàng nghìn phép tính cơ học lặp đi lặp lại. Đến từ Khoa Xây Dựng, Trường Đại Học Duy Tân, chúng tôi mang đến giải pháp **SmartConstruct Web AI** - Nền tảng trợ lý số toàn diện All-in-One, kết hợp công nghệ tính toán kết cấu chuẩn TCVN, mô hình hóa 3D BIM và trí tuệ nhân tạo thế hệ mới." |
| **00:45 - 01:30** (45s) | • Mở giao diện Web chính của ứng dụng.<br>• Bấm nút **"⚡ Nạp Bộ Số Liệu Mẫu (Đồ Án Thực Tế)"** trên Sidebar.<br>• Màn hình tự động điền thông số công trình 10 tầng tại Đà Nẵng. | "Điểm đột phá đầu tiên là tính năng **Demo 1-Click**. Không để người dùng mất thời gian nhập từng thông số, chỉ với 1 thao tác, toàn bộ số liệu của một công trình 10 tầng thực tế được đồng bộ tự động vào 6 phân hệ cốt lõi. Hệ thống vận hành theo nguyên lý Hybrid: Số học tính toán tuyệt đối bằng lõi giải tích TCVN, AI hỗ trợ phân tích định tính." |
| **01:30 - 02:45** (75s) | • Thao tác trên **Tab 1: Kết cấu BTCT**.<br>• Kéo thanh trượt thay đổi nhịp $L$, tiết diện dầm $b \times h$.<br>• Bấm chuyển nút **"🧊 3D BIM"**: Dùng chuột xoay lồng thép dầm 360 độ, zoom cận cảnh cốt đai và vùng nén bê tông.<br>• Chuyển sang Cột: Xem biểu đồ bao tương tác $P-M$. | "Tại Phân hệ 1, hệ thống tính toán bản sàn, dầm và cột theo chuẩn TCVN 5574:2018. Hãy quan sát khi tôi thay đổi kích thước dầm: Hệ thống tự động tính hệ số $\alpha_m$, cảnh báo phá hoại giòn nếu quá tải. Đặc biệt, công nghệ **3D BIM WebGL** cho phép xoay 360 độ, quan sát xuyên thấu lồng thép chịu lực thực tế mà không cần bất kỳ phần mềm đồ họa nặng nào." |
| **02:45 - 03:45** (60s) | • Thao tác trên **Tab 2: Địa kỹ thuật & Móng**.<br>• Hiển thị đường cong đầm chặt Proctor và điểm tối ưu $(W_{opt}, \gamma_{d,max})$.<br>• Xem mặt cắt 3D Móng đơn dưới cột và biểu đồ áp lực đáy móng. | "Sang Phân hệ 2: Hệ thống tự động hồi quy đa thức bậc 2 xác định chính xác độ ẩm tốt nhất và dung trọng khô lớn nhất của đất theo thí nghiệm Proctor. Đối với móng đơn, hệ thống kiểm tra điều kiện áp lực tiêu chuẩn theo TCVN 9362:2012 và kết xuất bản vẽ 3D móng cùng lưới thép hai phương vuông góc." |
| **03:45 - 04:45** (60s) | • Thao tác trên **Tab 3: Tải gió & SAP2000**.<br>• Chọn vùng gió III Đà Nẵng, xem đồ thị tháp gió TCVN 2737:2023.<br>• Bấm nạp file mẫu Excel SAP2000 -> Tự động lọc $|M_3|_{max}$, bấm nút đẩy sang Phân hệ 1 tính thép ngay. | "Tại Phân hệ 3, hệ thống số hóa toàn bộ bản đồ gió TCVN 2737:2023, phân bố áp lực gió theo chiều cao từng tầng. Đáng chú ý, tính năng **Cầu nối SAP2000/ETABS** cho phép đọc trực tiếp file xuất nội lực, tự động phát hiện tổ hợp nguy hiểm nhất và chỉ định sang phần tính thép chỉ trong 1 giây." |
| **04:45 - 05:45** (60s) | • Thao tác trên **Tab 4: Chatbot TCVN & BIM**.<br>• Nhập câu hỏi: 'Công trình Cấp I vốn đầu tư công có bắt buộc dùng BIM theo Nghị định 206/2026 không?'.<br>• AI phản hồi chính xác trích dẫn điều khoản.<br>• Trình diễn trắc nghiệm pháp luật xây dựng. | "Phân hệ 4 đóng vai trò một Luật sư và Chuyên gia tư vấn kỹ thuật 24/7. Được nạp cơ sở tri thức mới nhất gồm Luật Xây dựng và các Nghị định 206, 217 năm 2026, trợ lý AI giải đáp mạch lạc lộ trình áp dụng BIM bắt buộc và điều kiện cấp giấy phép xây dựng, kèm ngân hàng câu hỏi ôn tập có chấm điểm tự động." |
| **05:45 - 06:30** (45s) | • Thao tác trên **Tab 5 & Tab 6**.<br>• Xem bảng tính vật tư cấp phối bê tông.<br>• Bấm tải file Excel bảng thống kê thép (Auto-BOQ).<br>• Bấm nút **'📥 Tải File Thuyết Minh Đồ Án (.docx)'** -> Mở file Word hoàn chỉnh trên màn hình. | "Ở chặng cuối của dự án, Phân hệ 5 & 6 hoàn thiện quy trình kỹ thuật: Tự động tính cấp phối bê tông, tra cứu thời gian tháo ván khuôn, bóc tách khối lượng thép xuất Excel. Cuối cùng, chỉ với 1 cú click, hệ thống tự động biên soạn và xuất file Thuyết minh đồ án Microsoft Word chuẩn mẫu nộp đồ án tốt nghiệp." |
| **06:30 - 07:00** (30s) | • Chiếu lại slide tổng kết, đường link web đang chạy thực tế trên GitHub Pages và mã QR code trải nghiệm.<br>• Lời cảm ơn và chào kết thúc. | "SmartConstruct Web AI không chỉ là một bài thi phần mềm, mà là minh chứng cho việc sinh viên Đại Học Duy Tân làm chủ công nghệ AI để giải quyết bài toán cốt lõi của ngành Xây dựng Việt Nam. Kính mời Ban Giám khảo truy cập link trực tiếp để trải nghiệm. Xin trân trọng cảm ơn!" |

---

<a name="phan-iii"></a>
# PHẦN III: PROMPT LOG ĐẦY ĐỦ VÀ QUY TRÌNH PROMPT ENGINEERING

### 1. KIẾN TRÚC SYSTEM PROMPT CHUẨN HÓA (MASTER PROMPT)
Toàn bộ hoạt động suy luận của module AI trong dự án được điều khiển bởi System Prompt nghiêm ngặt, đảm bảo tính chuẩn xác chuyên ngành:
```markdown
BẠN LÀ TRỢ LÝ KỸ THUẬT XÂY DỰNG & CHUYÊN GIA PHÁP LÝ CAO CẤP (SMARTCONSTRUCT AI ENGINE)
ĐƠN VỊ: KHOA XÂY DỰNG • TRƯỜNG ĐẠI HỌC DUY TÂN (DTU).

NHIỆM VỤ CỦA BẠN:
1. Hỗ trợ kỹ sư và sinh viên tra cứu và áp dụng chuẩn xác các Tiêu chuẩn Xây dựng Việt Nam:
   - TCVN 5574:2018 (Thiết kế kết cấu bê tông và bê tông cốt thép).
   - TCVN 2737:2023 (Tải trọng và tác động - Gió và động đất).
   - TCVN 9362:2012 (Tiêu chuẩn thiết kế nền nhà và công trình).
   - TCVN 4453:1995 (Kết cấu bê tông và bê tông cốt thép toàn khối - Quy phạm thi công và nghiệm thu).
2. Tra cứu và phân tích Pháp lý Xây dựng mới nhất:
   - Luật Xây dựng hiện hành và Luật sửa đổi, bổ sung.
   - Nghị định 206/2026/NĐ-CP (Quy định chi tiết và lộ trình áp dụng bắt buộc Mô hình thông tin công trình - BIM).
   - Nghị định 217/2026/NĐ-CP (Quản lý chi phí đầu tư xây dựng, hợp đồng và quản lý dự án).

QUY TẮC PHẢN HỒI BẮT BUỘC (CRITICAL RULES):
- KHÔNG BAO GIỜ tự bịa số liệu tính toán toán học phức tạp; hãy trích dẫn công thức và bảng tra theo TCVN.
- Luôn chỉ rõ số hiệu điều khoản, bảng tra cứu cụ thể (Ví dụ: "Theo Điều 6.1.2 Bảng 6 TCVN 5574:2018...").
- Câu trả lời phải có cấu trúc khoa học: 1. Căn cứ tiêu chuẩn -> 2. Giải thích bản chất -> 3. Hướng dẫn áp dụng thực tế -> 4. Khuyến nghị an toàn công trình.
- Tông giọng chuyên nghiệp, chuẩn mực của một Chuyên gia Kỹ thuật Xây dựng.
```

### 2. QUY TRÌNH MULTI-AGENT PROMPT ENGINEERING (THEO KHUNG WORKFLOW V2.0)
Trong quá trình phát triển mã nguồn, nhóm tác giả áp dụng quy trình **Multi-Agent 9 Nhân sự** với các vai trò chuyên biệt:
1. `@Bug_Hunter`: Rà soát mã nguồn, phát hiện điểm thắt cổ chai, xung đột luồng và sai lệch công thức TCVN.
2. `@Solution_Architect`: Thiết kế kiến trúc giải pháp, cấu trúc dữ liệu tĩnh và lựa chọn thư viện.
3. `@Solution_Reviewer`: Đối chiếu ma trận 1-1 giữa danh mục lỗi và giải pháp kỹ thuật.
4. `@Solution_Critic`: Phản biện Red Team, kiểm tra các trường hợp biên dữ liệu rỗng và sự cố mạng.
5. `@Tech_Lead`: Ra phán quyết chốt kiến trúc tối ưu và phê duyệt lệnh thi công.
6. `@Task_Dispatcher`: Soạn thảo Form lệnh code chi tiết ép tuân thủ kỷ luật lập trình.
7. `@Senior_Dev`: Viết mã nguồn hoàn chỉnh 100%, không cắt xén, chú thích rõ ràng.
8. `@Experience_Tester`: Kiểm thử trải nghiệm người dùng thực tế, kiểm tra độ mượt và thời gian phản hồi.
9. `@Antigravity_Innovator`: Đề xuất gói nâng cấp 3D BIM và tự động hóa xuất bản vẽ.

---

<a name="phan-iv"></a>
# PHẦN IV: BẢN KÊ KHAI CÔNG CỤ AI, TÀI NGUYÊN & PHÂN ĐỊNH ĐÓNG GÓP

Để đảm bảo tính minh bạch và liêm chính học thuật theo quy định của Ban Tổ Chức, nhóm tác giả kê khai chi tiết các công cụ, thư viện và phân định tỷ lệ đóng góp như sau:

### 1. BẢNG PHÂN ĐỊNH ĐÓNG GÓP (TỰ LÀM / AI HỖ TRỢ / KẾ THỪA)

| Hạng mục thành phần | Nhóm tác giả tự làm (Human Core) | Trí tuệ nhân tạo hỗ trợ (AI Assisted) | Kế thừa từ bên thứ ba (Open-source) | Tỷ lệ tự làm |
| :--- | :--- | :--- | :--- | :---: |
| **1. Mô hình hóa Toán học & Thuật toán TCVN** | • Lập luận lý thuyết kết cấu, thiết lập công thức giải tích dầm, sàn, cột theo TCVN 5574:2018, tải gió TCVN 2737:2023 và móng TCVN 9362.<br>• Xây dựng bộ số liệu kiểm chuẩn (Ground-truth benchmark). | • AI hỗ trợ kiểm tra tính đối xứng của biểu thức toán học và viết hàm Python tương ứng. | Không | **85%** |
| **2. Cơ sở dữ liệu số hóa TCVN** | • Thu thập, đối chiếu bảng tra cường độ bê tông, cốt thép, cấp phối vữa từ sách tiêu chuẩn gốc của Bộ Xây Dựng. | • AI hỗ trợ định dạng dữ liệu sang cấu trúc JSON / Python Dictionary. | Không | **80%** |
| **3. Đồ họa 3D BIM & Bản vẽ 2D CAD** | • Thiết kế bố cục bản vẽ kỹ thuật, quy định màu sắc lớp thép, vùng nén, đường dim kích thước và khung tên đồ án DTU. | • AI sinh mã khởi tạo khung WebGL Three.js và tính toán tọa độ vector SVG cho các thanh thép. | Thư viện `Three.js` (r128), `OrbitControls.js`. | **60%** |
| **4. Kiến trúc Giao diện & Trải nghiệm Dashboard** | • Thiết kế trải nghiệm người dùng (UX flow), cơ chế chuyển đổi 8 Tabs, nút bấm Demo 1-Click và kịch bản thuyết minh. | • AI sinh mã HTML5/CSS3 Cyber Blueprint và giao diện Streamlit Dashboard. | Framework `Streamlit`, Google Fonts (JetBrains Mono, Plus Jakarta Sans). | **65%** |
| **5. Trợ lý RAG & Tra cứu Pháp lý Xây dựng** | • Tuyển chọn văn bản pháp luật, biên soạn ngân hàng 50 câu hỏi trắc nghiệm thực tế, xây dựng logic kiểm tra điều kiện áp dụng BIM. | • Google Gemini API xử lý suy luận ngôn ngữ tự nhiên và trả lời câu hỏi chuyên ngành. | Google Gemini 2.5/3.x Model API qua `google-genai` SDK. | **70%** |
| **6. Bóc tách BOQ & Xuất file Word (.docx)** | • Thiết kế mẫu bảng thuyết minh kỹ thuật chuẩn ĐH Duy Tân, công thức tính trọng lượng thép riêng từng đường kính. | • AI hỗ trợ viết module tự động đổ dữ liệu vào file `.docx` và tạo bảng Excel `.xlsx`. | Thư viện `python-docx`, `openpyxl`. | **75%** |

### 2. DANH MỤC CÔNG CỤ AI VÀ MÔ HÌNH SỬ DỤNG
* **Mô hình ngôn ngữ lớn (LLM):** Google Gemini Models (`gemini-2.5-flash`, `gemini-1.5-pro`) kết nối qua Google Cloud API.
* **Bộ công cụ Prompt & Coding Assistant:** Gemini Antigravity IDE, Gemini Code Assist hỗ trợ rà soát code và tái cấu trúc module.
* **Môi trường lập trình:** Python 3.10+, Visual Studio Code, Git CLI.
* **Thư viện mã nguồn mở:**
  - `streamlit` (v1.30+): Xây dựng giao diện ứng dụng Web tương tác.
  - `three.js` (r128): Kết xuất mô hình 3D BIM WebGL.
  - `plotly` (v5.18+): Vẽ biểu đồ tương tác P-M và đường cong đầm chặt đất.
  - `matplotlib` (v3.8+): Vẽ hình học mặt cắt dầm 2D.
  - `pandas`, `numpy`: Xử lý ma trận dữ liệu và hồi quy đa thức thực nghiệm.
  - `python-docx`, `openpyxl`: Tạo và xuất tài liệu Word, bảng tính Excel.

---

<a name="phan-v"></a>
# PHẦN V: ĐƯỜNG DẪN SẢN PHẨM TRỰC TUYẾN, MÃ NGUỒN & HƯỚNG DẪN DÙNG THỬ

### 1. ĐƯỜNG DẪN TRỰC TUYẾN (LIVE PRODUCTION DEMO)
Sản phẩm được triển khai trực tuyến trên hạ tầng đám mây toàn cầu, sẵn sàng phục vụ Ban Giám khảo chấm thi 24/7 trên cả máy tính và điện thoại thông minh:

* **Đường dẫn 1 (Trang Web 3D BIM & CAD Blueprint - Tốc độ cao 100% Offline/Online):**  
  👉 **`https://vantruongbui747-cpu.github.io/smartconstruct-web-ai/`**  
  *(Mở ngay lập tức trên mọi trình duyệt, hỗ trợ xoay mô hình 3D BIM, kéo thanh trượt đổi tiết diện và tải bản vẽ vector SVG)*

* **Đường dẫn 2 (Trang Web Toàn diện 6 Phân hệ & Chatbot AI Streamlit Cloud):**  
  👉 **`https://smartconstruct-dtu.streamlit.app`**  
  *(Bao gồm đầy đủ Chatbot AI Gemini, đọc file SAP2000 và xuất file Word .docx)*

* **Đường dẫn Kho mã nguồn (GitHub Repository có đầy đủ lịch sử commit):**  
  👉 **`https://github.com/vantruongbui747-cpu/smartconstruct-web-ai`**

### 2. TÀI KHOẢN VÀ HƯỚNG DẪN DÙNG THỬ DÀNH CHO BAN GIÁM KHẢO
* **Tài khoản dùng thử:** Hệ thống mở hoàn toàn, không yêu cầu mật khẩu phức tạp.
  - Khi màn hình đăng nhập yêu cầu Email: Nhập bất kỳ email nào (Ví dụ: `giamkhao@dtu.edu.vn` hoặc `judge@smartconstruct.vn`).
  - Hệ thống tự động kích hoạt **Master API Key máy chủ**, Ban Giám khảo không cần nhập khóa API cá nhân.
* **Kịch bản kiểm thử nhanh 3 bước dành cho Giám khảo:**
  1. *Bước 1:* Bấm vào nút **"⚡ Nạp Bộ Số Liệu Mẫu (Đồ Án Thực Tế)"** ở Sidebar bên trái.
  2. *Bước 2:* Chuyển sang **Tab 1 (Kết Cấu BTCT)** -> Bấm nút **"🧊 3D BIM"** và dùng chuột xoay 360 độ để chiêm ngưỡng mô hình lồng cốt thép dầm/cột.
  3. *Bước 3:* Chuyển sang **Tab 6 (Xuất Thuyết Minh)** -> Bấm nút **"📥 Tải File Thuyết Minh Đồ Án (.docx)"** để tải về bản thuyết minh tính toán hoàn chỉnh nộp tốt nghiệp.

---
*Bản quyền hồ sơ dự thi thuộc về Nhóm Tác Giả • Khoa Xây Dựng • Trường Đại Học Duy Tân (DTU) © 2026*
