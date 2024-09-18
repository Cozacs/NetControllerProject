import tkinter as tk
import subprocess
import os
import sys

process = None
email_to = "" 

def get_resource_path(relative_path):
    """Retorna o caminho absoluto, lidando com o modo de execução do PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def on_button_click():
    global process, email_to
    email_to = email_entry.get() 
    if not email_to:
        label.config(text="Por favor, insira um e-mail válido!")
        return

    label.config(text="Monitoramento Ativo!")
    button.config(state="disabled", text="Monitorando...")

    try:
        teste_ping_path = get_resource_path("testePing.py")
        process = subprocess.Popen(
            ["python", teste_ping_path, email_to], 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        print("Script testePing.py iniciado com sucesso.")
    except Exception as e:
        label.config(text=f"Erro ao iniciar o monitoramento: {e}")
        print(f"Erro: {e}")

def on_closing():
    global process
    if process:
        process.terminate()
        process.wait(timeout=5)
        if process.poll() is None:
            process.kill()
    root.destroy()  

root = tk.Tk()
root.title("Net Controller")
root.geometry("300x200")
root.config(bg='#2E2E2E')

root.protocol("WM_DELETE_WINDOW", on_closing)

label = tk.Label(root, text="Insira seu e-mail para monitoramento:", fg="white", bg="#2E2E2E")
label.pack(pady=10)

email_entry = tk.Entry(root, width=30)
email_entry.pack(pady=5)

button = tk.Button(root, text="Preparado para monitorar", command=on_button_click)
button.pack(pady=10)

root.mainloop()
