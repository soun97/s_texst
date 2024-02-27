import logging
import traceback

from pykiwoom import KiwoomManager
from pykiwoom.kiwoom import *
import os
import datetime
import time

formater = logging.Formatter("%(asctime)s - [%(filename)s:%(lineno)d] %(levelname)s -> %(message)s")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(filename)s:%(lineno)d] %(levelname)s -> %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.addHandler(logging.StreamHandler())
fileHandler = logging.FileHandler("kiwoom.log")
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formater)
logger.addHandler(fileHandler)

def get_10081():
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

    already_download_codes = get_file_name()

    # 전 종목의 일봉 데이터
    try:
        for i, code in enumerate(codes):
            if code in already_download_codes:
                logger.info(f"code [{code}] aleady exists skip...")
                continue

            logger.info(f"{i}/{len(codes)} {code}")
            dfs = get_opt10081_code(code, today, pages=100, sleep_seconds=0.8)

            dfs['종목코드'] = code
            out_name = f"original/{code}.xlsx"
            dfs.to_excel(out_name)
            time.sleep(3.6)
            logger.info(f"save file for {out_name}")
    except Exception as ex:
        traceback.print_exc()
        logger.error(traceback.format_exc())


def get_opt10081_code(code, base_date, pages=100, sleep_seconds=0.3):
    logger.info(f"start opt10081 {code} base_date : {base_date}")
    dfa = pd.DataFrame()

    km = KiwoomManager()
    tr_cmd = {
        'rqname': "opt10081",
        'trcode': 'opt10081',
        'next': '0',
        'screen': '1000',
        'input': {
            "종목코드": code,
            "기준일자": base_date,
            "수정주가구분": "0",
        },
        'output': ["종목코드", "현재가", "거래량", "거래대금", "일자", "시가", "고가", "저가", "수정주가구분", "수정비율", "대업종구분", "소업종구분", "종목정보",
                   "수정주가이벤트", "전일종가"]
    }
    for i in range(pages):
        if i != 0:
            tr_cmd['next'] = '2'

        km.put_tr(tr_cmd)
        data = km.get_tr()
        dfa = pd.concat([dfa, data[0]])
        logger.debug(f"[{code}] get {len(data[0])}, sleep {sleep_seconds}...")
        time.sleep(sleep_seconds)

    return dfa


def get_file_name():
    d = "C:\\Users\\soun\\Documents\\kiwoom_test\\original"
    filenames = os.listdir(d)
    # for f in filenames:
    #     print(f.replace(".xlsx", ""))
    #
    codes = [f.replace(".xlsx", "") for f in filenames]
    return codes


if __name__ == "__main__":
    get_10081()
    # get_file_name()
    # dfs = get_opt10081_code("005420", "20240227", 3)
    # print(dfs.describe())
    # print(dfs.head(3))
    # print(dfs.tail(3))
