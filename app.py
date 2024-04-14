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


# 選手の画像と選手名をペアに取得し、構造化して返す引数は取得する選手の数
def get_random_players_and_img_path(num=4) -> dict:
    """
    選手名と画像のパスをランダムに4人取得し、構造化して返す
    """
    random.seed()  # シード値をリセット
    get_random_players_and_img_path = random.sample(list(players.items()), num)

    return {
        "answer_player": {
            "name": get_random_players_and_img_path[0][0],
            "img_path": get_random_players_and_img_path[0][1],
        },
        "fail_players": [
            {"name": get_random_players_and_img_path[1][0], "img_path": get_random_players_and_img_path[1][1]},
            {"name": get_random_players_and_img_path[2][0], "img_path": get_random_players_and_img_path[2][1]},
            {"name": get_random_players_and_img_path[3][0], "img_path": get_random_players_and_img_path[3][1]},
        ],
    }


# 画像をBase64に変換する
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


# def main():
st.title("🏆⚽️プレミアリーグ選手クイズ⚽️🏆")

# 初回だけここに入る初期化処理
if (
    "option_list" not in st.session_state
    and "score" not in st.session_state
    and "random_selectbox_value" not in st.session_state
):
    # 選択肢に出す選手を取得
    st.session_state["option_list"] = get_random_players_and_img_path(4)
    # スコアを初期化
    st.session_state["score"] = 0
    # 選択肢をランダムにする
    selectbox_list = [st.session_state["option_list"]["answer_player"]["name"]] + [
        player["name"] for player in st.session_state["option_list"]["fail_players"]
    ]
    st.session_state["random_selectbox_value"] = random.sample(selectbox_list, 4)

# option_list = st.session_state["option_list"]


image_html = '<div style="display: flex; justify-content: center;">'
image_html += '<img src="data:image/png;base64,'
image_html += f'{get_image_base64(st.session_state["option_list"]["answer_player"]["img_path"])}" width="300"/>'
image_html += "</div>"

st.markdown(image_html, unsafe_allow_html=True)

st.markdown(
    f"<h3 style='text-align: center;'>{st.session_state['score']} 問連続正解中🎉🎉🎉</h1>", unsafe_allow_html=True
)

# セレクトボックスで選択肢を表示
user_select = st.selectbox(
    label="選手名はなんでしょう？？",
    options=st.session_state["random_selectbox_value"],
    index=None,
    placeholder="選手名を選択してください",
)

# 選択肢た選手が正解か不正解かを判定
if user_select:
    if user_select == st.session_state["option_list"]["answer_player"]["name"]:
        st.write("🎉🎉🎉正解です🎉🎉🎉")
        st.session_state["option_list"] = get_random_players_and_img_path()
        st.session_state["score"] += 1
        # 正解したら選択肢をリセット
        st.session_state["random_selectbox_value"] = None
    else:
        st.write(f"😭😭😭不正解です😭😭😭 正解は{st.session_state['option_list']['answer_player']['name']}でした")
        st.write(f"連続正解数は{st.session_state['score']}でした。\n 記録がリセットされます。")
        st.session_state["score"] = 0
        st.session_state["option_list"] = get_random_players_and_img_path()
        # 不正解したら選択肢をリセット
        st.session_state["random_selectbox_value"] = None

# ページ再実行
st.button("次の問題へ進む")
