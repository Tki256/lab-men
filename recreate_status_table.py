import sqlite3

def recreate_status_table():
    conn = sqlite3.connect('lab_status.db')
    cursor = conn.cursor()

    # 既存のstatusテーブルを削除
    cursor.execute("DROP TABLE IF EXISTS status")

    # 新しいstatusテーブルを作成
    cursor.execute('''
    CREATE TABLE status (
        id INTEGER PRIMARY KEY,
        member_id INTEGER,
        status TEXT NOT NULL,
        timestamp DATETIME NOT NULL,
        FOREIGN KEY (member_id) REFERENCES members (id)
    )
    ''')

    conn.commit()
    conn.close()

recreate_status_table()