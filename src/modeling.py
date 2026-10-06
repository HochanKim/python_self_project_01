from data_loading import df

# 사이킷런 가져오기 (학습용, 시험용 나누기)
from sklearn.model_selection import train_test_split

# 의사결정나무(Decision Tree)
from sklearn.tree import DecisionTreeClassifier

target_columns = [
    "Pastry",
    "Z_Scratch",
    "K_Scatch",
    "Stains",
    "Dirtiness",
    "Bumps",
    "Other_Faults",
    "fault_type",
]

X = df.drop(columns=target_columns)
y = df["fault_type"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,  # 20% 데이터를 test로 사용 (train용: 1,552개 / test용: 389개)
    random_state=60,
    stratify=y,  # 클래스 비율을 고려해서 Train/Test 나누기
)

# 모델 생성하기 ('의사결정나무'의 객체로 지정)
model = DecisionTreeClassifier(random_state=60)

# 실제 학습하기 01
model.fit(X_train, y_train)

# 학습한 이후 시험용에 모델을 적용하기
y_pred = model.predict(X_test)
