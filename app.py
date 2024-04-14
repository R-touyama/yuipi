import base64
import random

import streamlit as st

from ansers import players


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


def get_random_selectbox_value_and_option_list() -> tuple:
    """
    問題用に構造化された選手の辞書と、それをセレクトボックスの選択肢を用にランダムに並び替えたリストも返す
    """
    # 選択肢に出す選手を取得
    players_dict = get_random_players_and_img_path(4)
    # 選択肢をランダムにする
    selectbox_list = [players_dict["answer_player"]["name"]] + [
        player["name"] for player in players_dict["fail_players"]
    ]
    random_selectbox_value = random.sample(selectbox_list, 4)

    return players_dict, random_selectbox_value


st.title("🏆⚽️プレミアリーグ選手クイズ⚽️🏆")

# 初回だけここに入る(初期化処理)
if (
    "players_dict" not in st.session_state
    and "score" not in st.session_state
    and "random_selectbox_value" not in st.session_state
):
    # スコアを初期化
    st.session_state["score"] = 0
    st.session_state["players_dict"], st.session_state["random_selectbox_value"] = (
        get_random_selectbox_value_and_option_list()
    )


# 正解となる選手の画像を表示
image_html = '<div style="display: flex; justify-content: center;">'
image_html += '<img src="data:image/png;base64,'
image_html += f'{get_image_base64(st.session_state["players_dict"]["answer_player"]["img_path"])}" width="300"/>'
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
    if user_select == st.session_state["players_dict"]["answer_player"]["name"]:
        st.write("🎉🎉🎉正解です🎉🎉🎉")
        # スコアを加算
        st.session_state["score"] += 1
        # 正解の場合は次の問題の選手を取得
        st.session_state["players_dict"], st.session_state["random_selectbox_value"] = (
            get_random_selectbox_value_and_option_list()
        )
    else:
        st.write(f"😭😭😭不正解です😭😭😭 正解は{st.session_state['players_dict']['answer_player']['name']}でした")
        st.write(f"連続正解数は{st.session_state['score']}でした。\n 記録がリセットされます。")
        # 不正解の場合はスコアをリセット
        st.session_state["score"] = 0
        # 正解の場合は次の問題の選手を取得
        st.session_state["players_dict"], st.session_state["random_selectbox_value"] = (
            get_random_selectbox_value_and_option_list()
        )

# ページ再実行
st.button("次の問題へ進む")
