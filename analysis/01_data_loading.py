import pandas as pd  # pandas 가져오기 (데이터 불러오기, 계산 등)
import matplotlib.pyplot as plt  # matplotlib.pyplot 가져오기 (그래프, 그림과 같은 인터페이스 등)
import matplotlib.font_manager as fm  # 그래프에 노출할 폰트 설정

# 폰트 파일 경로
font_path = "../fonts/NanumGothic-Regular.ttf"

# 폰트 파일을 'matplotlib' 모듈에 등록하기 (addfont())
fm.fontManager.addfont(font_path)

# 그래프에 사용할 폰트 설정 (font 변수에 경로 값 담기)
font = fm.FontProperties(fname=font_path)

# 등록된 폰트를 전체 그래프에 적용
plt.rcParams["font.family"] = font.get_name()
# 음수('-') 기호 깨짐 방지
plt.rcParams["axes.unicode_minus"] = False

# ===================================================
# 01. 데이터 준비 및 가공
# ===================================================

# 데이터 파일 불러오기
df = pd.read_csv("../data/Faults.NNA", sep=r"\s+", header=None)
# => r'\s+'는 공백이 하나 이상 있는 곳을 구분자로 사용
# => sep=r"\s+":  탭이나 스페이스바가 여러 번 들어간 정렬되지 않은 공백 데이터도 깔끔하게 잘라주는 역할
# => header=None: 파일의 첫 번째 줄을 헤더로 사용 금지 => 열의 헤더가 숫자로 자동 지정

# print(df.shape)
# print(df.head())
# print(df.info())

# 컬럼명 모음 불러오기
columns = pd.read_csv("../data/Faults27x7_var", sep=r"\s+", header=None)
# print(columns.values)
# print(columns.shape)


# 컬럼명들을 데이터 프레임에 적용하기
df.columns = columns.iloc[:, 0].tolist()
# iloc[:, 0]: '모든 행, 0번째 열'을 가져오겠다
# tolist(): 리스트로 변환

# print(df.columns.tolist())
# print(df.head())  # 숫자로 임시 적용한 열 헤더가 컬럼명으로 정상적으로 변경
# print(df.shape) # 행열 확인
# print(df.dtypes)  # 각각 열들의 자료형 확인
# print(df.isnull().sum())  # 결측치 확인
# print(df.duplicated().sum())  # 중복값 확인
# print(df.describe())  # 데이터값의 대략적인 분포

## 제조, 조제품 검사, 표면 상태 점검(결함/결함 유형 분류) 등에서 사용되는 용어들
# => 뒷부분 컬럼명의 헤더
"""
Pastry (페이스트리): 표면 검사나 불량 분류 문맥에서는 반죽 찌꺼기나 얼룩 같은 오염을 의미하기도 합니다.
Z_Scratch (Z형 스크래치): 표면에 알파벳 Z자 모양으로 난 긁힘(흠집)을 의미합니다.
K_Scratch (K형 스크래치): 표면에 알파벳 K자 모양으로 난 긁힘(흠집)을 의미합니다.
Stains (얼룩): 액체 등이 묻어서 생긴 오염이나 자국을 뜻합니다.
Dirtiness (오염도/더러움): 먼지나 이물질 등이 묻어 지저분해진 상태를 의미합니다.
Bumps (요철/볼록한 부분): 표면이 평평하지 않고 볼록하게 튀어나온 부분이나 혹을 뜻합니다.
Other_Faults (기타 결함): 위에 분류된 항목 외에 나머지 불량이나 결함들을 모아놓은 항목입니다.

"""

# 결함 데이터들을 담은 열 헤더 모음
fault_columns = [
    "Pastry",
    "Z_Scratch",
    "K_Scatch",
    "Stains",
    "Dirtiness",
    "Bumps",
    "Other_Faults",
]

# print(df[fault_columns])

fault_count = df[fault_columns].sum(axis=1)  # 결함 데이터 열(axis=1)들의 데이터 합 계산
# print(fault_count.value_counts())  # 1    1941
# => 1941개의 각 행마다 7개의 결함 컬럼 값을 합산한 결과가 모두 1이다.
# 즉, 각 데이터에는 정확히 하나의 결함 유형만 1로 표시되어 있다. => 결함이 2개 이상이거나 결함이 없는 데이터는 없음


# 가장 큰 값을 가지고 있는 열을 행을 뒤지면서 찾기
df["fault_type"] = df[fault_columns].idxmax(
    axis=1
)  # idxmax(): 가장 큰 값을 가지고 있는 컬럼의 이름을 찾아주는 기능
# print(df["fault_type"])
# print(df[fault_columns])
# print(df.shape) # (1941, 35): 열 1개 증가 (fault_type)

# 각 결함 유형이 몇 개씩 존재하는가?
# => 각 결함 발생 건수
fault_cnts = df["fault_type"].value_counts()
# print(df["fault_type"].value_counts())
# # 총 개수 대조하기 (1941 개)
# print(df["fault_type"].value_counts().sum())  # 1941


# ===================================================
# 02. 데이터 분석 - 철판 결함 유형별 발생 현황
# ===================================================

# 각 결함 비율
fault_ratio = (fault_cnts / len(df)) * 100
# 소수점 절삭 (둘째자리)
fault_ratio = fault_ratio.round(2)
# print(fault_ratio.round(2))

# 결함 데이터 프레임
fault_summary = pd.DataFrame(
    {
        "fault_type": fault_cnts.index,
        "count": fault_cnts.values,
        "ratio": fault_ratio.values,
    }
)
# 생성한 결함 df 확인
# print(fault_summary)

# 결함 df를 csv 파일로 내보내기
fault_summary.to_csv("../data/fault_summary.csv", index=False, encoding="utf-8-sig")

# ===================================================
# 03. 결함 데이터의 시각화 - 그래프화
# ===================================================

# 그래프를 위한 bar 생성
# 목적: 결함 종류별 "얼마나 많이 발생했는가?"

# 시각화 자료 크기 조정
plt.figure(figsize=(10, 6))

# => (가로축: 결함 종류(fault_type), 세로축: 발생 건수(count))
plt.bar(fault_cnts.index, fault_summary["count"])

plt.title("Steel Plate Fault Distribution (철강 결함 분류)")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("Count (결함 개수)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()  # 결과물 보여주기 (bar - 그래프)

# fault_type별로 그룹을 만들어서 각 그룹의 Pixels_Areas(결함 면적) 평균 계산
# => pd.groupby(): 특정 기준 데이터를 그룹으로 묶어서 다음 그룹별(특정 열의 데이터들) 계산을 수행
pxl_a_avg = df.groupby("fault_type")["Pixels_Areas"].mean()
# print(round(pxl_a_avg, 2))

# 타입별 정보 불러오기 (개수, 평균, 중앙값 등등) - Pixels_Areas
pxl_a_decrib = df.groupby("fault_type")["Pixels_Areas"].describe()
# print(pxl_a_decrib)

# ===================================================
# 03. 결함 데이터의 시각화 - Box Plot
# ===================================================

# 'Box Plot'으로 평균값에 큰 영향을 주는 이상값의 분포를 알아내기 위한 시각화 자료
# 목적: 결함 종류별 "데이터가 어떻게 분포하는가?"
# 결함 데이터 묶기 (group 리스트 생성)

# 데이터 담는 빈 리스트
groups = []

# 결함 종류 (모든 Box Plot에 적용)
fault_types = fault_cnts.index


# 시각화 자료 크기 조정
plt.figure(figsize=(10, 6))

for fault in fault_types:
    # print(fault)
    groups.append(df[df["fault_type"] == fault]["Pixels_Areas"])
plt.boxplot(groups)  # boxplot 적용
plt.xticks(
    # fault_type의 개수 체크
    range(1, len(fault_types) + 1),
    # 결함 종류
    fault_types,
    rotation=45,
)
plt.title("Fault Type별 Pixels_Areas 분포")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("Pixels_Areas")
plt.show()  # 결과물 보여주기 (boxplot)

# ===================================================
# 04. 데이터 분석 - 철판 결함 유형별 밝기 특성 확인
# ===================================================

# fault_type별로 그룹을 만들어서 각 그룹의 Sum_of_Luminosity(철판 결함 유형별 밝기) 평균 계산
sol_a_avg = df.groupby("fault_type")["Sum_of_Luminosity"].mean()
# x축 결함 종류들의 배치 순서 조정 (첫 번째 그래프와 통일)
sol_a_avg = sol_a_avg.reindex(fault_cnts.index)

# 타입별 정보 불러오기 (개수, 평균, 중앙값 등등) - Sum_of_Luminosity
sol_a_decrib = df.groupby("fault_type")["Sum_of_Luminosity"].describe()


# 시각화 자료 크기 조정
plt.figure(figsize=(10, 6))

# Sum_of_Luminosity의 bar graph
# => (가로축: 결함 종류(fault_type), 세로축: 각 결함 평균 (Sum_of_Luminosity))
plt.bar(sol_a_avg.index, sol_a_avg.values)

plt.title("Sum_of_Luminosity (철판 결함 유형별 밝기)")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("AVG of SoL (각 결함 평균)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()  # 결과물 보여주기 (bar - 그래프)


# Sum_of_Luminosity의 boxplot
groups = []  # 리스트 초기화


for fault in fault_types:
    # print(fault)
    groups.append(df[df["fault_type"] == fault]["Sum_of_Luminosity"])
plt.boxplot(groups)
plt.xticks(
    # fault_type의 개수 체크
    range(1, len(fault_types) + 1),
    # 결함 종류
    fault_types,
    rotation=45,
)
plt.title("Fault Type별 Sum_of_Luminosity 분포")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("Sum_of_Luminosity")
plt.show()  # 결과물 보여주기 (boxplot)


# ===================================================
# 05. 데이터 분석 - 철판 두께와 결함 유형 사이의 관계
# ===================================================

# 각 그룹의 Steel_Plate_Thickness(철판 두께와 결함 유형 사이의 관계) 평균 계산
thick_a_avg = df.groupby("fault_type")["Steel_Plate_Thickness"].mean()
# x축 결함 종류들의 배치 순서 조정
thick_a_avg = thick_a_avg.reindex(fault_cnts.index)

# 타입별 정보 불러오기 (개수, 평균, 중앙값 등등) - Steel_Plate_Thickness
thick_a_decrib = df.groupby("fault_type")["Steel_Plate_Thickness"].describe()


# 시각화 자료 크기 조정
plt.figure(figsize=(10, 6))

# Steel_Plate_Thickness의 bar graph
# => (가로축: 결함 종류(fault_type), 세로축: 각 결함 평균(Steel_Plate_Thickness))
plt.bar(thick_a_avg.index, thick_a_avg.values)

plt.title("Steel_Plate_Thickness (철판 두께와 결함 유형 사이의 관계)")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("AVG of SPT (각 결함 평균)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()  # 결과물 보여주기 (bar - 그래프)

# Steel_Plate_Thickness의 boxplot
groups = []  # 리스트 초기화

for fault in fault_types:
    # print(fault)
    groups.append(df[df["fault_type"] == fault]["Steel_Plate_Thickness"])
plt.boxplot(groups)
plt.xticks(
    # fault_type의 개수 체크
    range(1, len(fault_types) + 1),
    # 결함 종류
    fault_types,
    rotation=45,
)
plt.title("Fault Type별 Steel_Plate_Thickness 분포")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("Steel_Plate_Thickness")
plt.show()  # 결과물 보여주기 (boxplot)

# ===================================================
# 06. 결함 데이터의 시각화 - Scatter Plot
# ===================================================
# 목적: 두 변수 사이에 "관계가 있는가?"


# 시각화 자료 크기 조정
plt.figure(figsize=(18, 15))

# 결함 별 색깔 표현하기
# 색 지정 딕셔너리 colors
colors = {
    "Other_Faults": "red",
    "Bumps": "blue",
    "K_Scatch": "green",
    "Z_Scratch": "orange",
    "Pastry": "purple",
    "Stains": "brown",
    "Dirtiness": "black",
}
for fault in fault_types:
    fault_data = df[df["fault_type"] == fault]
    # 결함 면적과 밝기의 상관 관계를 시각화하기
    plt.scatter(
        fault_data["Pixels_Areas"],
        fault_data["Sum_of_Luminosity"],
        color=colors[fault],
        alpha=0.5,
        label=fault,
    )

plt.legend()  # 범례 설정
plt.show()

# 이상치 추적
# print(df[df["fault_type"] == "K_Scatch"]["Pixels_Areas"].max())


# ===================================================
# 07. 두 데이터의 상관관계 확인
# ===================================================
# print(df["Pixels_Areas"].corr(df["Sum_of_Luminosity"]).round(2))  # 0.98

# K-Scatch의 'Pixels_Areas-Sum_of_Luminosity' 상관 관계
# kscatch = df[df["fault_type"] == "K_Scatch"]
# print(kscatch["Pixels_Areas"].corr(kscatch["Sum_of_Luminosity"]).round(2))  # 0.97

# K-Scatch 포함 'Pixels_Areas-Sum_of_Luminosity' 상관 관계
for fault in fault_types:
    # 결함 유형 데이터 담기
    fault_data = df[df["fault_type"] == fault]
    # 상관관계
    correlation = fault_data["Pixels_Areas"].corr(fault_data["Sum_of_Luminosity"])

    # print(f"{fault}: {correlation:.4f}")

# 여러 숫자 데이터의 상관관계를 한꺼번에 계산
# => 숫자형 열들만 골라서 계산 (numeric_only=True)
corr = df.corr(numeric_only=True).round(3)

# 라이브러리 호출 (Seaborn)
import seaborn as sns


# 시각화 자료 크기 조정
plt.figure(figsize=(18, 15))

# 상관관계 히트맵 사용
# => 상관계수 숫자를 그래프 안에 표시 (annot=True)
# => 히트맵 내부 숫자 사이즈 조정 (annot_kws={"size": 8})
sns.heatmap(corr, annot=True, annot_kws={"size": 8})

# 만들어진 히트맵 호출
plt.show()

# 상관관계 파악
# print(corr)

# 강한 상관관계 파악 (1)
# plt.figure(figsize=(8, 6))
# plt.scatter(df["X_Minimum"], df["X_Maximum"], alpha=0.5)
# plt.title("X_Minimum vs X_Maximum")
# plt.xlabel("X_Minimum")
# plt.ylabel("X_Maximum")
# plt.show()

# 강한 상관관계 파악 (2)
# plt.figure(figsize=(8, 6))
# plt.scatter(df["Y_Minimum"], df["Y_Maximum"], alpha=0.5)
# plt.title("Y_Minimum vs Y_Maximum")
# plt.xlabel("Y_Minimum")
# plt.ylabel("Y_Maximum")
# plt.show()

# 선택한 두 변수의 실제 값 차이 확인 (1)
# y_diff = df["Y_Maximum"] - df["Y_Minimum"]
# print(y_diff.describe())
# print()
# # 이상값 분석용
# print(df.loc[y_diff.idxmax()])
# print()
# => Y_Maximum - Y_Minimum에서 최대 18,141의 극단적인 값이 확인되었으며,
# 해당 데이터는 K_Scatch 유형으로 확인되었다.
# 또한 Pixels_Areas와 Y_Perimeter 역시 전체 데이터에서 최대값을 나타내어,
# 해당 관측치는 실제로 매우 큰 결함 영역을 가진 사례일 가능성을 확인하였다.

# 선택한 두 변수의 실제 값 차이 확인 (2)
# x_diff = df["X_Maximum"] - df["X_Minimum"]
# print(x_diff.describe())
# print()
# # 이상값 분석용
# print(df.loc[x_diff.idxmax()])

# Steel_Plate_Thickness와 결함 유형의 관계 분석
# print(thick_a_avg.round(2))

# Steel_Plate_Thickness의 boxplot
groups = []  # 리스트 초기화


for fault in fault_types:
    # print(fault)
    groups.append(df[df["fault_type"] == fault]["Steel_Plate_Thickness"])
plt.figure(figsize=(10, 6))
plt.boxplot(groups, tick_labels=fault_types)
plt.title("Fault Type별 Steel_Plate_Thickness 분포")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("Steel_Plate_Thickness")

plt.tight_layout()
plt.show()

# ===================================================
# 08. 철판 두께 파악
# ===================================================
# 목적: 데이터 속 철판 두께들을 파악하고 분류 작업 (편의상 프로젝트 내부 분류: 얇은 / 중간 / 두꺼운)
# print(df["Steel_Plate_Thickness"].describe())
# print()

# 실제 철판 두께 종류 확인
# => .value_counts().sort_index(): 집계된 데이터 개수를 오름차순으로 정렬하는 메서드가 'sort_index()'
thick_data_cnt = df["Steel_Plate_Thickness"].value_counts().sort_index()
# print(thick_data_cnt)

"""
두 데이터로 확인할 수 있는 점
    1) 두께 40의 철판이 가장 많다 (전체 1941개 중 710개, 약 36.6% 비율)
       => 40: 710개, 70: 380개, 100: 154개, 80: 150개, ...
    2) 두께 최소값(min)과 25% 기준값이 동일한 40 => 36.6% 비율의 두께 40 철판의 점유도

"""

# pd.cut()으로 데이터 분류하기
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


# 분류 결과 확인
# print(df[["Steel_Plate_Thickness", "Thickness_Group"]].head(20))
# print()

# 각 그룹의 데이터 개수 확인
# print(df["Thickness_Group"].value_counts())
# Thin       912  ← 약 47.0%
# Medium     750  ← 약 38.6%
# Thick      279  ← 약 14.4%

"""
분석 편의를 위해 데이터 분포를 기준으로 Steel_Plate_Thickness를 
Thin, Medium, Thick의 세 구간으로 분류하였다.
"""


# 각 철판 두께 그룹에서 어떤 결함들이 몇 개씩 발생했는가?
# pd.crosstab() => 두 범주형 데이터를 교차해서 표를 만들어주는 기능
thickness_fault = pd.crosstab(df["Thickness_Group"], df["fault_type"])
# print(thickness_fault)

# ※ groupby()와 차이점은?
# => groupby()는 '각 결함의 평균 두께가 얼마야?'
# ==> crosstab()는 '각 두께 그룹에 각각 결함이 몇 개야?'

# crosstab() 데이터 비율 만들기
thickness_fault_ratio = (
    # normalize="index": 각 행(row)의 합이 1이 되도록 행 기준 비율을 구합니다. ("각 행의 합계를 100%로 만들어라.")
    pd.crosstab(df["Thickness_Group"], df["fault_type"], normalize="index") * 100
)
# print(f"{thickness_fault_ratio.round(2)}")

"""
본 데이터에서 철판 두께 구간에 따라 결함 유형의 구성 비율에 뚜렷한 차이가 관찰되었다. 
Thin 그룹에서는 K_Scatch가 42.76%로 가장 높은 비율을 보인 반면, Medium에서는 0.13%, 
Thick에서는 관측되지 않았다. 

반대로 Other_Faults는 Thin 24.78%, Medium 34.53%, Thick 67.38%로 
두꺼운 그룹에서 높은 구성 비율을 보였다.
"""

# ===================================================
# 09. 철판 두께 그룹별 결함 비율 데이터 시각화 하기
# ===================================================


# 두께 그룹별 결함 비율 - 누적 막대그래프
# 그래프 기본 설정
ax = thickness_fault_ratio.plot(kind="bar", stacked=True, figsize=(10, 6))
# DataFrame.plot()의 역할은?
# => Pandas가 내부적으로 Matplotlib를 이용해서 자체적으로 그래프를 제작
# => kind="bar": Bar plot으로 제작 요청 / stacked=True: 여러 막대를 하나 위에 쌓기


# 막대별 숫자로 비율 표시
for container in ax.containers:
    for bar in container:
        # 해당 색깔 영역의 높이
        value = bar.get_height()

        # 0%는 표시하지 않음
        if value == 0:
            continue

        # 막대의 가운데 X 위치
        x = bar.get_x() + bar.get_width() / 2

        # 막대가 시작되는 Y 위치
        y = bar.get_y()

        # 5% 이상은 막대 내부에 숫자 표시
        if value >= 3:
            ax.text(
                x, y + value / 2, f"{value:.2f} %", ha="center", va="center", fontsize=9
            )
        else:
            # 5% 미만은 막대 바깥쪽으로 표시
            ax.annotate(
                f"{value:.2f} %",
                # 선을 어디에서 시작할 것인가?
                xy=(x, y + value),
                # 숫자를 어디에 놓을 것인가?
                xytext=(x + 0.12, y + value + 4),
                ha="center",
                fontsize=8,
                arrowprops={"arrowstyle": "-", "color": "gray", "linewidth": 0.8},
            )


ax.set_title("Fault Distribution by Steel Plate Thickness")
ax.set_xlabel("Thickness Group")
ax.set_ylabel("Fault Ratio (%)")

ax.legend(title="Fault Type", bbox_to_anchor=(1.02, 1), loc="upper left")

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()
# => 본 데이터에서 정의한 철판 두께 구간에 따라 결함 유형의 구성 비율에 뚜렷한 차이가 관찰되었다.

# 특정 결함을 선정해서 막대 그래프로 구현
# selected_faults = thickness_fault_ratio[["K_Scatch", "Other_Faults", "Z_Scratch"]]
# ax2 = selected_faults.plot(kind="bar", stacked=False, figsize=(10, 6))

# ax2.set_title("Fault Distribution by Steel Plate Thickness")
# ax2.set_xlabel("Thickness Group")
# ax2.set_ylabel("Fault Ratio (%)")

# plt.xticks(rotation=0)

# plt.tight_layout()
# plt.show()
