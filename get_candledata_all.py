import traceback

from pykiwoom.kiwoom import *
import datetime
import time

# 로그인
kiwoom = Kiwoom()
kiwoom.CommConnect()

# 전종목 종목코드
kospi = kiwoom.GetCodeListByMarket('0')
kosdaq = kiwoom.GetCodeListByMarket('10')
codes = kospi + kosdaq

# 문자열로 오늘 날짜 얻기
now = datetime.datetime.now()
today = now.strftime("%Y%m%d")

# 전 종목의 일봉 데이터
try:
    for i, code in enumerate(codes):
        dfs = []
        print(f"{i}/{len(codes)} {code}")
        df = kiwoom.block_request("opt10081",
                                  종목코드=code,
                                  기준일자=today,
                                  수정주가구분=0,
                                  output="주식일봉차트조회",
                                  next=0)

        dfs.append(df)
        count=0
        while kiwoom.tr_remained and count <10:
            count += 1
            df=kiwoom.block_request("opt10081",
                                  종목코드=code,
                                  기준일자=today,
                                  수정주가구분=0,
                                  output="주식일봉차트조회",
                                  next=2
            )
            dfs.append(df)
            time.sleep(0.3)

        df = pd.concat(dfs)
        df['종목코드'] = code
        out_name = f"data/{code}.xlsx"
        df.to_excel(out_name)
        time.sleep(2.6)
except Exception as ex:
    traceback.print_exc()