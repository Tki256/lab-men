import sqlite3

def check_db_structure():
    conn = sqlite3.connect('lab_status.db')
    cursor = conn.cursor()

    # テーブル一覧の取得
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("テーブル一覧:")
    for table in tables:
        print(table[0])
        # 各テーブルの構造を表示
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print(f"  カラム:")
        for column in columns:
            print(f"    {column[1]} ({column[2]})")
        print()

    conn.close()

check_db_structure()