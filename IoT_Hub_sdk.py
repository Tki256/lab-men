import os
from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv

load_dotenv()
# デバイスの接続文字列を設定
IOT_HUB_CON_STR = os.getenv("IOT_HUB_CON_STR")

# JSONデータ
json_data = '{"temperature": 25, "humidity": 60}'

# IoT Hubデバイスクライアントのインスタンスを作成
client = IoTHubDeviceClient.create_from_connection_string(IOT_HUB_CON_STR)

try:
    # メッセージ作成
    message = Message(json_data)

    # メッセージを送信
    print(f"メッセージを送信中: {json_data}")
    client.send_message(message)
    print("メッセージが送信されました")

except Exception as e:
    print("送信中にエラーが発生しました: {}".format(e))

finally:
    # クライアントの終了
    client.shutdown()

