import pandas as pd

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
print(df[["fault_type"]].head(10))
