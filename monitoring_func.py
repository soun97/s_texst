import logging
import traceback
import time
import pandas as pd
import pyautogui
from configparser import ConfigParser


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

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
    time.sleep(0.8)
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
            logger.error(ex)
            traceback.print_exc()

    # pyautogui.getWindowsWithTitle("다른 이름으로 저장")[0].activate()
    time.sleep(0.5)
    pyautogui.typewrite('C:\\Users\\soun\\Desktop\\nh_click\\inquiry.csv')
    pyautogui.press('enter')
    pyautogui.click(inquiry_center)
    pyautogui.move(830, 0, duration=2)
    pyautogui.click()


def drag_window(image_path1, image_path2):
    """

    :param image_path1: 파일명만 전달하기
    :param image_path2: 파일명만 전달
    :return:
    """
    try:
        image_click_and_move(image_path1, 0, 0, sleep_sec=0)
        time.sleep(2)
        pyautogui.dragTo(1300, 0, duration=0.5)
    except pyautogui.ImageNotFoundException:
        # log or print the exception
        logger.info(f'image "{image_path1}" not found. Trying alternative image.')
        image_click_and_move(image_path2, 0, 0, sleep_sec=0)
        time.sleep(2)
        pyautogui.dragTo(1300, 0, duration=0.5)

def find_balance(win_num):
    """
    #종합잔고화면
    :param image_path1: 파일명만
    :param image_path2: 파일명만
    :return:
    """
    try:
        time.sleep(0.3)
        image_click_and_move(f"{win_num}.png", 0, 200, sleep_sec=3)

    except pyautogui.ImageNotFoundException:
        time.sleep(0.3)
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
            logger.error(ex)
            traceback.print_exc()


    pyautogui.typewrite('C:\\Users\\soun\\Desktop\\nh_click\\balance.csv')
    pyautogui.press('enter')
    logger.info("balance.csv file saved")
    time.sleep(0.2)

def unprocessed_reason(win_num):
    """
    "#미처리사유
    """
    try:
        image_click_and_move(f"{win_num}.png", 0, 105, sleep_sec=0)
        # pyautogui.press('enter')
    except pyautogui.ImageNotFoundException:
        image_click_and_move(f"{win_num}_active.png", 0, 105, sleep_sec=0)

    try:
        pyautogui.rightClick()
        time.sleep(0.3)
        # csv저장클릭
        save_csv = pyautogui.locateOnScreen(f'{image_path}/save_csv.png')
        save_center = pyautogui.center(save_csv)
        pyautogui.click(save_center)
        time.sleep(0.3)
    except Exception as ex:
        logger.error(ex)
    pyautogui.typewrite('C:\\Users\\soun\\Desktop\\nh_click\\unprocessed_reason.csv')
    pyautogui.press('enter')

def image_click_and_move(image_file_name, move_x, move_y, duration=0.5, sleep_sec=3):
    logger.debug(f"image_click_and_movie - {image_path}/{image_file_name}")
    image_position = pyautogui.locateOnScreen(f"{image_path}/{image_file_name}")
    image_center = pyautogui.center(image_position)
    time.sleep(sleep_sec)
    pyautogui.click(image_center)
    pyautogui.move(move_x, move_y, duration=duration)
    return image_center

def write_password(win_name):
    logger.debug(f"{image_path}/{win_name}")
    unprocessed = pyautogui.locateOnScreen(f"{image_path}/{win_name}")
    unprocessed_center = pyautogui.center(unprocessed)
    pyautogui.click(unprocessed_center)
    pyautogui.press('enter')
    pyautogui.typewrite('vhfptmxm')

def merge_files():
    logger.info("start merge files")
    file_dir = "C:/Users/soun/Desktop/nh_click/"
    # -------------------------------------------------------
    # balance, inquiry file filtering
    # ------------------------------------------------------
    balance_df = pd.read_csv(f'{file_dir}/balance.csv', encoding='cp949')
    new_balance = balance_df[['종목코드', '종목명', '구분', '잔고수량']]
    inquiry_df = pd.read_csv(f'{file_dir}/inquiry.csv', encoding='cp949')
    new_inquiry = inquiry_df[['종목코드', '종목명', '기준수량']]

    # 서버실 컴퓨터에서는 필요 없는 코드 > inquiry 타입 비교해서 타입변경하기(수정)
    # new_inquiry['종목코드'] = new_inquiry['종목코드'].astype('str')
    # new_balance['종목코드'] = new_balance['종목코드'].astype('str')
    # -------------------------------------------------------
    # merge & calculate :설정상환단계보다 현금보유량이 낮으면 알림
    # ------------------------------------------------------
    merge = pd.merge(left=new_balance, right=new_inquiry, how='outer', on='종목코드')
    merge[f'기준가*{step}'] = merge['기준수량'] * int(step)
    merge = merge.dropna()
    merge['잔고수량'] = merge['잔고수량'].str.replace(",", "").astype('int')
    return merge

def get_loan_balance():
    # -------------------------------------------------------
    # balance, inquiry file filtering : 대출보유 종목 중 현재 잔고 기준수량 이하인 종목
    # ------------------------------------------------------
    merge = merge_files()
    담보 = merge[merge['구분'] == '대출담보']
    현금 = merge[merge['구분'] == '현금']
    merge2 = pd.merge(담보, 현금, left_on='종목코드', right_on='종목코드', how='left', suffixes=('_대출', '_현금'))
    result = merge2[merge2['잔고수량_현금'] < merge2[f'기준가*{step}_현금']]
    return result


def get_balance():
    """
    대출 보유하고 있지 않은 종목 중 현재 잔고 수량이 0인 것
    :return: 현재잔고 0인 종목
    """
    merge = merge_files()
    filtered_df = merge.groupby('종목명_x').filter(lambda x: (x['구분'] == '현금').all())
    empty_balance = filtered_df[filtered_df['잔고수량'] == 0]
    empty_balance = pd.DataFrame(empty_balance)
    return empty_balance

if __name__ == "__main__":
    main1()

