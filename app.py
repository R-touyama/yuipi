import base64
import random

import streamlit as st

from ansers import players

# 画像を表示して選手名を当てるクイズ

# 画像を表示する
# 画像のURLはランダムに選ぶ
# 画像のURLに対応する選手名を選択肢として表示する
# 選手名の選択肢は4つ表示して、選手名を選択する
# 選手名を選択したら正解か不正解かを表示する
# 不正解だったら正解の選手名を表示する
# 正解したら次のクイズに進む


# 選手の画像をランダムに取得する
def get_random_players_and_img_path() -> list[tuple[str, str]]:
    """
    選手名と画像のパスをランダムに4人取得する
    ex.
    [
        ["選手名", "画像のパス"],
        ["選手名", "画像のパス"],
        ["選手名", "画像のパス"],
        ["選手名", "画像のパス"]
    ]
    """
    random.seed()  # シード値をリセット
    return random.sample(list(players.items()), 4)


# 画像をBase64に変換する
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


# def main():
st.title("🏆⚽️プレミアリーグ選手クイズ⚽️🏆")

# Streamlitのセッション状態を取得または初期化
if "option_list" not in st.session_state:
    st.session_state["option_list"] = get_random_players_and_img_path()
    st.session_state["score"] = 0

option_list = st.session_state["option_list"]

# 正解の選手名
answer_player = {
    "name": option_list[0][0],
    "img_path": option_list[0][1],
}

# 不正解の選手名
fail_players = {
    "name": [player[0] for player in option_list[1:]],
    "img_path": [player[1] for player in option_list[1:]],
}

image_html = '<div style="display: flex; justify-content: center;">'
image_html += f'<img src="data:image/png;base64,{get_image_base64(answer_player["img_path"])}" width="300"/>'
image_html += "</div>"

st.markdown(image_html, unsafe_allow_html=True)

# st.write(f"{st.session_state['score']} 問連続正解中🎉🎉🎉")
st.markdown(
    f"<h3 style='text-align: center;'>{st.session_state['score']} 問連続正解中🎉🎉🎉</h1>", unsafe_allow_html=True
)


option = [answer_player["name"]] + fail_players["name"]

# セレクトボックスで選択肢を表示
user_select = st.selectbox(
    label="選手名はなんでしょう？？", options=option, index=None, placeholder="選手名を選択してください"
)

# 選択肢た選手が正解か不正解かを判定
if user_select:
    if user_select == answer_player["name"]:
        st.write("🎉🎉🎉正解です🎉🎉🎉")
        st.session_state["option_list"] = get_random_players_and_img_path()
        st.session_state["score"] += 1
    else:
        st.write(f"😭😭😭不正解です😭😭😭 正解は{answer_player['name']}でした")
        st.write(f"連続正解数は{st.session_state['score']}でした。\n 記録がリセットされます。")
        st.session_state["score"] = 0
        st.session_state["option_list"] = get_random_players_and_img_path()

# ページ再実行
st.button("次の問題へ進む")
