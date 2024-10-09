# これはサンプルの Python スクリプトです。

# Shift+F10 を押して実行するか、ご自身のコードに置き換えてください。
# Shift を2回押す を押すと、クラス/ファイル/ツールウィンドウ/アクション/設定を検索します。

def front_GUI():
    import PySimpleGUI as sg
    import sqlite3
    from datetime import datetime

    # データベース接続
    conn = sqlite3.connect('lab_status.db')
    cursor = conn.cursor()

    # テーブル作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS status (
        id INTEGER PRIMARY KEY,
        member_id INTEGER,
        status TEXT NOT NULL,
        timestamp DATETIME NOT NULL,
        FOREIGN KEY (member_id) REFERENCES members (id)
    )
    ''')

    # サンプルメンバーの追加（実際の使用時は管理画面から追加するようにしてください）
    sample_members = ['山田太郎', '鈴木花子', '佐藤次郎']
    for member in sample_members:
        cursor.execute('INSERT OR IGNORE INTO members (name) VALUES (?)', (member,))
    conn.commit()

    def get_all_members():
        cursor.execute('SELECT name FROM members ORDER BY name')
        return [row[0] for row in cursor.fetchall()]

    def update_status(member_name, status):
        cursor.execute('SELECT id FROM members WHERE name = ?', (member_name,))
        member_id = cursor.fetchone()[0]
        cursor.execute('INSERT INTO status (member_id, status, timestamp) VALUES (?, ?, ?)',
                       (member_id, status, datetime.now()))
        conn.commit()

    def get_current_status(member_name):
        cursor.execute('''
        SELECT status FROM status
        JOIN members ON status.member_id = members.id
        WHERE members.name = ?
        ORDER BY timestamp DESC LIMIT 1
        ''', (member_name,))
        result = cursor.fetchone()
        return result[0] if result else "Unknown"

    # GUIテーマの設定
    sg.theme('LightBlue')

    # メイン画面のレイアウト
    main_layout = [
        [sg.Text("研究室メンバー状態管理システム", font=("Any", 20))],
        [sg.Listbox(values=get_all_members(), size=(30, 10), key="-MEMBERS-", enable_events=True)],
        [sg.Button("更新", size=(10, 1)), sg.Button("終了", size=(10, 1))]
    ]

    # 状態選択画面のレイアウト
    status_layout = [
        [sg.Text("", key="-MEMBER_NAME-", font=("Any", 16))],
        [sg.Text("現在の状態: ", font=("Any", 14)), sg.Text("", key="-CURRENT_STATUS-", font=("Any", 14))],
        [sg.Button("在室", size=(10, 2)), sg.Button("実験所", size=(10, 2)), sg.Button("帰宅", size=(10, 2))],
        [sg.Button("戻る", size=(10, 1))]
    ]

    # メインウィンドウの作成
    main_window = sg.Window("研究室状態管理", main_layout, finalize=True)

    # イベントループ
    while True:
        event, values = main_window.read()
        if event == sg.WINDOW_CLOSED or event == "終了":
            break
        elif event == "-MEMBERS-" and values["-MEMBERS-"]:
            selected_member = values["-MEMBERS-"][0]
            main_window.hide()

            # 状態選択ウィンドウの作成
            status_window = sg.Window("状態選択", status_layout, finalize=True)
            status_window["-MEMBER_NAME-"].update(f"{selected_member}の状態")
            status_window["-CURRENT_STATUS-"].update(get_current_status(selected_member))

            # 状態選択画面のイベントループ
            while True:
                status_event, status_values = status_window.read()
                if status_event == sg.WINDOW_CLOSED or status_event == "戻る":
                    break
                elif status_event in ["在室", "実験所", "帰宅"]:
                    update_status(selected_member, status_event)
                    status_window["-CURRENT_STATUS-"].update(status_event)
                    sg.popup(f"{selected_member}の状態を{status_event}に更新しました")

            status_window.close()
            main_window.un_hide()
        elif event == "更新":
            main_window["-MEMBERS-"].update(values=get_all_members())

    # ウィンドウとデータベース接続を閉じる
    main_window.close()
    conn.close()

def main():
    front_GUI()


# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == '__main__':
    main()

# PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください
