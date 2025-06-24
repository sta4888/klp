import tkinter as tk
from pynput import keyboard
import threading

class KeyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Logger Display")
        self.root.geometry("600x400")
        self.root.configure(bg="black")

        self.text_area = tk.Text(root, font=("Courier", 16), bg="black", fg="lime", wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.insert(tk.END, "Начни нажимать клавиши...\n")
        self.text_area.configure(state=tk.DISABLED)

        self.listener_thread = threading.Thread(target=self.start_key_listener, daemon=True)
        self.listener_thread.start()



    def start_key_listener(self):
        def on_press(key):
            try:
                key_str = key.char
            except AttributeError:
                key_str = str(key).replace("Key.", "").upper()

            self.root.after(0, self.update_display, key_str)

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def update_display(self, key_str):
        self.text_area.configure(state=tk.NORMAL)
        self.text_area.insert(tk.END, key_str + " ")
        self.text_area.see(tk.END)
        self.text_area.configure(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyLoggerApp(root)
    root.mainloop()
