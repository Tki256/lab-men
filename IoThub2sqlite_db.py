import azure.functions as func
import logging
import json
import pyodbc
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

def main(event: func.EventHubEvent):
    body = event.get_body().decode('utf-8')
    logging.info(f'Python EventHub trigger processed an event: {body}')

    # SQL Database接続情報
    server = 'labmenserver.database.windows.net'
    database = 'LabMenDatabase'
    username = 'labmen'
    password = os.getenv("DATABASE_PASSWORD")
    driver = '{ODBC Driver 17 for SQL Server}'

    # データベース接続
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()

    # メッセージの解析と保存
    try:
        message = json.loads(body)
        member_id = message['member_id']
        status = message['status']
        timestamp = datetime.now()

        # SQLクエリの実行
        query = """
        INSERT INTO MemberStatus (MemberID, Status, Timestamp)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (member_id, status, timestamp))
        conn.commit()
        logging.info(f"Data inserted successfully: {message}")
    except Exception as e:
        logging.error(f"Error inserting data: {str(e)}")
    finally:
        cursor.close()
        conn.close()

main()