import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정 (Windows 기준)
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# 1. 데이터 불러오기 
df = pd.read_csv('changwon_temp.csv', encoding='cp949', skiprows=7)

# 2. 데이터 정제
df = df[['날짜', '평균기온(℃)', '최고기온(℃)', '최저기온(℃)']]
df.columns = ['date', 'avg_temp', 'max_temp', 'min_temp']
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
df = df.interpolate(method='linear')

# 3. 시계열 분석 기법 2개 적용
df['ma_30'] = df['avg_temp'].rolling(window=30).mean() # 첫 번째 기법: 이동평균
monthly_avg = df.groupby(df.index.month)['avg_temp'].mean() # 두 번째 기법: 월별 집계

# 4. 시각화 1: 10년 기온 추세와 30일 이동평균
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['avg_temp'], color='lightgray', label='일간 평균기온', alpha=0.5)
plt.plot(df.index, df['ma_30'], color='red', label='30일 이동평균', linewidth=2)
plt.title('창원시 일간 평균기온 및 30일 이동평균 (2016-2025)')
plt.xlabel('연도')
plt.ylabel('기온 (℃)')
plt.legend()
plt.tight_layout()
plt.savefig('temp_trend.png') 
plt.show()

# 5. 시각화 2: 월별 평균 기온 분포 (계절성)
plt.figure(figsize=(10, 5))
monthly_avg.plot(kind='bar', color='skyblue')
plt.title('창원시 월별 평균기온 (2016-2025)')
plt.xlabel('월')
plt.ylabel('평균기온 (℃)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('monthly_seasonality.png')
plt.show()

print("분석 완료! 필수 그래프 2개가 저장되었습니다.")
