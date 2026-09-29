# 준비된 데이터를 이용해 결과를 계산하는 py 파일

import pandas as pd

# 'data_loading' 모듈에서 데이터 분석에 필요한 객체 불러오기
from data_loading import df, fault_cnts, fault_types

# ===================================================
# 02. 데이터 분석 - 철판 결함 유형별 발생 현황
# ===================================================

# 각 결함 비율
fault_ratio = (fault_cnts / len(df)) * 100
fault_ratio = fault_ratio.round(2)

# 결함 요약
fault_summary = pd.DataFrame(
    {
        "fault_type": fault_cnts.index,
        "count": fault_cnts.values,
        "ratio": fault_ratio.values,
    }
)

# ===================================================
# Pixels_Areas 분석
# - 평균
pxl_a_avg = df.groupby("fault_type")["Pixels_Areas"].mean()

# - 타입별 정보
pxl_a_decrib = df.groupby("fault_type")["Pixels_Areas"].describe()
# ===================================================

# ===================================================
# Sum_of_Luminosity별 분석
# - 평균
sol_a_avg = df.groupby("fault_type")["Sum_of_Luminosity"].mean()

# - x축 결함 종류들의 배치 순서 조정 (첫 번째 그래프와 통일)
sol_a_avg = sol_a_avg.reindex(fault_types)

# - 타입별 정보
sol_a_decrib = df.groupby("fault_type")["Sum_of_Luminosity"].describe()
# ===================================================

# ===================================================
# Steel_Plate_Thickness 분석
# - 평균
thick_a_avg = df.groupby("fault_type")["Steel_Plate_Thickness"].mean()

# x축 결함 종류들의 배치 순서 조정
thick_a_avg = thick_a_avg.reindex(fault_cnts.index)

# - 타입별 정보
thick_a_decrib = df.groupby("fault_type")["Steel_Plate_Thickness"].describe()
# ===================================================

# ===================================================
# 철판 두께 분류
df["Thickness_Group"] = pd.cut(
    df["Steel_Plate_Thickness"],
    # 기준점 설정 (두께 39 / 60 / 100 / 300)
    # 39 < 값 ≤ 60       → Thin
    # 60 < 값 ≤ 100      → Medium
    # 100 < 값 ≤ 300     → Thick
    bins=[39, 60, 100, 300],
    # 두께 명칭 설정
    labels=["Thin", "Medium", "Thick"],
)

# 각 철판 두께 그룹에서 어떤 결함들이 몇 개씩 발생했는가?
thickness_fault = pd.crosstab(df["Thickness_Group"], df["fault_type"])

# crosstab() 데이터 비율 만들기
thickness_fault_ratio = (
    # normalize="index": 각 행(row)의 합이 1이 되도록 행 기준 비율을 구합니다. ("각 행의 합계를 100%로 만들어라.")
    pd.crosstab(df["Thickness_Group"], df["fault_type"], normalize="index") * 100
)
# ===================================================

# ===================================================
# 결함 종류 별 Luminosity_Index 평균치 계산
luminosity_avg = df.groupby("fault_type")["Luminosity_Index"].mean()

# 결함 종류 별 Luminosity_Index 값 분포 파악
luminosity_describe = df.groupby("fault_type")["Luminosity_Index"].describe()
# ===================================================

# ===================================================
# 여러 숫자 데이터의 상관관계를 한꺼번에 계산
corr = df.corr(numeric_only=True).round(3)

# Sum_of_Luminosity와 Luminosity_Index의 상관관계 확인
lum_corr = df["Sum_of_Luminosity"].corr(df["Luminosity_Index"])
# ===================================================

# ===================================================
# 결함 형태 데이터열
shape_columns = ["Edges_Index", "Edges_X_Index", "Edges_Y_Index", "Orientation_Index"]

# 결함 유형별 형태/방향 관련 변수의 평균
shape_columns_avg = df.groupby("fault_type")[shape_columns].mean()

# 기존 결함 순서로 통일
shape_columns_avg = shape_columns_avg.reindex(fault_types)
# ===================================================

if __name__ == "__main__":
    print(fault_summary)
    print()
    print(thickness_fault_ratio.round(2))
    print()
    print(shape_columns_avg.round(3))
