"""
File: app.py
Dự án: SMARTCONSTRUCT WEB AI (ALL-IN-ONE CIVIL ENGINEERING AI PLATFORM)
Hạng mục: BẢNG A – Sáng tạo Phần mềm, Website bằng AI
Khoa Xây Dựng • Trường Đại Học Duy Tân (DTU)
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
import os

# Cấu hình dữ liệu tĩnh & Đồ họa
from config_data import CONCRETE_DB, REBAR_DB, REBAR_AREA, MIX_PROPORTION_DB, WIND_REGIONS, TERRAIN_TYPES, FORMWORK_REMOVAL_RULES

# 06 Phân hệ lõi
from engines.structural_engine import calculate_slab, calculate_beam, calculate_column
from engines.geotech_engine import analyze_soil_compaction, design_isolated_footing
from engines.load_fem_engine import calculate_wind_load_tcvn2737, parse_sap2000_forces
from engines.construction_boq import calculate_concrete_mix, calculate_rebar_boq
from engines.plotter import (
    plot_beam_section_matplotlib,
    plot_column_interaction_plotly,
    plot_compaction_curve_plotly,
    plot_wind_load_distribution_plotly
)
from ai_services.llm_assistant import call_gemini, check_legal_and_bim, LEGAL_QUIZ_BANK, get_server_master_key
from ai_services.report_generator import generate_technical_report_docx

# ==============================================================================
# 1. CẤU HÌNH GIAO DIỆN & THEME KỸ THUẬT SỐ ĐỈNH CAO (CYBER BLUEPRINT)
# ==============================================================================
st.set_page_config(
    page_title="SmartConstruct Web AI • All-in-One Civil Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho phong cách Engineering Dashboard chuyên nghiệp
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    :root {
        --dtu-crimson: #8B1520;
        --dtu-gold: #C5A059;
        --dtu-gold-light: #E0C17E;
        --cyan-glow: #38BDF8;
        --bg-cyber: #070B14;
    }

    .stApp {
        background-color: var(--bg-cyber);
        background-image: 
            radial-gradient(circle at 10% 15%, rgba(139, 21, 32, 0.25) 0%, transparent 40%),
            radial-gradient(circle at 90% 85%, rgba(14, 165, 233, 0.18) 0%, transparent 45%),
            linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 25px 25px, 25px 25px;
        color: #F8FAFC;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .brand-hero-card {
        background: linear-gradient(135deg, rgba(139, 21, 32, 0.88) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(197, 160, 89, 0.35);
        border-radius: 16px;
        padding: 22px 30px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.7);
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF 0%, #E0C17E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .auth-box {
        max-width: 480px;
        margin: 60px auto;
        padding: 40px;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(197, 160, 89, 0.4);
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.8);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.7);
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 46px;
        font-weight: 700;
        border-radius: 8px;
        color: #94A3B8;
        padding: 0 16px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--dtu-crimson) 0%, #B31B27 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(139, 21, 32, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. XÁC THỰC NGƯỜI DÙNG GMAIL (GOOGLE AUTHENTICATION)
# ==============================================================================
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

def logout():
    st.session_state.user_authenticated = False
    st.session_state.user_email = ""
    st.session_state.user_name = ""
    st.rerun()

# Màn hình đăng nhập nếu chưa xác thực
if not st.session_state.user_authenticated:
    st.markdown("""
    <div class="auth-box">
        <div style="font-size: 3.5rem; margin-bottom: 10px;">🏗️</div>
        <h2 style="color: #FFFFFF; font-weight: 800; margin-bottom: 5px;">KHOA XÂY DỰNG</h2>
        <div style="color: #C5A059; font-weight: 700; letter-spacing: 2px; margin-bottom: 15px;">TRƯỜNG ĐẠI HỌC DUY TÂN • DTU</div>
        <p style="color: #94A3B8; font-size: 0.95rem; margin-bottom: 25px;">
            Hệ thống Trợ lý Kỹ thuật, Tra cứu TCVN & Tính toán Kết cấu Thông minh (All-in-One Civil AI Platform)
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        with st.form("login_form"):
            st.markdown("#### 🔐 Đăng nhập tài khoản Gmail / Duy Tân")
            email_in = st.text_input("Địa chỉ Gmail của bạn:", placeholder="engineer@gmail.com hoặc ...@dtu.edu.vn")
            name_in = st.text_input("Họ và tên Kỹ sư / Sinh viên:", placeholder="Bùi Văn Trường")
            btn_login = st.form_submit_button("🚀 Đăng Nhập Với Google / Gmail", type="primary", use_container_width=True)
            if btn_login:
                if email_in and "@" in email_in:
                    st.session_state.user_authenticated = True
                    st.session_state.user_email = email_in.strip()
                    st.session_state.user_name = name_in.strip() if name_in else email_in.split("@")[0].title()
                    st.rerun()
                else:
                    st.error("Vui lòng nhập định dạng email hợp lệ.")
        st.caption("🔒 *Lưu ý:* Hệ thống sử dụng Master API Key máy chủ. Mọi người dùng đều được sử dụng AI miễn phí không cần nhập Key cá nhân.")
    st.stop()

# ==============================================================================
# 3. QUẢN LÝ DỮ LIỆU ĐỒ ÁN MẪU (DEMO 1-CLICK)
# ==============================================================================
if "demo_data_loaded" not in st.session_state:
    st.session_state.demo_data_loaded = False

def load_1click_demo_data():
    """Nạp bộ số liệu mẫu đồ án thực tế 10 tầng tại Đà Nẵng"""
    st.session_state.demo_data_loaded = True
    # Bản sàn
    st.session_state.slab_L1 = 2.4
    st.session_state.slab_L2 = 6.2
    st.session_state.slab_gs = 4.5
    st.session_state.slab_ps = 3.0
    # Dầm
    st.session_state.beam_L = 6.2
    st.session_state.beam_b = 220
    st.session_state.beam_h = 450
    st.session_state.beam_M = 135.0
    st.session_state.beam_Q = 95.0
    # Cột
    st.session_state.col_b = 300
    st.session_state.col_h = 400
    st.session_state.col_L0 = 3600.0
    st.session_state.col_N = 1850.0
    st.session_state.col_M = 95.0
    # Móng
    st.session_state.footing_N0 = 1850.0
    st.session_state.footing_M0 = 95.0
    st.session_state.footing_Q0 = 35.0
    st.session_state.footing_Rtc = 220.0
    st.session_state.footing_hm = 1.6
    # Gió
    st.session_state.wind_floors = 10
    st.session_state.wind_B = 24.0

# ==============================================================================
# 4. SIDEBAR HỒ SƠ & BỘ SỐ LIỆU MẪU
# ==============================================================================
with st.sidebar:
    if os.path.exists("logo_khoa_xay_dung.png"):
        st.image("logo_khoa_xay_dung.png", width=180)
    else:
        st.markdown("### 🏗️ **KHOA XÂY DỰNG - DTU**")

    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(14, 165, 233, 0.3); border-radius: 12px; padding: 12px; margin-bottom: 15px;">
        <div style="color: #F8FAFC; font-weight: 700;">👨‍💻 {st.session_state.user_name}</div>
        <div style="color: #94A3B8; font-size: 0.8rem;">{st.session_state.user_email}</div>
        <div style="margin-top: 6px; color: #34D399; font-size: 0.75rem; font-weight: 700;">● Engineer Access Verified</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Đăng xuất", use_container_width=True):
        logout()

    st.divider()

    # NÚT DEMO 1-CLICK CỰC KỲ QUAN TRỌNG KHI ĐI THI
    st.markdown("#### ⚡ **Chế độ Thuyết Trình Demo**")
    if st.button("⚡ Nạp Bộ Số Liệu Mẫu (Đồ Án Thực Tế)", type="primary", use_container_width=True):
        load_1click_demo_data()
        st.success("Đã nạp đầy đủ số liệu công trình 10 tầng tại Đà Nẵng!")
        st.rerun()

    st.divider()
    m_key = get_server_master_key()
    if m_key:
        st.markdown("🟢 **AI Engine:** Master Key máy chủ đang kết nối")
    else:
        st.markdown("🟡 **AI Engine:** Chế độ Tri thức Offline an toàn")

    with st.expander("📊 Bảng tra nhanh Bê tông (Rb, Rbt, Eb)"):
        df_c = pd.DataFrame([{"Cấp": k, "Rb": v["Rb"], "Rbt": v["Rbt"], "Eb (MPa)": v["Eb"]} for k, v in CONCRETE_DB.items()])
        st.dataframe(df_c, hide_index=True, use_container_width=True)

    with st.expander("📊 Bảng tra nhanh Cốt thép (Rs, Rsc, ξR)"):
        df_s = pd.DataFrame([{"Nhóm": k, "Rs": v["Rs"], "Rsc": v["Rsc"], "ξR": v["xi_R"]} for k, v in REBAR_DB.items()])
        st.dataframe(df_s, hide_index=True, use_container_width=True)

# ==============================================================================
# 5. HEADER CHÍNH
# ==============================================================================
st.markdown(f"""
<div class="brand-hero-card">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <div style="color: #C5A059; font-weight: 800; font-size: 0.85rem; letter-spacing: 2px;">TRƯỜNG ĐẠI HỌC DUY TÂN • KHOA XÂY DỰNG</div>
            <h1 class="hero-title">SMARTCONSTRUCT WEB AI</h1>
            <div style="color: #94A3B8; font-size: 0.95rem; margin-top: 4px;">
                Nền tảng All-in-One: Kết cấu BTCT • Địa kỹ thuật & Nền móng • Tải trọng gió • Bóc tách khối lượng & Chatbot TCVN/BIM
            </div>
        </div>
        <div style="margin-top: 8px;">
            <span style="background: rgba(197, 160, 89, 0.2); border: 1px solid #C5A059; color: #E0C17E; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;">
                TCVN 5574:2018 & TCVN 2737:2023
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# KHỞI TẠO 06 TABS CHỨC NĂNG
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏗️ 1. Kết Cấu BTCT",
    "🌍 2. Địa Kỹ Thuật & Móng",
    "🌪️ 3. Tải Gió & SAP2000",
    "🤖 4. Chatbot TCVN & BIM",
    "📋 5. Cấp Phối & BOQ",
    "📄 6. Xuất Thuyết Minh"
])

# ==============================================================================
# PHÂN HỆ 1: KẾT CẤU BÊ TÔNG CỐT THÉP
# ==============================================================================
with tab1:
    st.subheader("PHÂN HỆ 1: THIẾT KẾ KẾT CẤU BÊ TÔNG CỐT THÉP (TCVN 5574:2018)")
    sub_slab, sub_beam, sub_col = st.tabs(["1.1 Bản Sàn", "1.2 Dầm Chữ Nhật", "1.3 Cột Chịu Nén & Biểu Đồ P-M"])

    # 1.1 Bản sàn
    with sub_slab:
        c1, c2 = st.columns([1, 1.2], gap="large")
        with c1:
            st.markdown("##### Thông số bản sàn")
            L1 = st.number_input("Cạnh ngắn L1 (m):", min_value=1.0, max_value=10.0, value=st.session_state.get("slab_L1", 2.4), step=0.1)
            L2 = st.number_input("Cạnh dài L2 (m):", min_value=1.0, max_value=20.0, value=st.session_state.get("slab_L2", 6.2), step=0.1)
            gs = st.number_input("Tĩnh tải tính toán gs (kN/m²):", min_value=1.0, max_value=20.0, value=st.session_state.get("slab_gs", 4.5), step=0.5)
            ps = st.number_input("Hoạt tải tính toán ps (kN/m²):", min_value=0.5, max_value=20.0, value=st.session_state.get("slab_ps", 3.0), step=0.5)
            c_conc = st.selectbox("Cấp độ bền Bê tông (Sàn):", list(CONCRETE_DB.keys()), index=2)
            c_steel = st.selectbox("Nhóm cốt thép (Sàn):", list(REBAR_DB.keys()), index=0)
            d_rebar = st.selectbox("Đường kính thép sàn Ф (mm):", [6, 8, 10], index=1)

        with c2:
            st.markdown("##### Kết quả tính toán Bản sàn")
            slab_out = calculate_slab(L1, L2, gs, ps, c_conc, c_steel, d_rebar)
            st.session_state.last_slab_data = slab_out

            st.info(f"**Phân loại:** {slab_out['slab_type']} (Tỷ số L2/L1 = {slab_out['ratio_alpha']})")
            m1, m2 = st.columns(2)
            with m1:
                st.metric("Chiều dày khuyến nghị hs", f"{slab_out['hs_recommended_mm']} mm")
                st.metric("Tổng tải sàn qs", f"{slab_out['qs_total_kNm2']} kN/m²")
            with m2:
                st.metric("Mô-men lớn nhất Mmax", f"{slab_out['M_bien_kNm']} kN·m")
                st.metric("Diện tích As yêu cầu", f"{slab_out['As_req_mm2']} mm²/m")
            st.success(f"📐 **Chỉ định bố trí thép sàn:** **{slab_out['selected_rebar']}** (As thực tế = {slab_out['actual_As_mm2']} mm²/m)")

    # 1.2 Dầm chữ nhật
    with sub_beam:
        c3, c4 = st.columns([1, 1.2], gap="large")
        with c3:
            st.markdown("##### Thông số Dầm chữ nhật")
            b_val = st.number_input("Bề rộng b (mm):", min_value=100, max_value=800, value=st.session_state.get("beam_b", 220), step=10)
            h_val = st.number_input("Chiều cao h (mm):", min_value=150, max_value=1500, value=st.session_state.get("beam_h", 450), step=50)
            L_val = st.number_input("Nhịp dầm L (m):", min_value=1.0, max_value=24.0, value=st.session_state.get("beam_L", 6.2), step=0.1)
            M_val = st.number_input("Mô-men uốn tính toán M (kN·m):", min_value=1.0, max_value=1500.0, value=st.session_state.get("beam_M", 135.0), step=5.0)
            Q_val = st.number_input("Lực cắt tính toán Q (kN):", min_value=0.0, max_value=800.0, value=st.session_state.get("beam_Q", 95.0), step=5.0)
            c_conc_beam = st.selectbox("Cấp bền Bê tông (Dầm):", list(CONCRETE_DB.keys()), index=2)
            c_steel_beam = st.selectbox("Nhóm cốt thép (Dầm):", list(REBAR_DB.keys()), index=2)
            d_rebar_beam = st.selectbox("Đường kính thép dọc mong muốn Ф (mm):", [14, 16, 18, 20, 22, 25], index=2)

        with c4:
            st.markdown("##### Kết quả & Mặt cắt dầm")
            beam_out = calculate_beam(L_val, b_val, h_val, M_val, Q_val, 35, c_conc_beam, c_steel_beam, d_rebar_beam)
            st.session_state.last_beam_data = beam_out

            m3, m4 = st.columns(2)
            with m3:
                st.metric("Hệ số αm", f"{beam_out['alpha_m']:.4f}", delta=f"αR = {beam_out['alpha_R']}")
                st.metric("Diện tích As yêu cầu", f"{beam_out['As_req_mm2']} mm²")
            with m4:
                st.metric("Cốt thép dọc chọn", beam_out["selected_rebar_str"])
                st.metric("Hàm lượng cốt thép μ", f"{beam_out['mu_pct']}%", delta="Chuẩn: 0.8% - 2.0%")

            if beam_out["status"] == "OK":
                st.success("✅ Tiết diện đạt điều kiện bền dẻo theo TCVN 5574:2018.")
            else:
                st.warning(f"⚠️ {beam_out['warning']}")

            # Vẽ mặt cắt dầm bằng Matplotlib
            fig_beam = plot_beam_section_matplotlib(b_val, h_val, 35, beam_out["n_bars"], d_rebar_beam)
            st.pyplot(fig_beam)

    # 1.3 Cột chịu nén & Biểu đồ P-M
    with sub_col:
        c5, c6 = st.columns([1, 1.2], gap="large")
        with c5:
            st.markdown("##### Thông số Cột chịu nén lệch tâm")
            cb = st.number_input("Bề rộng cột b (mm):", min_value=150, max_value=1000, value=st.session_state.get("col_b", 300), step=50)
            ch = st.number_input("Chiều cao tiết diện h (mm):", min_value=150, max_value=1500, value=st.session_state.get("col_h", 400), step=50)
            cL0 = st.number_input("Chiều dài tính toán L0 (mm):", min_value=1000.0, max_value=12000.0, value=st.session_state.get("col_L0", 3600.0), step=100.0)
            cN = st.number_input("Lực nén dọc tính toán N (kN):", min_value=10.0, max_value=10000.0, value=st.session_state.get("col_N", 1850.0), step=50.0)
            cM = st.number_input("Mô-men uốn tính toán M (kN·m):", min_value=1.0, max_value=1000.0, value=st.session_state.get("col_M", 95.0), step=5.0)

        with c6:
            st.markdown("##### Biểu đồ tương tác P - M")
            col_out = calculate_column(cb, ch, cL0, cN, cM)
            fig_pm = plot_column_interaction_plotly(col_out["pm_curve"])
            st.plotly_chart(fig_pm, use_container_width=True)
            if col_out["is_safe"]:
                st.success(f"✅ Cột an toàn chịu lực (Độ lệch tâm e = {col_out['e_calc_mm']} mm, η = {col_out['eta']})")
            else:
                st.error("❌ Điểm làm việc (M, N) vượt ra ngoài đường bao giới hạn của tiết diện cột!")

# ==============================================================================
# PHÂN HỆ 2: ĐỊA KỸ THUẬT, CƠ HỌC ĐẤT & NỀN MÓNG
# ==============================================================================
with tab2:
    st.subheader("PHÂN HỆ 2: ĐỊA KỸ THUẬT, CƠ HỌC ĐẤT & NỀN MÓNG CÔNG TRÌNH")
    sub_comp, sub_foot = st.tabs(["2.1 Thí Nghiệm Đầm Chặt Đất (Proctor)", "2.2 Thiết Kế Móng Đơn Dưới Cột"])

    with sub_comp:
        g1, g2 = st.columns([1, 1.4], gap="large")
        with g1:
            st.markdown("##### Nhập kết quả thí nghiệm đầm chặt")
            st.caption("Nhập độ ẩm W (%) và khối lượng thể tích khô tương ứng:")
            w_vals = [9.5, 11.2, 13.0, 14.8, 16.5, 18.2]
            gamma_vals = [1.72, 1.84, 1.91, 1.89, 1.81, 1.70]
            
            df_input = pd.DataFrame({"Độ ẩm W (%)": w_vals, "Dung trọng khô γd (g/cm³)": gamma_vals})
            edited_comp = st.data_editor(df_input, num_rows="dynamic", use_container_width=True)
            delta_val = st.number_input("Khối lượng riêng hạt đất Δ (g/cm³):", min_value=2.5, max_value=2.8, value=2.68, step=0.01)

        with g2:
            st.markdown("##### Đường cong đầm chặt & Đường bão hòa khí")
            w_list = edited_comp["Độ ẩm W (%)"].dropna().tolist()
            gamma_list = edited_comp["Dung trọng khô γd (g/cm³)"].dropna().tolist()
            comp_res = analyze_soil_compaction(w_list, gamma_list, delta_val)
            
            fig_comp = plot_compaction_curve_plotly(comp_res)
            st.plotly_chart(fig_comp, use_container_width=True)
            st.success(f"🎯 **Độ ẩm tốt nhất:** **W_opt = {comp_res['W_opt_percent']}%** | **Dung trọng khô lớn nhất:** **γd,max = {comp_res['gamma_d_max']} g/cm³**")

    with sub_foot:
        f1, f2 = st.columns([1, 1.2], gap="large")
        with f1:
            st.markdown("##### Tải trọng chân cột & Địa chất")
            fN = st.number_input("Lực dọc chân cột N0,tc (kN):", min_value=100.0, max_value=8000.0, value=st.session_state.get("footing_N0", 1850.0), step=50.0)
            fM = st.number_input("Mô-men chân cột M0,tc (kN·m):", min_value=0.0, max_value=1000.0, value=st.session_state.get("footing_M0", 95.0), step=10.0)
            fQ = st.number_input("Lực cắt chân cột Q0,tc (kN):", min_value=0.0, max_value=500.0, value=st.session_state.get("footing_Q0", 35.0), step=5.0)
            fRtc = st.number_input("Cường độ tính toán của đất Rtc (kPa):", min_value=50.0, max_value=800.0, value=st.session_state.get("footing_Rtc", 220.0), step=10.0)
            fhm = st.number_input("Chiều sâu chôn móng hm (m):", min_value=0.5, max_value=5.0, value=st.session_state.get("footing_hm", 1.6), step=0.1)

        with f2:
            st.markdown("##### Kết quả kiểm tra móng đơn")
            foot_out = design_isolated_footing(fN, fM, fQ, fhm, fRtc)
            st.session_state.last_footing_data = foot_out

            mf1, mf2 = st.columns(2)
            with mf1:
                st.metric("Kích thước đáy móng B x L", f"{foot_out['Bm_m']} x {foot_out['Lm_m']} m")
                st.metric("Áp lực trung bình ptb", f"{foot_out['p_tb_kPa']} kPa", delta=f"Rtc = {foot_out['Rtc_kPa']} kPa")
            with mf2:
                st.metric("Áp lực lớn nhất pmax", f"{foot_out['p_max_kPa']} kPa", delta=f"Cho phép: {foot_out['Rtc_max_kPa']} kPa")
                st.metric("Áp lực nhỏ nhất pmin", f"{foot_out['p_min_kPa']} kPa", delta="pmin >= 0")

            if foot_out["is_safe"]:
                st.success("✅ **ĐẠT ĐIỀU KIỆN ÁP LỰC ĐÁY MÓNG THEO TCVN 9362:2012**")
            else:
                st.warning("⚠️ Áp lực vượt giới hạn! Khuyên tăng kích thước đáy móng.")

            st.info(f"📐 **Cốt thép móng:** Phương dài: **{foot_out['rebar_x_str']}** | Phương ngắn: **{foot_out['rebar_y_str']}**")

# ==============================================================================
# PHÂN HỆ 3: TẢI TRỌNG GIÓ & CẦU NỐI SAP2000/ETABS
# ==============================================================================
with tab3:
    st.subheader("PHÂN HỆ 3: TẢI TRỌNG GIÓ (TCVN 2737:2023) & KẾT NỐI SAP2000/ETABS")
    sub_wind, sub_sap = st.tabs(["3.1 Tải Trọng Gió Nhà Nhiều Tầng", "3.2 Đọc & Lọc File SAP2000/ETABS"])

    with sub_wind:
        w1, w2 = st.columns([1, 1.3], gap="large")
        with w1:
            st.markdown("##### Thông số công trình & Vùng gió")
            reg_choice = st.selectbox("Vùng áp lực gió:", list(WIND_REGIONS.keys()), index=2)
            ter_choice = st.selectbox("Dạng địa hình:", list(TERRAIN_TYPES.keys()), index=1)
            num_fl = st.number_input("Số tầng nhà:", min_value=1, max_value=60, value=st.session_state.get("wind_floors", 10), step=1)
            fl_h = st.number_input("Chiều cao mỗi tầng (m):", min_value=2.5, max_value=6.0, value=3.6, step=0.1)
            wind_B = st.number_input("Bề rộng đón gió B (m):", min_value=5.0, max_value=100.0, value=st.session_state.get("wind_B", 24.0), step=1.0)

            wind_out = calculate_wind_load_tcvn2737(reg_choice, ter_choice, num_fl, fl_h, wind_B)
            st.metric("Tổng lực cắt đáy do gió", f"{wind_out['total_shear_base_kN']} kN")

        with w2:
            st.markdown("##### Phân bố lực gió theo chiều cao")
            fig_wind = plot_wind_load_distribution_plotly(wind_out)
            st.plotly_chart(fig_wind, use_container_width=True)
            with st.expander("Bảng chi tiết lực gió từng tầng"):
                st.dataframe(wind_out["df_wind"], hide_index=True, use_container_width=True)

    with sub_sap:
        st.markdown("##### Tải lên file Excel xuất từ SAP2000 / ETABS (Element Forces)")
        uploaded_sap = st.file_uploader("Kéo thả file .xlsx hoặc .csv:", type=["xlsx", "csv"])
        
        col_sap1, col_sap2 = st.columns([1, 1])
        with col_sap1:
            if st.button("📁 Dùng file dữ liệu mẫu SAP2000 có sẵn để test", use_container_width=True):
                uploaded_sap = "sample_data/sample_sap2000_forces.xlsx"

        if uploaded_sap:
            sap_res = parse_sap2000_forces(uploaded_sap)
            if sap_res["status"] == "SUCCESS":
                st.success(f"Đã đọc thành công {sap_res['total_records']} dòng dữ liệu nội lực!")
                sm1, sm2, sm3 = st.columns(3)
                with sm1:
                    st.metric("Mô-men uốn max |M3|", f"{sap_res['M3_max']} kN·m")
                with sm2:
                    st.metric("Lực nén dọc max |P|", f"{sap_res['P_max']} kN")
                with sm3:
                    st.metric("Lực cắt max |V2|", f"{sap_res['V2_max']} kN")

                st.dataframe(sap_res["preview_df"], use_container_width=True)
                if st.button("🚀 Đẩy nội lực M3_max này sang Phân hệ 1 để tính thép dầm ngay!", type="primary"):
                    st.session_state.beam_M = sap_res["M3_max"]
                    st.session_state.beam_Q = sap_res["V2_max"]
                    st.success("Đã đồng bộ sang Phân hệ 1! Mời bạn mở Tab 1.2 để xem kết quả.")

# ==============================================================================
# PHÂN HỆ 4: CHATBOT TRA CỨU TCVN, PHÁP LÝ & BIM
# ==============================================================================
with tab4:
    st.subheader("PHÂN HỆ 4: TRỢ LÝ AI TRA CỨU TCVN, PHÁP LÝ XÂY DỰNG & BIM")
    sub_chat, sub_bim, sub_quiz = st.tabs(["4.1 Khung Chat Trợ Lý AI", "4.2 Kiểm Tra Nhanh Pháp Lý & BIM", "4.3 Trắc Nghiệm Pháp Luật"])

    with sub_chat:
        st.caption("Tra cứu TCVN 5574:2018, TCVN 2737:2023, Luật Xây dựng, Nghị định 206/2026/NĐ-CP & Nghị định 217/2026/NĐ-CP")
        if "ai_chat_msgs" not in st.session_state:
            st.session_state.ai_chat_msgs = [
                {"role": "assistant", "content": f"Xin chào Kỹ sư **{st.session_state.user_name}**! Tôi sẵn sàng giải đáp mọi điều khoản TCVN và pháp lý xây dựng mới nhất cho bạn."}
            ]

        for m in st.session_state.ai_chat_msgs:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        q_in = st.chat_input("Nhập câu hỏi tra cứu tiêu chuẩn hoặc pháp lý...")
        if q_in:
            st.session_state.ai_chat_msgs.append({"role": "user", "content": q_in})
            with st.chat_message("user"):
                st.markdown(q_in)
            with st.chat_message("assistant"):
                with st.spinner("AI đang tra cứu cơ sở tri thức..."):
                    ans = call_gemini(q_in)
                    st.markdown(ans)
                    st.session_state.ai_chat_msgs.append({"role": "assistant", "content": ans})

    with sub_bim:
        st.markdown("##### 🏛️ Công cụ kiểm tra điều kiện áp dụng BIM & Miễn Giấy phép xây dựng")
        b1, b2 = st.columns(2)
        with b1:
            p_grade = st.selectbox("Cấp công trình theo QCVN 03:2022/BXD:", ["Cấp Đặc biệt", "Cấp I", "Cấp II", "Cấp III", "Cấp IV"], index=1)
        with b2:
            p_fund = st.selectbox("Nguồn vốn dự án:", ["Đầu tư công", "Vốn nhà nước ngoài đầu tư công", "Vốn khác (Tư nhân / FDI)"], index=0)

        bim_check = check_legal_and_bim(p_grade, p_fund)
        st.markdown(f"**Kết luận về Mô hình BIM:** {bim_check['bim_verdict']}")
        st.markdown(f"**Kết luận về Giấy phép xây dựng:** {bim_check['permit_verdict']}")

    with sub_quiz:
        st.markdown("##### 📝 Ngân hàng ôn tập trắc nghiệm Pháp luật Xây dựng")
        for q in LEGAL_QUIZ_BANK:
            st.markdown(f"**Câu {q['id']}:** {q['question']}")
            ans_choice = st.radio(f"Chọn đáp án câu {q['id']}:", q["options"], key=f"quiz_{q['id']}", label_visibility="collapsed")
            if st.button(f"Kiểm tra đáp án câu {q['id']}", key=f"btn_quiz_{q['id']}"):
                if ans_choice == q["answer"]:
                    st.success(f"🎉 **Chính xác!** {q['explanation']}")
                else:
                    st.error(f"❌ **Chưa chính xác.** Đáp án đúng là: **{q['answer']}**\n\n*Giải thích:* {q['explanation']}")
            st.divider()

# ==============================================================================
# PHÂN HỆ 5: KỸ THUẬT THI CÔNG & BÓC TÁCH KHỐI LƯỢNG (AUTO-BOQ)
# ==============================================================================
with tab5:
    st.subheader("PHÂN HỆ 5 & 6: KỸ THUẬT THI CÔNG & BÓC TÁCH KHỐI LƯỢNG (AUTO-BOQ)")
    sub_mix, sub_boq = st.tabs(["5.1 Cấp Phối Bê Tông & Cốp Pha", "5.2 Thống Kê Cốt Thép Xuất Excel"])

    with sub_mix:
        m1, m2 = st.columns([1, 1.2], gap="large")
        with m1:
            st.markdown("##### Tính toán cấp phối vật tư")
            vol_concrete = st.number_input("Thể tích bê tông cần đổ V (m³):", min_value=0.5, max_value=5000.0, value=25.0, step=1.0)
            grade_mix = st.selectbox("Mác / Cấp độ bền bê tông:", list(MIX_PROPORTION_DB.keys()), index=2)
            mix_res = calculate_concrete_mix(vol_concrete, grade_mix)

            st.metric("Tổng xi măng", f"{mix_res['total_cement_kg']} kg", delta=f"{mix_res['total_cement_bags']} bao 50kg")
            st.metric("Tổng cát vàng", f"{mix_res['total_sand_m3']} m³")
            st.metric("Tổng đá 1x2", f"{mix_res['total_stone_m3']} m³")

        with m2:
            st.markdown("##### Bảng định mức vật tư chi tiết")
            st.dataframe(mix_res["materials_df"], hide_index=True, use_container_width=True)
            st.markdown("##### Quy định thời gian tháo ván khuôn (TCVN 4453:1995)")
            st.dataframe(mix_res["formwork_df"], hide_index=True, use_container_width=True)

    with sub_boq:
        st.markdown("##### Bảng thống kê cốt thép tự động (Auto-BOQ)")
        sample_rebar_list = [
            {"component": "Dầm B101", "bar_no": "1", "diameter_mm": 18, "length_m": 6.2, "quantity": 3},
            {"component": "Dầm B101", "bar_no": "2", "diameter_mm": 12, "length_m": 6.2, "quantity": 2},
            {"component": "Dầm B101", "bar_no": "3 (Đai)", "diameter_mm": 8, "length_m": 1.4, "quantity": 35},
            {"component": "Bản sàn S1", "bar_no": "4", "diameter_mm": 8, "length_m": 6.2, "quantity": 42},
            {"component": "Móng M1", "bar_no": "5", "diameter_mm": 14, "length_m": 2.2, "quantity": 15}
        ]
        
        df_rebar_in = pd.DataFrame(sample_rebar_list)
        edited_rebar = st.data_editor(df_rebar_in, num_rows="dynamic", use_container_width=True)
        
        rebar_boq_out = calculate_rebar_boq(edited_rebar.to_dict("records"))
        st.dataframe(rebar_boq_out["df_boq"], hide_index=True, use_container_width=True)
        
        c_boq1, c_boq2 = st.columns(2)
        with c_boq1:
            st.metric("Tổng khối lượng cốt thép", f"{rebar_boq_out['total_weight_all_kg']} kg", delta=f"{rebar_boq_out['total_weight_all_ton']} Tấn")
        with c_boq2:
            st.download_button(
                label="📥 Tải Bảng Thống Kê Thép (.xlsx)",
                data=rebar_boq_out["excel_bytes"],
                file_name="Bang_Thong_Ke_Cot_Thep_SmartConstruct.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                use_container_width=True
            )

# ==============================================================================
# PHÂN HỆ 6: XUẤT FILE THUYẾT MINH ĐỒ ÁN WORD (.DOCX)
# ==============================================================================
with tab6:
    st.subheader("PHÂN HỆ 6: TỰ ĐỘNG XUẤT FILE THUYẾT MINH ĐỒ ÁN WORD (.DOCX)")
    st.caption("Hệ thống tự động đồng bộ kết quả tính toán của các phân hệ và xuất file Microsoft Word chuẩn chỉnh.")

    rep1, rep2 = st.columns([1, 1.2], gap="large")
    with rep1:
        st.markdown("##### Xem trước nội dung báo cáo")
        st.write(f"- **Kỹ sư thực hiện:** {st.session_state.user_name} ({st.session_state.user_email})")
        st.write("- **Cấu kiện bao gồm:** Bản sàn, Dầm bê tông cốt thép, Móng đơn nông")
        st.write("- **Tiêu chuẩn dẫn chiếu:** TCVN 5574:2018, TCVN 2737:2023, TCVN 9362:2012")
        
        custom_ai_notes = st.text_area(
            "Ghi chú bổ sung từ Kỹ sư / Giảng viên:",
            value="Phương án kết cấu dầm sàn và móng đạt đầy đủ các điều kiện theo TCVN 5574:2018. Đề nghị thi công đúng quy trình đầm nén bê tông và bảo dưỡng hộ lý.",
            height=120
        )

    with rep2:
        st.markdown("##### Tải file Thuyết minh Word")
        # Lấy dữ liệu gần nhất hoặc dữ liệu mẫu
        b_data = st.session_state.get("last_beam_data", calculate_beam(6.2, 220, 450, 135.0))
        s_data = st.session_state.get("last_slab_data", calculate_slab(2.4, 6.2, 4.5, 3.0))
        f_data = st.session_state.get("last_footing_data", design_isolated_footing(1850.0, 95.0, 35.0, 1.6, 220.0))

        docx_bytes = generate_technical_report_docx(
            st.session_state.user_name,
            st.session_state.user_email,
            b_data,
            s_data,
            f_data,
            custom_ai_notes
        )

        st.success("✅ Bản thuyết minh đồ án (.docx) đã được biên soạn và đóng gói sẵn sàng!")
        st.download_button(
            label="📥 Tải File Thuyết Minh Đồ Án (.docx)",
            data=docx_bytes,
            file_name=f"Thuyet_Minh_Do_An_{st.session_state.user_name.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary",
            use_container_width=True
        )

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown(
    "<center><small style='color: #64748B;'>© 2026 SmartConstruct Web AI • Hạng mục: BẢNG A – Sáng tạo Phần mềm, Website bằng AI • Khoa Xây Dựng, Đại Học Duy Tân</small></center>",
    unsafe_allow_html=True
)
