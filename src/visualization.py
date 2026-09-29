# 분석 결과를 시각화하는 파일

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# 원본 데이터가 필요한 그래프용
from data_loading import df, fault_cnts, fault_types

# 계산된 분석 결과가 필요한 그래프용
from analysis import (
    fault_summary,
    sol_a_avg,
    thick_a_avg,
    thickness_fault_ratio,
    luminosity_avg,
    corr,
    shape_columns_avg,
)


# ===================================================
# 01. Matplotlib 기본 설정
# ===================================================

# 폰트 파일 경로
font_path = "../fonts/NanumGothic-Regular.ttf"

# 폰트 파일을 Matplotlib에 등록
fm.fontManager.addfont(font_path)

# 그래프에 사용할 폰트 설정
font = fm.FontProperties(fname=font_path)

# 등록된 폰트를 전체 그래프에 적용
plt.rcParams["font.family"] = font.get_name()

# 음수(-) 기호 깨짐 방지
plt.rcParams["axes.unicode_minus"] = False


# ===================================================
# 02. 결함 유형별 발생 현황 - Bar Plot
# ===================================================

plt.figure(figsize=(10, 6))

plt.bar(fault_cnts.index, fault_summary["count"])

plt.title("Steel Plate Fault Distribution (철강 결함 분류)")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("Count (결함 개수)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ===================================================
# 03. 결함 유형별 Pixels_Areas 분포 - Box Plot
# ===================================================

groups = []

for fault in fault_types:
    groups.append(df[df["fault_type"] == fault]["Pixels_Areas"])

plt.figure(figsize=(10, 6))

plt.boxplot(groups, tick_labels=fault_types)

plt.title("Fault Type별 Pixels_Areas 분포")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("Pixels_Areas")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ===================================================
# 04. 결함 유형별 Sum_of_Luminosity 평균 - Bar Plot
# ===================================================

plt.figure(figsize=(10, 6))

plt.bar(sol_a_avg.index, sol_a_avg.values)

plt.title("Sum_of_Luminosity (철판 결함 유형별 밝기)")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("AVG of SoL (각 결함 평균)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ===================================================
# 05. 결함 유형별 Sum_of_Luminosity 분포 - Box Plot
# ===================================================

groups = []

for fault in fault_types:
    groups.append(df[df["fault_type"] == fault]["Sum_of_Luminosity"])

plt.figure(figsize=(10, 6))

plt.boxplot(groups, tick_labels=fault_types)

plt.title("Fault Type별 Sum_of_Luminosity 분포")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("Sum_of_Luminosity")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ===================================================
# 06. 결함 유형별 Steel_Plate_Thickness 평균 - Bar Plot
# ===================================================

plt.figure(figsize=(10, 6))

plt.bar(thick_a_avg.index, thick_a_avg.values)

plt.title("Steel_Plate_Thickness (철판 두께와 결함 유형 사이의 관계)")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("AVG of SPT (각 결함 평균)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ===================================================
# 07. 결함 유형별 Steel_Plate_Thickness 분포 - Box Plot
# ===================================================

groups = []

for fault in fault_types:
    groups.append(df[df["fault_type"] == fault]["Steel_Plate_Thickness"])

plt.figure(figsize=(10, 6))

plt.boxplot(groups, tick_labels=fault_types)

plt.title("Fault Type별 Steel_Plate_Thickness 분포")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("Steel_Plate_Thickness")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ===================================================
# 08. Pixels_Areas와 Sum_of_Luminosity 관계
#     - Scatter Plot
# ===================================================

plt.figure(figsize=(18, 15))

# 결함별 색상
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

    plt.scatter(
        fault_data["Pixels_Areas"],
        fault_data["Sum_of_Luminosity"],
        color=colors[fault],
        alpha=0.5,
        label=fault,
    )

plt.title("Pixels_Areas와 Sum_of_Luminosity의 관계")
plt.xlabel("Pixels_Areas")
plt.ylabel("Sum_of_Luminosity")

plt.legend()

plt.tight_layout()
plt.show()


# ===================================================
# 09. 전체 숫자형 변수 상관관계 - Heatmap
# ===================================================

plt.figure(figsize=(18, 15))

sns.heatmap(corr, annot=True, annot_kws={"size": 8})

plt.title("Steel Plate Fault Correlation Heatmap")

plt.tight_layout()
plt.show()


# ===================================================
# 10. 철판 두께 그룹별 결함 비율
#     - 누적 Bar Plot
# ===================================================

ax = thickness_fault_ratio.plot(kind="bar", stacked=True, figsize=(10, 6))

# 각 막대 영역에 비율 표시
for container in ax.containers:
    for bar in container:
        # 해당 영역의 높이
        value = bar.get_height()

        # 0%는 숫자 표시하지 않음
        if value == 0:
            continue

        # 막대 가운데 X 위치
        x = bar.get_x() + bar.get_width() / 2

        # 해당 영역이 시작되는 Y 위치
        y = bar.get_y()

        # 3% 이상은 막대 내부에 표시
        if value >= 3:
            ax.text(
                x, y + value / 2, f"{value:.2f} %", ha="center", va="center", fontsize=9
            )

        # 3% 미만은 막대 바깥쪽에 표시
        else:
            ax.annotate(
                f"{value:.2f} %",
                xy=(x, y + value),
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


# ===================================================
# 11. 주요 결함 3종과 철판 두께 그룹 비교 - Bar Plot
# ===================================================

selected_faults = thickness_fault_ratio[["K_Scatch", "Other_Faults", "Z_Scratch"]]

ax2 = selected_faults.plot(kind="bar", stacked=False, figsize=(10, 6))

ax2.set_title("Major Fault Distribution by Steel Plate Thickness")

ax2.set_xlabel("Thickness Group")
ax2.set_ylabel("Fault Ratio (%)")

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()


# ===================================================
# 12. 결함 유형별 Luminosity_Index 평균 - Bar Plot
# ===================================================

# 결함 유형 순서를 기존 그래프와 통일
luminosity_avg = luminosity_avg.reindex(fault_types)

plt.figure(figsize=(10, 6))

plt.bar(luminosity_avg.index, luminosity_avg.values)

plt.title("Fault Type별 Luminosity_Index 평균")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("AVG of Luminosity_Index")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ===================================================
# 13. 결함 유형별 Luminosity_Index 분포 - Box Plot
# ===================================================

groups = []

for fault in fault_types:
    groups.append(df[df["fault_type"] == fault]["Luminosity_Index"])

plt.figure(figsize=(10, 6))

plt.boxplot(groups, tick_labels=fault_types)

plt.title("Fault Type별 Luminosity_Index 분포")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("Luminosity_Index")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ===================================================
# 14. Sum_of_Luminosity와 Luminosity_Index 관계
#     - Scatter Plot
# ===================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    df["Sum_of_Luminosity"],
    df["Luminosity_Index"],
    alpha=0.5,
)

plt.title("Sum_of_Luminosity와 Luminosity_Index의 상관관계")

plt.xlabel("Sum_of_Luminosity")
plt.ylabel("Luminosity_Index")

plt.tight_layout()
plt.show()


# ===================================================
# 15. 결함 유형별 Orientation_Index 평균 - Bar Plot
# ===================================================

orientation_avg = shape_columns_avg["Orientation_Index"]

plt.figure(figsize=(10, 6))

plt.bar(orientation_avg.index, orientation_avg.values)

plt.title("Fault Type별 Orientation_Index 평균")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("AVG of Orientation_Index")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ===================================================
# 16. 결함 유형별 Orientation_Index 분포 - Box Plot
# ===================================================

groups = []

for fault in fault_types:
    groups.append(df[df["fault_type"] == fault]["Orientation_Index"])

plt.figure(figsize=(10, 6))

plt.boxplot(groups, tick_labels=fault_types)

plt.title("Fault Type별 Orientation_Index 데이터 분포")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("Orientation_Index")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ===================================================
# 17. 결함 유형별 Edges_Y_Index 평균 - Bar Plot
# ===================================================

edges_y_avg = shape_columns_avg["Edges_Y_Index"]

plt.figure(figsize=(10, 6))

plt.bar(edges_y_avg.index, edges_y_avg.values)

plt.title("Fault Type별 Edges_Y_Index 평균")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("AVG of Edges_Y_Index")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ===================================================
# 18. 결함 유형별 Edges_Y_Index 분포 - Box Plot
# ===================================================

groups = []

for fault in fault_types:
    groups.append(df[df["fault_type"] == fault]["Edges_Y_Index"])

plt.figure(figsize=(10, 6))

plt.boxplot(groups, tick_labels=fault_types)

plt.title("Fault Type별 Edges_Y_Index 데이터 분포")
plt.xlabel("Fault Type (결함 종류)")
plt.ylabel("Edges_Y_Index")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


def draw_boxplot():
    return True
