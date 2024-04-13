import streamlit as st
import glob
import random
import base64
# 画像を表示して選手名を当てるクイズ

# 画像を表示する
# 画像のURLはランダムに選ぶ
# 画像のURLに対応する選手名を選択肢として表示する
# 選手名の選択肢は4つ表示して、選手名を選択する
# 選手名を選択したら正解か不正解かを表示する
# 不正解だったら正解の選手名を表示する
# 正解したら次のクイズに進む

# 選手の画像をランダムに取得する
def get_random_image_paths():
    return random.choice(glob.glob("./imags/*"))

# 画像をBase64に変換する
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


st.title("🏆⚽️プレミアリーグ選手クイズ⚽️🏆")

image_path = get_random_image_paths()
st.markdown(f'<div style="display: flex; justify-content: center;"><img src="data:image/png;base64,{get_image_base64(image_path)}" width="300"/></div>', unsafe_allow_html=True)

options = ["", "ちんぽ", "ぼこた", "リュウタロス", "マクアリスター"]

# セレクトボックスで選択肢を表示
st.selectbox(
    label="選手名はなんでしょう？？",
    options=options,
    index=None,
    placeholder="選手名を選択してください"
)