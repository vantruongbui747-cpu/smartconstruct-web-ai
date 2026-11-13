"""
Module: data_tcvn.py
Mục đích: Số hóa và chuẩn hóa cơ sở dữ liệu vật liệu, thông số tính toán theo TCVN 5574:2018 & TCVN 2737:2023.
Dự án: SMARTCONSTRUCT WEB AI - Khoa Xây Dựng
"""

# ==============================================================================
# 1. BẢNG THÔNG SỐ BÊ TÔNG THEO TCVN 5574:2018 (Bảng 6 & Bảng 7)
# Đơn vị: MPa (N/mm2), Eb đơn vị 10^3 MPa
# ==============================================================================
CONCRETE_DATABASE = {
    "B15": {
        "Rb": 8.5,       # Cường độ chịu nén tính toán (MPa)
        "Rbt": 0.75,     # Cường độ chịu kéo tính toán (MPa)
        "Rb_ser": 11.0,  # Cường độ tiêu chuẩn trạng thái giới hạn II (MPa)
        "Rbt_ser": 1.15,
        "Eb": 23.0,      # Modun đàn hồi ban đầu (10^3 MPa)
        "density": 2500  # Khối lượng thể tích (kg/m3)
    },
    "B20": {
        "Rb": 11.5,
        "Rbt": 0.90,
        "Rb_ser": 15.0,
        "Rbt_ser": 1.35,
        "Eb": 27.0,
        "density": 2500
    },
    "B25": {
        "Rb": 14.5,
        "Rbt": 1.05,
        "Rb_ser": 18.5,
        "Rbt_ser": 1.55,
        "Eb": 30.0,
        "density": 2500
    },
    "B30": {
        "Rb": 17.0,
        "Rbt": 1.15,
        "Rb_ser": 22.0,
        "Rbt_ser": 1.75,
        "Eb": 32.5,
        "density": 2500
    },
    "B35": {
        "Rb": 19.5,
        "Rbt": 1.30,
        "Rb_ser": 25.5,
        "Rbt_ser": 1.95,
        "Eb": 34.5,
        "density": 2500
    },
    "B40": {
        "Rb": 22.0,
        "Rbt": 1.40,
        "Rb_ser": 29.0,
        "Rbt_ser": 2.10,
        "Eb": 36.0,
        "density": 2500
    }
}

# ==============================================================================
# 2. BẢNG THÔNG SỐ CỐT THÉP THEO TCVN 5574:2018 (Bảng 13 & Bảng 14)
# Đơn vị: MPa (N/mm2), Es đơn vị 10^5 MPa
# ==============================================================================
REBAR_DATABASE = {
    "CB240-T": {
        "Rs": 210,       # Cường độ chịu kéo tính toán (MPa)
        "Rsc": 210,      # Cường độ chịu nén tính toán (MPa)
        "Rsw": 170,      # Cường độ chịu cắt của cốt đai (MPa)
        "Rs_ser": 240,   # Cường độ tiêu chuẩn (MPa)
        "Es": 2.0,       # Modun đàn hồi (10^5 MPa)
        "type": "Thép trơn (Thường làm cốt đai hoặc bản sàn)"
    },
    "CB300-V": {
        "Rs": 260,
        "Rsc": 260,
        "Rsw": 210,
        "Rs_ser": 300,
        "Es": 2.0,
        "type": "Thép gai có gờ"
    },
    "CB400-V": {
        "Rs": 350,
        "Rsc": 350,
        "Rsw": 280,
        "Rs_ser": 400,
        "Es": 2.0,
        "type": "Thép gai cường độ cao thông dụng"
    },
    "CB500-V": {
        "Rs": 435,
        "Rsc": 400,
        "Rsw": 300,
        "Rs_ser": 500,
        "Es": 2.0,
        "type": "Thép gai cường độ cao đặc biệt"
    }
}

# ==============================================================================
# 3. BẢNG TRA DIỆN TÍCH CỐT THÉP THEO ĐƯỜNG KÍNH VÀ SỐ THANH (mm2)
# ==============================================================================
REBAR_DIAMETERS = [10, 12, 14, 16, 18, 20, 22, 25, 28, 32]

def get_rebar_area(d_mm: int, n: int) -> float:
    """Tính diện tích n thanh thép đường kính d (mm2)"""
    import math
    return round(n * math.pi * (d_mm ** 2) / 4.0, 1)

# Bảng tra diện tích các cỡ thép từ 1 đến 8 thanh
REBAR_AREA_TABLE = {}
for d in REBAR_DIAMETERS:
    REBAR_AREA_TABLE[d] = [get_rebar_area(d, n) for n in range(1, 9)]

# ==============================================================================
# 4. HÀM TÍNH HỆ SỐ GIỚI HẠN VÙNG NÉN xi_R VÀ alpha_R CHUẨN XÁC
# Công thức (TCVN 5574:2018 Điều 8.1.2.3.1):
# xi_R = 0.8 / (1 + (Rs / Es) / (epsilon_b2))
# Với bê tông thường (cấp <= B60): epsilon_b2 = 0.0035; Es = 2.0 * 10^5 MPa
# ==============================================================================
def calculate_xi_R(Rs: float, Es: float = 2.0e5, epsilon_b2: float = 0.0035) -> float:
    """Tính hệ số chiều cao giới hạn vùng nén xi_R theo TCVN 5574:2018"""
    epsilon_s_el = Rs / Es
    xi_R = 0.8 / (1.0 + epsilon_s_el / epsilon_b2)
    return round(xi_R, 3)

def calculate_alpha_R(xi_R: float) -> float:
    """Tính hệ số alpha_R = xi_R * (1 - 0.5 * xi_R)"""
    alpha_R = xi_R * (1.0 - 0.5 * xi_R)
    return round(alpha_R, 3)

# ==============================================================================
# 5. QUY ĐỊNH LỚP BẢO VỆ CỐT THÉP (TCVN 5574:2018 - Mục 10.3.1)
# ==============================================================================
COVER_REQUIREMENTS = {
    "Sàn, vách (trong nhà khô ráo)": ">= 15 mm và >= d thép",
    "Dầm (trong nhà khô ráo)": ">= 20 mm và >= d thép (khuyên dùng 25-30 mm)",
    "Cột (trong nhà khô ráo)": ">= 20 mm và >= d thép (khuyên dùng 30 mm)",
    "Móng, cấu kiện ngoài trời hoặc ngập nước": ">= 35 - 50 mm (có lớp lót: >= 35 mm, không lớp lót: >= 70 mm)"
}
