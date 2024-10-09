import tkinter as tk
from azure.iot.device import IoTHubDeviceClient, Message
import json
from datetime import datetime

CONNECTION_STRING = "YOUR_IOT_HUB_DEVICE_CONNECTION_STRING"

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def send_status(status):
    client = iothub_client_init()
    message = Message(json.dumps({
        "member_id": "MEMBER_ID",
        "status": status,
        "timestamp": datetime.now().isoformat()
    }))
    client.send_message(message)
    print(f"Message sent: {message}")
    client.shutdown()

def create_gui():
    window = tk.Tk()
    window.title("研究室在室管理")
    window.geometry("300x200")

    def update_status(status):
        send_status(status)
        result_label.config(text=f"状態を更新しました: {status}")

    tk.Button(window, text="在室", command=lambda: update_status("在室")).pack(fill=tk.X, padx=50, pady=10)
    tk.Button(window, text="外出", command=lambda: update_status("外出")).pack(fill=tk.X, padx=50, pady=10)
    tk.Button(window, text="帰宅", command=lambda: update_status("帰宅")).pack(fill=tk.X, padx=50, pady=10)

    result_label = tk.Label(window, text="")
    result_label.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_gui()