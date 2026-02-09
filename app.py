import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from fpdf import FPDF
import base64

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
    .status-normal {{ background-color: #D4EDDA; color: #155724; padding: 5px 10px; border-radius: 10px; font-weight: bold; }}
    .status-warning {{ background-color: #FFF3CD; color: #856404; padding: 5px 10px; border-radius: 10px; font-weight: bold; }}
    .rating-header {{ background: white; padding: 20px; border-radius: 15px; border: 2px solid #FFD93D; text-align: center; margin-bottom: 20px; }}
    .credit-footer {{ background-color: #FFDEE9; padding: 20px; border-radius: 20px; border: 2px dashed #FF9A9E; text-align: center; margin-top: 30px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE FUNCTIONS ---
DB_FILE = "pet_pro_data_v3.csv"
SURVEY_FILE = "survey_data.csv" # ไฟล์เก็บคะแนนประเมิน

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["ID", "ชื่อ", "ประเภท", "น้ำหนัก", "อายุ", "วัคซีน", "นัดหมาย", "วันที่", "ชื่อยา", "เวลาทานยา"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

def load_survey():
    if os.path.exists(SURVEY_FILE):
        return pd.read_csv(SURVEY_FILE)
    return pd.DataFrame(columns=["คะแนน"])

def save_survey(score):
    s_df = load_survey()
    new_score = pd.DataFrame([[score]], columns=["คะแนน"])
    s_df = pd.concat([s_df, new_score], ignore_index=True)
    s_df.to_csv(SURVEY_FILE, index=False)

df = load_data()

# --- 3. SIDEBAR MENU ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🐾 Pet Navigator</h1>", unsafe_allow_html=True)
    menu = st.radio("เลือกเมนูหลัก", ["🏠 หน้าแรก & Dashboard", "➕ ลงทะเบียนสัตว์เลี้ยง", "🔄 จัดการสุขภาพ & อัปเดต", "🚑 คลังความรู้ฉุกเฉิน", "⭐ ประเมินความพึงพอใจ"])
    st.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=150)

# --- 4. MAIN LOGIC ---

if menu == "🏠 หน้าแรก & Dashboard":
    st.markdown("<h1 class='main-title'>Smart Pet Care Dashboard</h1>", unsafe_allow_html=True)
    
    # --- 1. ระบบสรุปสถิติภาพรวม (Dashboard Overview) ---
    if not df.empty:
        total_pets = len(df["ชื่อ"].unique())
        latest_entries = df.sort_values(by="วันที่").drop_duplicates(subset="ชื่อ", keep="last")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='dashboard-card'><h3>🐶 สัตว์เลี้ยงทั้งหมด</h3><h2 style='color:#FF6B6B;'>{total_pets} ตัว</h2></div>", unsafe_allow_html=True)
        with c2:
            avg_weight = latest_entries["น้ำหนัก"].mean()
            st.markdown(f"<div class='dashboard-card'><h3>⚖️ น้ำหนักเฉลี่ย</h3><h2 style='color:#4D96FF;'>{avg_weight:.2f} kg</h2></div>", unsafe_allow_html=True)
        with c3:
            most_common = latest_entries["ประเภท"].mode()[0]
            st.markdown(f"<div class='dashboard-card'><h3>🏆 ประเภทที่นิยม</h3><h2 style='color:#6BCB77;'>{most_common}</h2></div>", unsafe_allow_html=True)
        
        st.write("### 📊 จำนวนสัตว์เลี้ยงแบ่งตามประเภท")
        type_counts = latest_entries["ประเภท"].value_counts().reset_index()
        type_counts.columns = ["ประเภท", "จำนวน"]
        fig_pie = px.pie(type_counts, values="จำนวน", names="ประเภท", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("ยังไม่มีข้อมูลในระบบ กรุณาลงทะเบียนสัตว์เลี้ยงตัวแรก")

    st.markdown(f"""
    <div class='credit-footer'>
        <h3>🌟 พัฒนาโดย :</h3>
        <p style='font-size: 1.2rem;'><b>นาย ภูมินทร์ ศรีสุขใส & นาย อธิศพัฒน์ จริยสุธรรมกุล</b></p>
        <p>ชั้นมัธยมศึกษาปีที่ 4/7</p>
        <p><i>"นวัตกรรมเพื่อสัตว์เลี้ยงที่คุณรัก"</i></p>
    </div>
    """, unsafe_allow_html=True)

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
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.balloons()
                st.success(f"ยินดีต้อนรับ {name} {PET_ICONS[p_type]}")
            else:
                st.error("กรุณากรอกชื่อสัตว์เลี้ยง")

elif menu == "🔄 จัดการสุขภาพ & อัปเดต":
    if not df.empty:
        pet_list = sorted(df["ชื่อ"].unique())
        selected = st.selectbox("เลือกสัตว์เลี้ยง", pet_list)
        history = df[df["ชื่อ"] == selected].copy()
        latest = history.iloc[-1]
        icon = PET_ICONS.get(latest["ประเภท"], "🐾")

        st.markdown(f"<div class='pet-card'><h2>{icon} {selected} ({latest['ประเภท']})</h2></div>", unsafe_allow_html=True)
        
        col_m1, col_m2 = st.columns([2, 1])

        with col_m1:
            st.subheader("🍽️ คำนวณปริมาณอาหารที่แนะนำ")
            rer = round((latest["น้ำหนัก"] * 30) + 70)
            st.info(f"พลังงานพื้นฐานที่ต้องการ (RER): **{rer} kcal/วัน**")
            fact = 1.6 
            total_kcal = round(rer * fact)
            st.success(f"ปริมาณที่แนะนำสำหรับ {selected}: **{total_kcal} kcal/วัน**")
            st.caption("*ค่านี้เป็นเพียงการคำนวณเบื้องต้น ควรปรึกษาสัตวแพทย์เพิ่มเติม")

        with col_m2:
            st.subheader("💊 การกินยา")
            st.warning(f"💊 ยา: {latest['ชื่อยา']}\n\n⏰ เวลา: {latest['เวลาทานยา']}")

        with st.expander("🆕 อัปเดตข้อมูลสุขภาพ / บันทึกยา"):
            with st.form("update_form"):
                u_c1, u_c2 = st.columns(2)
                u_weight = u_c1.number_input("น้ำหนักใหม่ (kg)", value=float(latest["น้ำหนัก"]))
                u_age = u_c2.number_input("อายุใหม่", value=int(latest["อายุ"]))
                u_vac = st.text_input("วัคซีนเพิ่มเติม", value=latest["วัคซีน"])
                u_med = st.text_input("ชื่อยาที่ต้องทาน", value=latest["ชื่อยา"])
                u_time = st.text_input("เวลาทานยา (เช่น เช้า-เย็น)", value=latest["เวลาทานยา"])
                u_app = st.date_input("วันนัดครั้งใหม่", value=datetime.strptime(latest["นัดหมาย"], '%Y-%m-%d'))
                
                if st.form_submit_button("บันทึกการอัปเดต"):
                    new_entry = pd.DataFrame([[
                        latest["ID"], selected, latest["ประเภท"], u_weight, u_age, u_vac, str(u_app), str(datetime.now().date()), u_med, u_time
                    ]], columns=df.columns)
                    df = pd.concat([df, new_entry], ignore_index=True)
                    save_data(df)
                    st.success("อัปเดตข้อมูลสำเร็จ!")
                    st.rerun()

        st.write("### 📈 กราฟพัฒนาการน้ำหนัก")
        fig = px.area(history, x="วันที่", y="น้ำหนัก", markers=True, color_discrete_sequence=['#FF8E8E'])
        st.plotly_chart(fig, use_container_width=True)

        if st.button(f"🗑️ ลบข้อมูล {selected}"):
            df = df[df["ชื่อ"] != selected]
            save_data(df)
            st.rerun()
    else:
        st.info("ยังไม่มีข้อมูลสัตว์เลี้ยง")

elif menu == "🚑 คลังความรู้ฉุกเฉิน":
    st.header("🚑 คู่มือปฐมพยาบาลสัตว์เลี้ยงเบื้องต้น")
    with st.expander("🐍 กรณีถูกงูกัด / แมลงมีพิษ"):
        st.write("1. ห้ามกรีดแผลหรือดูดพิษเด็ดขาด\n2. พยายามให้สัตว์เคลื่อนไหวตัวให้น้อยที่สุด\n3. รีบนำส่งโรงพยาบาลพร้อมรูปถ่ายงู")
    with st.expander("🧪 กรณีได้รับสารพิษ / กินของแปลกปลอม"):
        st.write("1. อย่าพยายามทำให้อาเจียนหากไม่ทราบชนิดสาร\n2. ล้างตัวด้วยน้ำสะอาดหากสารพิษถูกผิวหนัง\n3. นำบรรจุภัณฑ์สารพิษไปให้หมอด้วย")
    st.error("📞 เบอร์ฉุกเฉิน: รพ.สัตว์เกษตร (02-797-1900) | รพ.สัตว์จุฬา (02-218-9750)")

elif menu == "⭐ ประเมินความพึงพอใจ":
    st.header("⭐ สรุปผลความพึงพอใจ")
    
    # ส่วนคำนวณคะแนนเฉลี่ย
    s_df = load_survey()
    if not s_df.empty:
        avg_score = s_df["คะแนน"].mean()
        stars = "⭐" * int(round(avg_score))
        st.markdown(f"""
            <div class='rating-header'>
                <h1 style='color: #FFB300; font-size: 3.5rem; margin-bottom:0;'>{avg_score:.1f} / 5.0</h1>
                <h2 style='margin-top:0;'>{stars}</h2>
                <p>จากผู้ร่วมประเมิน {len(s_df)} ท่าน</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("ยังไม่มีผลการประเมินในขณะนี้ ร่วมเป็นคนแรกที่ประเมินเรา!")

    st.write("---")
    st.subheader("📋 แบบประเมินประสิทธิภาพ (5 ด้าน)")
    q = ["1. รูปแบบสวยงาม", "2. ทำงานถูกต้อง", "3. จัดการไฟล์สะดวก", "4. กราฟเข้าใจง่าย", "5. บันทึกข้อมูลแม่นยำ"]
    
    # แมปคะแนนจากข้อความสไลเดอร์
    score_map = {"น้อย": 1, "ปานกลาง": 2, "มาก": 3, "มากที่สุด": 4, "ยอดเยี่ยม": 5}
    
    with st.form("survey"):
        total_score = 0
        for text in q:
            val = st.select_slider(text, options=["น้อย", "ปานกลาง", "มาก", "มากที่สุด", "ยอดเยี่ยม"], value="มากที่สุด")
            total_score += score_map[val]
        
        if st.form_submit_button("ส่งประเมิน"):
            final_score = total_score / 5 # หาค่าเฉลี่ยของรอบนี้
            save_survey(final_score)
            st.balloons()
            st.success("ขอบคุณสำหรับคำแนะนำครับ!")
            st.rerun() # รีโหลดหน้าเพื่ออัปเดตคะแนนเฉลี่ยด้านบน
