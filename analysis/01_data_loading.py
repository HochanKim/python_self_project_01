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
# plt.show()  # 결과물 보여주기 (bar - 그래프)

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
# plt.show()  # 결과물 보여주기 (boxplot)

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
# plt.show()  # 결과물 보여주기 (bar - 그래프)


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
# plt.show()  # 결과물 보여주기 (boxplot)


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
# plt.show()  # 결과물 보여주기 (bar - 그래프)

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
# plt.show()  # 결과물 보여주기 (boxplot)

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
# plt.show()

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
# plt.show()

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
print(thick_a_avg.round(2))

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
