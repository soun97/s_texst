from datetime import datetime

import pandas as pd
from krxholidays import add_business_days


df = pd.read_csv('C:/Users/soun/Documents/soun_pycharm/strategy.csv', encoding='cp949')
df['종목코드'] = df['종목코드'].astype(str)
df['종목코드'] = df['종목코드'].str.zfill(6)
df['일자'] = df['일자'].astype(str)
df['일자'] = pd.to_datetime(df['일자'])
df['day+7'] = df.apply(lambda row : add_business_days(row['일자'], 6 ), axis=1)

def make_series(row):
    '''
    [date],[code]의 새로운 series를 만드는 함수
    :param row: df의 한개의 row
    :return: date_range_df(new dataframe, columns:'date','code')
    '''
    code = row['종목코드']
    start_date = row['일자']
    end_date = row['day+7']

    date_range_df = pd.DataFrame(pd.date_range(start_date, end_date, freq='D'))
    # pd.date_range(시작일,종료일) >  해당 범위 내의 데이터 생성 가능하다.
    date_range_df.columns = ['date']
    date_range_df['code'] = code

    return date_range_df

df_list = df.apply(lambda row : make_series(row), axis=1) #lambda 를 이용해 한행씩 새로운 series를 만듬
dfcopy = df.copy()
dfcopy['날짜'] = None

for x in df_list:
    dfcopy = pd.merge(dfcopy, x, left_on='종목코드', right_on='code', how='outer')
    dfcopy['날짜'] = dfcopy['날짜'].fillna(dfcopy['date'])
    dfcopy=dfcopy[['종목코드','일자','day+7','날짜']] #일자=시작일,day+7=종료일, 날짜=range

openfile = pd.DataFrame()

for code in set(dfcopy['종목코드']):
    df=pd.read_csv(f'd:/soun_pycharm/original/{code}.csv', encoding='utf-8')
    openfile = pd.concat([openfile, df], axis=0)

openfile['code']=openfile['종목코드'].str[1:]#종목콛 A003220 > 003220
openfile['date']=pd.to_datetime(openfile['일자'].astype(str))

merged=pd.merge(dfcopy,openfile, left_on=['종목코드','날짜'], right_on=['code','date'], how='left')
merged.to_parquet('merged.parquet')
df=pd.read_parquet('merged.parquet')
df=df.drop(columns=["종목코드_x", "일자_x", "day+7", "날짜", "일자_y", "종목코드_y"]) #필요없는 columns drop

def diff_시가_종가(ser, df):
    row = df.loc[ser.index]
    전일 = row.iloc[0]
    당일 = row.iloc[1]
    등락 = 당일["시가"] - 전일["종가"]
    return 등락

def diff_종가_종가(ser, df):
    row = df.loc[ser.index]
    전일 = row.iloc[0]
    당일 = row.iloc[1]
    등락 = 당일["종가"] - 전일["종가"]
    return 등락

df_dropped = df.dropna()
df_dropped["시가_종가차"] = df_dropped["종가"].rolling(window=2).apply(diff_시가_종가, args=(df_dropped,))
df_dropped["종가_종가차"] = df_dropped["종가"].rolling(window=2).apply(diff_종가_종가, args=(df_dropped,))

def check_group(base_field,x):
    """
    :param base_field: 기준일의 계산 기준이 되는 필드 예) 종가
    :param x:
    :return: 변화량
    """
    idx = x.index
    rows = [df_dropped.loc[idx[i]] for i in range(len(idx))]

    첫날종가 = rows[0][base_field]
    시가차목록 = []
    종가차목록 = []
    시종가차목록 = []

    for row in rows[1:]:
        시가종가차 = row['시가'] - 첫날종가
        종가종가차 = row['종가'] - 첫날종가
        시가차목록.append(시가종가차)
        종가차목록.append(종가종가차)
        시종가차목록.append(시가종가차)
        시종가차목록.append(종가종가차)

    변화량 = [f'{n / 첫날종가 * 100: .2}%' for n in 시종가차목록]

    return 변화량

df_dropped['변화율']=None
df_gr=df_dropped.groupby(['종목명','code'], sort=False).agg({'변화율' : lambda x:check_group('종가', x)})
df_gr.to_excel('변화율.xlsx')


df_gr['d0']=df_gr['변화율'].apply(lambda x: x[0])
df_gr['d1']=df_gr['변화율'].apply(lambda x: x[1])
df_gr['d2']=df_gr['변화율'].apply(lambda x: x[2])
df_gr['d3']=df_gr['변화율'].apply(lambda x: x[3])
df_gr['d4']=df_gr['변화율'].apply(lambda x: x[4])
df_gr['d5']=df_gr['변화율'].apply(lambda x: x[5])
df_gr['d6']=df_gr['변화율'].apply(lambda x: x[6])
df_gr['d7']=df_gr['변화율'].apply(lambda x: x[7])
df_gr['d8']=df_gr['변화율'].apply(lambda x: x[8])
df_gr['d9']=df_gr['변화율'].apply(lambda x: x[9])
df_gr['d10']=df_gr['변화율'].apply(lambda x: x[10])
df_gr['d11']=df_gr['변화율'].apply(lambda x: x[11])

strategy_df = pd.read_csv('strategy.csv', encoding='cp949')
strategy_df['종목코드']=strategy_df['종목코드'].astype('str')
strategy_df['zfill종목코드']=strategy_df['종목코드'].str.zfill(6)

result_df=pd.merge(strategy_df, df_gr, left_on='zfill종목코드', right_on='code', how='outer')
result_df.to_excel('final_strategy.xlsx')


