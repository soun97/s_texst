import asyncio
import logging
import traceback
import pyautogui
import schedule
import time
import telegram
import dataframe_image as dfi
from datetime import datetime, timedelta
from configparser import ConfigParser
import pandas as pd
from monitoring_func import find_inquiry, drag_window, find_balance, unprocessed_reason, image_click_and_move, \
    write_password, merge_files, get_balance, get_loan_balance
from nh_click_class import 반복작업
from telebot import TeleBot

formater = logging.Formatter("%(asctime)s - [%(filename)s:%(lineno)d] %(levelname)s -> %(message)s")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(filename)s:%(lineno)d] %(levelname)s -> %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.addHandler(logging.StreamHandler())
fileHandler = logging.FileHandler("test.log")
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formater)
logger.addHandler(fileHandler)

config = ConfigParser()
config.read("config.ini")

# config=pd.read_excel('config.xlsx')
# '이미지경로'
image_path = config["images"]["dir"]

print("image_path : ", image_path)
# 대출상환단계
step=config["loan"]["step"]


main_job_done = False

log_print = None  # 로그를 찍기위한 함수

bot = TeleBot()

def start_scheduler(start_time, end_time, logfunc):
    """
    스케줄러 이용해서 프로그램 돌리기
    :param start_time: 프로그램 시작시간
    :param end_time: 프로그램 끝내는 시간
    :param logfunc: 로그 찍어주기
    :return: main1, repetition_work작업을 자동으로  정해진 시간에 진행하고 마치기.
    """
    # global log_print
    # log_print = logfunc
    logger.info(f"Start at : {start_time}, until : {end_time}")

    try:
        schedule.every().day.at(start_time).do(main1)
        # schedule.every(10).seconds.hours.at(start_time).until(end_time).do(repetition_work)
        schedule.every(10).seconds.do(repetition_work)

        while True:
            schedule.run_pending()
            time.sleep(0.2)

    except Exception as ex:
        logging.error(traceback.format_exc())
        asyncio.run(bot.send_telegram_message(f"exception raised: {traceback.format_exc()}"))


def repetition_work():
    """
    반복작업 함수
    loop돌기[대출잔고,현재잔고 확인 > 미처리사유확인]

    """
    # global main_job_done
    # if not main_job_done:
    #     logger.debug("main job not done")
    #     return

    logger.info("start repetition")
    # find_balance(8655)

    work = 반복작업(step=step, image_path=image_path)

    result = work.get_loan_balance()

    if result.empty:
        logger.info("result is empty")
    else:
        dfi.export(result, 'result.png')


        asyncio.run(bot.send_telegram_photo('result'))

    # result2=work.get_balance()
    #
    # if result2.empty:
    #     logger.info("result2 is empty")
    #
    # else:
    #     dfi.export(result2, 'result2.png')
    #     telegram_token = '6952860214:AAEUUVuetpIEhsv0NMGp3wF-IaXuFsUwS6w'
    #     telegram_id = '-1002074418471'
    #
    #     async def send_telegram_photo():
    #         try:
    #             bot = telegram.Bot(telegram_token)
    #             res = await bot.send_photo(chat_id=telegram_id,
    #                                        photo=open('C:/Users/soun/Desktop/nh_click/result2.png', 'rb'))
    #
    #             return res
    #
    #         # ---------------------------------------------
    #         # 모든 함수의 공통 부분(Exception 처리)
    #         # ---------------------------------------------
    #         except Exception:
    #             raise
    #
    #     logger.info("no message to send")
    #     asyncio.run(send_telegram_photo())
    #
    # logger.info("start unprocessed_reason")
    # unprocessed_reason(8733)

def main1():
    """
    연속조회부터 미처리사유작업까지 싸이클 한바퀴 돌기

    :return: 기준가 데이터 받기, 잔고확인, 미처리사유 비밀번호작성 및 사유확인, 텔레그램 메세지 발송
    """
    # log_print("start main1")
    find_inquiry()
    time.sleep(2)
    pyautogui.click(x=128, y=63)
    pyautogui.typewrite('8655')
    time.sleep(2)
    pyautogui.click(x=128, y=63)
    pyautogui.typewrite('8733')
    time.sleep(2)
    drag_window("8733_active.png", "8655.png")
    find_balance(8655)
    result = get_loan_balance()

    if result.empty:
        logger.info("no message to send")
    else:
        dfi.export(result, 'result.png')

        asyncio.run(bot.send_telegram_photo("result"))

    result2 = get_balance()

    if result2.empty:
        logger.info("result2 is empty")

    else:
        dfi.export(result2, 'result2.png')
        telegram_token = '6952860214:AAEUUVuetpIEhsv0NMGp3wF-IaXuFsUwS6w'
        telegram_id = '-1002074418471'

        async def send_telegram_photo():
            try:
                bot = telegram.Bot(telegram_token)
                res = await bot.send_photo(chat_id=telegram_id,
                                           photo=open('C:/Users/soun/Desktop/nh_click/result2.png', 'rb'))

                return res

            # ---------------------------------------------
            # 모든 함수의 공통 부분(Exception 처리)
            # ---------------------------------------------
            except Exception:
                raise

        logger.info("no message to send")
        asyncio.run(send_telegram_photo())

    write_password("8733.png")
    unprocessed_reason(8733)
    global main_job_done
    main_job_done = True
    logger.info("main job done")


if __name__ == "__main__":
    repetition_work()