# [csv파일읽고 csv저장]
import pandas as pd
import os
from datetime import datetime

dir = "C:\souncoding"
file = 'C:\souncoding\strategy.csv'
datalist = pd.read_csv(file,encoding='cp949', dtype='object')
# datalist['일자'] = datalist['일자'].astype(str)
# dt = [datetime.strptime(date,"%Y%m%d").strftime("%Y-%m-%d") for date in datalist['일자']]
# datalist['일자'] = dt
# datalist['일자'] =pd.to_datetime(datalist['일자'])
codelist = [str(i).zfill(6)+'.csv' for i in datalist['종목코드']]
datelist = datalist['일자'].values
number = 0
headerframe =pd.DataFrame(columns=['종목코드','시가','종가'])

def find_data(file_name, number):
     newdata = pd.read_csv(os.path.join(dir,file_name), encoding='cp949')
     row_num = newdata[newdata['일자'] == datelist[number]].index[0]
     df2 = newdata.loc[row_num : row_num+69, ['종목코드','시가','종가','일자']]
     return df2

for i in codelist:
    df2 = find_data(i,number)
    headerframe = pd.concat((headerframe,df2),axis=0)
    number = number+1


headerframe.to_csv('C:/souncoding/append.csv',encoding='cp949')

tax = 0.99985
stock_tax = 0.9977

def chane_rate(a,b):
    if a==0:
        return 0
    else:    
        return str(round((b-a)*100/a,2)) + "%" #cal(a, b)에 return한 값이 들어간다.

def earning_rate(a,b):
    if a==0:
        return 0
    else:    
        return str(round((b*tax*stock_tax-a*tax)*100/a*tax,2)) + "%" #cal(a, b)에 return한 값이 들어간다.

file = 'C:/souncoding/append.csv'
df = pd.read_csv(file,encoding='cp949')
sigalist = df['시가']
jongalist= df['종가']
resultlist = []
resultlist_b = []

for i in range(len(sigalist)):
    a = sigalist[i]
    b = jongalist[i]
    result = chane_rate(a,b)
    result_b = earning_rate(a,b)
    resultlist.append(result)
    resultlist_b.append(result_b)
# print(resultlist)

df2= pd.DataFrame({'변화율': resultlist, '수익률':resultlist_b})#dataframe 만드는 방법: 
# print(df,df2)
pd.concat((df,df2), axis = 1).to_csv('C:/souncoding/append.csv', encoding='cp949', index=False)#dataframe끼리 더하는 방법