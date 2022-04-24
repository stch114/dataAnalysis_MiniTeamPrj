import statsmodels.formula.api as smf
import pandas as pd
import matplotlib.pyplot as plt
plt.rc('font', family='malgun gothic')

# 전처리 작업한 데이터 파일 불러오기
data = pd.read_csv('Olympics_GDP_Pop.csv').drop(['Unnamed: 0'], axis=1)
print(data.info())
print(data.head())

# 상관계수 판단
print(data.corr())
# 메달-GDP간: 0.440265 / 메달-인구간: 0.205056
# 절대수치로 높은 건 X. But 사회과학에서는 +-0.2 ~ +-0.4정도만 되어도 연관성이 있다고 판단한다고 한다. 

# 모델1 -> GDP로 메달 수 예측. 단순회귀분석 모델
model1 = smf.ols("medals ~ GDP", data=data).fit()
print(model1.summary())  
# 결정계수(R-squared): 0.194 -> 설명력은 적다.
# Prob (F-statistic): 6.07e-07 < 0.05 -> 유의한 모델
# slope(기울기): 0.0135 / bias(절편): 25.6867

# 시각화
plt.scatter(data.GDP, data.medals)  # 실제 값으로 산포도 표시
plt.plot(data.GDP, 0.0135 * data.GDP + 25.6867, 'r')  # 회귀식을 화면에 표시
# Wx + B -> 기울기 * x + intercept / 예측 값 표시
plt.xlabel('GDP')
plt.ylabel('medals')
plt.show()

# 모델1의 적절성 확인
# 잔차(실제 값 - 예측 값) 구하기
fitted = model1.predict(data)  # 예측 값
residual = data['medals'] - fitted  # 잔차(실제 값 - 예측 값)

print('선형성: 예측 값과 잔차가 비슷한 패턴을 가지는가?')
import seaborn as sns
sns.regplot(fitted, residual, line_kws={'color':'red'}, lowess=True)  # regplot(예측 값, 잔차 값)
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
# .summary()의 더빈왓슨 값으로 확인 -> Durbin-Watson: 2.059 
# 0에 가까우면 양의 상관, 4에 가까우면 음의 상관. 2에 가까우면 자기상관이 없다고 판단.
# 자기상관이 없다고 볼 수 있으므로 독립성은 만족한다.

# GDP를 입력 받아 메달 획득 수 예측하기
data.GDP = float(input("GDP를 입력하세요: "))
pred1 = model1.predict(pd.DataFrame({'GDP':data.GDP}))
print("예상 메달 수: ", int(pred1[0]))
