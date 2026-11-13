"""
Module: engines/plotter.py
Mục đích: Module đồ họa chuyên nghiệp cho kỹ sư xây dựng:
- Vẽ mặt cắt dầm bê tông cốt thép bằng Matplotlib (hình chữ nhật, cốt đai, chấm thép đỏ)
- Vẽ Biểu đồ tương tác P - M cột bằng Plotly
- Vẽ Đường cong đầm chặt đất & Đường bão hòa không khí bằng Plotly
- Vẽ Biểu đồ phân bố tải trọng gió theo chiều cao nhà bằng Plotly
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import plotly.graph_objects as go
from typing import Dict, Any

# ==============================================================================
# 1. VẼ MẶT CẮT DẦM CHỮ NHẬT BẰNG MATPLOTLIB
# ==============================================================================
def plot_beam_section_matplotlib(
    b_mm: int,
    h_mm: int,
    a_mm: int,
    n_bars: int,
    d_mm: int
) -> plt.Figure:
    """Vẽ mặt cắt dầm chữ nhật chuẩn kỹ thuật với Matplotlib"""
    fig, ax = plt.subplots(figsize=(4.5, 5.5), facecolor="#0B1120")
    ax.set_facecolor("#0B1120")
    
    # 1. Khối bê tông
    beam_rect = patches.Rectangle(
        (0, 0), b_mm, h_mm,
        linewidth=2.5, edgecolor="#38BDF8", facecolor="#1E293B"
    )
    ax.add_patch(beam_rect)
    
    # 2. Cốt đai bên trong (cách mép 25mm)
    cover = 25.0
    stirrup_w = b_mm - 2 * cover
    stirrup_h = h_mm - 2 * cover
    stirrup_rect = patches.Rectangle(
        (cover, cover), stirrup_w, stirrup_h,
        linewidth=2.0, edgecolor="#94A3B8", facecolor="none", linestyle="-"
    )
    ax.add_patch(stirrup_rect)
    
    # 3. Thép cấu tạo lớp trên (2 thanh Ф12)
    top_y = h_mm - cover - 8.0
    top_x1 = cover + 8.0
    top_x2 = b_mm - cover - 8.0
    ax.add_patch(patches.Circle((top_x1, top_y), 6.0, facecolor="#60A5FA", edgecolor="#93C5FD", linewidth=1.5))
    ax.add_patch(patches.Circle((top_x2, top_y), 6.0, facecolor="#60A5FA", edgecolor="#93C5FD", linewidth=1.5))
    ax.text((top_x1 + top_x2) / 2.0, top_y + 12.0, "2Ф12 (Thép giá)", color="#93C5FD", fontsize=9, ha="center")
    
    # 4. Thép chủ lớp dưới (n_bars thanh Фd màu vàng/đỏ)
    bot_y = cover + 10.0
    r_bar = max(6.0, min(12.0, d_mm / 2.0))
    if n_bars == 2:
        xs = [cover + 10.0, b_mm - cover - 10.0]
    elif n_bars == 3:
        xs = [cover + 10.0, b_mm / 2.0, b_mm - cover - 10.0]
    elif n_bars == 4:
        step = (stirrup_w - 20.0) / 3.0
        xs = [cover + 10.0 + i * step for i in range(4)]
    else:
        step = (stirrup_w - 20.0) / (n_bars - 1)
        xs = [cover + 10.0 + i * step for i in range(n_bars)]
        
    for bx in xs:
        ax.add_patch(patches.Circle((bx, bot_y), r_bar, facecolor="#F59E0B", edgecolor="#FDE68A", linewidth=1.8))
        
    # Ghi chú thép chủ
    ax.text(b_mm / 2.0, bot_y - 22.0, f"Thép chủ: {n_bars}Ф{d_mm}", color="#FDE68A", fontsize=11, fontweight="bold", ha="center")
    
    # Kích thước b và h
    ax.text(b_mm / 2.0, h_mm + 18.0, f"b = {b_mm} mm", color="#38BDF8", fontsize=11, fontweight="bold", ha="center")
    ax.text(-25.0, h_mm / 2.0, f"h = {h_mm} mm", color="#38BDF8", fontsize=11, fontweight="bold", va="center", ha="right", rotation=90)
    
    ax.set_xlim(-60, b_mm + 60)
    ax.set_ylim(-40, h_mm + 50)
    ax.axis("off")
    plt.tight_layout()
    return fig

# ==============================================================================
# 2. VẼ BIỂU ĐỒ TƯƠNG TÁC P - M CỘT BẰNG PLOTLY
# ==============================================================================
def plot_column_interaction_plotly(pm_data: Dict[str, Any]) -> go.Figure:
    """Vẽ đường bao tương tác P - M của cột và điểm làm việc"""
    curve_p = pm_data.get("P", [2000, 1500, 800, 300, 0])
    curve_m = pm_data.get("M", [0, 80, 120, 130, 110])
    pt_p = pm_data.get("point_P", 1200)
    pt_m = pm_data.get("point_M", 85)
    
    fig = go.Figure()
    
    # Đường bao an toàn
    fig.add_trace(go.Scatter(
        x=curve_m, y=curve_p,
        mode="lines+markers",
        name="Đường bao giới hạn [P-M]",
        line=dict(color="#38BDF8", width=3),
        marker=dict(size=8, color="#0284C7"),
        fill="tozerox",
        fillcolor="rgba(56, 189, 248, 0.12)"
    ))
    
    # Điểm làm việc thực tế
    fig.add_trace(go.Scatter(
        x=[pt_m], y=[pt_p],
        mode="markers+text",
        name="Điểm tải trọng thiết kế (M, N)",
        marker=dict(size=14, color="#EF4444", symbol="star"),
        text=[f"  N = {pt_p} kN<br>  M = {pt_m} kNm"],
        textposition="top right",
        textfont=dict(color="#FCA5A5", size=12)
    ))
    
    fig.update_layout(
        title="Biểu đồ tương tác P - M tiết diện Cột",
        xaxis_title="Mô-men uốn M (kN·m)",
        yaxis_title="Lực nén dọc P (kN)",
        template="plotly_dark",
        paper_bgcolor="#0B1120",
        plot_bgcolor="#0F172A",
        font=dict(color="#F8FAFC"),
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(x=0.05, y=0.95)
    )
    return fig

# ==============================================================================
# 3. VẼ ĐƯỜNG CONG ĐẦM CHẶT ĐẤT TIÊU CHUẨN BẰNG PLOTLY
# ==============================================================================
def plot_compaction_curve_plotly(compaction_res: Dict[str, Any]) -> go.Figure:
    """Vẽ đường cong đầm chặt W - gamma_d và đường bão hòa Sr = 1.0"""
    c_data = compaction_res["curve_data"]
    w_opt = compaction_res["W_opt_percent"]
    gamma_max = compaction_res["gamma_d_max"]
    
    fig = go.Figure()
    
    # Đường cong đầm chặt nội suy mượt
    fig.add_trace(go.Scatter(
        x=c_data["W_smooth"], y=c_data["gamma_smooth"],
        mode="lines",
        name="Đường cong đầm chặt (Proctor)",
        line=dict(color="#F59E0B", width=3)
    ))
    
    # Điểm thí nghiệm thực tế
    fig.add_trace(go.Scatter(
        x=c_data["W_raw"], y=c_data["gamma_raw"],
        mode="markers",
        name="Điểm đo thí nghiệm",
        marker=dict(size=10, color="#EF4444", symbol="circle")
    ))
    
    # Đường bão hòa Sr = 1.0
    fig.add_trace(go.Scatter(
        x=c_data["W_smooth"], y=c_data["gamma_zav"],
        mode="lines",
        name="Đường bão hòa Sr = 1.0 (Zero Air Voids)",
        line=dict(color="#38BDF8", width=2, dash="dash")
    ))
    
    # Đánh dấu đỉnh tối ưu (W_opt, gamma_max)
    fig.add_trace(go.Scatter(
        x=[w_opt], y=[gamma_max],
        mode="markers+text",
        name="Điểm đầm chặt tối ưu",
        marker=dict(size=14, color="#10B981", symbol="diamond"),
        text=[f"  W_opt = {w_opt}%<br>  γ_d,max = {gamma_max} g/cm³"],
        textposition="top right",
        textfont=dict(color="#6EE7B7", size=12)
    ))
    
    fig.update_layout(
        title="Đường cong đầm chặt đất tiêu chuẩn & Đường bão hòa khí",
        xaxis_title="Độ ẩm W (%)",
        yaxis_title="Khối lượng thể tích khô γ_d (g/cm³)",
        template="plotly_dark",
        paper_bgcolor="#0B1120",
        plot_bgcolor="#0F172A",
        font=dict(color="#F8FAFC"),
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(x=0.05, y=0.05)
    )
    return fig

# ==============================================================================
# 4. VẼ BIỂU ĐỒ PHÂN BỐ TẢI TRỌNG GIÓ THEO CHIỀU CAO BẰNG PLOTLY
# ==============================================================================
def plot_wind_load_distribution_plotly(wind_res: Dict[str, Any]) -> go.Figure:
    """Vẽ biểu đồ lực gió tác dụng theo các tầng nhà"""
    df_wind = wind_res["df_wind"]
    
    fig = go.Figure()
    
    # Vẽ cột lực gió ngang theo từng tầng
    fig.add_trace(go.Bar(
        y=df_wind["Tầng"],
        x=df_wind["Lực gió tầng W_i (kN)"],
        orientation="h",
        name="Lực gió sàn tầng Wi (kN)",
        marker=dict(
            color=df_wind["Lực gió tầng W_i (kN)"],
            colorscale="Viridis",
            showscale=True
        ),
        text=df_wind["Lực gió tầng W_i (kN)"].apply(lambda x: f"{x} kN"),
        textposition="outside"
    ))
    
    fig.update_layout(
        title=f"Phân bố tải trọng gió theo chiều cao nhà ({wind_res['region_name']})",
        xaxis_title="Lực gió tập trung Wi (kN)",
        yaxis_title="Tầng nhà",
        template="plotly_dark",
        paper_bgcolor="#0B1120",
        plot_bgcolor="#0F172A",
        font=dict(color="#F8FAFC"),
        margin=dict(l=50, r=40, t=50, b=40)
    )
    return fig
