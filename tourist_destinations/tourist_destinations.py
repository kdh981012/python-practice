import pandas as pd

df = pd.read_csv("~/dev/python_lessons/tourist_destinations.csv")

# 1. 대륙별 평균 비용 (비싼 순으로 정렬)
print(df.groupby("Continent")["Avg Cost (USD/day)"].mean().sort_values(ascending=False))

# 2. 여행 유형별 평균 평점
print(df.groupby("Type")["Avg Rating"].mean())

# 3. UNESCO 등재 vs 미등재 평균 평점 비교
print(df.groupby("UNESCO Site")["Avg Rating"].mean())

# 4. (Avg Cost 낮고 Avg Rating 높은) 가성비 여행지 top 10
df["value_score"] = round(df["Avg Rating"] / df["Avg Cost (USD/day)"] * 100, 2)
print(df[["Destination Name", "Country", "Avg Cost (USD/day)", "Avg Rating", "value_score"]].sort_values("value_score",ascending=False).head(10))
