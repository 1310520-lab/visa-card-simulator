import streamlit as st
import base64
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="互動卡片模擬器", layout="wide")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return ""

visa_bg_b64 = get_image_base64("card.png")

# 側邊欄設定
st.sidebar.header("🎛️ 卡片資訊與設定")
card_number = st.sidebar.text_input("卡號 (16 位數)", "4123 4567 8901 2345")
card_holder = st.sidebar.text_input("持卡人英文姓名", "CHIA WEI LIN")
exp_date = st.sidebar.text_input("有效期限 (MM/YY)", "12/28")
cvv_code = st.sidebar.text_input("CVV 安全碼 (背面)", "888")

st.sidebar.markdown("---")
st.sidebar.header("🎨 網頁背景設定")
page_bg_color = st.sidebar.color_picker("網頁背景顏色", "#1e3a5f")

st.sidebar.markdown("---")
st.sidebar.header("📐 正面文字位置微調")
top_num = st.sidebar.slider("卡號 Y 軸位置 (Top)", 50, 220, 155)
left_num = st.sidebar.slider("卡號 X 軸位置 (Left)", 10, 150, 40)
top_name = st.sidebar.slider("姓名 Y 軸位置 (Top)", 100, 260, 215)
left_name = st.sidebar.slider("姓名 X 軸位置 (Left)", 10, 150, 40)

# 動態注入網頁背景顏色
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {page_bg_color};
    }}
    </style>
""", unsafe_allow_html=True)

# 設定正面底圖
front_bg_style = f"url({visa_bg_b64}) center/cover" if visa_bg_b64 else "linear-gradient(135deg, #111827, #1f2937)"

card_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: transparent;
    font-family: 'Courier New', Courier, monospace;
  }}

  .card-container {{
    width: 420px;
    height: 260px;
    perspective: 1000px;
    cursor: pointer;
  }}

  .card-inner {{
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }}

  .card-inner.is-flipped {{
    transform: rotateY(180deg);
  }}

  .card-front, .card-back {{
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 16px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    overflow: hidden;
  }}

  /* 保留 card.png 底圖 */
  .card-front {{
    background: {front_bg_style};
  }}

  .card-number {{
    position: absolute;
    top: {top_num}px;
    left: {left_num}px;
    font-size: 21px;
    font-weight: bold;
    letter-spacing: 2px;
    color: #f3f4f6;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
  }}

  .card-holder {{
    position: absolute;
    top: {top_name}px;
    left: {left_name}px;
    font-size: 15px;
    font-weight: bold;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #f3f4f6;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
  }}

  .card-exp {{
    position: absolute;
    top: {top_name}px;
    left: {left_name + 210}px;
    font-size: 14px;
    font-weight: bold;
    color: #f3f4f6;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
  }}

  /* 背面樣式 */
  .card-back {{
    background: linear-gradient(135deg, #1f2937, #0f172a);
    color: #333;
    transform: rotateY(180deg);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }}

  .stripe {{
    background: #000;
    width: 100%;
    height: 45px;
    margin-top: 25px;
  }}

  .signature-bar {{
    background: #e5e7eb;
    width: 75%;
    height: 35px;
    margin: 20px auto 0 20px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    padding-right: 15px;
    font-family: sans-serif;
    font-weight: bold;
    font-style: italic;
    letter-spacing: 1px;
    color: #111;
    border-radius: 4px;
  }}

  .visa-logo-back {{
    position: absolute;
    bottom: 20px;
    right: 25px;
    font-family: 'Arial', sans-serif;
    font-size: 22px;
    font-weight: 900;
    font-style: italic;
    background: linear-gradient(135deg, #f3e5ab, #d4af37);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
</style>
</head>
<body>

<div class="card-container" id="cardContainer">
  <div class="card-inner" id="cardInner">
    <!-- 正面 -->
    <div class="card-front">
      <div class="card-number">{card_number}</div>
      <div class="card-exp">{exp_date}</div>
      <div class="card-holder">{card_holder}</div>
    </div>
    <!-- 背面 -->
    <div class="card-back">
      <div class="stripe"></div>
      <div class="signature-bar">{cvv_code}</div>
      <div class="visa-logo-back">VISA</div>
    </div>
  </div>
</div>

<script>
  const card = document.getElementById('cardContainer');
  const inner = document.getElementById('cardInner');

  card.addEventListener('click', () => {{
    inner.classList.toggle('is-flipped');
  }});
</script>

</body>
</html>
"""

# 已完全刪除 st.title 標題行
components.html(card_html, height=330)
st.caption("🖱️ 點擊卡片即可輕鬆切換正反面（點一下翻到背面，再點一下翻回正面）")