"""Simple Tkinter GUI for sending commands to the Minecraft bot."""

import asyncio
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from gpt_server import send_instruction


class BotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minecraft GPT Bot")

        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill=tk.X)

        self.entry = tk.Entry(frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.focus()

        send_btn = tk.Button(frame, text="Send", command=self.on_send)
        send_btn.pack(side=tk.RIGHT, padx=(5, 0))

        self.output = ScrolledText(self.root, width=80, height=20)
        self.output.pack(padx=10, pady=(0, 10))

    def log(self, text: str) -> None:
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def on_send(self) -> None:
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, tk.END)
        self.log(f"> {text}")
        try:
            asyncio.run(send_instruction(text))
        except Exception as exc:
            self.log(f"Error: {exc}")

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    BotGUI().run()
