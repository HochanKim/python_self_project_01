# 데이터 자료 대시보드 구현

# Streamlit 웹 대시보드 실행 파일 불러오기
import streamlit as st
from src.data_loading import df, fault_cnts, fault_types

st.title("Steel Plate Fault Analysis")
st.write("철판 결함 데이터 분석 대시보드")

st.write("데이터 크기:", df.shape)

st.dataframe(df.head())

st.metric(label="전체 데이터 수", value=len(df))
