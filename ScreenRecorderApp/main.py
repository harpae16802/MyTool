import tkinter as tk
from tkinter import messagebox
import pyautogui
from PIL import Image, ImageDraw, ImageTk
import os
import time
import threading

class ScreenRecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("螢幕錄製器")
        self.master.geometry("300x200")
        self.master.configure(bg='#2e3f4f')

        self.record_button = tk.Button(master, text="開始錄製", command=self.start_recording)
        self.record_button.pack(pady=20)

        self.stop_button = tk.Button(master, text="停止錄製", state=tk.DISABLED, command=self.stop_recording)
        self.stop_button.pack(pady=20)

        self.recording = False
        self.frames = []

    def start_recording(self):
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.recording = True
        self.frames = []
        self.select_area()

    def stop_recording(self):
        self.recording = False
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.create_gif()

    def select_area(self):
        self.master.withdraw()
        time.sleep(0.2)
        self.show_canvas()

    def show_canvas(self):
        self.canvas_window = tk.Toplevel(self.master)
        self.canvas_window.attributes('-fullscreen', True)
        self.canvas_window.attributes('-topmost', True)
        self.canvas_window.attributes('-alpha', 0.3)
        self.canvas_window.configure(bg='gray')

        screenshot = pyautogui.screenshot()
        self.screenshot_image = ImageTk.PhotoImage(screenshot)

        self.canvas = tk.Canvas(self.canvas_window, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.screenshot_image)

        self.start_x = self.start_y = 0
        self.rect = None
        self.text = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = None
        self.text = None

    def on_mouse_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        if self.text:
            self.canvas.delete(self.text)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline='red', fill='blue', stipple='gray50')
        width = abs(event.x - self.start_x)
        height = abs(event.y - self.start_y)
        self.text = self.canvas.create_text((self.start_x + event.x) / 2, (self.start_y + event.y) / 2, text=f"{width}x{height}", fill="white")

    def on_button_release(self, event):
        self.end_x, self.end_y = event.x, event.y
        self.canvas_window.destroy()
        self.master.deiconify()  # 重新顯示主窗口
        self.record_area(self.start_x, self.start_y, self.end_x, self.end_y)

    def record_area(self, start_x, start_y, end_x, end_y):
        start_x, start_y = min(start_x, end_x), min(start_y, end_y)
        end_x, end_y = max(start_x, end_x), max(start_y, end_y)
        width, height = end_x - start_x, end_y - start_y

        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # 使用線程來避免阻塞主線程
        threading.Thread(target=self.record, args=(start_x, start_y, width, height)).start()

    def record(self, start_x, start_y, width, height):
        while self.recording:
            frame = pyautogui.screenshot(region=(start_x, start_y, width, height))
            self.frames.append(frame)
            time.sleep(0.1)

    def create_gif(self):
        self.master.withdraw()
        messagebox.showinfo("處理中", "正在生成GIF，請稍候...")
        folder_path = "C:\\ScreenRecorderGIFs"
        os.makedirs(folder_path, exist_ok=True)  # 確保目錄存在
        gif_path = os.path.join(folder_path, "recording.gif")
        try:
            if self.frames:
                self.frames[0].save(gif_path, save_all=True, append_images=self.frames[1:], duration=100, loop=0)
            self.master.deiconify()
            messagebox.showinfo("成功", f"GIF已保存到C:\\ScreenRecorderGIFs文件夾中，文件名為recording.gif")
        except Exception as e:
            self.master.deiconify()
            messagebox.showerror("錯誤", f"無法保存GIF文件: {str(e)}")

def main():
    try:
        root = tk.Tk()
        app = ScreenRecorderApp(root)
        root.mainloop()
    except Exception as e:
        error_message = str(e)
        with open("error_log.txt", "w") as f:
            f.write(error_message)
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("錯誤", error_message)
        root.destroy()

if __name__ == "__main__":
    main()
