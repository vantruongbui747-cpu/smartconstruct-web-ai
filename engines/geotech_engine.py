"""
Module: engines/geotech_engine.py
Mục đích: Địa kỹ thuật, Cơ học đất & Nền móng công trình:
- Phân tích thí nghiệm đầm chặt đất tiêu chuẩn (Proctor Compaction Curve & Zero-Air-Voids)
- Thiết kế Móng đơn dưới cột bê tông cốt thép theo TCVN 9362:2012 & TCVN 5574:2018
"""

import math
import numpy as np
from typing import Dict, Any, List

# ==============================================================================
# 2.1 XỬ LÝ THÍ NGHIỆM ĐẦM CHẶT ĐẤT TIÊU CHUẨN (PROCTOR COMPACTION CURVE)
# ==============================================================================
def analyze_soil_compaction(
    moisture_list: List[float],
    dry_density_list: List[float],
    specific_gravity: float = 2.68
) -> Dict[str, Any]:
    """
    Xử lý số liệu thí nghiệm đầm chặt:
    - Hồi quy đa thức bậc 2 bằng numpy.polyfit
    - Xác định W_opt (%) và gamma_d_max (g/cm3)
    - Tạo đường bão hòa khí bằng 0 (Zero Air Voids Curve, Sr = 1.0)
    """
    W = np.array(moisture_list, dtype=float)
    gamma_d = np.array(dry_density_list, dtype=float)
    
    # Hồi quy bậc 2: y = a*x^2 + b*x + c
    poly = np.polyfit(W, gamma_d, 2)
    a, b, c = poly[0], poly[1], poly[2]
    
    # Đỉnh parabol (W_opt)
    if a < 0:
        W_opt = -b / (2.0 * a)
        gamma_d_max = a * (W_opt ** 2) + b * W_opt + c
    else:
        # Dự phòng nếu dữ liệu đo bất thường
        idx_max = int(np.argmax(gamma_d))
        W_opt = float(W[idx_max])
        gamma_d_max = float(gamma_d[idx_max])
        
    # Tạo dải điểm mượt cho đường cong đầm chặt
    W_smooth = np.linspace(max(0.0, float(min(W)) - 3.0), float(max(W)) + 3.0, 50)
    gamma_smooth = a * (W_smooth ** 2) + b * W_smooth + c
    
    # Đường bão hòa Sr = 1.0: gamma_zav = (Delta * gamma_w) / (1 + (w * Delta) / 100)
    gamma_w = 1.0 # g/cm3
    gamma_zav = (specific_gravity * gamma_w) / (1.0 + (W_smooth * specific_gravity) / 100.0)
    
    return {
        "W_opt_percent": round(float(W_opt), 2),
        "gamma_d_max": round(float(gamma_d_max), 3),
        "poly_coeffs": [float(a), float(b), float(c)],
        "curve_data": {
            "W_raw": [float(x) for x in W],
            "gamma_raw": [float(y) for y in gamma_d],
            "W_smooth": [round(float(x), 2) for x in W_smooth],
            "gamma_smooth": [round(float(y), 3) for y in gamma_smooth],
            "gamma_zav": [round(float(y), 3) for y in gamma_zav]
        }
    }

# ==============================================================================
# 2.2 THIẾT KẾ MÓNG ĐƠN DƯỚI CỘT BÊ TÔNG CỐT THÉP
# ==============================================================================
def design_isolated_footing(
    N0_tc_kN: float,
    M0_tc_kNm: float,
    Q0_tc_kN: float,
    hm_m: float = 1.5,
    Rtc_kPa: float = 200.0,
    col_b_m: float = 0.25,
    col_h_m: float = 0.35,
    gamma_soil_kN_m3: float = 20.0,
    concrete_grade: str = "B25",
    rebar_grade: str = "CB400-V"
) -> Dict[str, Any]:
    """
    Thiết kế móng đơn nông dưới cột theo TCVN 9362:2012:
    - Sơ bộ diện tích đáy móng Fsb
    - Xác định kích thước Lm x Bm
    - Tính áp lực tiêu chuẩn p_tb, p_max, p_min
    - Kiểm tra điều kiện biến dạng & cường độ nền đất
    - Tính diện tích cốt thép đáy móng Asx, Asy
    """
    # 1. Sơ bộ diện tích đáy móng
    R_net = Rtc_kPa - gamma_soil_kN_m3 * hm_m
    if R_net <= 0:
        R_net = Rtc_kPa * 0.7
    F_sb = (N0_tc_kN * 1.15) / R_net # Hệ số 1.15 kể đến mô men
    
    # Giả định tỷ lệ L/B = 1.2
    B_raw = math.sqrt(F_sb / 1.2)
    Bm_m = max(1.0, round(B_raw * 2.0) / 2.0)
    Lm_m = max(1.0, round((1.2 * Bm_m) * 2.0) / 2.0)
    F_actual = Bm_m * Lm_m
    
    # 2. Tổng tải trọng tiêu chuẩn tại đáy móng
    N_total = N0_tc_kN + gamma_soil_kN_m3 * hm_m * F_actual
    M_total = M0_tc_kNm + Q0_tc_kN * hm_m
    
    # Áp lực tiêu chuẩn đáy móng
    W_m3 = (Bm_m * (Lm_m ** 2)) / 6.0
    p_tb = N_total / F_actual
    p_diff = M_total / W_m3 if W_m3 > 0 else 0.0
    
    p_max = p_tb + p_diff
    p_min = p_tb - p_diff
    
    # 3. Kiểm tra điều kiện bền
    cond_tb = p_tb <= Rtc_kPa
    cond_max = p_max <= 1.2 * Rtc_kPa
    cond_min = p_min >= 0.0
    is_safe = cond_tb and cond_max and cond_min
    
    # 4. Tính cốt thép đáy móng (giả định chiều cao đài móng hm_dai = 0.6m)
    h_dai_m = 0.6
    h0_dai = h_dai_m - 0.05
    Rs = 350.0 if "400" in rebar_grade else 260.0 # MPa
    
    # Ngàm tại mép cột theo phương L
    c_L = (Lm_m - col_h_m) / 2.0
    M_I = (p_max * Bm_m * (c_L ** 2)) / 2.0 # kNm
    As_x = (M_I * 1.0e6) / (0.9 * h0_dai * 1000.0 * Rs) if h0_dai > 0 else 0.0 # mm2
    
    # Ngàm tại mép cột theo phương B
    c_B = (Bm_m - col_b_m) / 2.0
    M_II = (p_tb * Lm_m * (c_B ** 2)) / 2.0
    As_y = (M_II * 1.0e6) / (0.9 * h0_dai * 1000.0 * Rs) if h0_dai > 0 else 0.0 # mm2

    return {
        "Bm_m": Bm_m,
        "Lm_m": Lm_m,
        "F_actual_m2": round(F_actual, 2),
        "p_tb_kPa": round(p_tb, 1),
        "p_max_kPa": round(p_max, 1),
        "p_min_kPa": round(p_min, 1),
        "Rtc_kPa": Rtc_kPa,
        "Rtc_max_kPa": round(1.2 * Rtc_kPa, 1),
        "cond_tb": cond_tb,
        "cond_max": cond_max,
        "cond_min": cond_min,
        "is_safe": is_safe,
        "h_dai_m": h_dai_m,
        "As_x_mm2": round(As_x, 1),
        "As_y_mm2": round(As_y, 1),
        "rebar_x_str": f"Ф14a150 ({math.ceil(As_x / 153.9)} thanh)" if As_x > 0 else "Ф12a150",
        "rebar_y_str": f"Ф14a150 ({math.ceil(As_y / 153.9)} thanh)" if As_y > 0 else "Ф12a150"
    }
