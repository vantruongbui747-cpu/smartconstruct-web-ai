"""
Module: engines/structural_engine.py
Mục đích: Lõi tính toán kết cấu bê tông cốt thép (Bản sàn, Dầm chữ nhật, Cột chịu nén lệch tâm) theo TCVN 5574:2018.
"""

import math
from typing import Dict, Any, List, Tuple
from config_data import CONCRETE_DB, REBAR_DB, REBAR_AREA

# ==============================================================================
# 1.1 TÍNH TOÁN BẢN SÀN BÊ TÔNG CỐT THÉP (SLAB DESIGN)
# ==============================================================================
def calculate_slab(
    L1_m: float,
    L2_m: float,
    gs_kNm2: float,
    ps_kNm2: float,
    concrete_name: str = "B25",
    rebar_name: str = "CB240-T",
    d_rebar_mm: int = 8
) -> Dict[str, Any]:
    """
    Tính toán bản sàn theo TCVN 5574:2018:
    - Phân loại bản 1 phương (bản loại dầm) hay bản 2 phương (bản kê 4 cạnh)
    - Sơ bộ chiều dày bản hs
    - Tính mô-men uốn và diện tích cốt thép As trên 1m bề rộng sàn
    """
    concrete = CONCRETE_DB.get(concrete_name, CONCRETE_DB["B25"])
    rebar = REBAR_DB.get(rebar_name, REBAR_DB["CB240-T"])
    
    Rb = concrete["Rb"]
    Rs = rebar["Rs"]
    xi_R = rebar["xi_R"]
    alpha_R = xi_R * (1.0 - 0.5 * xi_R)
    
    L_short = min(L1_m, L2_m)
    L_long = max(L1_m, L2_m)
    ratio_alpha = round(L_long / L_short, 2)
    
    qs_total = gs_kNm2 + ps_kNm2 # kN/m2 (trên dải bản b = 1000mm)
    b_slab = 1000.0 # mm
    
    if ratio_alpha > 2.0:
        slab_type = "Bản loại dầm (Làm việc 1 phương theo cạnh ngắn L1)"
        hs_raw = (L_short * 1000.0) / 32.0 # Trung bình (1/35 ÷ 1/30)
        hs_mm = max(80, int(math.ceil(hs_raw / 10.0) * 10))
        
        # Mô-men trên 1m bề rộng dải bản
        M_bien_kNm = (qs_total * (L_short ** 2)) / 11.0
        M_giua_kNm = (qs_total * (L_short ** 2)) / 16.0
    else:
        slab_type = "Bản kê 4 cạnh (Làm việc 2 phương)"
        hs_raw = (L_short * 1000.0) / 42.5 # Trung bình (1/45 ÷ 1/40)
        hs_mm = max(80, int(math.ceil(hs_raw / 10.0) * 10))
        
        # Mô-men tính toán dải bản
        M_bien_kNm = (qs_total * (L_short ** 2)) / 14.0
        M_giua_kNm = (qs_total * (L_short ** 2)) / 18.0
        
    a_slab = 20.0 # Lớp bảo vệ + bán kính thanh (mm)
    h0_slab = hs_mm - a_slab
    
    # Tính thép cho mô men lớn nhất (nhịp biên M_bien)
    denom = Rb * b_slab * (h0_slab ** 2)
    alpha_m = (M_bien_kNm * 1.0e6) / denom if denom > 0 else 0.0
    
    if alpha_m > alpha_R or alpha_m >= 0.5:
        xi = 0.5
        status = "WARNING_OVERLOAD"
    else:
        xi = 1.0 - math.sqrt(max(0.0, 1.0 - 2.0 * alpha_m))
        status = "OK"
        
    As_req = (xi * Rb * b_slab * h0_slab) / Rs
    # Kiểm tra hàm lượng tối thiểu 0.1%
    mu_min = 0.1
    As_min = (mu_min / 100.0) * b_slab * h0_slab
    As_final = max(As_req, As_min)
    
    # Tính bước thép s (mm)
    As1 = REBAR_AREA.get(d_rebar_mm, 50.3)
    s_calc = (As1 * 1000.0) / As_final if As_final > 0 else 200.0
    s_standard = [100, 120, 150, 180, 200]
    s_chosen = min(s_standard, key=lambda x: abs(x - s_calc) if x <= s_calc else 999)
    if s_chosen == 999:
        s_chosen = 100
        
    return {
        "ratio_alpha": ratio_alpha,
        "slab_type": slab_type,
        "hs_recommended_mm": hs_mm,
        "qs_total_kNm2": round(qs_total, 2),
        "M_bien_kNm": round(M_bien_kNm, 2),
        "M_giua_kNm": round(M_giua_kNm, 2),
        "alpha_m": round(alpha_m, 4),
        "As_req_mm2": round(As_final, 1),
        "selected_rebar": f"Ф{d_rebar_mm}a{s_chosen}",
        "actual_As_mm2": round((As1 * 1000.0) / s_chosen, 1),
        "status": status
    }

# ==============================================================================
# 1.2 TÍNH TOÁN DẦM CHỮ NHẬT CHỊU UỐN & CẮT (BEAM DESIGN)
# ==============================================================================
def calculate_beam(
    L_m: float,
    b_mm: int,
    h_mm: int,
    M_kNm: float,
    Q_kN: float = 0.0,
    a_mm: int = 35,
    concrete_name: str = "B25",
    rebar_name: str = "CB400-V",
    d_chosen_mm: int = 18
) -> Dict[str, Any]:
    """
    Tính toán dầm chữ nhật chịu uốn theo TCVN 5574:2018:
    - Tính alpha_m, kiểm tra alpha_R
    - Tính As_yc, hàm lượng mu%
    - Tự động chọn số thanh thép n_thanh = ceil(As_yc / As1)
    """
    concrete = CONCRETE_DB.get(concrete_name, CONCRETE_DB["B25"])
    rebar = REBAR_DB.get(rebar_name, REBAR_DB["CB400-V"])
    
    Rb = concrete["Rb"]
    Rbt = concrete["Rbt"]
    Rs = rebar["Rs"]
    Rsw = rebar.get("Rsw", 280)
    xi_R = rebar["xi_R"]
    alpha_R = xi_R * (1.0 - 0.5 * xi_R)
    
    h0 = h_mm - a_mm
    if h0 <= 0:
        return {"status": "ERROR", "message": "Chiều cao làm việc h0 <= 0"}
        
    denom = Rb * b_mm * (h0 ** 2)
    alpha_m = (M_kNm * 1.0e6) / denom
    
    status = "OK"
    warning = ""
    
    if alpha_m > 0.5:
        status = "CRITICAL_OVERLOAD"
        warning = f"Alpha_m ({alpha_m:.3f}) > 0.5: Phá hoại giòn bê tông vùng nén! Phải tăng tiết diện b x h!"
        xi = 0.5
        As_calc = (xi * Rb * b_mm * h0) / Rs
    elif alpha_m > alpha_R:
        status = "WARNING_OVER_REINFORCED"
        warning = f"Alpha_m ({alpha_m:.3f}) > Alpha_R ({alpha_R:.3f}): Cần đặt cốt kép hoặc tăng chiều cao h dầm!"
        xi = 1.0 - math.sqrt(max(0.0, 1.0 - 2.0 * min(alpha_m, 0.499)))
        As_calc = (xi * Rb * b_mm * h0) / Rs
    else:
        xi = 1.0 - math.sqrt(1.0 - 2.0 * alpha_m)
        As_calc = (xi * Rb * b_mm * h0) / Rs
        
    # Hàm lượng mu
    mu_calc = (As_calc / (b_mm * h0)) * 100.0
    mu_min = 0.1
    if mu_calc < mu_min:
        As_req = (mu_min / 100.0) * b_mm * h0
        mu_actual = mu_min
        warning = f"Hàm lượng tính toán ({mu_calc:.2f}%) < 0.1%. Tự động chọn theo As_min = {As_req:.1f} mm²."
    else:
        As_req = As_calc
        mu_actual = mu_calc
        
    # Chọn số thanh thép
    As1 = REBAR_AREA.get(d_chosen_mm, 254.5)
    n_bars = max(2, int(math.ceil(As_req / As1)))
    As_chosen = round(n_bars * As1, 1)
    
    # Kiểm tra sơ bộ lực cắt Q (bê tông có đủ chịu cắt không)
    # Qb_min = 0.5 * Rbt * b * h0 (N)
    Qb_kN = (0.5 * Rbt * b_mm * h0) / 1000.0
    if Q_kN > 0:
        shear_check = "Đạt (Cốt đai đặt theo cấu tạo)" if Q_kN <= Qb_kN else "Cần tính toán cốt đai chịu cắt theo TCVN 5574"
    else:
        shear_check = "Chưa nhập Q (Đặt đai cấu tạo Ф6-Ф8 a100/a150)"

    return {
        "status": status,
        "warning": warning,
        "b_mm": b_mm,
        "h_mm": h_mm,
        "h0_mm": h0,
        "M_kNm": M_kNm,
        "alpha_m": round(alpha_m, 4),
        "alpha_R": round(alpha_R, 3),
        "xi": round(xi, 4),
        "As_req_mm2": round(As_req, 1),
        "mu_pct": round(mu_actual, 2),
        "d_chosen_mm": d_chosen_mm,
        "n_bars": n_bars,
        "As_chosen_mm2": As_chosen,
        "selected_rebar_str": f"{n_bars}Ф{d_chosen_mm}",
        "shear_check": shear_check
    }

# ==============================================================================
# 1.3 CỘT CHỊU NÉN LỆCH TÂM & TÍNH BIỂU ĐỒ TƯƠNG TÁC P-M (COLUMN ANALYSIS)
# ==============================================================================
def calculate_column(
    b_mm: int,
    h_mm: int,
    L0_mm: float,
    N_kN: float,
    M_kNm: float,
    concrete_name: str = "B25",
    rebar_name: str = "CB400-V",
    a_mm: int = 40
) -> Dict[str, Any]:
    """
    Tính toán cột chịu nén lệch tâm phẳng & tạo dữ liệu Biểu đồ tương tác P-M:
    - Độ lệch tâm tĩnh học e1 = M / N
    - Độ lệch tâm ngẫu nhiên ea = max(L0/600, h/30, 10)
    - Hệ số uốn dọc eta
    - Tọa độ các điểm đường bao tương tác P - M
    """
    concrete = CONCRETE_DB.get(concrete_name, CONCRETE_DB["B25"])
    rebar = REBAR_DB.get(rebar_name, REBAR_DB["CB400-V"])
    
    Rb = concrete["Rb"]
    Rs = rebar["Rs"]
    Rsc = rebar.get("Rsc", 350)
    
    # 1. Độ lệch tâm
    e1_mm = (M_kNm * 1.0e3) / N_kN if N_kN > 0 else 0.0
    ea_mm = max(L0_mm / 600.0, h_mm / 30.0, 10.0)
    e0_mm = e1_mm + ea_mm
    
    # 2. Chiều dài tính toán và độ mảnh lambda
    i_radius = 0.288 * h_mm # Bán kính quán tính tiết diện chữ nhật
    slenderness = L0_mm / i_radius if i_radius > 0 else 0.0
    
    # Hệ số uốn dọc eta (gần đúng cho cột nhà dân dụng)
    if slenderness <= 14:
        eta = 1.0
    else:
        eta = round(1.0 + (slenderness / 100.0) ** 1.5, 3)
        
    e_calc_mm = eta * e0_mm
    
    # 3. Tính điểm giới hạn chịu nén đúng tâm P0 và uốn thuần túy M0
    # Giả định bố trí thép đối xứng 2% tiết diện
    Ast = 0.02 * b_mm * h_mm
    h0 = h_mm - a_mm
    
    P_max_kN = round((Rb * b_mm * h_mm + Rsc * Ast) / 1000.0, 1) # Nén đúng tâm
    P_bal_kN = round((0.4 * Rb * b_mm * h0) / 1000.0, 1)         # Điểm phá hoại cân bằng
    M_bal_kNm = round((0.15 * Rb * b_mm * (h0 ** 2)) / 1.0e6, 1)
    M_max_kNm = round((Rs * (Ast / 2.0) * (h0 - a_mm)) / 1.0e6, 1) # Uốn thuần túy
    
    # Sinh dữ liệu đường bao P-M tương tác
    pm_curve_p = [P_max_kN, P_max_kN * 0.85, P_bal_kN, P_bal_kN * 0.5, 0.0]
    pm_curve_m = [0.0, M_bal_kNm * 0.65, M_bal_kNm, M_max_kNm * 1.1, M_max_kNm]
    
    # Kiểm tra an toàn của điểm (M, N)
    is_safe = (N_kN <= P_max_kN) and (M_kNm <= M_bal_kNm * 1.2)
    
    return {
        "b_mm": b_mm,
        "h_mm": h_mm,
        "L0_mm": L0_mm,
        "N_kN": N_kN,
        "M_kNm": M_kNm,
        "e1_mm": round(e1_mm, 1),
        "ea_mm": round(ea_mm, 1),
        "e0_mm": round(e0_mm, 1),
        "slenderness": round(slenderness, 1),
        "eta": eta,
        "e_calc_mm": round(e_calc_mm, 1),
        "P_max_kN": P_max_kN,
        "is_safe": is_safe,
        "pm_curve": {
            "P": pm_curve_p,
            "M": pm_curve_m,
            "point_P": N_kN,
            "point_M": M_kNm
        }
    }
