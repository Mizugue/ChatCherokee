import tkinter as tk
from tkinter import Text, Entry, Button, Frame

def enviar_mensagem():
    mensagem = entry1.get()
    if mensagem:
        messages_text.insert(tk.END, f"You: {mensagem}\n")
        entry1.delete(0, tk.END)

root2 = tk.Tk()
root2.title("Chat Cherokee")
root2.geometry("600x600")

# Cor de fundo e estilo da janela principal
root2.configure(background='#f0f0f0')

# Frame principal
frame_main = Frame(root2, bg='#ffffff', bd=2, relief=tk.SUNKEN)
frame_main.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Título do chat
label_title = tk.Label(frame_main, text="Chat Cherokee", bg='#4b0082', fg='white', font=('Verdana', 24), pady=10)
label_title.pack(fill=tk.X)

# Área de exibição das mensagens
messages_text = Text(frame_main, bg='white', font=('Verdana', 12), wrap=tk.WORD)
messages_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Campo de entrada de mensagem
entry1 = Entry(frame_main, font=('Verdana', 12))
entry1.pack(pady=10, padx=10, fill=tk.X)

# Botão para enviar mensagem
botao_enviar = Button(frame_main, text='Enviar', bg='#008000', fg='white', font=('Verdana', 12), command=enviar_mensagem)
botao_enviar.pack(pady=10, padx=10, fill=tk.X)

# Função para pressionar Enter para enviar mensagem
root2.bind('<Return>', lambda event=None: botao_enviar.invoke())

root2.mainloop()
