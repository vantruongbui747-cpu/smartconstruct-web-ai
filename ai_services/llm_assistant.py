"""
Module: ai_services/llm_assistant.py
Mục đích:
- Trợ lý AI tra cứu Tiêu chuẩn Xây dựng (TCVN 5574:2018, TCVN 2737:2023, TCVN 9362:2012, TCVN 4453:1995)
- Tra cứu Pháp lý Xây dựng & Lộ trình áp dụng BIM (Luật Xây dựng, Nghị định 206/2026/NĐ-CP, NĐ 217/2026/NĐ-CP)
- Kiểm tra nhanh điều kiện Miễn Giấy phép xây dựng & Bắt buộc áp dụng BIM
- Ngân hàng câu hỏi trắc nghiệm Pháp luật Xây dựng có chấm điểm và giải thích
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

load_dotenv()

SYSTEM_INSTRUCTION = """
Bạn là Trợ lý Pháp lý & Kỹ thuật Xây dựng cao cấp (Khoa Xây Dựng, Đại học Duy Tân).
Bạn nắm vững hệ thống Tiêu chuẩn & Quy chuẩn Xây dựng Việt Nam:
1. Tiêu chuẩn kỹ thuật: TCVN 5574:2018 (BTCT), TCVN 2737:2023 (Tải trọng), TCVN 9362:2012 (Móng), TCVN 4453:1995 (Thi công bê tông).
2. Pháp lý xây dựng: Luật Xây dựng sửa đổi bổ sung, Nghị định 206/2026/NĐ-CP (Quản lý dự án & Lộ trình áp dụng BIM bắt buộc), Nghị định 217/2026/NĐ-CP (Quản lý chi phí & hợp đồng).

NGUYÊN TẮC PHẢN HỒI:
- Trả lời khúc chiết, phân cấp đầu mục rõ ràng, trích dẫn rõ tên Nghị định, Điều, Khoản.
- Nếu người dùng hỏi về BIM, luôn dẫn chiếu lộ trình áp dụng theo cấp công trình và nguồn vốn.
"""

def get_server_master_key() -> Optional[str]:
    key = os.getenv("GEMINI_API_KEY")
    if key and key.strip():
        return key.strip()
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip():
            return st.secrets["GEMINI_API_KEY"].strip()
    except Exception:
        pass
    return None

def call_gemini(prompt: str) -> str:
    key = get_server_master_key()
    if not key:
        return _offline_knowledge_fallback(prompt)
        
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=key)
        for model in ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-1.5-flash", "gemini-flash"]:
            try:
                res = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.3
                    )
                )
                if res and res.text:
                    return res.text
            except Exception:
                continue
    except Exception:
        try:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=key)
            m = legacy_genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_INSTRUCTION)
            res = m.generate_content(prompt)
            if res and res.text:
                return res.text
        except Exception:
            pass
            
    return _offline_knowledge_fallback(prompt, prefix="*(Chế độ Tri thức Pháp lý Offline)*\n\n")

def _offline_knowledge_fallback(prompt: str, prefix: str = "") -> str:
    p = prompt.lower()
    if "bim" in p or "nghị định 206" in p:
        return prefix + (
            "### 📌 LỘ TRÌNH ÁP DỤNG BIM BẮT BUỘC THEO NGHỊ ĐỊNH 206/2026/NĐ-CP\n\n"
            "1. **Dự án sử dụng vốn đầu tư công, vốn nhà nước ngoài đầu tư công:**\n"
            "   - **Công trình Cấp Đặc biệt và Cấp I:** BẮT BUỘC áp dụng mô hình thông tin công trình (BIM) trong giai đoạn thiết kế, thi công và quản lý vận hành.\n"
            "   - **Công trình Cấp II:** BẮT BUỘC áp dụng BIM từ năm 2026 trở đi.\n"
            "   - **Công trình Cấp III, Cấp IV:** Khuyến khích áp dụng nếu Chủ đầu tư có đủ năng lực công nghệ.\n\n"
            "2. **Dự án sử dụng vốn khác (Tư nhân, FDI):** Nhà nước khuyến khích áp dụng BIM để tối ưu chi phí và minh bạch vòng đời công trình."
        )
    elif "giấy phép xây dựng" in p or "miễn" in p:
        return prefix + (
            "### 📌 ĐIỀU KIỆN MIỄN GIẤY PHÉP XÂY DỰNG (ĐIỀU 89 LUẬT XÂY DỰNG)\n\n"
            "Các trường hợp được MIỄN giấy phép xây dựng gồm:\n"
            "1. Công trình bí mật nhà nước, công trình xây dựng khẩn cấp.\n"
            "2. Công trình thuộc dự án sử dụng vốn đầu tư công được Thủ tướng, người đứng đầu cơ quan trung ương quyết định đầu tư.\n"
            "3. Công trình tạm phục vụ thi công xây dựng công trình chính.\n"
            "4. Công trình quảng cáo không thuộc đối tượng phải cấp GPXD theo quy định pháp luật về quảng cáo.\n"
            "5. Nhà ở riêng lẻ có quy mô dưới 7 tầng thuộc dự án đầu tư xây dựng khu đô thị đã có quy hoạch chi tiết 1/500."
        )
    return prefix + (
        "### 🏛️ CĂN CỨ TIÊU CHUẨN & PHÁP LÝ KỸ THUẬT XÂY DỰNG\n\n"
        "Hệ thống Tiêu chuẩn Xây dựng Việt Nam hiện hành quy định chặt chẽ về điều kiện an toàn chịu lực:\n"
        "- **TCVN 5574:2018:** Tính toán theo 2 trạng thái giới hạn (TTGH 1: Cường độ & Ổn định; TTGH 2: Độ võng và Bề rộng khe nứt).\n"
        "- **TCVN 2737:2023:** Phân loại tải trọng thường xuyên, tải trọng tạm thời và hệ số độ tin cậy tải trọng gamma_f."
    )

# ==============================================================================
# BỘ CÔNG CỤ: KIỂM TRA NHANH PHÁP LÝ & BIM
# ==============================================================================
def check_legal_and_bim(project_grade: str, fund_source: str) -> Dict[str, Any]:
    """Kiểm tra điều kiện áp dụng BIM và Miễn GPXD theo Nghị định 206/2026/NĐ-CP"""
    # 1. Kiểm tra BIM
    is_bim_mandatory = False
    bim_status_text = ""
    
    if "Đầu tư công" in fund_source or "Vốn nhà nước" in fund_source:
        if project_grade in ["Cấp Đặc biệt", "Cấp I"]:
            is_bim_mandatory = True
            bim_status_text = "🔴 BẮT BUỘC ÁP DỤNG BIM trong toàn bộ giai đoạn Thiết kế, Thi công & Hoàn công (NĐ 206/2026/NĐ-CP)."
        elif project_grade == "Cấp II":
            is_bim_mandatory = True
            bim_status_text = "🟠 BẮT BUỘC ÁP DỤNG BIM từ năm 2026 theo lộ trình số hóa quốc gia."
        else:
            bim_status_text = "🟢 KHÔNG BẮT BUỘC (Khuyến khích áp dụng để tăng hiệu quả quản lý dự án)."
    else:
        bim_status_text = "🟢 Vốn khác: Nhà nước KHUYẾN KHÍCH áp dụng BIM, Chủ đầu tư tự quyết định."

    # 2. Kiểm tra Giấy phép xây dựng
    if "Đầu tư công" in fund_source and project_grade in ["Cấp Đặc biệt", "Cấp I"]:
        permit_text = "🛡️ Đủ điều kiện xem xét MIỄN Giấy phép xây dựng nếu dự án được Thủ tướng Chính phủ hoặc Bộ trưởng phê duyệt quyết định đầu tư."
    else:
        permit_text = "📋 BẮT BUỘC phải lập hồ sơ xin Cấp Giấy phép xây dựng tại Sở Xây dựng hoặc UBND cấp có thẩm quyền trước khi khởi công."

    return {
        "project_grade": project_grade,
        "fund_source": fund_source,
        "is_bim_mandatory": is_bim_mandatory,
        "bim_verdict": bim_status_text,
        "permit_verdict": permit_text
    }

# ==============================================================================
# NGÂN HÀNG CÂU HỎI TRẮC NGHIỆM PHÁP LUẬT XÂY DỰNG
# ==============================================================================
LEGAL_QUIZ_BANK = [
    {
        "id": 1,
        "question": "Theo Nghị định 206/2026/NĐ-CP, dự án sử dụng vốn đầu tư công nào sau đây BẮT BUỘC phải áp dụng Mô hình thông tin công trình (BIM)?",
        "options": [
            "A. Công trình từ Cấp II trở lên",
            "B. Chỉ áp dụng cho công trình Cấp Đặc biệt",
            "C. Tất cả mọi công trình từ Cấp IV trở lên",
            "D. Công trình nhà ở riêng lẻ nông thôn"
        ],
        "answer": "A. Công trình từ Cấp II trở lên",
        "explanation": "Theo lộ trình áp dụng BIM, công trình Cấp Đặc biệt và Cấp I bắt buộc từ 2024, công trình Cấp II bắt buộc từ năm 2026 đối với dự án sử dụng vốn đầu tư công."
    },
    {
        "id": 2,
        "question": "Theo TCVN 5574:2018, hệ số độ tin cậy của bê tông về cường độ khi tính toán theo Trạng thái giới hạn thứ nhất với tổ hợp cơ bản là:",
        "options": [
            "A. gamma_b = 1.3 đối với chịu nén và gamma_bt = 1.5 đối với chịu kéo",
            "B. gamma_b = 1.0 đối với mọi trạng thái",
            "C. gamma_b = 1.15 cho cốt thép và gamma_b = 1.5 cho bê tông",
            "D. gamma_b = 1.25 đối với bê tông cấp thấp"
        ],
        "answer": "A. gamma_b = 1.3 đối với chịu nén và gamma_bt = 1.5 đối với chịu kéo",
        "explanation": "Theo Điều 6.1.3 TCVN 5574:2018, hệ số độ tin cậy gamma_b = 1.3 (chịu nén) và gamma_bt = 1.5 (chịu kéo)."
    },
    {
        "id": 3,
        "question": "Theo Luật Xây dựng hiện hành, hành vi nào sau đây bị nghiêm cấm trong hoạt động xây dựng?",
        "options": [
            "A. Khởi công xây dựng công trình khi chưa đủ điều kiện khởi công",
            "B. Áp dụng tiến bộ khoa học công nghệ BIM vào dự án",
            "C. Sử dụng vật liệu xây dựng thân thiện với môi trường",
            "D. Thuê tư vấn giám sát độc lập kiểm định chất lượng"
        ],
        "answer": "A. Khởi công xây dựng công trình khi chưa đủ điều kiện khởi công",
        "explanation": "Điều 12 Luật Xây dựng quy định nghiêm cấm khởi công xây dựng công trình khi chưa có mặt bằng xây dựng, chưa có giấy phép xây dựng hoặc chưa đủ điều kiện quy định."
    }
]
