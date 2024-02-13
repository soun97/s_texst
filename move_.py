import asyncio
import logging
import traceback
import time
import pandas as pd
import pyautogui
from configparser import ConfigParser
import telegram
import dataframe_image as dfi

from func_click_nh import get_result

logging.basicConfig(filename='my_log_file.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
config = ConfigParser()
config.read("config.ini")

# config=pd.read_excel('config.xlsx')
# '이미지경로'
image_path = config["images"]["dir"]

print("image_path : ", image_path)
# 대출상환단계
step=config["loan"]["step"]


def find_inquiry():
    pyautogui.click(133,63)
    pyautogui.typewrite('8729')
    inquiry_center = image_click_and_move("8729.png", 50, 200, sleep_sec=0)

    success = False
    while not success:
        try:
            time.sleep(0.1)
            pyautogui.rightClick()
            time.sleep(0.5)
            # csv저장클릭
            image_click_and_move("save_csv.png", 0, 0, sleep_sec=0)
            success = True
            time.sleep(0.5)
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    # pyautogui.getWindowsWithTitle("다른 이름으로 저장")[0].activate()
    time.sleep(0.5)
    pyautogui.typewrite('C:\\Users\\soun\\Desktop\\nh_click\\inquiry.csv')
    pyautogui.press('enter')
    pyautogui.click(inquiry_center)
    pyautogui.move(830, 0, duration=2)
    pyautogui.click()

def drag_window(image_path1,image_path2):
    """
    
    :param image_path1: 파일명만 전달하기 
    :param image_path2: 파일명만 전달
    :return: 
    """
    try:
        image_click_and_move(image_path1, 0, 0, sleep_sec=0)
        time.sleep(2)
        pyautogui.dragTo(1350,450, duration=0.5)
    except pyautogui.ImageNotFoundException:
        #log or print the exception
        print(f'image "{image_path1}" not found. Trying alternative image.')
        image_click_and_move(image_path2, 0, 0, sleep_sec=0)
        time.sleep(2)
        pyautogui.dragTo(1350, 450, duration=0.5)

def find_balance(win_num):
    """
    #종합잔고화면
    :param image_path1: 파일명만
    :param image_path2: 파일명만
    :return:
    """
    try:
        image_click_and_move(f"{win_num}.png", 0, 200, sleep_sec=3)
    except pyautogui.ImageNotFoundException:
        image_click_and_move(f"{win_num}_active.png", 0, 200, sleep_sec=3)


    success = False
    while not success:
        try:
            time.sleep(0.1)
            pyautogui.rightClick()
            time.sleep(0.5)
            # csv저장클릭
            image_click_and_move("save_csv.png", 0, 0, sleep_sec=0)
            success = True
            time.sleep(0.5)
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    # pyautogui.getWindowsWithTitle("다른 이름으로 저장")[0].activate()
    # pyautogui.press('hangul')
    pyautogui.typewrite('C:\\Users\\soun\\Desktop\\nh_click\\balance.csv')
    pyautogui.press('enter')


def unprocessed_reason(win_num):
    """
    "#미처리사유
    """
    try:
        image_click_and_move(f"{win_num}.png", 0, 200, sleep_sec=0)
    except pyautogui.ImageNotFoundException:
        image_click_and_move(f"{win_num}_active.png", 0, 200, sleep_sec=0)

    # success = False
    # while not success:
    #     try:
    #         time.sleep(0.1)
    #         pyautogui.rightClick()
    #         time.sleep(0.5)
    #         # csv저장클릭
    #         save_csv = pyautogui.locateOnScreen(f'{image_path}/save_csv.png')
    #         save_center = pyautogui.center(save_csv)
    #         pyautogui.click(save_center)
    #         success = True
    #         time.sleep(0.5)
    #     except Exception as ex:
    #         print(ex)
    #         traceback.print_exc()
    #
    # # pyautogui.getWindowsWithTitle("다른 이름으로 저장")[0].activate()
    # # pyautogui.press('hangul')
    # pyautogui.typewrite('C:\\Users\\soun\\Desktop\\nh_click\\balance.csv')
    # pyautogui.press('enter')


def image_click_and_move(image_file_name, move_x, move_y, duration=0.5, sleep_sec=3):
    image_position = pyautogui.locateOnScreen(f"{image_path}/{image_file_name}")
    image_center = pyautogui.center(image_position)
    time.sleep(sleep_sec)
    pyautogui.click(image_center)
    pyautogui.move(move_x, move_y, duration=duration)
    return image_center


def write_password(win_name):
    unprocessed = pyautogui.locateOnScreen(f"{image_path}/{win_name}")
    unprocessed_center = pyautogui.center(unprocessed)
    pyautogui.click(unprocessed_center)
    pyautogui.press('enter')
    pyautogui.typewrite('1234')







find_inquiry()
pyautogui.click(x=128, y=63)
pyautogui.typewrite('8655')
time.sleep(0.5)
pyautogui.click(x=128, y=63)
pyautogui.typewrite('8733')
drag_window("8655.png", "8733_active.png")
find_balance(8655)
write_password("8733.png")
unprocessed_reason(8733)
# result=get_result()
# dfi.export(result,'result.png')



#
# telegram_token = '6952860214:AAEUUVuetpIEhsv0NMGp3wF-IaXuFsUwS6w'
# telegram_id = '-1002074418471'
# async def send_telegram_photo():
#     try:
#         bot = telegram.Bot(telegram_token)
#         res = await bot.send_photo(chat_id=telegram_id,
#                                    photo=open('C:/Users/soun/Desktop/nh_click/result.png', 'rb'))
#
#         return res
#
#     # ---------------------------------------------
#     # 모든 함수의 공통 부분(Exception 처리)
#     # ---------------------------------------------
#     except Exception:
#         raise


