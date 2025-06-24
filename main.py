import tkinter as tk
from pynput import keyboard
import threading
import time
import json  # Для сохранения в JSON
import os


class KeyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Logger Display")
        self.root.geometry("600x400")
        self.root.configure(bg="black")

        self.text_area = tk.Text(
            root,
            font=("Courier", 14),
            bg="black",
            fg="lime",
            wrap=tk.WORD
        )
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.insert(tk.END, "Нажимайте клавиши...\n")
        self.text_area.configure(state=tk.DISABLED)

        self.start_time = time.time()
        self.key_log = []  # Список для хранения данных о нажатиях

        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Запуск слушателя клавиш в фоновом потоке
        self.listener_thread = threading.Thread(
            target=self.start_key_listener,
            daemon=True
        )
        self.listener_thread.start()

    def start_key_listener(self):
        def on_press(key):
            elapsed = time.time() - self.start_time
            timestamp = round(elapsed, 3)

            try:
                key_str = key.char
            except AttributeError:
                key_str = str(key).replace("Key.", "").upper()

            # Добавляем в лог
            self.key_log.append({
                "time": timestamp,
                "key": key_str
            })

            # Отображаем на экране
            display_str = f"[{timestamp:.3f}s] {key_str}"
            self.root.after(0, self.update_display, display_str)

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def update_display(self, text):
        self.text_area.configure(state=tk.NORMAL)
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)
        self.text_area.configure(state=tk.DISABLED)

    def on_close(self):
        # Сохраняем key_log в JSON-файл
        try:
            with open("keylog.json", "w", encoding="utf-8") as f:
                json.dump(self.key_log, f, indent=4, ensure_ascii=False)
            print("Сохранено в keylog.json")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")

        self.root.destroy()  # Закрываем окно


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyLoggerApp(root)
    root.mainloop()
