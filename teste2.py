import threading
import socket
import tkinter
from tkinter import messagebox
import queue
from tkinter import Text, Entry, Button, Frame

class Chat():
    def __init__(self):
        self.telauser()
        self.root.mainloop()


    def telauser(self):
        self.root = tkinter.Tk()
        self.root.title('Titulo')
        self.root.configure(background='blue')
        self.root.geometry("1000x1000")
        self.root.resizable(False, False)
        self.root.maxsize(width=500, height=500)
        self.entrada1 = tkinter.Entry(self.root, font=('arial', 15), )
        self.entrada1.place(relx=0.30, rely=0.4, relwidth=0.4, relheight=0.06)
        self.label1 = tkinter.Label(self.root, text="Digite o seu usuário", bd=10, bg='gray', font=('verdana', 10))
        self.label1.place(relx=0.30, rely=0.35, relwidth=0.4, relheight=0.06)
        self.botaoacesso = tkinter.Button(self.root, text='Acessar chat', command=self.entrarchat, activebackground='green',activeforeground='white')
        self.botaoacesso.place(relx=0.4, rely=0.48, relwidth=0.2, relheight=0.06)


        self.client = None
        self.usernames = []
        self.receive_queue = queue.Queue()
        self.root.mainloop()



    def telachat(self):
        self.root2 = tkinter.Toplevel()
        self.root2.title("Chat Cherokee")
        self.root2.geometry("600x600")
        self.root2.configure(background='gray')
        self.frame_main = Frame(self.root2, bg='#ffffff', bd=2, relief=tkinter.SUNKEN)
        self.frame_main.pack(pady=20, padx=20, fill=tkinter.BOTH, expand=True)


        self.label_title = tkinter.Label(self.frame_main, text="Chat Cherokee", bg='#4b0082', fg='white', font=('Verdana', 24),
                               pady=10)
        self.label_title.pack(fill=tkinter.X)


        self.messages_text = Text(self.frame_main, bg='white', font=('Verdana', 12), wrap=tkinter.WORD)
        self.messages_text.pack(pady=10, padx=10, fill=tkinter.BOTH, expand=True)


        self.entry1 = Entry(self.frame_main, font=('Verdana', 12))
        self.entry1.pack(pady=10, padx=10, fill=tkinter.X)

        self.botao_send = Button(self.frame_main, text='Enviar', bg='#008000', fg='black', font=('Verdana', 12),command=self.send_message)
        self.botao_send.place(relx=0.9, rely=0.95, relwidth=0.1, relheight=0.05)
        self.root2.bind('<Return>', lambda event=None: self.botao_send.invoke())



    def entrarchat(self):
        self.username = self.entrada1.get()

        if not self.username:
            messagebox.showwarning("Aviso!", "Por favor, insira um usuário.")
            return

        if self.username in self.usernames:
            messagebox.showwarning("Aviso!", "Este usuario ja existe na sua máquina.")
            return

        self.usernames.append(self.username)



        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(('192.168.2.126', 666))
        except Exception as e:
            messagebox.showinfo("Aviso!", "Não foi possível estabilizar uma conexão com o servidor.")
            print(e)
            self.entrada1.delete(0, tkinter.END)
            return

        messagebox.showinfo("Sucesso", 'Você entrou no servidor')
        self.telachat()

        threading.Thread(target=self.receive).start()
        threading.Thread(target=self.process_send_queue).start()

    def send_message(self):
        if not self.client:
            return

        message = self.entry1.get().strip()
        if not message:
            return

        try:
            self.client.send(f'{self.username}- {message}'.encode('utf-8'))
        except Exception as e:
            messagebox.showerror('Erro de conexão', 'Não foi possível manter a conexão com o servidor.')
            print(e)

        self.entry1.delete(0, tkinter.END)
        self.msg = f'{self.username}(you)- {message}'
        self.update_messages(self.msg)


    def receive(self):
        while True:
            try:
                self.msg = self.client.recv(2048).decode('utf-8')
                self.update_messages(self.msg)
            except Exception as e:
                messagebox.showerror('Connection error', 'Didnt possible to maintain connected in the server')
                print(e)
                self.client.close()
                return

    def update_messages(self, msg):
        self.messages_text.insert(tkinter.END, msg + "\n")
        self.messages_text.see(tkinter.END)

    def process_send_queue(self):
        while True:
            try:
                if not self.receive_queue.empty():
                    message = self.receive_queue.get()
                    self.update_messages(message)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    Chat()







