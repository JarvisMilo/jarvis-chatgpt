from __future__ import annotations
import tkinter as tk
from ..runtime.state import JarvisState

class AmbientHUD:
    def __init__(self,title="JARVIS"):
        self.root=tk.Tk(); self.root.title(title); self.root.geometry("720x420"); self.root.configure(bg="#05070a")
        self.state=tk.StringVar(value=JarvisState.SLEEPING.value); self.message=tk.StringVar(value="JARVIS")
        tk.Label(self.root,textvariable=self.state,bg="#05070a",fg="#bfe8ff",font=("Segoe UI",18)).pack(pady=60)
        tk.Label(self.root,textvariable=self.message,bg="#05070a",fg="#eaf6ff",font=("Segoe UI",28)).pack()
    def set_state(self,state:JarvisState): self.state.set(state.value)
    def set_message(self,message:str): self.message.set(message)
    def run(self): self.root.mainloop()
