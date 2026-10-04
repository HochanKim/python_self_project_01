# 데이터 자료 대시보드 구현

# Streamlit 웹 대시보드 실행 파일 불러오기
import streamlit as st
from src.data_loading import df, fault_cnts, fault_types

import matplotlib.pyplot as plt
import seaborn as sns

# 'analysis' 모듈에서 대시보드에 필요한 분석 결과 객체 불러오기
# => 현재 파일이 최상위에 위치하므로 'src.analysis'로 표기
from src.analysis import thickness_fault_ratio, corr, shape_columns_avg


# ===================================================
# 01. 대시보드 기본 설정
# ===================================================

# 대시보드 타이틀
st.title("Steel Plate Fault Analysis")
st.write("철판 결함 데이터 분석 대시보드")

# ===================================================
# 02. 주요 데이터 요약
# ===================================================

# 핵심 지표
col1, col2, col3 = st.columns(3)
data_nums = f"{len(df):,}"  # 천 단위 쉼표

with col1:
    st.metric(label="전체 데이터 수", value=data_nums)

with col2:
    st.metric(label="결함 유형 수", value=len(fault_types))

with col3:
    st.metric(label="최다 발생 결함", value=fault_cnts.index[0])


# ===================================================
# 03. 원본 데이터 확인
# ===================================================

with st.expander("원본 데이터 열어보기"):
    st.write("데이터 크기:", df.shape)
    st.dataframe(df)

# ===================================================
# 04. 결함 유형 선택
# ===================================================

# 셀렉트 박스로 데이터 불러오기
## 셀렉트 박스 옵션 지정 01
selected_fault = st.selectbox(
    label="결함 유형을 선택하세요",
    options=fault_types,
)

## 옵션 적용
### 선택한 결함 데이터 필터링
selected_data_01 = df[df["fault_type"] == selected_fault]

st.write("선택한 결함:", selected_fault)
st.write("데이터 수:", len(selected_data_01))

with st.expander("선택한 결함 데이터 열어보기"):
    st.dataframe(selected_data_01)

# ===================================================
# 05. 분석 변수 선택
# ===================================================

## 셀렉트 박스 옵션 지정 02
analysis_columns = [
    "Pixels_Areas",
    "Sum_of_Luminosity",
    "Steel_Plate_Thickness",
    "Luminosity_Index",
    "Orientation_Index",
    "Edges_Y_Index",
]

selected_columns = st.selectbox(
    label="분석 변수를 선택하세요",
    options=analysis_columns,
)


# ===================================================
# 06. 선택 데이터 분포 시각화
# ===================================================

# 결함 통계를 담을 객체들
col1, col2, col3, col4 = st.columns(4)

# 사용자가 선택한 분석 변수
selected_values_01 = selected_data_01[selected_columns]

# 통계값 계산
mean_value = round(selected_values_01.mean(), 2)
median_value = round(selected_values_01.median(), 2)
minimum_value = round(selected_values_01.min(), 2)
maximum_value = f"{round(selected_values_01.max(), 2):,}"

with col1:
    st.metric(label="평균", value=mean_value)
with col2:
    st.metric(label="중앙값", value=median_value)
with col3:
    st.metric(label="최솟값", value=minimum_value)
with col4:
    st.metric(label="최댓값", value=maximum_value)


### 선택한 결함의 그래프 생성
fig, ax = plt.subplots(figsize=(10, 6))
# fig = 전체 그림판
# ax  = 그림판 안에서 실제 그래프를 그리는 영역
ax.hist(selected_data_01[selected_columns], bins=20)

ax.set_title(
    f"{selected_fault} - {selected_columns} Distribution"
)  # 선택한 결함 유형의 Pixels_Areas 분포
ax.set_xlabel(selected_columns)  # 선택한 결함의 면적 (픽셀 수)
ax.set_ylabel(
    "Count"
)  # 각 Pixels_Areas 구간에 포함된 결함 데이터의 개수 (ex. 0~200 구간: 10개)

st.pyplot(fig)


# ===================================================
# 탭 구현
# ===================================================

tab1, tab2, tab3 = st.tabs(["두께 분석", "상관관계", "형태/방향 분석"])

with tab1:
    st.subheader("두께 분석")
    st.write("두께별 결함 유형을 분석하는 영역입니다.")

    fig_01, ax_01 = plt.subplots(figsize=(15, 9))

    thickness_fault_ratio.plot(kind="bar", stacked=True, ax=ax_01)

    ax_01.set_title("Fault Distribution by Steel Plate Thickness")
    ax_01.set_xlabel("Thickness Group")
    ax_01.set_ylabel("Fault Ratio (%)")

    ax_01.tick_params(axis="x", rotation=0)

    fig_01.tight_layout()

    st.pyplot(fig_01)


with tab2:
    st.subheader("상관관계")
    st.write("숫자형 변수 간의 상관관계를 분석하는 영역입니다.")

    fig_02, ax_02 = plt.subplots(figsize=(15, 9))

    sns.heatmap(corr, ax=ax_02)

    ax_02.set_title("Correlation Heatmap")

    fig_02.tight_layout()

    st.pyplot(fig_02)

with tab3:
    st.subheader("형태/방향 분석")
    st.write("결함의 형태와 방향에 따른 결함을 분석하는 영역입니다.")

    fig_03, ax_03 = plt.subplots(figsize=(15, 9))

    shape_columns_avg.plot(kind="bar", stacked=False, ax=ax_03)

    ax_03.set_title("Average Indicators of Form/Orientation by Fault Type")
    ax_03.set_xlabel("Fault Type")
    ax_03.set_ylabel("Average Value")

    ax_01.tick_params(axis="x", rotation=45)

    fig_01.tight_layout()

    st.pyplot(fig_03)
