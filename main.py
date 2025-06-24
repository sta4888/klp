import tkinter as tk                  # Библиотека для создания GUI
from pynput import keyboard           # Для перехвата нажатий клавиш
import threading                      # Для запуска перехвата клавиш в отдельном потоке

class KeyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Logger Display")       # Заголовок окна
        self.root.geometry("600x400")               # Размер окна
        self.root.configure(bg="black")             # Цвет фона

        # Создаем текстовое поле для отображения нажатых клавиш
        self.text_area = tk.Text(
            root,
            font=("Courier", 16),                   # Шрифт
            bg="black",                             # Черный фон
            fg="lime",                              # Зеленый текст
            wrap=tk.WORD                            # Перенос по словам
        )
        self.text_area.pack(expand=True, fill=tk.BOTH)   # Растягиваем по всему окну
        self.text_area.insert(tk.END, "Начни нажимать клавиши...\n")  # Начальное сообщение
        self.text_area.configure(state=tk.DISABLED)   # Делаем поле только для чтения

        # Запускаем поток с обработчиком клавиш
        self.listener_thread = threading.Thread(
            target=self.start_key_listener,
            daemon=True                            # Фоновый поток завершится при закрытии окна
        )
        self.listener_thread.start()

    def start_key_listener(self):
        # Функция-обработчик нажатий клавиш
        def on_press(key):
            try:
                key_str = key.char                # Если это обычный символ (буква, цифра и т.п.)
            except AttributeError:
                key_str = str(key).replace("Key.", "").upper()  # Если это спецклавиша (Enter, Shift...)

            # Запланировать обновление GUI из основного потока
            self.root.after(0, self.update_display, key_str)

        # Запускаем слушателя клавиш
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()  # Ожидаем завершения слушателя (будет работать вечно)

    def update_display(self, key_str):
        # Разблокируем поле, вставляем символ, блокируем обратно
        self.text_area.configure(state=tk.NORMAL)
        self.text_area.insert(tk.END, key_str + " ")  # Добавляем символ
        self.text_area.see(tk.END)                    # Прокручиваем вниз
        self.text_area.configure(state=tk.DISABLED)

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = KeyLoggerApp(root)
    root.mainloop()
