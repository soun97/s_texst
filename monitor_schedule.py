import asyncio
import logging
import traceback
import pyautogui
import schedule
import time
import telegram
from move_ import find_inquiry, drag_window, find_balance, write_password, unprocessed_reason, get_loan_balance, get_balance
import dataframe_image as dfi
from datetime import datetime

formater = logging.Formatter("%(asctime)s - [%(filename)s:%(lineno)d] %(levelname)s -> %(message)s")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(filename)s:%(lineno)d] %(levelname)s -> %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.addHandler(logging.StreamHandler())
fileHandler = logging.FileHandler("test.log")
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formater)
logger.addHandler(fileHandler)

main_job_done = False

log_print = None  # 로그를 찍기위한 함수

def repetition_work():
    global main_job_done
    if not main_job_done:
        logger.debug("main job not done")
        return

    logger.info("start repetition")
    find_balance(8655)
    result = get_loan_balance()

    if result.empty:
        logger.info("result is empty")
    else:
        dfi.export(result, 'result.png')
        telegram_token = '6952860214:AAEUUVuetpIEhsv0NMGp3wF-IaXuFsUwS6w'
        telegram_id = '-1002074418471'

        async def send_telegram_photo():
            try:
                bot = telegram.Bot(telegram_token)
                res = await bot.send_photo(chat_id=telegram_id,
                                           photo=open('C:/Users/soun/Desktop/nh_click/result.png', 'rb'))

                return res

            # ---------------------------------------------
            # 모든 함수의 공통 부분(Exception 처리)
            # ---------------------------------------------
            except Exception:
                raise

        logger.info("no message to send")
        asyncio.run(send_telegram_photo())

    result2=get_balance()

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

    logger.info("start unprocessed_reason")
    unprocessed_reason(8733)

def main1():
    log_print("start main1")
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
        telegram_token = '6952860214:AAEUUVuetpIEhsv0NMGp3wF-IaXuFsUwS6w'
        telegram_id = '-1002074418471'

        async def send_telegram_photo():
            try:
                bot = telegram.Bot(telegram_token)
                res = await bot.send_photo(chat_id=telegram_id,
                                           photo=open('C:/Users/soun/Desktop/nh_click/result.png', 'rb'))



            # ---------------------------------------------
            # 모든 함수의 공통 부분(Exception 처리)
            # ---------------------------------------------
            except Exception:
                raise


        asyncio.run(send_telegram_photo())

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


async def send_telegram_message(text):
    telegram_token = '6952860214:AAEUUVuetpIEhsv0NMGp3wF-IaXuFsUwS6w'
    telegram_id = '-1002074418471'
    try:
        bot = telegram.Bot(telegram_token)
        res = await bot.send_message(chat_id=telegram_id,
                                   text=text)
    # ---------------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ---------------------------------------------
    except Exception:
        raise Exception


def start_scheduler(start_time, end_time, logfunc):
    global log_print
    log_print = logfunc

    try:
        schedule.every().day.at(start_time).do(main1)
        schedule.every(15).seconds.hours.at(start_time).until(end_time).do(repetition_work)

        while True:
            schedule.run_pending()
            time.sleep(0.2)

    except Exception as ex:
        logging.error(ex)
        asyncio.run(send_telegram_message(f"exception raised: {traceback.format_exc()}"))


if __name__ == "__main__":
    start_scheduler("15:37", "15:40")
    # print(is_time_over("15:"))