import streamlit as st
import pandas as pd
import os
import math
from datetime import datetime

# =====================================
# ページ設定
# =====================================
st.set_page_config(
    page_title="交通費計算システム",
    page_icon="🚗",
    layout="wide"
)

# =====================================
# サイドバー設定
# =====================================
st.sidebar.header("⚙ 単価設定")

CAR_FEE = st.sidebar.number_input(
    "車両費",
    min_value=0,
    value=1000
)

FUEL_EFFICIENCY = st.sidebar.number_input(
    "燃費(km/L)",
    min_value=1,
    value=10
)

FUEL_PRICE = st.sidebar.number_input(
    "燃料単価(円)",
    min_value=0,
    value=170
)

# =====================================
# 遠方費設定
# =====================================
st.sidebar.subheader("遠方費設定")

REMOTE_DISTANCE_1 = st.sidebar.number_input(
    "遠方距離①(km)",
    min_value=0,
    value=100
)

REMOTE_FEE_1 = st.sidebar.number_input(
    "遠方費①(円)",
    min_value=0,
    value=3000
)

REMOTE_DISTANCE_2 = st.sidebar.number_input(
    "遠方距離②(km)",
    min_value=0,
    value=150
)

REMOTE_FEE_2 = st.sidebar.number_input(
    "遠方費②(円)",
    min_value=0,
    value=5000
)

REMOTE_DISTANCE_3 = st.sidebar.number_input(
    "遠方距離③(km)",
    min_value=0,
    value=200
)

REMOTE_FEE_3 = st.sidebar.number_input(
    "遠方費③(円)",
    min_value=0,
    value=8000
)

# =====================================
# 管理費設定
# =====================================
MANAGEMENT_RATE = st.sidebar.number_input(
    "管理費(%)",
    min_value=0,
    value=10
)

# =====================================
# Excelファイル名
# =====================================
EXCEL_FILE = "交通費履歴.xlsx"

# =====================================
# タイトル
# =====================================
st.title("🚗 交通費計算システム")

st.caption(
    "警備会社向け交通費・請求管理システム"
)

# =====================================
# 入力フォーム
# =====================================
st.header("📋 入力")

col1, col2 = st.columns(2)

with col1:

    staff_name = st.text_input(
        "隊員名"
    )

    site_name = st.text_input(
        "現場名"
    )

    origin = st.text_input(
        "出発地",
        value="釧路営業所"
    )

with col2:

    destination = st.text_input(
        "目的地"
    )

    distance = st.number_input(
        "片道距離(km)",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    round_trip = st.checkbox(
        "往復計算",
        value=True
    )

# =====================================
# 計算ボタン
# =====================================
if st.button("💰 交通費計算"):

    # -----------------------------
    # 距離計算
    # -----------------------------
    calc_distance = (
        distance * 2
        if round_trip
        else distance
    )

    # -----------------------------
    # 燃料費
    # -----------------------------
    fuel_fee = round(
        (calc_distance / FUEL_EFFICIENCY)
        * FUEL_PRICE
    )

    # -----------------------------
    # 遠方費判定
    # -----------------------------
    if distance >= REMOTE_DISTANCE_3:

        remote_fee = REMOTE_FEE_3

    elif distance >= REMOTE_DISTANCE_2:

        remote_fee = REMOTE_FEE_2

    elif distance >= REMOTE_DISTANCE_1:

        remote_fee = REMOTE_FEE_1

    else:

        remote_fee = 0

    # -----------------------------
    # 実費交通費
    # -----------------------------
    base_fee = (
        CAR_FEE
        + fuel_fee
        + remote_fee
    )

    # -----------------------------
    # 管理費
    # -----------------------------
    management_fee = round(
        base_fee
        * (MANAGEMENT_RATE / 100)
    )

    # -----------------------------
    # 管理費込み合計
    # -----------------------------
    subtotal = (
        base_fee
        + management_fee
    )

    # -----------------------------
    # 100円単位切り上げ
    # -----------------------------
    total_fee = math.ceil(
        subtotal / 100
    ) * 100

    # =====================================
    # 結果表示
    # =====================================
    st.success("✅ 計算完了")

    st.subheader("📊 計算結果")

    st.write(
        f"総走行距離: {calc_distance:.1f} km"
    )

    st.header(
        f"💴 合計請求交通費: {total_fee:,} 円"
    )

    # =====================================
    # 内訳表示
    # =====================================
    breakdown_df = pd.DataFrame({

        "項目": [
            "車両費",
            "燃料費",
            "遠方費",
            f"管理費({MANAGEMENT_RATE}%)",
            "最終請求額"
        ],

        "金額": [
            CAR_FEE,
            fuel_fee,
            remote_fee,
            management_fee,
            total_fee
        ]

    })

    st.table(breakdown_df)

    # =====================================
    # 保存データ
    # =====================================
    save_data = {

        "日時": [datetime.now()],
        "隊員名": [staff_name],
        "現場名": [site_name],
        "出発地": [origin],
        "目的地": [destination],
        "片道距離(km)": [distance],
        "総距離(km)": [calc_distance],
        "車両費": [CAR_FEE],
        "燃料費": [fuel_fee],
        "遠方費": [remote_fee],
        "管理費": [management_fee],
        "請求交通費": [total_fee]

    }

    new_df = pd.DataFrame(save_data)

    # =====================================
    # Excel保存
    # =====================================
    if os.path.exists(EXCEL_FILE):

        old_df = pd.read_excel(EXCEL_FILE)

        combined_df = pd.concat(
            [old_df, new_df],
            ignore_index=True
        )

    else:

        combined_df = new_df

    combined_df.to_excel(
        EXCEL_FILE,
        index=False
    )

    st.success(
        f"📁 {EXCEL_FILE} に保存しました"
    )

# =====================================
# 保存履歴表示
# =====================================
st.markdown("---")

st.header("📄 保存履歴")

# =====================================
# 履歴削除ボタン
# =====================================
if os.path.exists(EXCEL_FILE):

    if st.button("🗑 保存履歴を削除"):

        os.remove(EXCEL_FILE)

        st.success("保存履歴を削除しました")

        st.rerun()

# =====================================
# Excelダウンロード
# =====================================
if os.path.exists(EXCEL_FILE):

    with open(EXCEL_FILE, "rb") as file:

        st.download_button(
            label="📥 Excelダウンロード",
            data=file,
            file_name=EXCEL_FILE,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# =====================================
# 履歴表示
# =====================================
if os.path.exists(EXCEL_FILE):

    history_df = pd.read_excel(EXCEL_FILE)

    st.dataframe(
        history_df,
        use_container_width=True
    )

else:

    st.info(
        "まだ保存履歴はありません"
    )
