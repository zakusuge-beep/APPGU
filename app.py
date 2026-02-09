import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

# --- 1. SETTINGS & STYLES ---
st.set_page_config(page_title="Smart Pet Care V3 Pro", page_icon="🐾", layout="wide")

PET_ICONS = {
    "สุนัข": "🐶", "แมว": "🐱", "ปลา": "🐠", "นก": "🦜", "กระต่าย": "🐰",
    "แฮมสเตอร์": "🐹", "เต่า": "🐢", "เม่นแคระ": "🦔", "ชูการ์ไกลเดอร์": "🐿️", "สัตว์เลื้อยคลาน": "🦎"
}

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@300;500;700&display=swap');
    * {{ font-family: 'Chakra Petch', sans-serif; }}
    .stApp {{ background: linear-gradient(to right, #FFF5F5, #F0F4FF); }}
    .main-title {{ color: #FF6B6B; text-align: center; font-size: 3rem; font-weight: bold; text-shadow: 2px 2px #FFD9D9; }}
    .pet-card {{ background: white; padding: 20px; border-radius: 20px; border-left: 10px solid #FFADAD; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; }}
    .dashboard-card {{ background: #FFFFFF; padding: 20px; border-radius: 15px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.03); border: 1px solid #FFE0E0; }}
    .rating-box {{ background-color: white; padding: 30px; border-radius: 20px; text-align: center; border: 3px solid #FFD93D; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
    .credit-footer {{ background-color: #FFDEE9; padding: 20px; border-radius: 20px; border: 2px dashed #FF9A9E; text-align: center; margin-top: 30px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE FUNCTIONS ---
DB_FILE = "pet_pro_data_v3.csv"
SURVEY_FILE = "survey_results.csv"

def load_data():
    if os.path.exists(DB_FILE): return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["ID", "ชื่อ", "ประเภท", "น้ำหนัก", "อายุ", "วัคซีน", "นัดหมาย", "วันที่", "ชื่อยา", "เวลาทานยา"])

def save_data(df): df.to_csv(DB_FILE, index=False)

def load_survey():
    if os.path.exists(SURVEY_FILE): return pd.read_csv(SURVEY_FILE)
    return pd.DataFrame(columns=["คะแนน"])

def save_survey(score_val):
    s_df = load_survey()
    new_score = pd.DataFrame([[score_val]], columns=["คะแนน"])
    s_df = pd.concat([s_df, new_score], ignore_index=True)
    s_df.to_csv(SURVEY_FILE, index=False)

def get_star_rating(avg_score):
    full_stars = int(avg_score)
    # แสดงดาวเต็มตามจำนวนเลขจำนวนเต็ม และใช้ดาวดวงอื่นเป็นดาวว่าง
    stars = "⭐" * full_stars + "☆" * (5 - full_stars)
    return stars

df = load_data()

# --- 3. SIDEBAR MENU ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🐾 Pet Navigator</h1>", unsafe_allow_html=True)
    menu = st.radio("เลือกเมนูหลัก", ["🏠 หน้าแรก & Dashboard", "➕ ลงทะเบียนสัตว์เลี้ยง", "🔄 จัดการสุขภาพ & อัปเดต", "🚑 คลังความรู้ฉุกเฉิน", "⭐ ประเมินความพึงพอใจ"])
    st.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=150)

# --- 4. MAIN LOGIC ---

if menu == "🏠 หน้าแรก & Dashboard":
    st.markdown("<h1 class='main-title'>Smart Pet Care Dashboard</h1>", unsafe_allow_html=True)
    if not df.empty:
        total_pets = len(df["ชื่อ"].unique())
        latest_entries = df.sort_values(by="วันที่").drop_duplicates(subset="ชื่อ", keep="last")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='dashboard-card'><h3>🐶 สัตว์เลี้ยงทั้งหมด</h3><h2 style='color:#FF6B6B;'>{total_pets} ตัว</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='dashboard-card'><h3>⚖️ น้ำหนักเฉลี่ย</h3><h2 style='color:#4D96FF;'>{latest_entries['น้ำหนัก'].mean():.2f} kg</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='dashboard-card'><h3>🏆 ประเภทที่นิยม</h3><h2 style='color:#6BCB77;'>{latest_entries['ประเภท'].mode()[0]}</h2></div>", unsafe_allow_html=True)
        st.write("### 📊 จำนวนสัตว์เลี้ยงแบ่งตามประเภท")
        type_counts = latest_entries["ประเภท"].value_counts().reset_index()
        type_counts.columns = ["ประเภท", "จำนวน"]
        fig_pie = px.pie(type_counts, values="จำนวน", names="ประเภท", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("ยังไม่มีข้อมูลในระบบ")
    
    st.markdown(f"""<div class='credit-footer'><h3>🌟 พัฒนาโดย :</h3><p style='font-size: 1.2rem;'><b>นาย ภูมินทร์ ศรีสุขใส & นาย อธิศพัฒน์ จริยสุธรรมกุล</b></p><p>ชั้นมัธยมศึกษาปีที่ 4/7</p></div>""", unsafe_allow_html=True)

elif menu == "➕ ลงทะเบียนสัตว์เลี้ยง":
    st.subheader("➕ เพิ่มสมาชิกใหม่ในครอบครัว")
    with st.form("add_pet"):
        name = st.text_input("ชื่อสัตว์เลี้ยง")
        p_type = st.selectbox("ประเภทสัตว์", list(PET_ICONS.keys()))
        col1, col2 = st.columns(2)
        weight = col1.number_input("น้ำหนักแรกเริ่ม (kg)", min_value=0.01)
        age = col2.number_input("อายุ (ปี/เดือน)", min_value=0)
        vac = st.text_input("วัคซีนที่เคยฉีด")
        app = st.date_input("วันนัดหมายแพทย์")
        if st.form_submit_button("บันทึกสมาชิกใหม่ 🐾"):
            if name:
                new_id = datetime.now().strftime("%Y%m%d%H%M%S")
                new_row = pd.DataFrame([[new_id, name, p_type, weight, age, vac, str(app), str(datetime.now().date()), "ไม่มี", "ไม่มี"]], columns=df.columns)
                df = pd.concat([df, new_row], ignore_index=True); save_data(df)
                st.balloons(); st.success(f"ยินดีต้อนรับ {name} {PET_ICONS[p_type]}")
            else: st.error("กรุณากรอกชื่อสัตว์เลี้ยง")

elif menu == "🔄 จัดการสุขภาพ & อัปเดต":
    if not df.empty:
        pet_list = sorted(df["ชื่อ"].unique())
        selected = st.selectbox("เลือกสัตว์เลี้ยง", pet_list)
        history = df[df["ชื่อ"] == selected].copy()
        latest = history.iloc[-1]
        st.markdown(f"<div class='pet-card'><h2>{PET_ICONS.get(latest['ประเภท'], '🐾')} {selected}</h2></div>", unsafe_allow_html=True)
        
        # คำนวณแคลอรี่ RER
        rer = round((latest["น้ำหนัก"] * 30) + 70)
        st.info(f"🍽️ พลังงานที่ต้องการ (RER): **{rer} kcal/วัน**")
        
        with st.expander("🆕 อัปเดตข้อมูลสุขภาพ / บันทึกยา"):
            with st.form("update_form"):
                u_weight = st.number_input("น้ำหนักใหม่ (kg)", value=float(latest["น้ำหนัก"]))
                u_med = st.text_input("ชื่อยา", value=latest["ชื่อยา"])
                u_time = st.text_input("เวลาทานยา", value=latest["เวลาทานยา"])
                if st.form_submit_button("บันทึกการอัปเดต"):
                    new_entry = pd.DataFrame([[latest["ID"], selected, latest["ประเภท"], u_weight, latest["อายุ"], latest["วัคซีน"], latest["นัดหมาย"], str(datetime.now().date()), u_med, u_time]], columns=df.columns)
                    df = pd.concat([df, new_entry], ignore_index=True); save_data(df); st.rerun()

        fig = px.area(history, x="วันที่", y="น้ำหนัก", title=f"📈 กราฟพัฒนาการน้ำหนักของ {selected}", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ไม่มีข้อมูลสัตว์เลี้ยง")

elif menu == "🚑 คลังความรู้ฉุกเฉิน":
    st.header("🚑 คู่มือปฐมพยาบาลเบื้องต้น")
    st.write("1. **งูกัด:** ห้ามดูดพิษเด็ดขาด รีบส่งโรงพยาบาล\n2. **สารพิษ:** ล้างตัวด้วยน้ำสะอาด นำบรรจุภัณฑ์ไปพบหมอ")

elif menu == "⭐ ประเมินความพึงพอใจ":
    st.markdown("<h1 style='text-align: center;'>⭐ คะแนนความพึงพอใจจากผู้ใช้</h1>", unsafe_allow_html=True)
    
    # ส่วนแสดงผลคะแนนเฉลี่ย (Dashboard ของคะแนน)
    survey_df = load_survey()
    if not survey_df.empty:
        avg_score = survey_df["คะแนน"].mean()
        total_votes = len(survey_df)
        
        st.markdown(f"""
        <div class='rating-box'>
            <h2 style='margin:0; color:#444;'>คะแนนรวมเฉลี่ย</h2>
            <h1 style='font-size: 4rem; color: #FFB300; margin: 10px 0;'>{avg_score:.1f} <span style='font-size:1.5rem; color:#888;'>/ 5.0</span></h1>
            <div style='font-size: 3rem; margin-bottom: 10px;'>{get_star_rating(avg_score)}</div>
            <p style='color: #666;'>จากผู้ร่วมประเมินทั้งหมด {total_votes} ท่าน</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("ยังไม่มีการประเมิน ร่วมเป็นท่านแรกที่ให้คะแนนเรา!")

    st.write("---")
    
    # ส่วนฟอร์มสำหรับโหวต
    st.subheader("📋 แบบประเมินประสิทธิภาพระบบ")
    q = ["1. รูปแบบสวยงามน่าใช้งาน", "2. การทำงานถูกต้องแม่นยำ", "3. จัดการข้อมูลได้สะดวก", "4. กราฟสรุปผลเข้าใจง่าย", "5. ประสิทธิภาพโดยรวม"]
    score_map = {"น้อย": 1, "ปานกลาง": 2, "มาก": 3, "มากที่สุด": 4, "ดีเยี่ยม": 5}
    
    with st.form("survey_form"):
        total_form_score = 0
        for text in q:
            choice = st.select_slider(text, options=["น้อย", "ปานกลาง", "มาก", "มากที่สุด", "ดีเยี่ยม"], value="ดีเยี่ยม")
            total_form_score += score_map[choice]
        
        if st.form_submit_button("ส่งคะแนนประเมิน 🚀"):
            # หาค่าเฉลี่ยของ 5 ข้อที่ผู้ใช้เลือกในครั้งนี้
            final_user_score = total_form_score / len(q)
            save_survey(final_user_score)
            st.balloons()
            st.success(f"บันทึกคะแนน {final_user_score:.1f} เรียบร้อยแล้ว ขอบคุณครับ!")
            st.rerun()
