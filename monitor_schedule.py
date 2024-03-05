import asyncio
import logging
import pyautogui
import schedule
import time
import telegram
from move_ import find_inquiry, drag_window, find_balance, get_result, write_password, unprocessed_reason
import dataframe_image as dfi

formater = logging.Formatter("%(asctime)s - [%(filename)s:%(lineno)d] %(levelname)s -> %(message)s")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(filename)s:%(lineno)d] %(levelname)s -> %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.addHandler(logging.StreamHandler())
fileHandler = logging.FileHandler("test.log")
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formater)
logger.addHandler(fileHandler)


def repetition_work():
    logger.info("start repetition")
    find_balance(8655)
    result = get_result()

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
    logger.info("start unprocessed_reason")
    unprocessed_reason(8733)

def main1():
    logger.info("start main1")
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
    result=get_result()

    if result.empty:
        logger.info("no message to send")
    else:
        dfi.export(result, 'result.png')
        telegram_token = '6952860214:AAEUUVuetpIEhsv0NMGp3wF-IaXuFsUwS6w'
        telegram_id = '-1002074418471'

        async def send_telegram_photo(re8729s=None):
            try:
                bot = telegram.Bot(telegram_token)
                res = await bot.send_photo(chat_id=telegram_id,
                                           photo=open('C:/Users/soun/Desktop/nh_click/result.png', 'rb'))

                return re8729s

            # ---------------------------------------------
            # 모든 함수의 공통 부분(Exception 처리)
            # ---------------------------------------------
            except Exception:
                raise


        asyncio.run(send_telegram_photo())

    write_password("8733.png")
    unprocessed_reason(8733)

if __name__=="__main__":
    main1()
    schedule.every(20).seconds.do(repetition_work)

    while True:
        schedule.run_pending()
        time.sleep(0.2)
        