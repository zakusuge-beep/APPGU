import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from fpdf import FPDF
import base64

# --- 1. SETTINGS & STYLES ---
st.set_page_config(page_title="Smart Pet Care V2", page_icon="🐾", layout="wide")

# Mapping ไอคอนสัตว์ 10 ชนิด
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
    .pet-card {{ background: white; padding: 15px; border-radius: 20px; border-left: 10px solid #FFADAD; box-shadow: 5px 5px 15px rgba(0,0,0,0.05); margin-bottom: 10px; }}
    .status-normal {{ background-color: #D4EDDA; color: #155724; padding: 5px 10px; border-radius: 10px; font-weight: bold; }}
    .status-warning {{ background-color: #FFF3CD; color: #856404; padding: 5px 10px; border-radius: 10px; font-weight: bold; }}
    .credit-footer {{ background-color: #FFDEE9; padding: 20px; border-radius: 20px; border: 2px dashed #FF9A9E; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE FUNCTIONS ---
DB_FILE = "pet_pro_data.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["ID", "ชื่อ", "ประเภท", "น้ำหนัก", "อายุ", "วัคซีน", "นัดหมาย", "วันที่"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

def create_pdf(pet_name, history):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Arial', '', '', unicode=True)
    pdf.set_font('Arial', size=16)
    pdf.cell(200, 10, txt=f"Health Report: {pet_name}", ln=True, align='C')
    pdf.set_font('Arial', size=12)
    for i, row in history.iterrows():
        pdf.cell(200, 10, txt=f"Date: {row['วันที่']} | Weight: {row['น้ำหนัก']} kg | Vaccine: {row['วัคซีน']}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

df = load_data()

# --- 3. SIDEBAR MENU ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🐾 Pet Navigator</h1>", unsafe_allow_html=True)
    menu = st.radio("เลือกเมนูหลัก", ["🏠 หน้าแรก & เครดิต", "➕ ลงทะเบียนสัตว์เลี้ยง", "🔄 อัปเดต & วิเคราะห์สุขภาพ", "🚑 คลังความรู้ฉุกเฉิน", "⭐ ประเมินความพึงพอใจ"])
    st.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=150)

# --- 4. MAIN LOGIC ---
if menu == "🏠 หน้าแรก & เครดิต":
    st.markdown("<h1 class='main-title'>Smart Pet Care & Health Tracker</h1>", unsafe_allow_html=True)
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1: st.info("🐶 บันทึกประวัติแม่นยำ")
    with c2: st.warning("📊 กราฟน้ำหนักรายตัว")
    with c3: st.success("🏥 คู่มือฉุกเฉิน 24 ชม.")
    
    st.markdown("""
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
            new_id = datetime.now().strftime("%H%M%S")
            new_row = pd.DataFrame([[new_id, name, p_type, weight, age, vac, str(app), str(datetime.now().date())]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.balloons()
            st.success(f"ยินดีต้อนรับ {name} {PET_ICONS[p_type]}")

elif menu == "🔄 อัปเดต & วิเคราะห์สุขภาพ":
    if not df.empty:
        pet_list = df["ชื่อ"].unique()
        selected = st.selectbox("เลือกสัตว์เลี้ยงที่ต้องการดูข้อมูล", pet_list)
        history = df[df["ชื่อ"] == selected]
        latest = history.iloc[-1]
        icon = PET_ICONS.get(latest["ประเภท"], "🐾")

        st.markdown(f"<div class='pet-card'><h2>{icon} {selected} ({latest['ประเภท']})</h2></div>", unsafe_allow_html=True)
        
        # 1. ระบบ Badge แจ้งเตือนสุขภาพ
        first_weight = history.iloc[0]["น้ำหนัก"]
        current_weight = latest["น้ำหนัก"]
        diff = ((current_weight - first_weight) / first_weight) * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("น้ำหนักปัจจุบัน", f"{current_weight} kg")
        
        if diff > 15:
            col2.markdown("<span class='status-warning'>⚠️ ระวัง: น้ำหนักเกินเกณฑ์ (เริ่มอ้วน)</span>", unsafe_allow_html=True)
        else:
            col2.markdown("<span class='status-normal'>✅ สุขภาพปกติ (น้ำหนักเหมาะสม)</span>", unsafe_allow_html=True)

        # 2. กราฟเฉพาะตัว
        fig = px.area(history, x="วันที่", y="น้ำหนัก", title=f"📈 แนวโน้มน้ำหนักของ {selected}", markers=True)
        st.plotly_chart(fig, use_container_width=True)

        # 3. ส่งออก PDF
        if st.button("📥 ดาวน์โหลดรายงานสุขภาพ (PDF)"):
            st.info("ระบบกำลังเจนไฟล์ PDF... (ฟังก์ชันส่งออกเป็นข้อมูลสรุป)")
            st.download_button("Click เพื่อโหลดไฟล์", data="Pet Report Data Content", file_name=f"{selected}_report.txt")

        if st.button("🗑️ ลบข้อมูลสัตว์เลี้ยงตัวนี้"):
            df = df[df["ชื่อ"] != selected]
            save_data(df)
            st.rerun()
    else:
        st.info("กรุณาเพิ่มข้อมูลสัตว์เลี้ยงก่อน")

elif menu == "🚑 คลังความรู้ฉุกเฉิน":
    st.header("🚑 คู่มือปฐมพยาบาลสัตว์เลี้ยงเบื้องต้น")
    with st.expander("🐍 กรณีถูกงูกัด / แมลงมีพิษ"):
        st.write("1. ห้ามกรีดแผลหรือดูดพิษเด็ดขาด\n2. พยายามให้สัตว์เคลื่อนไหวตัวให้น้อยที่สุด\n3. รีบนำส่งโรงพยาบาลพร้อมรูปถ่ายงู")
    with st.expander("🧪 กรณีได้รับสารพิษ / กินของแปลกปลอม"):
        st.write("1. อย่าพยายามทำให้อาเจียนหากไม่ทราบชนิดสาร\n2. ล้างตัวด้วยน้ำสะอาดหากสารพิษถูกผิวหนัง\n3. นำบรรจุภัณฑ์สารพิษไปให้หมอด้วย")
    st.error("📞 เบอร์ฉุกเฉิน: รพ.สัตว์เกษตร (02-797-1900) | รพ.สัตว์จุฬา (02-218-9750)")

elif menu == "⭐ ประเมินความพึงพอใจ":
    st.subheader("📋 แบบประเมินประสิทธิภาพ (5 ด้าน)")
    q = [
        "1. โปรแกรมมีการจัดรูปแบบเหมาะสม สวยงาม และน่าใช้งาน",
        "2. การทำงานของโปรแกรมมีความถูกต้องและใช้งานได้จริง",
        "3. ระบบจัดการไฟล์สามารถค้นหาหรือแก้ไขข้อมูลได้สะดวก",
        "4. การแสดงผลด้วยรูปภาพหรือกราฟช่วยให้เข้าใจข้อมูลได้ง่ายขึ้น",
        "5. โปรแกรมสามารถบันทึกและจัดการข้อมูลสัตว์เลี้ยงได้อย่างถูกต้อง"
    ]
    with st.form("survey"):
        for text in q: st.select_slider(text, options=["น้อย", "ปานกลาง", "มาก", "มากที่สุด"])
        if st.form_submit_button("ส่งประเมิน"):
            st.success("บันทึกความพึงพอใจแล้ว! ขอบคุณครับ")
