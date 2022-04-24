import pandas as pd

# 데이터 읽기 및 확인
summer_data = pd.read_csv("summer.csv")
winter_data = pd.read_csv("winter.csv")
dic_data = pd.read_csv("dictionary.csv")

# 데이터 병합 코드
frame = [summer_data, winter_data]
data = pd.concat(frame)
# print(data.columns)
# print(data)

series = data.groupby(['Country']).Medal.count()  # 국가별 메달 수 추출 
df = pd.DataFrame({'country':series.index, 'medals':series.values})
# print(df)
# print(type(df))

print()
final_df = pd.merge(df, dic_data, left_on='country', right_on='Code').drop(['Code', 'Country'], axis=1)

# 결측 값 제거.
final_df = final_df.dropna(how='any')
print(final_df)

# csv 파일로 저장
final_df.to_csv('Olympics_GDP_Pop.csv', sep=',')

