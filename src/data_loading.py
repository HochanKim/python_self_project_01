# 데이터 준비 단계 py 파일

import pandas as pd  # pandas 가져오기 (데이터 불러오기, 계산 등)

# ===================================================
# 01. 데이터 준비 및 가공
# ===================================================

# 데이터 파일 불러오기
df = pd.read_csv("../data/Faults.NNA", sep=r"\s+", header=None)
# => r'\s+'는 공백이 하나 이상 있는 곳을 구분자로 사용
# => sep=r"\s+":  탭이나 스페이스바가 여러 번 들어간 정렬되지 않은 공백 데이터도 깔끔하게 잘라주는 역할
# => header=None: 파일의 첫 번째 줄을 헤더로 사용 금지 => 열의 헤더가 숫자로 자동 지정


# 컬럼명 모음 불러오기
columns = pd.read_csv("../data/Faults27x7_var", sep=r"\s+", header=None)


# 컬럼명들을 데이터 프레임에 적용하기
df.columns = columns.iloc[:, 0].tolist()
# => iloc[:, 0]: '모든 행, 0번째 열'을 가져오겠다
# => tolist(): 리스트로 변환

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

# 각 행의 결함 개수 확인 (데이터 열(axis=1)들의 합 계산)
fault_count = df[fault_columns].sum(axis=1)

# 하나의 fault_type 컬럼으로 변환 (가장 큰 값을 가지고 있는 열을 행을 뒤지면서 찾기)
df["fault_type"] = df[fault_columns].idxmax(axis=1)

# 각 결함 유형이 몇 개씩 존재하는가?
fault_cnts = df["fault_type"].value_counts()

# 결함 유형 순서 (모든 Box Plot에 적용)
fault_types = fault_cnts.index

# 다른 파일에서 불필요한 출력 방지
if __name__ == "__main__":
    print(df.shape)
    print(df.head())
    print(fault_cnts)
