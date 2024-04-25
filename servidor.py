
from tkinter import ttk
import threading
import socket
import tkinter as tk
import datetime


class Servidor():
    def __init__(self, ip=str, porta=int):
        self.ip = ip
        self.porta = porta
        self.maintk()

    def maintk(self):
        icon_path = 'media/id1.ico'
        self.check = False
        self.clients = []

        self.root = tk.Tk()
        self.root.title("Server Pawnee")
        self.root.iconbitmap(icon_path)
        self.root.configure(background='white')
        self.root.geometry("800x600")
        self.root.resizable(True, True)


        self.button_ligar = tk.Button(self.root, text="Turn on server", font=("Helvetica", 14), command=self.turnon)
        self.button_ligar.place(relx=0, rely=0, relwidth=0.5, relheight=0.1)
        self.button_desligar = tk.Button(self.root, text="Turn off server", font=("Helvetica", 14), command=self.quit)
        self.button_desligar.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.1)

        self.variable = tk.StringVar()
        self.label = tk.Label(self.root, font=("Helvetica", 16), bg='#B0C4DE', textvariable=self.variable)
        self.label.place(relx=0, rely=0.1, relwidth=1, relheight=0.1)

        self.frame1 = tk.Frame(self.root, bd=4, bg='#B0C4DE', highlightbackground='#5F9EA0', highlightthickness=2)
        self.frame1.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)

        self.tree = ttk.Treeview(self.frame1, columns=("ID", "Cliente", "Horário"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Horário", text="Horário")
        self.tree.column("ID", width=100)
        self.tree.column("Cliente", width=200)
        self.tree.column("Horário", width=300)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(self.frame1, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.root.mainloop()

    def quit(self):

        if self.check:
            self.root.destroy()
        else:
            self.variable.set('No one server on, so there is not what turn off!\n'
                              'If you wish quit, close the tab...')

    def turnon(self):

        self.check = True
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.ip, self.porta))
            self.server.listen()
            self.variable.set('Server on. Waiting for connections...\n'
                              f'IP: {self.ip} / PORT: {self.porta}')
            threading.Thread(target=self.accept_clients).start()
        except:
            self.variable.set('Did not possible launch the server...\n'
                              f'IP: {self.ip} / PORT: {self.porta}')

    def accept_clients(self):

        while True:
            client, addr = self.server.accept()
            self.clients.append(client)
            self.register_client(addr)

            threading.Thread(target=self.messages_treatment, args=(client,)).start()

    def register_client(self, addr):

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tree.insert("", tk.END, values=(f'                       {len(self.clients)}', f"                        {addr[0]}:{addr[1]}", f'                                         {timestamp}'))

    def messages_treatment(self, client):

        while True:
            try:
                msg = client.recv(2048)
                if not msg:
                    self.delete_client(client)
                    break
                self.broadcast(msg, client)
            except:
                self.delete_client(client)
                break

    def broadcast(self, msg, sender):

        for client in self.clients:
            if client != sender:
                try:
                    client.send(msg)
                except:
                    self.delete_client(client)


    def delete_client(self, client):
        
        if client in self.clients:
            self.clients.remove(client)



Servidor("192.168.2.126", 666)
