import tkinter as tk
from tkinter import messagebox
import cv2
import requests
import numpy as np
import os
from datetime import datetime, timedelta

# ESP32-CAM URL
url = 'http://XXXXXXXXXX/capture'
is_streaming = False
video_writer = None  # 用於錄製影片
frame_size = (320, 240)  # ESP32-CAM 的解析度
fps = 10  # 每秒幀數

# Functions

def parse_duration(duration_str):
    """ 將 HH:MM:SS 格式轉換為秒數 """
    try:
        h, m, s = map(int, duration_str.split(':'))
        return h * 3600 + m * 60 + s
    except ValueError:
        messagebox.showerror("錯誤", "請輸入正確的時間格式，例如：0:1:20")
        return None

def open_camera():
    global is_streaming, video_writer
    
    # 每次開啟畫面時重新讀取錄影時間
    duration_str = record_duration.get().strip()
    duration = parse_duration(duration_str)
    if duration is None:
        return
    
    if is_streaming:
        messagebox.showinfo("提示", "畫面已經開啟！")
        return
    
    is_streaming = True
    
    def stream():
        global is_streaming, video_writer
        save_dir = save_path.get().strip()
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # 建立影片檔案名稱
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_filename = f"{save_dir}/video_{timestamp}.mp4"
        video_writer = cv2.VideoWriter(
            video_filename, 
            cv2.VideoWriter_fourcc(*'mp4v'), 
            fps, 
            frame_size
        )

        # 錄影結束時間
        end_time = datetime.now() + timedelta(seconds=duration)
        
        while is_streaming and datetime.now() < end_time:
            try:
                img_resp = requests.get(url, timeout=5)
                img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                img = cv2.imdecode(img_arr, -1)
                
                # 加入時間戳
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(img, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # 顯示影像
                cv2.imshow("ESP32-CAM Stream", img)
                video_writer.write(img)
                
                if cv2.waitKey(1) == ord('q'):
                    break
            except Exception as e:
                messagebox.showerror("錯誤", f"無法取得影像：{e}")
                break
        
        close_camera()

    stream()

def close_camera():
    global is_streaming, video_writer
    is_streaming = False
    if video_writer:
        video_writer.release()
        video_writer = None
    cv2.destroyAllWindows()
    messagebox.showinfo("提示", "錄影已結束，影片已儲存。")

def take_photo():
    save_dir = save_path.get().strip()
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    file_name = f"{save_dir}/photo_{timestamp}.jpg"
    cv2.imwrite(file_name, img)
    messagebox.showinfo("提示", f"照片已儲存：{file_name}")

# GUI Setup
root = tk.Tk()
root.title("ESP32-CAM 控制介面")
root.geometry("400x300")

# Save Path
tk.Label(root, text="儲存位置：").pack()
save_path = tk.Entry(root, width=40)
save_path.pack()
save_path.insert(0, os.getcwd())

# Record Duration (HH:MM:SS)
tk.Label(root, text="錄製時間 (小時:分鐘:秒鐘)：").pack()
record_duration = tk.Entry(root, width=10)
record_duration.pack()
record_duration.insert(0, "0:1:20")

# Buttons
tk.Button(root, text="開啟畫面", command=open_camera).pack(pady=5)
tk.Button(root, text="關閉畫面", command=close_camera).pack(pady=5)
tk.Button(root, text="照相", command=take_photo).pack(pady=5)

root.mainloop()
