"""
Module: engines/construction_boq.py
Mục đích:
- Tính định mức cấp phối vật liệu bê tông cho V m3 & Tra cứu tháo dỡ ván khuôn (TCVN 4453:1995)
- Bóc tách khối lượng cốt thép & Thống kê thép tự động (Auto-BOQ) xuất Excel
"""

import math
import io
import pandas as pd
from typing import Dict, Any, List
from config_data import MIX_PROPORTION_DB, FORMWORK_REMOVAL_RULES, REBAR_AREA

# ==============================================================================
# 5.1 TÍNH ĐỊNH MỨC CẤP PHỐI VẬT TƯ CHO V m3 BÊ TÔNG
# ==============================================================================
def calculate_concrete_mix(
    volume_m3: float,
    grade_name: str = "B25 (M300)"
) -> Dict[str, Any]:
    """
    Tính tổng khối lượng vật tư xi măng, cát, đá, nước cho V m3 bê tông:
    - Quy đổi xi măng ra số bao 50kg
    - Hiển thị quy định tháo dỡ cốp pha theo TCVN 4453:1995
    """
    mix = MIX_PROPORTION_DB.get(grade_name, MIX_PROPORTION_DB["B25 (M300)"])
    
    total_cement_kg = round(volume_m3 * mix["cement_kg"], 1)
    total_cement_bags = math.ceil(total_cement_kg / 50.0)
    total_sand_m3 = round(volume_m3 * mix["sand_m3"], 2)
    total_stone_m3 = round(volume_m3 * mix["stone_m3"], 2)
    total_water_lit = round(volume_m3 * mix["water_lit"], 0)
    
    materials_summary = pd.DataFrame([
        {"Vật tư": "Xi măng PCB40", "Định mức 1m3": f"{mix['cement_kg']} kg", "Tổng nhu cầu": f"{total_cement_kg} kg", "Quy đổi thực tế": f"{total_cement_bags} bao (50kg)"},
        {"Vật tư": "Cát vàng", "Định mức 1m3": f"{mix['sand_m3']} m3", "Tổng nhu cầu": f"{total_sand_m3} m3", "Quy đổi thực tế": f"{total_sand_m3} m3"},
        {"Vật tư": "Đá 1x2", "Định mức 1m3": f"{mix['stone_m3']} m3", "Tổng nhu cầu": f"{total_stone_m3} m3", "Quy đổi thực tế": f"{total_stone_m3} m3"},
        {"Vật tư": "Nước sạch", "Định mức 1m3": f"{mix['water_lit']} lít", "Tổng nhu cầu": f"{total_water_lit} lít", "Quy đổi thực tế": f"{total_water_lit} lít"}
    ])
    
    df_formwork = pd.DataFrame(FORMWORK_REMOVAL_RULES)
    
    return {
        "volume_m3": volume_m3,
        "grade_name": grade_name,
        "total_cement_kg": total_cement_kg,
        "total_cement_bags": total_cement_bags,
        "total_sand_m3": total_sand_m3,
        "total_stone_m3": total_stone_m3,
        "total_water_lit": total_water_lit,
        "materials_df": materials_summary,
        "formwork_df": df_formwork
    }

# ==============================================================================
# 5.2 BÓC TÁCH KHỐI LƯỢNG & BẢNG THỐNG KÊ CỐT THÉP (AUTO-BOQ)
# ==============================================================================
def calculate_rebar_boq(rebar_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Tính bảng thống kê cốt thép:
    - Trọng lượng đơn vị: g = (pi * d^2 / 4) * 7.85e-3 (kg/m)
    - Tổng chiều dài = n_thanh * chieu_dai
    - Tổng trọng lượng (kg)
    """
    rows = []
    total_weight_all = 0.0
    
    for item in rebar_items:
        comp_name = item.get("component", "Cấu kiện")
        bar_no = item.get("bar_no", "1")
        d_mm = int(item.get("diameter_mm", 18))
        length_m = float(item.get("length_m", 6.0))
        qty = int(item.get("quantity", 3))
        
        # Trọng lượng 1 mét dài: g = (pi * d^2 / 4) * 7.85 * 10^-3 (kg/m)
        unit_weight = round((math.pi * (d_mm ** 2) / 4.0) * 7.85e-3, 3)
        total_len = round(length_m * qty, 2)
        total_weight = round(total_len * unit_weight, 2)
        total_weight_all += total_weight
        
        rows.append({
            "Cấu kiện": comp_name,
            "Số hiệu": bar_no,
            "Đường kính Ф (mm)": d_mm,
            "Chiều dài 1 thanh (m)": length_m,
            "Số lượng (thanh)": qty,
            "Tổng chiều dài (m)": total_len,
            "Trọng lượng đơn vị (kg/m)": unit_weight,
            "Tổng khối lượng (kg)": total_weight
        })
        
    df_boq = pd.DataFrame(rows)
    
    # Xuất ra file Excel bytes
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df_boq.to_excel(writer, index=False, sheet_name="Thong_Ke_Thep")
    excel_bytes = excel_buffer.getvalue()
    
    return {
        "df_boq": df_boq,
        "total_weight_all_kg": round(total_weight_all, 2),
        "total_weight_all_ton": round(total_weight_all / 1000.0, 3),
        "excel_bytes": excel_bytes
    }
