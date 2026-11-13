"""
Module: calculations.py
Mục đích: Tính toán kết cấu bê tông cốt thép theo TCVN 5574:2018.
Chức năng: Sơ bộ tiết diện dầm, tính toán nội lực M, tính diện tích cốt thép As, kiểm tra hàm lượng mu%,
gợi ý chọn thép thực tế và xuất bản vẽ hình học mặt cắt dầm SVG tương tác trực quan.
"""

import math
from typing import Dict, Any, Tuple, List
from data_tcvn import (
    CONCRETE_DATABASE,
    REBAR_DATABASE,
    REBAR_DIAMETERS,
    REBAR_AREA_TABLE,
    calculate_xi_R,
    calculate_alpha_R
)

def recommend_beam_section(L_m: float, beam_type: str = "main") -> Dict[str, Any]:
    """
    Hàm chọn sơ bộ kích thước tiết diện dầm b x h dựa trên nhịp L (m)
    - Dầm chính: h = (1/12 ÷ 1/8) * L
    - Dầm phụ: h = (1/16 ÷ 1/12) * L
    - Dầm console: h = (1/6 ÷ 1/4) * L
    - Bề rộng b = (0.3 ÷ 0.5) * h, làm tròn chuẩn ván khuôn (150, 200, 220, 250, 300, 350, 400 mm)
    """
    L_mm = L_m * 1000.0
    
    if beam_type == "console":
        h_min = L_mm / 6.0
        h_max = L_mm / 4.0
    elif beam_type == "secondary":
        h_min = L_mm / 16.0
        h_max = L_mm / 12.0
    else:  # main beam
        h_min = L_mm / 12.0
        h_max = L_mm / 8.0
        
    h_target = (h_min + h_max) / 2.0
    h_rec = int(math.ceil(h_target / 50.0) * 50)
    if h_rec < 200:
        h_rec = 200

    b_target = 0.4 * h_rec
    standard_b = [150, 200, 220, 250, 300, 350, 400]
    b_rec = min(standard_b, key=lambda x: abs(x - b_target))
    
    return {
        "L_m": L_m,
        "beam_type": beam_type,
        "h_range_mm": (int(h_min), int(h_max)),
        "h_rec_mm": h_rec,
        "b_rec_mm": b_rec,
        "section_str": f"{b_rec} x {h_rec} mm"
    }

def suggest_rebar_combinations(As_req: float, b_mm: int, max_layers: int = 2) -> List[Dict[str, Any]]:
    """Gợi ý phương án chọn thanh thép thực tế tối ưu"""
    suggestions = []
    
    for d in [14, 16, 18, 20, 22, 25]:
        for n in range(2, 6):
            area = REBAR_AREA_TABLE[d][n - 1]
            if area >= As_req and (area - As_req) / As_req <= 0.20:
                diff_pct = round(((area - As_req) / As_req) * 100, 1)
                suggestions.append({
                    "description": f"{n}Ф{d}",
                    "total_area": area,
                    "diff_pct": diff_pct,
                    "bars_count": n,
                    "diameters": [d]
                })
                
    combo_pairs = [(18, 16), (20, 18), (22, 20), (25, 22)]
    for d1, d2 in combo_pairs:
        area_d1 = REBAR_AREA_TABLE[d1][0]
        area_d2 = REBAR_AREA_TABLE[d2][0]
        for n1 in [2, 3]:
            for n2 in [1, 2]:
                area = round(n1 * area_d1 + n2 * area_d2, 1)
                if area >= As_req and (area - As_req) / As_req <= 0.15:
                    diff_pct = round(((area - As_req) / As_req) * 100, 1)
                    suggestions.append({
                        "description": f"{n1}Ф{d1} + {n2}Ф{d2}",
                        "total_area": area,
                        "diff_pct": diff_pct,
                        "bars_count": n1 + n2,
                        "diameters": [d1, d2]
                    })
                    
    suggestions.sort(key=lambda x: (x["diff_pct"], x["bars_count"]))
    return suggestions[:4]

def generate_beam_cross_section_svg(
    b_mm: int,
    h_mm: int,
    a_mm: int,
    rebar_desc: str,
    xi: float,
    alpha_m: float
) -> str:
    """
    Sinh mã SVG chất lượng cao vẽ mặt cắt dầm bê tông cốt thép chuẩn kỹ thuật công trình.
    Hiển thị: Vùng nén bê tông màu hổ phách/đỏ, đường trục trung hòa, cốt đai, thép chủ phát sáng, kích thước b x h.
    """
    canvas_w, canvas_h = 420, 480
    pad_x, pad_y = 75, 45
    draw_w, draw_h = 270, 370
    
    scale_y = draw_h / max(h_mm, 300)
    scale_x = scale_y * (b_mm / h_mm) if h_mm > 0 else 1.0
    
    # Giới hạn chiều rộng vẽ
    beam_w = max(110.0, min(draw_w, 240.0 * (b_mm / max(h_mm, 200))))
    beam_h = draw_h
    start_x = pad_x + (draw_w - beam_w) / 2.0
    start_y = pad_y
    
    # Chiều cao vùng nén x = xi * h0
    h0 = h_mm - a_mm
    comp_x_mm = min(xi * h0, float(h_mm))
    comp_h_px = comp_x_mm * (beam_h / h_mm) if h_mm > 0 else 40.0
    
    # Đọc số thanh thép từ rebar_desc (ví dụ: '3Ф18' -> 3 thanh)
    n_bars = 3
    rebar_label = rebar_desc
    try:
        if "Ф" in rebar_desc:
            parts = rebar_desc.split("Ф")
            n_bars = int(parts[0].replace("+", "").strip().split()[-1])
        elif "phi" in rebar_desc.lower():
            n_bars = int(rebar_desc.lower().split("phi")[0].strip())
    except Exception:
        n_bars = 3
    n_bars = max(2, min(n_bars, 5))
    
    # Tọa độ các thanh thép chủ lớp dưới
    cover_px = 18.0
    stirrup_x = start_x + 10.0
    stirrup_y = start_y + 10.0
    stirrup_w = beam_w - 20.0
    stirrup_h = beam_h - 20.0
    
    rebar_y = (start_y + beam_h) - cover_px
    bar_positions = []
    if n_bars == 2:
        bar_positions = [stirrup_x + 10.0, stirrup_x + stirrup_w - 10.0]
    elif n_bars == 3:
        bar_positions = [stirrup_x + 10.0, stirrup_x + stirrup_w / 2.0, stirrup_x + stirrup_w - 10.0]
    elif n_bars == 4:
        step = (stirrup_w - 20.0) / 3.0
        bar_positions = [stirrup_x + 10.0 + i * step for i in range(4)]
    else:
        step = (stirrup_w - 20.0) / (n_bars - 1)
        bar_positions = [stirrup_x + 10.0 + i * step for i in range(n_bars)]

    # Tạo các thẻ SVG cho thép chủ
    rebar_svg = ""
    for bx in bar_positions:
        rebar_svg += f"""
        <circle cx="{bx:.1f}" cy="{rebar_y:.1f}" r="8.5" fill="#F59E0B" stroke="#FDE68A" stroke-width="2" filter="url(#glow)"/>
        <circle cx="{bx:.1f}" cy="{rebar_y:.1f}" r="3" fill="#FFFBEB"/>
        """
        
    # Thép cấu tạo lớp trên (2 thanh Ф12 làm giá đỡ cốt đai)
    top_y = stirrup_y + 10.0
    top_bar_1 = stirrup_x + 10.0
    top_bar_2 = stirrup_x + stirrup_w - 10.0
    top_rebar_svg = f"""
    <circle cx="{top_bar_1:.1f}" cy="{top_y:.1f}" r="5.5" fill="#60A5FA" stroke="#93C5FD" stroke-width="1.5"/>
    <circle cx="{top_bar_2:.1f}" cy="{top_y:.1f}" r="5.5" fill="#60A5FA" stroke="#93C5FD" stroke-width="1.5"/>
    """

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="100%" height="380" style="background: #0B1120; border-radius: 12px; border: 1px solid rgba(245, 158, 11, 0.25); box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);">
      <defs>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="3" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <linearGradient id="concreteGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1E293B" />
          <stop offset="100%" stop-color="#0F172A" />
        </linearGradient>
        <linearGradient id="compGrad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="rgba(239, 68, 68, 0.45)" />
          <stop offset="100%" stop-color="rgba(239, 68, 68, 0.15)" />
        </linearGradient>
        <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
          <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(255, 255, 255, 0.04)" stroke-width="1"/>
        </pattern>
      </defs>

      <!-- Nền lưới Blueprint kỹ thuật -->
      <rect width="100%" height="100%" fill="url(#grid)" />

      <!-- Tiêu đề bản vẽ -->
      <text x="20" y="28" fill="#F8FAFC" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" letter-spacing="1">MẶT CẮT KẾT CẤU DẦM (BIM SECTION)</text>
      <text x="{canvas_w - 20}" y="28" fill="#F59E0B" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="600" text-anchor="end">b x h = {b_mm} x {h_mm} mm</text>

      <!-- Khối bê tông dầm -->
      <rect x="{start_x:.1f}" y="{start_y:.1f}" width="{beam_w:.1f}" height="{beam_h:.1f}" fill="url(#concreteGrad)" stroke="#38BDF8" stroke-width="2" rx="3" />

      <!-- Vùng nén bê tông x (màu đỏ gạch chịu nén) -->
      <rect x="{start_x:.1f}" y="{start_y:.1f}" width="{beam_w:.1f}" height="{comp_h_px:.1f}" fill="url(#compGrad)" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="4,2" />
      <text x="{start_x + beam_w/2:.1f}" y="{start_y + comp_h_px/2 + 4:.1f}" fill="#FCA5A5" font-family="sans-serif" font-size="11" font-weight="600" text-anchor="middle">VÙNG NÉN BÊ TÔNG (x = {comp_x_mm:.1f} mm)</text>

      <!-- Đường trục trung hòa Neutral Axis -->
      <line x1="{start_x - 15:.1f}" y1="{start_y + comp_h_px:.1f}" x2="{start_x + beam_w + 15:.1f}" y2="{start_y + comp_h_px:.1f}" stroke="#F43F5E" stroke-width="1.8" stroke-dasharray="6,3" />
      <text x="{start_x + beam_w + 18:.1f}" y="{start_y + comp_h_px + 4:.1f}" fill="#F43F5E" font-family="sans-serif" font-size="10" font-weight="700">T.T.H</text>

      <!-- Cốt đai (Stirrups) bo góc -->
      <rect x="{stirrup_x:.1f}" y="{stirrup_y:.1f}" width="{stirrup_w:.1f}" height="{stirrup_h:.1f}" fill="none" stroke="#94A3B8" stroke-width="2" rx="4" />
      <text x="{stirrup_x + 6:.1f}" y="{start_y + beam_h/2:.1f}" fill="#94A3B8" font-family="sans-serif" font-size="9" transform="rotate(-90 {stirrup_x + 6:.1f} {start_y + beam_h/2:.1f})">Cốt đai Ф6-Ф8</text>

      <!-- Thép cấu tạo lớp trên -->
      {top_rebar_svg}
      <text x="{top_bar_2 + 15:.1f}" y="{top_y + 4:.1f}" fill="#93C5FD" font-family="sans-serif" font-size="10">2Ф12 (Thép giá)</text>

      <!-- Thép chủ lớp dưới (Chịu kéo As) -->
      {rebar_svg}
      <line x1="{stirrup_x + stirrup_w/2:.1f}" y1="{rebar_y + 12:.1f}" x2="{stirrup_x + stirrup_w/2:.1f}" y2="{rebar_y + 26:.1f}" stroke="#F59E0B" stroke-width="1.5"/>
      <text x="{stirrup_x + stirrup_w/2:.1f}" y="{rebar_y + 38:.1f}" fill="#FDE68A" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Thép chủ: {rebar_label}</text>

      <!-- Kích thước b (ngang phía trên) -->
      <line x1="{start_x:.1f}" y1="{start_y - 12:.1f}" x2="{start_x + beam_w:.1f}" y2="{start_y - 12:.1f}" stroke="#38BDF8" stroke-width="1.2" />
      <line x1="{start_x:.1f}" y1="{start_y - 16:.1f}" x2="{start_x:.1f}" y2="{start_y - 8:.1f}" stroke="#38BDF8" stroke-width="1.2" />
      <line x1="{start_x + beam_w:.1f}" y1="{start_y - 16:.1f}" x2="{start_x + beam_w:.1f}" y2="{start_y - 8:.1f}" stroke="#38BDF8" stroke-width="1.2" />
      <text x="{start_x + beam_w/2:.1f}" y="{start_y - 17:.1f}" fill="#38BDF8" font-family="sans-serif" font-size="11" font-weight="600" text-anchor="middle">b = {b_mm} mm</text>

      <!-- Kích thước h (dọc bên trái) -->
      <line x1="{start_x - 18:.1f}" y1="{start_y:.1f}" x2="{start_x - 18:.1f}" y2="{start_y + beam_h:.1f}" stroke="#38BDF8" stroke-width="1.2" />
      <line x1="{start_x - 22:.1f}" y1="{start_y:.1f}" x2="{start_x - 14:.1f}" y2="{start_y:.1f}" stroke="#38BDF8" stroke-width="1.2" />
      <line x1="{start_x - 22:.1f}" y1="{start_y + beam_h:.1f}" x2="{start_x - 14:.1f}" y2="{start_y + beam_h:.1f}" stroke="#38BDF8" stroke-width="1.2" />
      <text x="{start_x - 24:.1f}" y="{start_y + beam_h/2:.1f}" fill="#38BDF8" font-family="sans-serif" font-size="11" font-weight="600" text-anchor="middle" transform="rotate(-90 {start_x - 24:.1f} {start_y + beam_h/2:.1f})">h = {h_mm} mm</text>

      <!-- Thông số chân bản vẽ -->
      <rect x="20" y="{canvas_h - 35}" width="{canvas_w - 40}" height="24" rx="4" fill="rgba(30, 41, 59, 0.7)" />
      <text x="30" y="{canvas_h - 19}" fill="#94A3B8" font-family="sans-serif" font-size="10">αm = {alpha_m:.3f} | ξ = {xi:.3f} | a = {a_mm}mm | Lớp bảo vệ c ≥ 25mm</text>
    </svg>
    """
    return svg

def calculate_beam_reinforcement(
    L_m: float,
    q_kNm: float,
    b_mm: int,
    h_mm: int,
    concrete_grade: str = "B20",
    steel_grade: str = "CB300-V",
    a_mm: int = 35
) -> Dict[str, Any]:
    concrete = CONCRETE_DATABASE.get(concrete_grade, CONCRETE_DATABASE["B20"])
    steel = REBAR_DATABASE.get(steel_grade, REBAR_DATABASE["CB300-V"])
    
    Rb = concrete["Rb"]
    Rbt = concrete["Rbt"]
    Rs = steel["Rs"]
    Es = steel["Es"] * 1.0e5
    
    h0 = h_mm - a_mm
    if h0 <= 0:
        return {
            "status": "ERROR",
            "message": "Chiều cao làm việc h0 <= 0! Lớp bảo vệ a quá lớn so với chiều cao h."
        }
        
    M_kNm = (q_kNm * (L_m ** 2)) / 8.0
    M_Nmm = M_kNm * 1.0e6
    
    denom = Rb * b_mm * (h0 ** 2)
    alpha_m = M_Nmm / denom
    
    xi_R = calculate_xi_R(Rs=Rs, Es=Es)
    alpha_R = calculate_alpha_R(xi_R)
    
    status = "OK"
    warning = ""
    is_safe = True
    
    if alpha_m > 0.5:
        status = "CRITICAL_OVERLOAD"
        is_safe = False
        warning = (
            f"Alpha_m = {alpha_m:.3f} > 0.5 (Vượt quá giới hạn chịu lực đơn cực đại)! "
            "Tiết diện dầm quá nhỏ hoặc tải trọng quá lớn, bê tông vùng nén bị phá hoại giòn. "
            "BẮT BUỘC phải tăng chiều cao h, mở rộng b hoặc nâng cấp bê tông!"
        )
        xi = 0.5
        As_calc = (xi * Rb * b_mm * h0) / Rs
    elif alpha_m > alpha_R:
        status = "WARNING_COMPRESSIVE_REBAR_NEEDED"
        is_safe = False
        warning = (
            f"Alpha_m ({alpha_m:.3f}) > Alpha_R ({alpha_R:.3f})! "
            "Cần bố trí cốt thép kép (đặt thêm cốt thép vùng nén A's) hoặc tăng kích thước tiết diện dầm."
        )
        xi = 1.0 - math.sqrt(max(0.0, 1.0 - 2.0 * min(alpha_m, 0.499)))
        As_calc = (xi * Rb * b_mm * h0) / Rs
    else:
        xi = 1.0 - math.sqrt(1.0 - 2.0 * alpha_m)
        As_calc = (xi * Rb * b_mm * h0) / Rs
        
    mu_calc = (As_calc / (b_mm * h0)) * 100.0
    mu_min = 0.1
    mu_max_rec = 2.0
    mu_min_rec = 0.8
    
    adjusted_by_mumin = False
    if mu_calc < mu_min:
        As_req = (mu_min / 100.0) * b_mm * h0
        mu_actual = mu_min
        adjusted_by_mumin = True
        warning = f"Hàm lượng tính toán ({mu_calc:.2f}%) < mu_min (0.1%). Tự động chọn theo cấu tạo tối thiểu As = {As_req:.1f} mm²."
    else:
        As_req = As_calc
        mu_actual = mu_calc

    if mu_actual < mu_min_rec:
        economy_eval = "Hàm lượng thép hơi thưa (lãng phí bê tông, có thể giảm tiết diện dầm để tiết kiệm chi phí)."
    elif mu_actual <= mu_max_rec:
        economy_eval = "Hàm lượng thép hợp lý, đạt hiệu quả kinh tế - kỹ thuật tối ưu (0.8% - 2.0%)."
    else:
        economy_eval = "Hàm lượng thép quá dày (> 2.0%), khó đổ bê tông và kém kinh tế. Khuyên tăng h dầm."

    suggestions = suggest_rebar_combinations(As_req, b_mm)
    chosen_rebar_str = suggestions[0]["description"] if suggestions else "3Ф18"

    # Sinh mã bản vẽ SVG mặt cắt
    svg_drawing = generate_beam_cross_section_svg(
        b_mm=b_mm,
        h_mm=h_mm,
        a_mm=a_mm,
        rebar_desc=chosen_rebar_str,
        xi=xi,
        alpha_m=alpha_m
    )

    return {
        "status": status,
        "is_safe": is_safe,
        "warning": warning,
        "inputs": {
            "L_m": L_m,
            "q_kNm": q_kNm,
            "b_mm": b_mm,
            "h_mm": h_mm,
            "h0_mm": h0,
            "a_mm": a_mm,
            "concrete_grade": concrete_grade,
            "steel_grade": steel_grade,
            "Rb": Rb,
            "Rbt": Rbt,
            "Rs": Rs
        },
        "results": {
            "M_max_kNm": round(M_kNm, 2),
            "alpha_m": round(alpha_m, 4),
            "xi": round(xi, 4),
            "xi_R": round(xi_R, 3),
            "alpha_R": round(alpha_R, 3),
            "As_calc_mm2": round(As_calc, 1),
            "As_req_mm2": round(As_req, 1),
            "mu_pct": round(mu_actual, 2),
            "mu_min_pct": mu_min,
            "adjusted_by_mumin": adjusted_by_mumin,
            "economy_eval": economy_eval,
            "rebar_suggestions": suggestions,
            "chosen_rebar_str": chosen_rebar_str,
            "svg_drawing": svg_drawing
        }
    }
