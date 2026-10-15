import base64
import os
from PIL import Image
from string import Template
import streamlit as st
import streamlit.components.v1 as components

# 1. 設定網頁標題
st.set_page_config(
    page_title="Amex Centurion 數位錢包模擬", page_icon="💳", layout="centered"
)

st.title("💳 美國運通黑卡模擬器（3D 翻轉互動版）")
st.markdown("---")


# 2. 自動偵測圖片檔名
def find_card_image():
  for ext in ["png", "jpg", "jpeg", "webp"]:
    filename = f"card.{ext}"
    if os.path.exists(filename):
      return filename
  return None


actual_card_file = find_card_image()

# 側邊欄控制與背面參數設定
with st.sidebar:
  st.header("⚙️ 卡片資訊與設定")
  if actual_card_file:
    st.success(f"✅ 已成功抓到底圖：`{actual_card_file}`")
  else:
    st.error("card.png")

  st.markdown("---")
  st.markdown("🛠️ **正面字體位置微調**")
  num_top = st.slider("卡號 Y 軸位置 (Top)", 50, 200, 130)
  num_left = st.slider("左側卡號 X 軸位置 (Left)", 10, 200, 115)
  name_bottom = st.slider("姓名底部距離 (Bottom)", 10, 100, 42)
  name_left = st.slider("姓名 X 軸位置 (Left)", 10, 200, 115)


def get_image_base64(path):
  if path and os.path.exists(path):
    with open(path, "rb") as f:
      return base64.b64encode(f.read()).decode("utf-8")
  return None


img_b64 = get_image_base64(actual_card_file)

# 3. 主畫面控制面板（正面與背面欄位）
col1, col2 = st.columns(2)
with col1:
  card_num_left = st.text_input("左側卡號", value="3749")
with col2:
  card_num_right = st.text_input("右側卡號", value="71008")

col3, col4 = st.columns(2)
with col3:
  card_name_input = st.text_input("持卡人姓名", value="NICOLAS LEMAITRE")
with col4:
  card_cvv = st.text_input("CVV 安全碼", value="374")

if st.button("使用此卡模擬付款", use_container_width=True, type="primary"):
  st.warning("⚠️ 【模擬安全警告】交易已成功模擬加密授權！")
  st.balloons()

# 背景 CSS 設定
bg_css = (
    f"background-image: url('data:image/png;base64,{img_b64}');"
    " background-size: cover; background-position: center;"
    if img_b64
    else "background: #111;"
)

num_right_left = num_left + 145

# 4. 支援 3D 翻轉的 HTML / CSS / JS 範本
html_template = Template("""
<!DOCTYPE html>
<html translate="no">
<head>
<meta name="google" content="notranslate">
<style>
    body {
        background-color: #0b0f19;
        margin: 0;
        padding: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .scene {
        width: 420px;
        height: 260px;
        perspective: 1000px;
        cursor: pointer;
    }
    
    .card-flipper {
        width: 100%;
        height: 100%;
        position: relative;
        transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
        border-radius: 12px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }
    
    .card-flipper.is-flipped {
        transform: rotateY(180deg);
    }
    
    .card-face {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 12px;
        box-sizing: border-box;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .card-front {
        $bg_css
    }
    
    .card-back {
        background: linear-gradient(135deg, #1c2028 0%, #0d1117 100%);
        transform: rotateY(180deg);
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        padding-top: 15px;
    }
    
    .embossed {
        font-family: 'Courier New', Courier, monospace;
        font-weight: 900;
        color: #f3f4f6;
        text-shadow: 
            1px 1px 1px #ffffff,
            -1px -1px 1px #000000,
            2px 2px 4px rgba(0,0,0,0.9);
        position: absolute;
    }

    .card-num-left {
        top: ${num_top}px;
        left: ${num_left}px;
        font-size: 20px;
        letter-spacing: 3px;
    }
    .card-num-right {
        top: ${num_top}px;
        left: ${num_right_left}px;
        font-size: 20px;
        letter-spacing: 3px;
    }
    .card-holder {
        bottom: ${name_bottom}px;
        left: ${name_left}px;
        font-size: 14px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .mag-stripe {
        width: 100%;
        height: 45px;
        background: #0b0f19;
        margin-bottom: 15px;
        border-top: 1px solid #333;
        border-bottom: 1px solid #333;
    }
    
    .signature-row {
        padding: 0 20px;
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .signature-box {
        flex: 1;
        height: 36px;
        background: #e2e8f0;
        border-radius: 4px;
        display: flex;
        align-items: center;
        padding-left: 12px;
        font-family: 'Brush Script MT', cursive, monospace;
        color: #1a202c;
        font-size: 16px;
        font-weight: bold;
    }
    
    .cvv-box {
        width: 55px;
        height: 36px;
        background: #ffffff;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Courier New', Courier, monospace;
        font-weight: 900;
        color: #000;
        font-size: 16px;
        margin-left: 12px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.3);
    }

    .back-text {
        padding: 0 20px;
        font-size: 9px;
        color: #94a3b8;
        line-height: 1.4;
        font-family: sans-serif;
    }

    .hint {
        margin-top: 12px;
        font-size: 12px;
        color: #94a3b8;
        letter-spacing: 1px;
    }
</style>
</head>
<body>

<div class="scene" onclick="document.getElementById('flipper').classList.toggle('is-flipped');">
    <div class="card-flipper" id="flipper">
        <div class="card-face card-front">
            <div class="embossed card-num-left" translate="no">$card_num_left</div>
            <div class="embossed card-num-right" translate="no">$card_num_right</div>
            <div class="embossed card-holder" translate="no">$name_input</div>
        </div>
        
        <div class="card-face card-back">
            <div class="mag-stripe"></div>
            <div class="signature-row">
                <div class="signature-box" translate="no">$name_input</div>
                <div class="cvv-box" translate="no">$card_cvv</div>
            </div>
            <div class="back-text">
                MEMBER SINCE 85 • USE OF THIS CARD IS SUBJECT TO THE AGREEMENT. AMERICAN EXPRESS NETWORK.
            </div>
        </div>
    </div>
</div>

<div class="hint"></div>

</body>
</html>
""")

card_html = html_template.substitute(
    bg_css=bg_css,
    card_num_left=card_num_left,
    card_num_right=card_num_right,
    name_input=card_name_input,
    card_cvv=card_cvv,
    num_top=num_top,
    num_left=num_left,
    num_right_left=num_right_left,
    name_bottom=name_bottom,
    name_left=name_left,
)

components.html(card_html, height=330)