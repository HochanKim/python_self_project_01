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
# => (가로축: 결함 종류(fault_type), 세로축: 발생 건수(count))
plt.bar(fault_summary["fault_type"], fault_summary["count"])

plt.title("Steel Plate Fault Distribution (철강 결함 분류)")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("Count (결함 개수)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()  # 결과물 보여주기 (bar - 그래프)

# fault_type별로 그룹을 만들어서 각 그룹의 Pixels_Areas(결함 면적) 평균 계산
# => pd.groupby(): 특정 기준 데이터를 그룹으로 묶어서 다음 그룹별(특정 열의 데이터들) 계산을 수행
grby_fy_pxl_a_avg = df.groupby("fault_type")["Pixels_Areas"].mean()
# print(round(grby_fy_pxl_a_avg, 2))

# 타입별 정보 불러오기 (개수, 평균, 중앙값 등등)
grby_fy_pxl_a_decrib = df.groupby("fault_type")["Pixels_Areas"].describe()
# print(grby_fy_pxl_a_decrib)
#               count         mean       std     min      25%     50%      75%       max
#       (결함 개수)(결함 평균)(표준편차)(최소값)(데이터 25% 기준)(중앙값)(데이터 75% 기준)(최대값)
# fault_type
# Bumps         402.0   238.465174   561.446680  25.0    78.25   120.5    197.50    8391.0
# Dirtiness      55.0   363.490909   384.570221  52.0    84.50   145.0    581.50    2028.0
# K_Scatch      391.0  7622.654731  9100.607359   2.0  3948.50  6281.0  10908.50  152655.0
# Other_Faults  673.0   584.371471  2040.210152  15.0    81.00   146.0    308.00   37334.0
# Pastry        158.0   561.620253  1314.772648  30.0   112.50   209.0    381.25   10914.0
# Stains         72.0    19.916667    14.147861   6.0    13.50    16.5     18.00      86.0
# Z_Scratch     190.0   506.594737  1039.794647  51.0    75.25   146.0    442.00    7579.0


# ===================================================
# 03. 결함 데이터의 시각화 - Box Plot
# ===================================================

# 결함 데이터 묶기 (group 리스트 생성)

# 데이터 담는 빈 리스트
groups = []

# 중복 필터링 적용한 df["fault_type"] 데이터의 행값(실제 결함 7종류) 담기
fault_types = df["fault_type"].unique()


for fault in fault_types:
    # print(fault)
    groups.append(df[df["fault_type"] == fault]["Pixels_Areas"])
plt.boxplot(groups)
plt.show()  # 결과물 보여주기 (boxplot)
