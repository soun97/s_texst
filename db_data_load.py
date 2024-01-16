import pymysql


def insert_csv_to_db(table_name, csv_file):
    # read csv
    df = pd.read_csv("~~")

    rows = df.to_dict("records")

    # 종목코드 = rows[0].get("종목코드")
    for row in rows:

    # for loop over csv list

    query = f"""
        INSERT INTO `original_db` (
            `index`, `종목코드`, `현재가`, `거래량`, `거래대금`, 
            `일자`, `시가`, `고가`, `저가`, `수정주가구분`, 
            `수정비율`, `대업종구분`, `소업종구분`, `종목정보`, `수정주가이벤트`, 
            `전일종가`
        ) VALUES (
            {index}, 'ABCD', 198500, 331186, 65619, 
            20231227, 198700, 199300, 197200, 4, 
            0, NULL, NULL, NULL, NULL, 
        NULL)
    """

    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='thdns^^04', db='stock_data', charset='utf8')
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()


if __name__ == "__main__":
    insert_csv_to_db("", "")