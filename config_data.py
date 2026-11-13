"""
Module: config_data.py
Cơ sở dữ liệu tĩnh phục vụ tính toán kỹ thuật xây dựng theo tiêu chuẩn Việt Nam hiện hành.
Dự án: SMARTCONSTRUCT WEB AI (ALL-IN-ONE CIVIL ENGINEERING AI PLATFORM)
"""

# ==============================================================================
# 1. BẢNG TRA BÊ TÔNG (TCVN 5574:2018)
# Đơn vị: Rb, Rbt, Eb tính bằng MPa (N/mm2)
# ==============================================================================
CONCRETE_DB = {
    "B15": {"Rb": 8.5,  "Rbt": 0.75, "Eb": 24000, "label": "B15 (Mác 200)"},
    "B20": {"Rb": 11.5, "Rbt": 0.90, "Eb": 27500, "label": "B20 (Mác 250)"},
    "B25": {"Rb": 14.5, "Rbt": 1.05, "Eb": 30000, "label": "B25 (Mác 300)"},
    "B30": {"Rb": 17.0, "Rbt": 1.15, "Eb": 32500, "label": "B30 (Mác 400)"},
    "B35": {"Rb": 19.5, "Rbt": 1.30, "Eb": 34500, "label": "B35 (Mác 450)"},
    "B40": {"Rb": 22.0, "Rbt": 1.40, "Eb": 36000, "label": "B40 (Mác 500)"}
}

# ==============================================================================
# 2. BẢNG TRA CỐT THÉP (TCVN 5574:2018)
# Đơn vị: MPa (N/mm2)
# ==============================================================================
REBAR_DB = {
    "CB240-T": {"Rs": 210, "Rsc": 210, "Rsw": 170, "xi_R": 0.615, "type": "Thép cuộn tròn trơn"},
    "CB300-V": {"Rs": 260, "Rsc": 260, "Rsw": 210, "xi_R": 0.583, "type": "Thép thanh vằn"},
    "CB400-V": {"Rs": 350, "Rsc": 350, "Rsw": 280, "xi_R": 0.533, "type": "Thép thanh vằn cường độ cao"},
    "CB500-V": {"Rs": 435, "Rsc": 400, "Rsw": 300, "xi_R": 0.493, "type": "Thép thanh vằn cường độ cao đặc biệt"}
}

# ==============================================================================
# 3. BẢNG DIỆN TÍCH MẶT CẮT NGANG THANH THÉP TRÒN (mm2)
# ==============================================================================
REBAR_AREA = {
    6: 28.3, 8: 50.3, 10: 78.5, 12: 113.1, 14: 153.9,
    16: 201.1, 18: 254.5, 20: 314.2, 22: 380.1, 25: 490.9,
    28: 615.8, 32: 804.2
}

# ==============================================================================
# 4. BẢNG TRA CẤP PHỐI CHO 1m3 BÊ TÔNG (Định mức vật tư thông dụng)
# ==============================================================================
MIX_PROPORTION_DB = {
    "B15 (M200)": {"cement_kg": 285, "sand_m3": 0.475, "stone_m3": 0.855, "water_lit": 185},
    "B20 (M250)": {"cement_kg": 325, "sand_m3": 0.455, "stone_m3": 0.870, "water_lit": 185},
    "B25 (M300)": {"cement_kg": 375, "sand_m3": 0.435, "stone_m3": 0.880, "water_lit": 190},
    "B30 (M400)": {"cement_kg": 445, "sand_m3": 0.400, "stone_m3": 0.875, "water_lit": 195}
}

# ==============================================================================
# 5. DỮ LIỆU TẢI TRỌNG GIÓ THEO TCVN 2737:2023
# Áp lực gió cơ sở W0 theo từng vùng gió (kN/m2)
# ==============================================================================
WIND_REGIONS = {
    "Vùng I":   {"W0": 0.65, "desc": "Vùng I: Miền núi phía Bắc, Tây Bắc"},
    "Vùng II":  {"W0": 0.95, "desc": "Vùng II: Trung du, một phần đồng bằng Bắc Bộ"},
    "Vùng III": {"W0": 1.25, "desc": "Vùng III: Ven biển miền Trung, Đà Nẵng, Quảng Nam"},
    "Vùng IV":  {"W0": 1.55, "desc": "Vùng IV: Ven biển chịu ảnh hưởng bão mạnh"},
    "Vùng V":   {"W0": 1.85, "desc": "Vùng V: Ven biển và hải đảo đặc biệt nguy hiểm"}
}

# Dạng địa hình theo TCVN 2737:2023
TERRAIN_TYPES = {
    "A": {"name": "Địa hình A", "desc": "Vùng đất trống trải, bờ biển không có chướng ngại vật"},
    "B": {"name": "Địa hình B", "desc": "Vùng tương đối trống trải có chướng ngại vật thưa (ngoại ô, làng mạc)"},
    "C": {"name": "Địa hình C", "desc": "Khu vực đô thị có các công trình xây dựng san sát (nội thành)"}
}

# ==============================================================================
# 6. QUY ĐỊNH THỜI GIAN THÁO DỠ VÁN KHUÔN (TCVN 4453:1995)
# ==============================================================================
FORMWORK_REMOVAL_RULES = [
    {"type": "Bản sàn nhịp L <= 2m", "min_percent": "50% R28", "days_summer": "3 - 4 ngày", "days_winter": "5 - 7 ngày"},
    {"type": "Bản sàn nhịp 2m < L <= 8m", "min_percent": "70% R28", "days_summer": "7 - 10 ngày", "days_winter": "10 - 14 ngày"},
    {"type": "Dầm, vòm nhịp L <= 8m", "min_percent": "70% R28", "days_summer": "7 - 10 ngày", "days_winter": "10 - 14 ngày"},
    {"type": "Dầm, vòm nhịp L > 8m", "min_percent": "90% R28", "days_summer": "21 - 28 ngày", "days_winter": "28 - 35 ngày"},
    {"type": "Cấu kiện công xôn (Console)", "min_percent": "100% R28", "days_summer": "21 - 28 ngày", "days_winter": "28 ngày"},
    {"type": "Cốp pha thành đứng (Cột, dầm, tường)", "min_percent": "Chịu lực bản thân (>5 MPa)", "days_summer": "1 - 2 ngày", "days_winter": "2 - 3 ngày"}
]
