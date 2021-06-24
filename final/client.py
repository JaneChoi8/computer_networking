import socket
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


HOST = "127.0.0.1"
PORT = 65234

class Books_app():
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)

client.connect(server_address)

app = Books_app()

try:
    app.mainloop()
except:
    print("Error: server is not responding")
    client.close()

finally:
    client.close()

