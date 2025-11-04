import tkinter as tk
from tkinter import ttk
from pynput import keyboard, mouse
import threading
import time
import sv_ttk

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("sola clicker thingy")
        self.root.geometry("280x290")
        self.root.resizable(False, False)

        self.target_key = None
        self.clicking = False
        self.running = False
        self.listener = None
        self.click_mode = tk.StringVar(value="hold")
        self.mouse_controller = mouse.Controller()

        # Set Sunvalley theme with sv_ttk
        sv_ttk.set_theme("dark")

        self.create_widgets()

        self.click_thread = threading.Thread(target=self.click_loop)
        self.click_thread.daemon = True
        self.click_thread.start()

    def create_widgets(self):
        tk.Label(self.root, text="Key to activate:").pack(pady=(20, 5))

        self.key_entry = ttk.Entry(self.root, justify="center", font=("Segoe UI", 12), width=5)
        self.key_entry.pack()
        self.key_entry.bind("<KeyRelease>", self.limit_key_length)

        tk.Label(self.root, text="Click Mode:").pack(pady=(15, 5))

        self.hold_radio = ttk.Radiobutton(self.root, text="Hold", variable=self.click_mode, value="hold")
        self.hold_radio.pack()

        self.toggle_radio = ttk.Radiobutton(self.root, text="Toggle", variable=self.click_mode, value="toggle")
        self.toggle_radio.pack()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_listener)
        self.start_button.pack(side="left", padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_listener, state="disabled")
        self.stop_button.pack(side="left", padx=5)

        self.quit_button = ttk.Button(self.root, text="Quit", command=self.quit_program)
        self.quit_button.pack(pady=(0, 10))

    def limit_key_length(self, event=None):
        content = self.key_entry.get()
        if len(content) > 1:
            self.key_entry.delete(1, tk.END)

    def click_loop(self):
        while True:
            if self.running and self.clicking:
                self.mouse_controller.click(mouse.Button.left)
                time.sleep(0.05)
            else:
                time.sleep(0.01)

    def on_press(self, key):
        try:
            if key.char == self.target_key:
                if self.click_mode.get() == "hold":
                    self.clicking = True
                elif self.click_mode.get() == "toggle":
                    self.clicking = not self.clicking
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key.char == self.target_key and self.click_mode.get() == "hold":
                self.clicking = False
        except AttributeError:
            pass

    def start_listener(self):
        key = self.key_entry.get().strip().lower()
        if len(key) == 0:
            return

        self.target_key = key
        self.running = True
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.key_entry.config(state="disabled")
        self.hold_radio.config(state="disabled")
        self.toggle_radio.config(state="disabled")

    def stop_listener(self):
        if self.listener:
            self.listener.stop()
        self.listener = None
        self.running = False
        self.clicking = False

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.key_entry.config(state="normal")
        self.hold_radio.config(state="normal")
        self.toggle_radio.config(state="normal")

    def quit_program(self):
        self.stop_listener()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
