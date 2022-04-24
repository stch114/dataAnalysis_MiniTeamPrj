import pandas as pd
import numpy as np
import scipy.stats as stats

data = pd.read_csv('recent10Olympics_hostCntry.csv')
print(data.head(4))

# 사용하지 않을 데이터 제거
df = data.drop(['Sex', 'Name', 'Age', 'Height', 'Weight', 'Season', 'Sport', 'Year'], axis=1)
print(df.head(3))

print()
print("----"*10)
print()

df['Country_bi'] = np.where(df['NOC'] == df['Host'], 1, 0)  # 개최국일 시에 1, 아닐 시 0.
print(df.head(4))
# 귀무 : 개최국 여부는 메달 성적과 관계가 없다.
# 대립 : 개최국 여부는 메달 성적과 관계가 있다. 

ctab = pd.crosstab(index=df['Country_bi'], columns=df['Medal_bi'])
print(ctab)
print("----"*10)

chi2, p, ddof, expected = stats.chi2_contingency(ctab)
print('chi2: ', chi2)  # 55.63413944379663
print('p: ', p)  # 8.729439456355027e-14 < 0.05
print('ddof: ', ddof)  # 1 = (2 - 1) * (2 - 1)

# 대립 가설 채택 -> 개최국 여부와 메달 성적은 관계가 있다.
