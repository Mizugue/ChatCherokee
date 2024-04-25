import threading
import socket
import tkinter
from tkinter import messagebox
import queue
from tkinter import Text, Entry, Button, Frame

class Chat():
    def __init__(self, ip, port):
        self.telauser()
        self.ip = ip
        self.port = port



    def telauser(self):
        self.BACKGROUND_COLOR = "#363746"
        self.TEXT_COLOR = "white"
        self.FONT = ("verdana", 14)
        self.icon_path = 'media/id.ico'


        self.root = tkinter.Tk()
        self.root.title("Chat Cherokee")
        self.root.iconbitmap(self.icon_path)
        self.root.configure(bg=self.BACKGROUND_COLOR)
        self.root.geometry("600x600")  # More compact size
        self.root.resizable(False, False)  # Non-resizable


        self.image = tkinter.PhotoImage(file="media/idcor.png")
        self.imagelabel = tkinter.Label(self.root, image=self.image, bg=self.BACKGROUND_COLOR)
        self.imagelabel.place(rely=0.10, relx=0.23)


        self.username_entry = tkinter.Entry(self.root, font=self.FONT, bg="#404040", fg=self.TEXT_COLOR, highlightthickness=2, highlightbackground="#66fcff")
        self.username_entry.place(relx=0.31, rely=0.70)


        self.username_label = tkinter.Label(self.root, text="Username", font=self.FONT, fg=self.TEXT_COLOR, bg=self.BACKGROUND_COLOR)
        self.username_label.place(rely=0.65, relx=0.43)


        self.connect_button = tkinter.Button(self.root, text="Connect", font=self.FONT, bg="#2ecc71", fg="white", command=self.entrarchat,activebackground="#4CAF50")
        self.connect_button.place(relx=0.44, rely=0.75)
        self.root.bind('<Return>', lambda event=None: self.connect_button.invoke())


        self.client = None
        self.usernames = []
        self.receive_queue = queue.Queue()

        self.root.mainloop()


    def telachat(self):
        self.root2 = tkinter.Toplevel()
        self.root2.title(f"Chat Cherokee - {self.username}")
        self.root2.iconbitmap(self.icon_path)
        self.root2.geometry("650x650")
        self.root2.configure(background='gray')



        self.frame_main = Frame(self.root2, bg='#ffffff', bd=2, relief=tkinter.SUNKEN)
        self.frame_main.pack(pady=20, padx=20, fill=tkinter.BOTH, expand=True)

        self.image1 = tkinter.PhotoImage(file="media/sa-removebg-preview.png")
        self.imagelabel1 = tkinter.Label(self.root2, image=self.image1, background='white')
        self.imagelabel1.place(rely=0.12, relx=0.80)


        self.label_title = tkinter.Label(self.frame_main, text="Chat Cherokee", bg='#4682B4', fg='white',font=('Verdana', 24))
        self.label_title.pack(fill=tkinter.X)


        self.messages_text = Text(self.frame_main, bg='white', font=('Verdana', 12), wrap=tkinter.WORD)
        self.messages_text.pack(pady=10, padx=10, fill=tkinter.BOTH, expand=True)


        self.entry1 = Entry(self.frame_main, font=('Verdana', 12))
        self.entry1.pack(pady=10, padx=10, fill=tkinter.X)

        self.botao_send = Button(self.frame_main, text='Enviar', bg='#008000', fg='black', font=('Verdana', 12),command=self.send_message)
        self.botao_send.place(relx=0.9, rely=0.95, relwidth=0.1, relheight=0.05)
        self.root2.bind('<Return>', lambda event=None: self.botao_send.invoke())

    def entrarchat(self):
        self.username = self.username_entry.get()
        self.variable = f' Connected like {self.username}'

        if not self.username:
            messagebox.showwarning("Warning!", "Please, put a user.")
            return

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.ip, self.port))
        except:
            messagebox.showinfo("Warning!", "Did not possible stabilish a connection with the server.")
            self.entrada1.delete(0, tkinter.END)
            return

        if self.username in self.usernames:
            messagebox.showwarning("Warning!", "This user already exist in your machine.")
            return

        self.usernames.append(self.username)

        messagebox.showinfo("Success", 'You are connected')

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
        except:
            messagebox.showerror('Connection error', 'Did not possible to maintain connected in the server .')
            return


        self.entry1.delete(0, tkinter.END)
        self.msg = f'{self.username}(you)- {message}'
        self.update_messages(self.msg)


    def receive(self):

        while True:
            try:
                self.msg = self.client.recv(2048).decode('utf-8')
                self.update_messages(self.msg)
            except:
                messagebox.showerror('Connection error', 'Did not possible to maintain connected in the server')
                self.client.close()
                return

    def update_messages(self, msg):

        self.messages_text.insert(tkinter.END, msg + "\n")
        self.messages_text.insert(tkinter.END, "\n")
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
    Chat('192.168.2.126', 666)







