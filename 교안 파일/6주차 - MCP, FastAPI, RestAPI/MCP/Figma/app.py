import os

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


@st.cache_resource
def get_engine():
    user = os.environ["MARIADB_USER"]
    password = os.environ["MARIADB_PASSWORD"]
    host = os.environ["MARIADB_HOST"]
    port = os.environ["MARIADB_PORT"]
    database = os.environ["MARIADB_DATABASE"]
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(url)


@st.cache_data(ttl=300)
def load_finance():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM finance ORDER BY trade_date", engine)
    return df


st.set_page_config(page_title="Finance Dashboard", layout="wide")
st.title("주식 시세 대시보드 (finance)")

df = load_finance()

companies = sorted(df["company_name"].unique())
selected = st.sidebar.multiselect("종목 선택", companies, default=companies)

filtered = df[df["company_name"].isin(selected)]

st.subheader("캔들스틱 차트")
for company in selected:
    company_df = filtered[filtered["company_name"] == company].sort_values("trade_date")
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=company_df["trade_date"],
                open=company_df["open_price"],
                high=company_df["high_price"],
                low=company_df["low_price"],
                close=company_df["close_price"],
                name=company,
            )
        ]
    )
    fig.update_layout(title=company, xaxis_rangeslider_visible=False, height=350)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("거래량")
volume_fig = go.Figure()
for company in selected:
    company_df = filtered[filtered["company_name"] == company].sort_values("trade_date")
    volume_fig.add_trace(go.Bar(x=company_df["trade_date"], y=company_df["volume"], name=company))
volume_fig.update_layout(barmode="group", height=400)
st.plotly_chart(volume_fig, use_container_width=True)

st.subheader("원본 데이터")
st.dataframe(filtered, use_container_width=True)
