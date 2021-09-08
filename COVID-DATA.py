# 3가지 
# 1. 2020.02~ 은평구 코로나 , 중구 코로나 추가 확진자 추이
# 2. 날짜별 확진자 현황
# 3. 각 구별 코로나 확진자 지도에 나타내기


from matplotlib import colors
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc
import folium

rc('font', family='AppleGothic')

# 데이터 가져오기
df = pd.read_csv('/Users/qkrdnjsrl/Desktop/coding study/코로나 바이러스 데이터/서울특별시 코로나19 자치구별 확진자 발생동향.csv', encoding='euc-kr')
# print(df.info())

# 사용하지 않는 데이터는 전부 삭제하기
df.drop(['기타 전체','기타 추가','수집일'], axis= 1, inplace=True)              


# ---------------------------------------------------------- 시간값 정리하기
# 시간값을 잘라서 넣기
# 이미 문자열로 되어 있으므로 astype()을 통해서 자료형을 변환해줄 필요는 없다.
# 이때 시각을 나타내는 3번째 배열 값은 버린다.

df['Date'] = df['자치구 기준일']
df.drop(['자치구 기준일'], axis=1, inplace=True)
dates = df['Date'].str.split('.')
df['년'] = dates.str.get(0)
df['월'] = dates.str.get(1)
df['일'] = dates.str.get(2)
# df.drop(['Date'], axis=1, inplace=True)
# print(df.tail())

# ------------------------------------------------- NaN 값 전부 삭제하기(2020.02~2021.09)까지의 데이터 확보
df = df.dropna(subset=['종로구 전체'], how='any', axis=0)             
# print(df.head())
# print(df.info())

# <------------ 선택한 구 코로나 추가 확진자 추이 나타내기 ---------->!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# plt.style.use('fivethirtyeight')
# mask1 = (df['년'] == '2021') & (df['월'] == '08')                           # 2021.8 데이터만 가져오기
# df_city = df[mask1]                                         

# df_city_seoul = df_city.loc[ : , ['은평구 추가', '중구 추가','용산구 추가']]       # 은평구, 중구, 용산구의 데이터만 가져오기
# df_city_seoul['Date'] = range(1,32)
# df_city_seoul.set_index('Date', inplace= True)

# print(df_city_seoul)
# fig = plt.figure(figsize =(16, 8))
# ax1 = plt.plot(df_city_seoul['은평구 추가'], ls=':', label = '은평구 추가 확진자')
# ax2 = plt.plot(df_city_seoul['중구 추가'],  ls='--', label = '중구 추가 확진자')
# ax3 = plt.plot(df_city_seoul['용산구 추가'], label = '용산구 추가 확진자')
# plt.legend(loc = 'best')
# plt.xticks(df_city_seoul.index)
# plt.title('2021년 8월 은평구, 중구, 용산구 코로나 추가 확진자', size = 20)
# plt.yticks([5, 12, 20, 28, 36 , 44])                                # y_label 과 눈금이 겹치는 것을 방지하기 위해 yticks 사용하기

#     # ------ 틀 꾸미기 ------- 
# plt.ylabel('확진자', rotation = 0)
# plt.xlabel('날짜', size = 20)
# plt.show()


# <------------ 9.3일 코로나 구별 지도에 나타내기---------->!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# 1. 먼저 각 구청별 위도, 경도의 위치 가져오기

df1 = pd.read_csv('/Users/qkrdnjsrl/Desktop/coding study/코로나 바이러스 데이터/서울시 행정구역 시군구 정보 (좌표계_ WGS1984).csv', header= 0)
df1.drop(['시군구코드', '순번', '시군구명_영문', 'ESRI_PK'], axis  = 1 , inplace = True)
df1.rename(columns={'시군구명_한글':'시군구'}, inplace = True)

df.rename(columns={'종로구 전체' : '종로구', '중구 전체' : '중구','은평구 전체':'은평구',  '용산구 전체': '용산구', '성동구 전체': '성동구', '광진구 전체': '광진구','노원구 전체':'노원구','금천구 전체':'금천구', '마포구 전체' : '마포구','동대문구 전체' : '동대문구','서대문구 전체':'서대문구', '중랑구 전체': '중랑구', '양천구 전체':'양천구','강서구 전체':'강서구','구로구 전체':'구로구', '관악구 전체':'관악구','성북구 전체':'성북구', '강북구 전체': '강북구', '도봉구 전체':'도봉구', '영등포구 전체':'영등포구', '동작구 전체': '동작구', '서초구 전체': '서초구', '강남구 전체': '강남구', '송파구 전체':'송파구', '강동구 전체': '강동구'}, inplace=True)
df.drop(['종로구 추가', '중구 추가','용산구 추가', '성동구 추가', '광진구 추가', '동대문구 추가', '은평구 추가', '중랑구 추가', '관악구 추가','마포구 추가', '성북구 추가','강남구 추가','노원구 추가','도봉구 추가', '금천구 추가', '영등포구 추가', '동작구 추가', '서추구 추가', '송파구 추가' , '강동구 추가', '강북구 추가', '서대문구 추가','양천구 추가', '강서구 추가', '구로구 추가'], axis = 1, inplace = True)
df_city_folium = df.loc[0]
# 9.3 일자 정보 가져오기
df_city_folium.drop(['Date', '년', '월', '일'], inplace = True)
df_city_folium = df_city_folium.sort_index()          # 배열 정리하기

df1.set_index('시군구', inplace = True)
df1 = df1.sort_index()

df1['확진자'] = df_city_folium.values                       # 데이터 전처리 한후 values 값을 추가하기
print(df1)

today_cvd_map = folium.Map(location=[37.55, 126.98], zoom_start=12)


for name, lat, lng, peolpes in zip(df1.index, df1['위도'], df1['경도'], df1['확진자']):
    folium.CircleMarker([lat, lng],
                        radius = int(peolpes/80),                               # 반지름 길이
                         fill = True,
                         fill_color = 'red',
                         fil_opacity = 0.8,                                     # 투명도
                          popup=( name, peolpes,'명') ).add_to(today_cvd_map)

today_cvd_map.save('/Users/qkrdnjsrl/Desktop/coding study/코로나 바이러스 데이터/first_folium_project.html')
