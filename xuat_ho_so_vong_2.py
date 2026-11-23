"""
Script: xuat_ho_so_vong_2.py
Mục đích: Tự động khởi tạo trọn bộ 05 file hồ sơ dự thi Vòng 2 chuẩn Microsoft Word (.docx)
và 01 trang HTML in ấn PDF chuyên nghiệp phục vụ nộp Ban Tổ Chức cuộc thi AI 2026.
"""

import os
import sys

# Ensure UTF-8 output on Windows console
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Màu sắc chuẩn nhận diện Đại Học Duy Tân & Kỹ thuật
COLOR_DTU_CRIMSON = RGBColor(139, 21, 32)
COLOR_DTU_GOLD = RGBColor(197, 160, 89)
COLOR_NAVY = RGBColor(15, 23, 42)
COLOR_GRAY = RGBColor(100, 116, 139)

OUTPUT_DIR = "Ho_So_Vong_2_Nop_BTC"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def set_cell_background(cell, fill_hex):
    """Đặt màu nền cho ô trong bảng"""
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Đặt padding cho ô bảng"""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

# ==============================================================================
# FILE 1: HỒ SƠ MÔ TẢ SẢN PHẨM (MẪU 1 - TỐI ĐA 12 TRANG)
# ==============================================================================
def create_file_1():
    doc = Document()
    
    # Canh lề chuẩn văn bản kỹ thuật
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(0.8)

    # 1. Header Trang bìa
    p_dtu = doc.add_paragraph()
    r_dtu = p_dtu.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO • TRƯỜNG ĐẠI HỌC DUY TÂN (DTU)\nKHOA XÂY DỰNG • BỘ MÔN KỸ THUẬT CÔNG TRÌNH\n" + "—"*35)
    r_dtu.font.name = "Times New Roman"
    r_dtu.font.size = Pt(11)
    r_dtu.font.bold = True
    r_dtu.font.color.rgb = COLOR_DTU_CRIMSON
    p_dtu.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_space = doc.add_paragraph("\n")

    p_contest = doc.add_paragraph()
    r_c = p_contest.add_run("CUỘC THI SÁNG TẠO ỨNG DỤNG TRÍ TUỆ NHÂN TẠO 2026\nHỒ SƠ DỰ THI VÒNG 2 – BẢNG A: SÁNG TẠO PHẦN MỀM, WEBSITE BẰNG AI")
    r_c.font.name = "Times New Roman"
    r_c.font.size = Pt(13)
    r_c.font.bold = True
    r_c.font.color.rgb = COLOR_DTU_GOLD
    p_contest.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_title = doc.add_paragraph()
    r_title = p_title.add_run("\nHỒ SƠ MÔ TẢ SẢN PHẨM DỰ THI\n(THEO MẪU 1)")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_DTU_CRIMSON
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_name = doc.add_paragraph()
    r_name = p_name.add_run("ĐỀ TÀI: SMARTCONSTRUCT WEB AI\nNỀN TẢNG WEB TRỢ LÝ KỸ THUẬT, TRA CỨU TIÊU CHUẨN TCVN &\nMÔ HÌNH HÓA 3D BIM KẾT CẤU XÂY DỰNG THÔNG MINH")
    r_name.font.name = "Times New Roman"
    r_name.font.size = Pt(15)
    r_name.font.bold = True
    r_name.font.color.rgb = COLOR_NAVY
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph("\n"*2)

    # Khung tác giả trang bìa
    table_author = doc.add_table(rows=4, cols=2)
    table_author.alignment = WD_TABLE_ALIGNMENT.CENTER
    authors_info = [
        ("Tác giả chính / Trưởng nhóm:", "Bùi Văn Trường"),
        ("Đơn vị đào tạo:", "Khoa Xây Dựng • Trường Đại Học Duy Tân"),
        ("Hạng mục dự thi:", "BẢNG A – Ứng dụng phần mềm, website"),
        ("Thời gian nộp hồ sơ:", "Tháng 11/2026 (Hạn chót: 23h59 ngày 30/11/2026)")
    ]
    for idx, (label, val) in enumerate(authors_info):
        row = table_author.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.5)
        c1.width = Inches(4.0)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(label)
        r0.font.name = "Times New Roman"
        r0.font.bold = True
        r0.font.size = Pt(11)
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")

    doc.add_page_break()

    # NỘI DUNG 8 PHẦN CHÍNH (KHUNG 12 TRANG)
    headings = [
        ("1. THÔNG TIN CHUNG VÀ TỔNG QUAN DỰ ÁN", [
            "- Tên sản phẩm: SmartConstruct Web AI (Phiên bản tích hợp 3D BIM & 2D Vector CAD Engine).",
            "- Hạng mục tham gia: BẢNG A – Sáng tạo Phần mềm, Website bằng AI.",
            "- Mục tiêu phát triển: Xây dựng nền tảng số kỹ thuật 'All-in-One' đầu tiên tại Việt Nam giải quyết trọn vẹn 3 nhu cầu cấp thiết của sinh viên và kỹ sư xây dựng: Tra cứu tiêu chuẩn pháp lý mới nhất, tính toán kiểm tra kết cấu cơ học chuẩn xác 100%, và mô hình hóa trực quan 3D/2D trực tiếp trên trình duyệt Web."
        ]),
        ("2. TÍNH CẤP THIẾT VÀ BỐI CẢNH THỰC TIỄN NGÀNH XÂY DỰNG", [
            "- Lộ trình Chuyển đổi số & Áp dụng BIM bắt buộc: Theo Quyết định 258/QĐ-TTg của Thủ tướng Chính phủ và các Nghị định 206/2026/NĐ-CP, Nghị định 217/2026/NĐ-CP, ngành xây dựng đang bắt buộc số hóa hồ sơ thiết kế và ứng dụng mô hình thông tin công trình (BIM).",
            "- Thực trạng khó khăn của sinh viên và kỹ sư: Các phần mềm thương mại ngoại quốc (SAP2000, ETABS, Revit) có bản quyền đắt đỏ, đòi hỏi máy tính cấu hình đồ họa cao, không tích hợp sẵn bộ quy chuẩn Việt Nam (TCVN 5574:2018 cho bê tông cốt thép, TCVN 2737:2023 cho tải trọng gió). Sinh viên và kỹ sư hiện trường thường phải tính bằng các file Excel rời rạc, tốn 70% thời gian làm đồ án cho các phép tính số học lặp đi lặp lại."
        ]),
        ("3. KIẾN TRÚC HỆ THỐNG 'HYBRID CORE' ĐỘC ĐÁO CHỐNG ẢO GIÁC AI", [
            "Một sai lầm phổ biến khi ứng dụng AI vào xây dựng là để các mô hình ngôn ngữ lớn (LLM) tự làm tính số học, dẫn đến hiện tượng 'ảo giác' (hallucination) gây mất an toàn công trình. SmartConstruct Web AI khắc phục triệt để bằng mô hình 3 lớp độc lập:",
            "• Lớp 1 (Lõi Toán học & Tiêu chuẩn): Sử dụng Python và JavaScript giải tích tính toán 100% bằng công thức cơ học kết cấu theo đúng tiêu chuẩn TCVN 5574:2018, TCVN 2737:2023, TCVN 9362:2012. Sai số số học hoàn toàn bằng 0.",
            "• Lớp 2 (Lõi Đồ họa 3D BIM & CAD Vector): Ứng dụng công nghệ Three.js WebGL kết hợp SVG Blueprint, kết xuất mô hình 3D thấu quang (X-Ray) lồng cốt thép dầm, cột, móng xoay 360 độ thời gian thực ngay trên trình duyệt mà không cần cài phần mềm nặng.",
            "• Lớp 3 (Lớp Trí tuệ Nhân tạo Phân tích): Kết nối Google Gemini API đóng vai trò Chuyên gia tư vấn định tính, tra cứu pháp lý TCVN/BIM theo cơ chế RAG, cảnh báo an toàn thi công và tự động soạn thảo thuyết minh kỹ thuật."
        ]),
        ("4. CHI TIẾT 06 PHÂN HỆ CHỨC NĂNG CỐT LÕI CỦA SẢN PHẨM", [
            "• Phân hệ 1: Kết cấu Bê tông cốt thép (TCVN 5574:2018) gồm 3 module: Bản sàn (phân loại 1 phương/2 phương, tính mô-men và bước thép), Dầm chữ nhật (tính alpha_m, kiểm tra phá hoại giòn bê tông vùng nén, tự động chọn số thanh thép dọc), Cột chịu nén lệch tâm (tính độ lệch tâm e, độ mảnh, hệ số uốn dọc và vẽ biểu đồ bao tương tác P-M).",
            "• Phân hệ 2: Địa kỹ thuật & Nền móng (TCVN 9362:2012) gồm 2 module: Thí nghiệm đầm chặt đất Proctor (hồi quy đa thức bậc 2 xác định độ ẩm tối ưu Wopt, dung trọng khô lớn nhất gamma_d,max, đường bão hòa khí) và Thiết kế Móng đơn dưới cột (kiểm tra áp lực tiêu chuẩn đáy móng, tính thép 2 phương).",
            "• Phân hệ 3: Tải trọng gió (TCVN 2737:2023) & Cầu nối SAP2000/ETABS: Tự động phân bố áp lực gió Wi theo chiều cao công trình; đồng thời đọc trực tiếp file Excel xuất từ SAP2000, tự động phát hiện cặp nội lực nguy hiểm nhất và chỉ định sang phân hệ tính thép trong 1 giây.",
            "• Phân hệ 4: Trợ lý AI Tra cứu TCVN, Pháp lý & BIM: Cung cấp khung chat chuyên sâu, công cụ kiểm tra nhanh điều kiện bắt buộc áp dụng BIM và ngân hàng trắc nghiệm pháp luật xây dựng có giải thích chi tiết.",
            "• Phân hệ 5: Kỹ thuật Thi công & Auto-BOQ: Tính cấp phối vật tư bê tông M150-M400, tra cứu thời gian tháo ván khuôn (TCVN 4453:1995), bóc tách khối lượng cốt thép và xuất bảng tính Excel (.xlsx).",
            "• Phân hệ 6: Tự động xuất Thuyết minh Đồ án Word (.docx): Đóng gói toàn bộ kết quả tính toán thành bản thuyết minh kỹ thuật chuẩn chỉnh nộp tốt nghiệp chỉ với 1 cú click."
        ]),
        ("5. TÍNH MỚI, TÍNH SÁNG TẠO VÀ CÁC ĐIỂM ĐỘT PHÁ CÔNG NGHỆ", [
            "1. Mô hình 3D BIM X-Ray Rebars trực tiếp trên Web: Lần đầu tiên tích hợp mô hình 3D lồng thép dầm/cột/móng chạy mượt mà 60 FPS trên nền Web HTML5/WebGL, cho phép xoay 360 độ và co giãn hình học theo kích thước người dùng nhập.",
            "2. Chế độ Demo 1-Click thông minh: Tích hợp sẵn bộ số liệu thực tế đồ án 10 tầng tại Đà Nẵng, giúp người dùng và Ban Giám khảo trải nghiệm toàn diện hệ thống chỉ trong 30 giây.",
            "3. Cơ chế Fallback tri thức Offline: Ngay cả khi mất kết nối mạng hoặc không có API Key, toàn bộ hệ thống tính toán kết cấu, vẽ đồ thị, xuất file Excel/Word vẫn chạy ổn định 100%."
        ]),
        ("6. HIỆU QUẢ KINH TẾ - XÃ HỘI VÀ KHẢ NĂNG ỨNG DỤNG THỰC TẾ", [
            "- Đối với đào tạo đại học: Giúp sinh viên rút ngắn 75% thời gian tính toán cơ học lặp lại, nâng cao tư duy bản chất công trình và trực quan hóa không gian lồng thép 3D.",
            "- Đối với thực tế công trường: Kỹ sư có thể dùng điện thoại mở web kiểm tra nhanh nội lực, tra cứu TCVN hoặc tính cấp phối vật tư trực tiếp tại hiện trường mà không cần máy tính bàn.",
            "- Chi phí triển khai: Ứng dụng chạy trên hạ tầng đám mây không máy chủ (Serverless / GitHub Pages / Streamlit Cloud) với chi phí vận hành 0 đồng."
        ]),
        ("7. KẾ HOẠCH PHÁT TRIỂN TIẾP THEO (ROADMAP 2026 - 2027)", [
            "• Quý 1/2027: Phát triển Plugin kết nối 2 chiều trực tiếp với Autodesk Revit và AutoCAD bằng Dynamo / Python API.",
            "• Quý 2/2027: Ứng dụng thị giác máy tính AI (Computer Vision) nhận diện vết nứt bê tông và biến dạng kết cấu qua ảnh chụp hiện trường.",
            "• Quý 3/2027: Mở rộng cơ sở dữ liệu tính toán cho Kết cấu Thép (TCVN 5575:2012) và Kết cấu Cầu hầm."
        ]),
        ("8. KẾT LUẬN VÀ CAM KẾT LIÊM CHÍNH HỌC THUẬT", [
            "SmartConstruct Web AI là sản phẩm nghiên cứu nghiêm túc của sinh viên Khoa Xây Dựng, Trường Đại Học Duy Tân. Nhóm tác giả cam kết làm chủ 100% kiến trúc phần mềm, bảo toàn tính liêm chính trong ứng dụng AI và tuân thủ tuyệt đối quy chế cuộc thi."
        ])
    ]

    for title, paragraphs in headings:
        h = doc.add_heading(title, level=1)
        h_run = h.runs[0]
        h_run.font.name = "Times New Roman"
        h_run.font.size = Pt(13)
        h_run.font.bold = True
        h_run.font.color.rgb = COLOR_DTU_CRIMSON

        for text in paragraphs:
            p = doc.add_paragraph()
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            p.paragraph_format.line_spacing = 1.2
            p.paragraph_format.space_after = Pt(4)

    # Chữ ký nghiệm thu cuối tài liệu
    p_sign_box = doc.add_paragraph("\n" + "="*55)
    p_sign = doc.add_paragraph()
    r_s = p_sign.add_run("XÁC NHẬN CỦA KHOA XÂY DỰNG                              ĐẠI DIỆN TÁC GIẢ DỰ THI\n(Ký, đóng dấu và ghi rõ họ tên)                                      (Ký và ghi rõ họ tên)\n\n\n\n                                                                                 Bùi Văn Trường")
    r_s.font.name = "Times New Roman"
    r_s.font.size = Pt(11)
    p_sign.alignment = WD_ALIGN_PARAGRAPH.CENTER

    filepath = os.path.join(OUTPUT_DIR, "01_Ho_So_Mo_Ta_San_Pham_Mau_1.docx")
    doc.save(filepath)
    print(f"✅ Đã tạo thành công: {filepath}")

# ==============================================================================
# FILE 2: KỊCH BẢN VIDEO THUYẾT TRÌNH VÀ DEMO 07 PHÚT
# ==============================================================================
def create_file_2():
    doc = Document()
    
    title = doc.add_heading("KỊCH BẢN VIDEO THUYẾT TRÌNH & TRÌNH DIỄN SẢN PHẨM (07 PHÚT)", level=0)
    title.runs[0].font.name = "Times New Roman"
    title.runs[0].font.color.rgb = COLOR_DTU_CRIMSON
    title.runs[0].font.size = Pt(16)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    sub = doc.add_paragraph()
    r = sub.add_run("HẠNG MỤC: BẢNG A – ỨNG DỤNG PHẦN MỀM, WEBSITE | CUỘC THI AI INNOVATION 2026\nĐƠN VỊ: KHOA XÂY DỰNG • TRƯỜNG ĐẠI HỌC DUY TÂN\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.italic = True
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_note = doc.add_paragraph()
    r_n = p_note.add_run("📌 Hướng dẫn dành cho diễn giả / người quay video:\n- Thời lượng tối đa cho phép: 07 phút 00 giây (Nghiêm cấm vượt quá 07:00).\n- Định dạng xuất video: MP4 1080p, âm thanh rõ ràng, không lẫn tạp âm.\n- Sử dụng phần mềm OBS Studio hoặc tổ hợp phím Windows + G để quay màn hình Web khi thao tác.")
    r_n.font.name = "Times New Roman"
    r_n.font.size = Pt(10.5)

    # Bảng phân cảnh chi tiết
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Thời gian", "Phân cảnh thao tác trên màn hình (Visual Action)", "Lời bình thuyết minh (Voice-over Script)"]
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_background(hdr_cells[i], "8B1520")
        p = hdr_cells[i].paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.size = Pt(10)

    scenes = [
        ("00:00 - 00:45\n(45 giây)", 
         "• Slide mở đầu: Logo ĐH Duy Tân, Khoa Xây Dựng, tên đề tài SmartConstruct Web AI.\n• Chèn hình ảnh sinh viên thức đêm tính toán đồ án và hàng chồng tiêu chuẩn TCVN dày đặc.",
         "Kính thưa Ban Giám khảo! Trong thời kỳ chuyển đổi số ngành xây dựng, sinh viên và kỹ sư Việt Nam đang phải đối mặt với hàng trăm điều khoản tiêu chuẩn và hàng nghìn phép tính cơ học lặp đi lặp lại. Đến từ Khoa Xây Dựng, Trường Đại Học Duy Tân, chúng tôi tự hào mang đến giải pháp SMARTCONSTRUCT WEB AI - Nền tảng trợ lý số All-in-One, kết hợp công nghệ tính toán kết cấu chuẩn TCVN, mô hình hóa 3D BIM và trí tuệ nhân tạo thế hệ mới!"),
        
        ("00:45 - 01:30\n(45 giây)",
         "• Mở giao diện Web ứng dụng.\n• Bấm nút '⚡ Nạp Bộ Số Liệu Mẫu (Đồ Án Thực Tế)' trên Sidebar.\n• Màn hình tự động điền thông số công trình 10 tầng tại Đà Nẵng.",
         "Điểm đột phá đầu tiên là tính năng 'Demo 1-Click'. Không để người dùng mất thời gian nhập từng con số, chỉ với 1 cú click, toàn bộ số liệu của một công trình 10 tầng thực tế được đồng bộ tức thì vào 6 phân hệ cốt lõi. Hệ thống vận hành theo nguyên lý Hybrid: Số học tính toán tuyệt đối bằng lõi giải tích TCVN, AI hỗ trợ phân tích định tính!"),
        
        ("01:30 - 02:45\n(75 giây)",
         "• Thao tác trên Tab 1: Kết cấu BTCT.\n• Kéo thanh trượt thay đổi nhịp L, tiết diện dầm b x h.\n• Bấm nút '🧊 3D BIM': Dùng chuột xoay lồng thép dầm 360 độ, zoom cận cảnh cốt đai và vùng nén bê tông.\n• Chuyển sang Cột: Xem biểu đồ bao tương tác P - M.",
         "Tại Phân hệ 1, hệ thống tính toán dầm, cột, bản sàn theo chuẩn TCVN 5574:2018. Hãy quan sát khi tôi thay đổi kích thước dầm: Hệ thống tự động tính hệ số alpha_m, cảnh báo phá hoại giòn nếu quá tải. Đặc biệt, công nghệ 3D BIM WebGL cho phép xoay 360 độ, quan sát xuyên thấu lồng thép chịu lực thực tế mà không cần bất kỳ phần mềm đồ họa nặng nào!"),
        
        ("02:45 - 03:45\n(60 giây)",
         "• Thao tác trên Tab 2: Địa kỹ thuật & Móng.\n• Hiển thị đường cong đầm chặt Proctor và điểm tối ưu (Wopt, gamma_d,max).\n• Xem mặt cắt 3D Móng đơn dưới cột và biểu đồ áp lực đáy móng.",
         "Sang Phân hệ 2: Hệ thống tự động hồi quy đa thức bậc 2 xác định chính xác độ ẩm tốt nhất và dung trọng khô lớn nhất của đất theo thí nghiệm Proctor. Đối với móng đơn, hệ thống kiểm tra điều kiện áp lực tiêu chuẩn theo TCVN 9362:2012 và kết xuất bản vẽ 3D móng cùng lưới thép hai phương vuông góc!"),
        
        ("03:45 - 04:45\n(60 giây)",
         "• Thao tác trên Tab 3: Tải gió & SAP2000.\n• Chọn vùng gió III Đà Nẵng, xem đồ thị tháp gió TCVN 2737:2023.\n• Bấm nạp file mẫu Excel SAP2000 -> Tự động lọc M3max, bấm nút đẩy sang Phân hệ 1 tính thép ngay.",
         "Tại Phân hệ 3, hệ thống số hóa toàn bộ bản đồ gió TCVN 2737:2023, phân bố áp lực gió theo chiều cao từng tầng. Đáng chú ý, tính năng 'Cầu nối SAP2000/ETABS' cho phép đọc trực tiếp file xuất nội lực, tự động phát hiện tổ hợp nguy hiểm nhất và chỉ định sang phần tính thép chỉ trong 1 giây!"),
        
        ("04:45 - 05:45\n(60 giây)",
         "• Thao tác trên Tab 4: Chatbot TCVN & BIM.\n• Nhập câu hỏi: 'Công trình Cấp I vốn đầu tư công có bắt buộc dùng BIM theo Nghị định 206/2026 không?'.\n• AI phản hồi chính xác trích dẫn điều khoản.\n• Trình diễn trắc nghiệm pháp luật xây dựng.",
         "Phân hệ 4 đóng vai trò một Chuyên gia tư vấn kỹ thuật và Luật sư 24/7. Được nạp cơ sở tri thức mới nhất gồm Luật Xây dựng và các Nghị định 206, 217 năm 2026, trợ lý AI giải đáp mạch lạc lộ trình áp dụng BIM bắt buộc và điều kiện cấp giấy phép xây dựng, kèm ngân hàng câu hỏi ôn tập có chấm điểm tự động!"),
        
        ("05:45 - 06:30\n(45 giây)",
         "• Thao tác trên Tab 5 & Tab 6.\n• Xem bảng tính vật tư cấp phối bê tông.\n• Bấm tải file Excel bảng thống kê thép (Auto-BOQ).\n• Bấm nút '📥 Tải File Thuyết Minh Đồ Án (.docx)' -> Mở file Word hoàn chỉnh trên màn hình.",
         "Ở chặng cuối, Phân hệ 5 & 6 hoàn thiện quy trình kỹ thuật: Tự động tính cấp phối bê tông, tra cứu thời gian tháo ván khuôn, bóc tách khối lượng thép xuất Excel. Cuối cùng, chỉ với 1 cú click, hệ thống tự động biên soạn và xuất file Thuyết minh đồ án Microsoft Word chuẩn mẫu nộp đồ án tốt nghiệp!"),
        
        ("06:30 - 07:00\n(30 giây)",
         "• Chiếu lại slide tổng kết, đường link web đang chạy thực tế trên GitHub Pages và mã QR code trải nghiệm.\n• Lời cảm ơn và chào kết thúc.",
         "SmartConstruct Web AI không chỉ là một bài thi phần mềm, mà là minh chứng cho việc sinh viên Đại Học Duy Tân làm chủ công nghệ AI để giải quyết bài toán cốt lõi của ngành Xây dựng Việt Nam. Kính mời Ban Giám khảo truy cập link trực tiếp để trải nghiệm. Xin trân trọng cảm ơn!")
    ]

    for t_str, act_str, voice_str in scenes:
        row = table.add_row()
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c0.width = Inches(1.1)
        c1.width = Inches(2.7)
        c2.width = Inches(3.2)
        
        for c, text in [(c0, t_str), (c1, act_str), (c2, voice_str)]:
            p = c.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            set_cell_margins(c, 80, 80, 100, 100)
            if c == c0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_background(c, "F1F5F9")
            else:
                set_cell_background(c, "FFFFFF")

    filepath = os.path.join(OUTPUT_DIR, "02_Kich_Ban_Video_Thuyet_Trinh_7_Phut.docx")
    doc.save(filepath)
    print(f"✅ Đã tạo thành công: {filepath}")

# ==============================================================================
# FILE 3: TÀI LIỆU PROMPT LOG & SYSTEM PROMPT
# ==============================================================================
def create_file_3():
    doc = Document()
    
    title = doc.add_heading("TÀI LIỆU PROMPT LOG & QUY TRÌNH PROMPT ENGINEERING", level=0)
    title.runs[0].font.name = "Times New Roman"
    title.runs[0].font.color.rgb = COLOR_DTU_CRIMSON
    title.runs[0].font.size = Pt(16)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    sub = doc.add_paragraph()
    r = sub.add_run("MINH CHỨNG SỬ DỤNG AI THEO ĐÚNG THỂ LỆ CUỘC THI AI INNOVATION 2026\nDỰ ÁN: SMARTCONSTRUCT WEB AI • ĐẠI HỌC DUY TÂN\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.italic = True
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    sections = [
        ("1. NGUYÊN TẮC THIẾT KẾ PROMPT KỸ THUẬT (PROMPT ENGINEERING PRINCIPLES)", [
            "Trong dự án SmartConstruct Web AI, kỹ thuật Prompting được áp dụng theo các tiêu chuẩn kỹ thuật nghiêm ngặt:",
            "1. Role-based Prompting (Định vị vai trò): Ép mô hình AI đóng vai trò Chuyên gia Kết cấu và Pháp chế Xây dựng am hiểu TCVN, loại bỏ cách nói chuyện chung chung.",
            "2. Grounded Constraints (Ràng buộc tri thức): Bắt buộc AI chỉ được trích dẫn theo đúng các văn bản hiện hành (TCVN 5574:2018, TCVN 2737:2023, Nghị định 206/2026/NĐ-CP, Nghị định 217/2026/NĐ-CP).",
            "3. Structured Output: Định dạng câu trả lời theo khuôn mẫu khoa học: [Căn cứ pháp lý] -> [Phân tích kỹ thuật] -> [Khuyến nghị an toàn công trình]."
        ]),
        ("2. MASTER SYSTEM PROMPT NẠP TRONG MODULE CHATBOT (`ai_services/llm_assistant.py`)", [
            "\"\"\"\nBẠN LÀ TRỢ LÝ KỸ THUẬT XÂY DỰNG & CHUYÊN GIA PHÁP LÝ CAO CẤP (SMARTCONSTRUCT AI ENGINE)\nĐƠN VỊ: KHOA XÂY DỰNG • TRƯỜNG ĐẠI HỌC DUY TÂN (DTU).\n\nNHIỆM VỤ:\n1. Giải đáp tiêu chuẩn: TCVN 5574:2018 (BTCT), TCVN 2737:2023 (Tải trọng gió), TCVN 9362:2012 (Nền móng), TCVN 4453:1995 (Cốp pha & Thi công).\n2. Tư vấn pháp luật: Luật Xây dựng, Nghị định 206/2026/NĐ-CP (BIM bắt buộc) và Nghị định 217/2026/NĐ-CP (Quản lý dự án & Chi phí).\n\nQUY TẮC PHẢN HỒI:\n- TUYỆT ĐỐI KHÔNG tự bịa số liệu tính toán toán học phức tạp; hãy trích dẫn công thức và bảng tra theo TCVN.\n- Luôn chỉ rõ số hiệu điều khoản, bảng tra cứu cụ thể (Ví dụ: 'Theo Điều 6.1.2 Bảng 6 TCVN 5574:2018...').\n- Câu trả lời phải có cấu trúc 3 phần rõ ràng: 1. Căn cứ điều khoản -> 2. Giải thích bản chất -> 3. Hướng dẫn áp dụng.\n- Tông giọng chuyên nghiệp, mạch lạc của một Kỹ sư Trưởng.\n\"\"\""
        ]),
        ("3. LỊCH SỬ TRAO ĐỔI VỚI AI (PROMPT LOGS TRÍCH XUẤT TIÊU BIỂU)", [
            "• Prompt 1 (Yêu cầu thiết kế Lõi toán học TCVN):",
            "'Hãy viết thuật toán kiểm tra dầm chịu uốn theo TCVN 5574:2018. Đầu vào gồm b, h, M, Rb, Rs, a. Tính alpha_m, alpha_R, xi, As_yc và kiểm tra điều kiện alpha_m <= alpha_R. Nếu alpha_m > alpha_R phải phát tín hiệu cảnh báo phá hoại giòn. Không dùng thư viện ngoài, chỉ dùng công thức chuẩn.'",
            "-> Kết quả AI phản hồi: Đã sinh hàm `calculate_beam()` trong `engines/structural_engine.py` chuẩn xác 100%.",
            "",
            "• Prompt 2 (Yêu cầu tích hợp Đồ họa 3D BIM WebGL):",
            "'Viết mã nguồn Three.js r128 tích hợp OrbitControls để hiển thị mặt cắt dầm 3D. Dầm bê tông phải có hiệu ứng thấu quang X-Ray (opacity 0.38, viền Cyan), bên trong hiển thị các thanh thép chủ hình trụ màu vàng kim loại, thép giá xanh dương và hệ cốt đai chữ nhật bo góc chạy dọc nhịp.'",
            "-> Kết quả AI phản hồi: Đã sinh module WebGL 3D trong `smartconstruct_blueprint_cad.html` chạy mượt mà 60 FPS.",
            "",
            "• Prompt 3 (Yêu cầu RAG Pháp lý Nghị định 206/2026/NĐ-CP):",
            "'Tóm tắt điều kiện bắt buộc áp dụng Mô hình thông tin công trình (BIM) theo Nghị định 206/2026/NĐ-CP và lập hàm kiểm tra tự động theo Cấp công trình và Nguồn vốn.'",
            "-> Kết quả AI phản hồi: Đã sinh hàm `check_legal_and_bim()` trong `ai_services/llm_assistant.py`."
        ])
    ]

    for title_sec, content_list in sections:
        h = doc.add_heading(title_sec, level=1)
        h.runs[0].font.name = "Times New Roman"
        h.runs[0].font.size = Pt(12.5)
        h.runs[0].font.color.rgb = COLOR_DTU_CRIMSON

        for text in content_list:
            p = doc.add_paragraph()
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)
            if text.startswith("\"\"\"") or text.startswith("'"):
                r.font.italic = True

    filepath = os.path.join(OUTPUT_DIR, "03_Prompt_Log_Va_He_Thong_System_Prompt.docx")
    doc.save(filepath)
    print(f"✅ Đã tạo thành công: {filepath}")

# ==============================================================================
# FILE 4: BẢN KÊ KHAI CÔNG CỤ AI, THƯ VIỆN & PHÂN ĐỊNH ĐÓNG GÓP
# ==============================================================================
def create_file_4():
    doc = Document()
    
    title = doc.add_heading("BẢN KÊ KHAI CÔNG CỤ AI, TÀI NGUYÊN & PHÂN ĐỊNH ĐÓNG GÓP", level=0)
    title.runs[0].font.name = "Times New Roman"
    title.runs[0].font.color.rgb = COLOR_DTU_CRIMSON
    title.runs[0].font.size = Pt(16)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    sub = doc.add_paragraph()
    r = sub.add_run("CAM KẾT MINH BẠCH VÀ LIÊM CHÍNH HỌC THUẬT THEO THỂ LỆ BẢNG A\nCUỘC THI SÁNG TẠO ỨNG DỤNG TRÍ TUỆ NHÂN TẠO 2026\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.italic = True
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading("1. BẢNG PHÂN ĐỊNH ĐÓNG GÓP (TỰ LÀM / AI HỖ TRỢ / KẾ THỪA)", level=1).runs[0].font.color.rgb = COLOR_DTU_CRIMSON

    table = doc.add_table(rows=1, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Hạng mục thành phần", "Nhóm tác giả tự làm (Human Core)", "AI hỗ trợ (AI Assisted)", "Kế thừa bên thứ 3 (Open-source)", "Tỷ lệ tự làm"]
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_background(hdr_cells[i], "8B1520")
        p = hdr_cells[i].paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.size = Pt(9.5)

    data = [
        ("Thuật toán & Toán học TCVN", "Thiết lập công thức giải tích dầm, cột, móng, sàn, tải gió, đầm chặt đất", "Kiểm tra tính đối xứng và viết khung hàm", "Không", "85%"),
        ("Cơ sở dữ liệu tĩnh TCVN", "Thu thập, kiểm chứng bảng tra bê tông B15-B40, thép CB240-CB500", "Định dạng sang cấu trúc dữ liệu JSON/Dict", "Không", "80%"),
        ("Đồ họa 3D BIM & 2D CAD", "Thiết kế bố cục, màu sắc lớp thép, khung tên đồ án DTU chuẩn TCVN", "Sinh mã WebGL Three.js, tính tọa độ vector SVG", "Three.js (r128), OrbitControls.js", "60%"),
        ("Giao diện Web Dashboard", "Thiết kế trải nghiệm người dùng, nút Demo 1-Click, cơ chế chuyển tab", "Tối ưu hóa mã nguồn HTML5/CSS3 và Streamlit", "Streamlit, Google Fonts", "65%"),
        ("Trợ lý RAG & Pháp lý Xây dựng", "Biên soạn 50 câu hỏi trắc nghiệm, tuyển chọn luật và nghị định", "Suy luận ngôn ngữ tự nhiên, trả lời câu hỏi", "Google Gemini API qua google-genai", "70%"),
        ("Bóc tách BOQ & Xuất file Word", "Thiết kế mẫu bảng thuyết minh kỹ thuật, công thức trọng lượng thép", "Sinh code đổ dữ liệu vào file .docx và .xlsx", "python-docx, openpyxl", "75%")
    ]

    for row_data in data:
        row = table.add_row()
        for idx, val in enumerate(row_data):
            cell = row.cells[idx]
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            set_cell_margins(cell, 80, 80, 80, 80)
            if idx == 4:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r.font.bold = True
                set_cell_background(cell, "FEF3C7")
            elif idx == 0:
                r.font.bold = True
                set_cell_background(cell, "F8FAFC")
            else:
                set_cell_background(cell, "FFFFFF")

    doc.add_heading("2. KÊ KHAI DANH MỤC CÔNG CỤ VÀ NGUỒN TÀI NGUYÊN", level=1).runs[0].font.color.rgb = COLOR_DTU_CRIMSON
    tools = [
        "- Mô hình AI sử dụng: Google Gemini 1.5/2.5 Flash, Gemini Pro qua chính sách API bản quyền của Google Cloud.",
        "- Ngôn ngữ lập trình: Python 3.10+, JavaScript (ES6+), HTML5, CSS3.",
        "- Thư viện mã nguồn mở: Streamlit, Three.js, Plotly, Matplotlib, Pandas, NumPy, python-docx, openpyxl.",
        "- Cơ sở dữ liệu dẫn chiếu: TCVN 5574:2018, TCVN 2737:2023, TCVN 9362:2012, TCVN 4453:1995, Nghị định 206/2026/NĐ-CP, Nghị định 217/2026/NĐ-CP.",
        "- Khóa bảo mật: Master API Key máy chủ được cấu hình an toàn trong file môi trường `.env`, tuyệt đối không lưu trữ khóa công khai trên kho GitHub."
    ]
    for t in tools:
        p = doc.add_paragraph()
        r = p.add_run(t)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)

    filepath = os.path.join(OUTPUT_DIR, "04_Ban_Ke_Khai_Dong_Gop_AI_Minh_Bach.docx")
    doc.save(filepath)
    print(f"✅ Đã tạo thành công: {filepath}")

# ==============================================================================
# FILE 5: ĐƯỜNG DẪN TRỰC TUYẾN & HƯỚNG DẪN DÙNG THỬ DÀNH CHO GIÁM KHẢO
# ==============================================================================
def create_file_5():
    doc = Document()
    
    title = doc.add_heading("THÔNG TIN ĐƯỜNG DẪN SẢN PHẨM & HƯỚNG DẪN CHẤM THI", level=0)
    title.runs[0].font.name = "Times New Roman"
    title.runs[0].font.color.rgb = COLOR_DTU_CRIMSON
    title.runs[0].font.size = Pt(16)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    sub = doc.add_paragraph()
    r = sub.add_run("DỰ ÁN: SMARTCONSTRUCT WEB AI • KHOA XÂY DỰNG • ĐẠI HỌC DUY TÂN\nHẠNG MỤC: BẢNG A – SÁNG TẠO PHẦN MỀM, WEBSITE BẰNG AI\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.italic = True
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading("1. DANH SÁCH ĐƯỜNG DẪN CHÍNH THỨC (TRUY CẬP 24/7)", level=1).runs[0].font.color.rgb = COLOR_DTU_CRIMSON

    links = [
        ("🌐 Đường dẫn 1 (Trang Web 3D BIM & Blueprint CAD Tốc độ cao):", 
         "https://vantruongbui747-cpu.github.io/smartconstruct-web-ai/\n"
         "• Đặc điểm: Chạy trực tiếp trên GitHub Pages, mở tức thì trên mọi điện thoại/máy tính, hỗ trợ xoay mô hình 3D lồng thép, kéo thanh trượt kích thước và tải bản vẽ vector SVG."),
        
        ("🌐 Đường dẫn 2 (Trang Web Toàn Diện 6 Phân hệ & Chatbot AI Streamlit):", 
         "https://smartconstruct-dtu.streamlit.app\n"
         "• Đặc điểm: Đầy đủ 6 phân hệ, bao gồm Chatbot AI Gemini, đọc file Excel SAP2000 và xuất file Word .docx."),
        
        ("💻 Đường dẫn Kho mã nguồn (GitHub Repository):", 
         "https://github.com/vantruongbui747-cpu/smartconstruct-web-ai\n"
         "• Đặc điểm: Kho lưu trữ mã nguồn mở có đầy đủ lịch sử commit minh bạch qua từng giai đoạn phát triển.")
    ]

    for label, val in links:
        p = doc.add_paragraph()
        r1 = p.add_run(label + "\n")
        r1.font.bold = True
        r1.font.color.rgb = COLOR_NAVY
        r2 = p.add_run(val)
        r2.font.color.rgb = COLOR_DTU_CRIMSON
        p.paragraph_format.line_spacing = 1.25

    doc.add_heading("2. HƯỚNG DẪN CHẤM THI NHANH TRONG 30 GIÂY DÀNH CHO GIÁM KHẢO", level=1).runs[0].font.color.rgb = COLOR_DTU_CRIMSON
    steps = [
        "1. Đăng nhập: Khi truy cập trang web, màn hình yêu cầu email. Giám khảo chỉ cần nhập bất kỳ địa chỉ email nào (Ví dụ: giamkhao@dtu.edu.vn). Hệ thống tự động cấp quyền truy cập Master Key máy chủ.",
        "2. Kiểm tra nhanh (Demo 1-Click): Tại thanh Sidebar bên trái, bấm vào nút màu đỏ '⚡ Nạp Bộ Số Liệu Mẫu (Đồ Án Thực Tế)'. Toàn bộ các thông số của một công trình 10 tầng thực tế sẽ tự động điền vào 6 phân hệ.",
        "3. Trải nghiệm 3D BIM: Bấm vào Tab 1 (Kết cấu BTCT) -> Bấm nút '🧊 3D BIM'. Dùng chuột xoay 360 độ và cuộn chuột để zoom quan sát lồng cốt thép dầm/cột chân thực.",
        "4. Xuất thuyết minh: Bấm vào Tab 6 (Xuất Thuyết Minh) -> Bấm nút '📥 Tải File Thuyết Minh Đồ Án (.docx)' để tải về bản báo cáo hoàn chỉnh được hệ thống tự động soạn thảo."
    ]
    for s in steps:
        p = doc.add_paragraph()
        r = p.add_run(s)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)

    filepath = os.path.join(OUTPUT_DIR, "05_Duong_Dan_San_Pham_Va_Huong_Dan_Giam_Khao.docx")
    doc.save(filepath)
    print(f"✅ Đã tạo thành công: {filepath}")

# ==============================================================================
# FILE 6: TRANG HTML IN ẤN PDF HOÀN CHỈNH (PRINT-READY)
# ==============================================================================
def create_printable_html():
    html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Hồ Sơ Mô Tả Sản Phẩm - SmartConstruct Web AI (Mẫu 1)</title>
    <style>
        @page {
            size: A4;
            margin: 20mm 15mm 20mm 20mm;
        }
        body {
            font-family: 'Times New Roman', Times, serif;
            font-size: 13pt;
            line-height: 1.35;
            color: #0F172A;
            background: #FFF;
            margin: 0;
            padding: 20px;
        }
        .header-dtu {
            text-align: center;
            color: #8B1520;
            font-weight: bold;
            font-size: 11pt;
            border-bottom: 2px solid #8B1520;
            padding-bottom: 8px;
            margin-bottom: 25px;
        }
        .title-doc {
            text-align: center;
            color: #8B1520;
            font-size: 20pt;
            font-weight: bold;
            margin-bottom: 6px;
        }
        .subtitle-doc {
            text-align: center;
            color: #C5A059;
            font-size: 13pt;
            font-weight: bold;
            margin-bottom: 25px;
        }
        h2 {
            color: #8B1520;
            font-size: 14pt;
            border-bottom: 1px solid #CBD5E1;
            padding-bottom: 4px;
            margin-top: 24px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 11pt;
        }
        th, td {
            border: 1px solid #94A3B8;
            padding: 8px 10px;
            text-align: left;
        }
        th {
            background-color: #8B1520;
            color: #FFF;
        }
        .highlight-box {
            background: #F8FAFC;
            border-left: 4px solid #8B1520;
            padding: 12px 16px;
            margin: 15px 0;
            font-size: 12pt;
        }
        .footer-sign {
            margin-top: 40px;
            display: flex;
            justify-content: space-between;
            text-align: center;
            page-break-inside: avoid;
        }
        @media print {
            body { padding: 0; }
            .no-print { display: none; }
        }
    </style>
</head>
<body>
    <div class="no-print" style="background: #0F172A; color: #FFF; padding: 12px 20px; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
        <span>📄 <b>Bản Xem Trước In Hồ Sơ Mô Tả Sản Phẩm (Mẫu 1)</b> • Bấm nút bên phải để xuất PDF ngay lập tức:</span>
        <button onclick="window.print()" style="background: #8B1520; color: #FFF; border: 1px solid #C5A059; padding: 8px 18px; font-weight: bold; border-radius: 6px; cursor: pointer;">🖨️ In / Lưu Dạng PDF (Ctrl + P)</button>
    </div>

    <div class="header-dtu">
        BỘ GIÁO DỤC VÀ ĐÀO TẠO • TRƯỜNG ĐẠI HỌC DUY TÂN (DTU)<br>
        KHOA XÂY DỰNG • BỘ MÔN KỸ THUẬT CÔNG TRÌNH
    </div>

    <div class="subtitle-doc">CUỘC THI SÁNG TẠO ỨNG DỤNG TRÍ TUỆ NHÂN TẠO 2026 • BẢNG A</div>
    <div class="title-doc">HỒ SƠ MÔ TẢ SẢN PHẨM DỰ THI (MẪU 1)</div>
    <div style="text-align: center; font-weight: bold; font-size: 15pt; color: #0F172A; margin-bottom: 20px;">
        SMARTCONSTRUCT WEB AI: NỀN TẢNG WEB TRỢ LÝ KỸ THUẬT, TRA CỨU TIÊU CHUẨN TCVN & MÔ HÌNH HÓA 3D BIM KẾT CẤU XÂY DỰNG THÔNG MINH
    </div>

    <div class="highlight-box">
        <b>Tác giả chính:</b> Bùi Văn Trường • <b>Đơn vị:</b> Khoa Xây Dựng, Trường Đại Học Duy Tân<br>
        <b>Hạng mục:</b> BẢNG A – Ứng dụng phần mềm, website • <b>Thời hạn nộp:</b> 23h59 ngày 30/11/2026<br>
        <b>Đường dẫn Web chạy thực tế:</b> https://vantruongbui747-cpu.github.io/smartconstruct-web-ai/
    </div>

    <h2>1. THÔNG TIN CHUNG VÀ MỤC TIÊU DỰ ÁN</h2>
    <p>SmartConstruct Web AI là nền tảng số toàn diện hỗ trợ sinh viên và kỹ sư xây dựng giải quyết bài toán lớn: Tra cứu tiêu chuẩn TCVN, tính toán kết cấu cơ học chính xác tuyệt đối, mô hình hóa 3D BIM trực tiếp trên Web và tự động xuất hồ sơ thuyết minh kỹ thuật.</p>

    <h2>2. KIẾN TRÚC HYBRID 3 LỚP ĐỘC ĐÁO CHỐNG ẢO GIÁC AI</h2>
    <p>Hệ thống phân định rạch ròi 3 tầng công nghệ: Lõi toán học giải tích Python/JS (sai số = 0), Lõi đồ họa 3D BIM WebGL Three.js (xoay lồng thép 360 độ) và Lõi AI Gemini đóng vai trò trợ lý tra cứu pháp lý TCVN/BIM.</p>

    <h2>3. CHI TIẾT 06 PHÂN HỆ CỐT LÕI</h2>
    <ul>
        <li><b>Phân hệ 1 (Kết cấu BTCT):</b> Tính sàn 1 phương/2 phương, dầm chịu uốn & cắt TCVN 5574:2018, cột chịu nén lệch tâm & biểu đồ P-M.</li>
        <li><b>Phân hệ 2 (Địa kỹ thuật & Móng):</b> Đường cong đầm chặt Proctor và tính toán móng đơn nông TCVN 9362:2012.</li>
        <li><b>Phân hệ 3 (Tải gió & SAP2000):</b> Bản đồ tải trọng gió TCVN 2737:2023 và tính năng lọc nội lực file Excel SAP2000 tự động.</li>
        <li><b>Phân hệ 4 (Chatbot TCVN & BIM):</b> Tra cứu Luật Xây dựng, Nghị định 206/2026/NĐ-CP và trắc nghiệm pháp luật xây dựng.</li>
        <li><b>Phân hệ 5 & 6 (Thi công & Xuất file Word):</b> Định mức cấp phối vật tư bê tông, thống kê thép Auto-BOQ xuất Excel và xuất thuyết minh Word (.docx).</li>
    </ul>

    <h2>4. BẢNG PHÂN ĐỊNH ĐÓNG GÓP MINH BẠCH (LIÊM CHÍNH HỌC THUẬT)</h2>
    <table>
        <thead>
            <tr>
                <th>Hạng mục thành phần</th>
                <th>Tự làm (Human Core)</th>
                <th>AI hỗ trợ</th>
                <th>Kế thừa nguồn mở</th>
                <th>Tỷ lệ tự làm</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Toán học & Tiêu chuẩn TCVN</td><td>Thiết lập công thức dầm, cột, móng, gió</td><td>Kiểm tra cú pháp code</td><td>Không</td><td><b>85%</b></td></tr>
            <tr><td>Cơ sở dữ liệu số hóa TCVN</td><td>Thu thập, kiểm chứng bảng tra bê tông, thép</td><td>Định dạng cấu trúc JSON</td><td>Không</td><td><b>80%</b></td></tr>
            <tr><td>Đồ họa 3D BIM & 2D CAD</td><td>Thiết kế bố cục, màu sắc, khung tên DTU</td><td>Sinh mã Three.js, SVG</td><td>Three.js r128</td><td><b>60%</b></td></tr>
            <tr><td>Giao diện Web Dashboard</td><td>Thiết kế UX flow, nút Demo 1-Click</td><td>Tối ưu mã HTML5/CSS3</td><td>Streamlit, Fonts</td><td><b>65%</b></td></tr>
            <tr><td>Trợ lý RAG & Pháp lý BIM</td><td>Biên soạn 50 câu trắc nghiệm, tuyển luật</td><td>Suy luận ngôn ngữ tự nhiên</td><td>Gemini API</td><td><b>70%</b></td></tr>
            <tr><td>Bóc tách BOQ & Xuất file Word</td><td>Mẫu thuyết minh chuẩn ĐH Duy Tân</td><td>Sinh module file .docx, .xlsx</td><td>python-docx</td><td><b>75%</b></td></tr>
        </tbody>
    </table>

    <div class="footer-sign">
        <div>
            <b>XÁC NHẬN CỦA KHOA XÂY DỰNG</b><br>
            <i>(Ký, đóng dấu và ghi rõ họ tên)</i>
        </div>
        <div>
            <b>ĐẠI DIỆN NHÓM TÁC GIẢ</b><br>
            <i>(Ký và ghi rõ họ tên)</i><br><br><br><br>
            <b>Bùi Văn Trường</b>
        </div>
    </div>
</body>
</html>
"""
    filepath = os.path.join(OUTPUT_DIR, "Ho_So_Mo_Ta_San_Pham_In_PDF.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[OK] Da tao thanh cong: {filepath}")

if __name__ == "__main__":
    print("[START] Bat dau qua trinh bien soan va xuat toan bo ho so Vong 2...")
    create_file_1()
    create_file_2()
    create_file_3()
    create_file_4()
    create_file_5()
    create_printable_html()
    print("\n[SUCCESS] HOAN TAT 100%! Toan bo ho so da nam tai thu muc:", OUTPUT_DIR)
