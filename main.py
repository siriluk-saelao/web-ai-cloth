import streamlit as st
import pandas as pd
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.preprocessing import LabelEncoder

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ระบบแนะนำการแต่งกาย AI", layout="wide")

# ==========================================
# ส่วนที่ 1: เตรียมความรู้เรื่องสีมงคล (ปี 2569)
# ==========================================
# ข้อมูลนี้จะถูกนำไปใช้ผสมผสานตอนสร้าง "ข้อมูลตัวอย่าง" ให้ AI เรียนรู้
lucky_colors_db = {
    "วันอาทิตย์": ["สีเขียว", "สีชมพู", "สีดำ"],
    "วันจันทร์": ["สีม่วง", "สีส้ม", "สีฟ้า"],
    "วันอังคาร": ["สีส้ม", "สีดำ", "สีแดง"],
    "วันพุธ": ["สีเขียว", "สีเหลือง", "สีฟ้า"],
    "วันพฤหัสบดี": ["สีแดง", "สีฟ้า", "สีเขียว"],
    "วันศุกร์": ["สีชมพู", "สีขาว", "สีส้ม"],
    "วันเสาร์": ["สีฟ้า", "สีแดง", "สีน้ำตาล"]
}

# ==========================================
# ส่วนที่ 2: จำลองข้อมูลตัวอย่าง 100 คน (Data Generation)
# ==========================================
@st.cache_data
def generate_data(n=100):
    data = []
    
    # ตัวเลือกต่างๆ
    days = list(lucky_colors_db.keys())
    occasions = ["ชีวิตประจำวัน", "งานบวช", "งานแต่ง", "งานศพ", "งานบุญ", "ทางการ"]
    genders = ["ชาย", "หญิง"]
    weathers = ["ร้อน", "หนาว", "ฝน"]

    # เริ่มสร้างข้อมูลทีละคนจนครบ n คน (Loop)
    for i in range(n):
        # สุ่มสถานการณ์
        day = random.choice(days)
        occ = random.choice(occasions)
        gen = random.choice(genders)
        wea = random.choice(weathers)
        
        # --- Logic จำลองความจริง (Simulator) ---
        # ตรงนี้คือการจำลองว่า "คนปกติเขาแต่งตัวกันยังไง" เพื่อสร้างเป็นข้อมูลให้ AI เรียน
        # AI จะไม่เห็นโค้ดส่วนนี้ มันจะเห็นแค่ตารางผลลัพธ์สุดท้าย
        
        recommended_outfit = ""
        
        # เลือกสีมงคลมา 1 สีเพื่อใช้ประกอบชุด (ถ้าไม่ใช่โอกาสที่บังคับสี)
        lucky_color = random.choice(lucky_colors_db[day])

        if occ == "งานศพ":
            # กฎสังคม: งานศพต้องดำ
            if gen == "ชาย":
                recommended_outfit = "เสื้อเชิ้ตดำ กางเกงสแล็คดำ รองเท้าคัทชู"
            else:
                recommended_outfit = "เดรสสีดำสุภาพคลุมเข่า รองเท้าหุ้มส้น"
        
        elif occ in ["งานบวช", "งานบุญ"]:
            # กฎสังคม: เน้นขาว/ครีม/สุภาพ
            tone = random.choice(["สีขาว", "สีครีม", "สีนวล"])
            if gen == "ชาย":
                recommended_outfit = f"เสื้อเชิ้ต{tone} กางเกงสแล็คสุภาพ"
            else:
                recommended_outfit = f"เสื้อลูกไม้{tone} ผ้าถุงหรือกระโปรงยาว"

        elif occ == "งานแต่ง":
            # กฎสังคม: ห้ามดำ ห้ามขาวล้วน เน้นสีสดใส/มงคล
            theme_color = lucky_color
            if theme_color in ["สีดำ", "สีขาว"]: 
                theme_color = "สีชมพูโอรส" # เปลี่ยนสีถ้าบังเอิญสุ่มโดนสีต้องห้าม
            
            if gen == "ชาย":
                if wea == "ร้อน":
                    recommended_outfit = f"สูทลินิน{theme_color} เสื้อยืดด้านใน รองเท้า Loafer"
                else:
                    recommended_outfit = f"ชุดสูทสากล{theme_color} เนคไทเข้าชุด"
            else:
                recommended_outfit = f"ชุดราตรี{theme_color} รองเท้าส้นสูง (ธีมงานมงคล)"

        elif occ == "ทางการ":
            # กฎสังคม: สุภาพ เรียบร้อย
            if gen == "ชาย":
                recommended_outfit = f"สูทสีกรมท่าหรือเทา เสื้อเชิ้ตขาว รองเท้าหนัง"
            else:
                recommended_outfit = f"สูทผู้หญิง{lucky_color}เข้ม กระโปรงทรงสอบ รองเท้าคัทชู"

        else: # ชีวิตประจำวัน
            # ตามสภาพอากาศ + สีมงคล
            if gen == "ชาย":
                if wea == "ร้อน":
                    recommended_outfit = f"เสื้อยืด{lucky_color} กางเกงขาสั้นผ้าชิโน"
                elif wea == "ฝน":
                    recommended_outfit = f"เสื้อยืดสีเข้มทับด้วยแจ็คเก็ตกันน้ำ กางเกงขาสั้น"
                else: # หนาว
                    recommended_outfit = f"เสื้อฮู้ดดี้{lucky_color} กางเกงยีนส์ขายาว"
            else: # หญิง
                if wea == "ร้อน":
                    recommended_outfit = f"เสื้อสายเดี่ยว{lucky_color} กางเกงลินินขายาว"
                elif wea == "ฝน":
                    recommended_outfit = f"เสื้อยืด{lucky_color} กางเกงสามส่วน รองเท้ายาง"
                else: # หนาว
                    recommended_outfit = f"เสื้อไหมพรม{lucky_color} กางเกงยีนส์ บุ๊ทสั้น"

        # บันทึกข้อมูลลงรายการ
        data.append([day, occ, gen, wea, recommended_outfit])
    
    return pd.DataFrame(data, columns=['วัน', 'โอกาส', 'เพศ', 'สภาพอากาศ', 'ชุดที่แนะนำ'])

# สร้างข้อมูล 100 แถว
df = generate_data(100)

# ==========================================
# ส่วนที่ 3: สร้างสมอง AI (Decision Tree)
# ==========================================

# 1. แปลงข้อความเป็นตัวเลข (Encoding)
le_day = LabelEncoder()
le_occ = LabelEncoder()
le_gen = LabelEncoder()
le_wea = LabelEncoder()

# สร้างตารางสำหรับสอน AI (X)
X = pd.DataFrame()
X['วัน'] = le_day.fit_transform(df['วัน'])
X['โอกาส'] = le_occ.fit_transform(df['โอกาส'])
X['เพศ'] = le_gen.fit_transform(df['เพศ'])
X['สภาพอากาศ'] = le_wea.fit_transform(df['สภาพอากาศ'])

# คำตอบที่ต้องการให้ AI จำ (y)
y = df['ชุดที่แนะนำ']

# 2. สอนโมเดล (Training)
# ขั้นตอนนี้ AI จะอ่านตาราง X และ y แล้วสร้างกฎการตัดสินใจขึ้นมาเอง
model = DecisionTreeClassifier(criterion='entropy', max_depth=12, random_state=42)
model.fit(X, y)

# ==========================================
# ส่วนที่ 4: หน้าจอใช้งาน (User Interface)
# ==========================================

st.header("ระบบ AI เลือกชุดตามโอกาสและสีมงคล (Machine Learning)")
st.write("ระบบใช้โมเดล Decision Tree เรียนรู้จากข้อมูลตัวอย่าง 100 รายการ เพื่อแนะนำชุดที่เหมาะสมที่สุด")

col1, col2 = st.columns(2)

with col1:
    st.subheader("ระบุข้อมูลของคุณ")
    in_day = st.selectbox("วันนี้วันอะไร", df['วัน'].unique())
    in_occ = st.selectbox("โอกาสที่จะไป", df['โอกาส'].unique())
    in_gen = st.selectbox("เพศ", df['เพศ'].unique())
    in_wea = st.selectbox("สภาพอากาศ", df['สภาพอากาศ'].unique())

with col2:
    st.subheader("ผลลัพธ์การวิเคราะห์")
    
    if st.button("ให้ AI เลือกชุดให้", type="primary"):
        # 1. แปลงข้อมูลที่เลือกเป็นตัวเลข (เพื่อให้เหมือนตอนสอน AI)
        input_data = [
            le_day.transform([in_day])[0],
            le_occ.transform([in_occ])[0],
            le_gen.transform([in_gen])[0],
            le_wea.transform([in_wea])[0]
        ]
        
        # 2. ให้ AI ทำนายผล (Predict)
        # สังเกตว่าตรงนี้ไม่มี if-else เลือกชุดเลย เราถาม model ตรงๆ
        prediction = model.predict([input_data])
        
        # 3. แสดงผล
        st.success(f"ชุดที่แนะนำ: {prediction[0]}")
        
        # อธิบายเพิ่มเติม
        st.write("---")
        st.write("**ทำไม AI ถึงเลือกชุดนี้?**")
        st.write(f"AI วิเคราะห์จากแพทเทิร์นข้อมูล พบว่าเมื่อเป็น **{in_occ}** + **{in_gen}** + **{in_wea}** ชุดนี้มีความเหมาะสมที่สุด")
        
        # แสดงสีมงคลประกอบ (ดึงจากฐานข้อมูลมาโชว์เฉยๆ เพื่อให้ความรู้)
        lucky = lucky_colors_db[in_day]
        st.info(f"เกร็ดความรู้: สีมงคลประจำ{in_day} คือ {', '.join(lucky)}")

# ==========================================
# ส่วนที่ 5: แสดงหลักฐานการเรียนรู้ (Data)
# ==========================================
st.write("---")
with st.expander("ดูข้อมูลตัวอย่าง 100 รายการที่ AI ใช้เรียนรู้ (Training Data)"):
    st.write("นี่คือข้อมูลที่สร้างขึ้นจำลองตามกฎระเบียบสังคมไทย เพื่อให้ AI นำไปสร้างโมเดล")
    st.dataframe(df)

with st.expander("ดูโครงสร้างการตัดสินใจของ AI (Tree Visualization)"):
    # แสดงโครงสร้างต้นไม้แบบข้อความ
    tree_rules = tree.export_text(model, feature_names=['วัน', 'โอกาส', 'เพศ', 'สภาพอากาศ'])
    st.text(tree_rules)