import streamlit as st
import pandas as pd
import datetime
import os

# データを保存するCSVファイル
FILE_PATH = "workout_log.csv"

# データの読み込み
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    else:
        return pd.DataFrame(columns=["日付", "Squat(回)", "Push-up(回)", "Sit-up(回)", "BackExtension(秒)"])

df = load_data()

st.title("💪 筋トレ記録アプリ")

# 1. 総合計を常に表示（画面上部）
st.subheader("🏆 ワークアウト総合計")
if not df.empty:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Squat", f"{df['Squat(回)'].sum()} 回")
    col2.metric("Push-up", f"{df['Push-up(回)'].sum()} 回")
    col3.metric("Sit-up", f"{df['Sit-up(回)'].sum()} 回")
    col4.metric("Back Extension", f"{df['BackExtension(秒)'].sum()} 秒")
else:
    st.info("データがまだありません。今日の記録を入力してみましょう！")

st.divider()

# 2. 日々の入力ボックス
st.subheader("📝 今日の記録を入力")
with st.form("workout_form"):
    date = st.date_input("日付", datetime.date.today())
    
    c1, c2 = st.columns(2)
    squat = c1.number_input("Squat (回)", min_value=0, step=1)
    pushup = c2.number_input("Push-up (回)", min_value=0, step=1)
    
    c3, c4 = st.columns(2)
    situp = c3.number_input("Sit-up (回)", min_value=0, step=1)
    backext = c4.number_input("Back Extension (秒)", min_value=0, step=10)
    
    submitted = st.form_submit_button("記録を保存")

    if submitted:
        # 新しいデータを追加
        new_data = pd.DataFrame([{
            "日付": date.strftime("%Y-%m-%d"),
            "Squat(回)": squat,
            "Push-up(回)": pushup,
            "Sit-up(回)": situp,
            "BackExtension(秒)": backext
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(FILE_PATH, index=False)
        st.success("記録を保存しました！画面を更新すると合計が反映されます。")
        st.rerun()

# 3. 履歴の表示
st.subheader("📅 過去の記録")
st.dataframe(df.sort_values("日付", ascending=False), use_container_width=True)
