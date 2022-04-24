import statsmodels.formula.api as smf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rc('font', family='malgun gothic')

# 전처리 작업한 데이터 파일 불러오기
data = pd.read_csv('Olympics_GDP_Pop.csv').drop(['Unnamed: 0'], axis=1)
print(data.info())
print(data.head())

# 모델2 -> GDP와 인구수로 메달 수 예측(독립변수 2개). 다중회귀분석 모델
model2 = smf.ols("medals ~ GDP + Population", data=data)
res = model2.fit()
print(res.summary())  
# 복수의 독립변수를 설정했기 때문에 조정된 결정계수를 확인 -> Adj. R-squared: 0.241 -> 설명력은 적다. 
# p-value 확인. Prob (F-statistic): 4.69e-08 < 0.05 -> 유의한 모델
# slope_GDP(GDP 기울기): 0.0142 / slope_Population: 기울기(기울기2) : 8.611e-07 / bias(절편): -33.1082

# 모델2의 적절성 확인(복수의 독립변수를 설정했으므로 등분산성과 다중공선성까지도 확인해야 한다.)
# 잔차(실제 값 - 예측 값) 구하기
fitted = res.predict(data)  
residual = data['medals'] - fitted  

print('선형성: 예측 값과 잔차가 비슷한 패턴을 가지는가?')
import seaborn as sns
sns.regplot(fitted, residual, line_kws={'color':'red'}, lowess=True)  
plt.plot([fitted.min(), fitted.max()], [0, 0], '--', color='grey')
plt.show()  # 완벽한 직선은 아니기에 만족하지는 못한다고 볼 수 있다.

print('정규성: 잔차가 정규분포를 따르는가?')
import scipy.stats
sr = scipy.stats.zscore(residual)
(x, y), _ = scipy.stats.probplot(sr)
sns.scatterplot(x, y)
plt.plot([-3, 3], [-3, 3], '--', color='grey')
plt.show()  # 직선을 벗어나는 값들이 꽤 있기에 만족스러운 결과는 아니다.

print('독립성: 잔차가 독립적인가? -> 자기 상관(인접 관측치와 오차가 상관이 있는 것)이 없는가?')
# Durbin-Watson: 1.977 
# 2에 근접. 자기상관이 없다고 볼 수 있으므로 독립성은 만족한다.

print('등분산성: 잔차의 분산이 일정한가?')
sns.regplot(fitted, np.sqrt(np.abs(sr)), lowess=True, line_kws={'color':'red'})
plt.show()  # 일정하지 않다. 
# 정규성과 선형성을 만족하지 못하므로 곧 등분산성에 문제가 있을 것이라고 판단할 수도 있다.

print('다중 공선성: 독립변수들 간에 강한 상관관계가 있지는 않은가?(하나의 독립변수가 다른 독립변수들로 잘 예측되지 않나?)')
# VIF(분산 인플레 요인) 값이 10을 넘으면 다중공선성 발생한다.
from statsmodels.stats.outliers_influence import  variance_inflation_factor
print(model2.exog_names)  
print(variance_inflation_factor(model2.exog, 1))  # 1.008295250855819 < 10 
print(variance_inflation_factor(model2.exog, 2))  # 1.0082952508558192 < 10
# 다중공선성은 없는 것으로 판단된다.

# GDP와 인구수를 입력 받아 메달 획득 수 예측하기
data.GDP = float(input("GDP를 입력하세요: "))
data.Population = float(input("인구수를 입력하세요: "))
pred2 = res.predict(pd.DataFrame({'GDP':data.GDP, 'Population':data.Population}))
print("예상 메달 수: ", int(pred2[0]))
