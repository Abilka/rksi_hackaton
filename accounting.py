import auth
from tkinter import *


class Window(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        # параметры окна
        self.geometry('400x400+450+150')
        self.title("Turtle")
        self.config(bg='#D5E8D4')
        self.resizable(False, False)

        # навигационная панель (меню)
        menu = Menu(self)
        self.config(menu=menu)

        test1 = Menu(menu, tearoff=0)
        test1.add_command(label='Выйти', font=("Arial Bold", 10), command=self.back_auth)

        test2 = Menu(menu, tearoff=0)
        test2.add_command(label='Обратная связь', font=("Arial Bold", 10), command=self.help)

        menu.add_cascade(label='Действия', font=("Arial Bold", 10), menu=test1)
        menu.add_cascade(label='Помощь', font=("Arial Bold", 10), menu=test2)

        Button(self, text='Загрузить\nотсутствующих', width=15, height=3, font=("Arial Bold", 10)).grid(
            row=1, column=0, padx=140, sticky=NW, pady=(60, 10))
        Button(self, text='Загрузить\nприсутствующих', width=15, height=3, font=("Arial Bold", 10)).grid(
            row=2, column=0, pady=10, padx=140, sticky=NW)

    def back_auth(self):
        auth.AuthApp()
        self.destroy()

    def help(self):
        top = Toplevel(self)
        top.geometry('200x200+450+150')
        top.config(bg='#D5E8D4')
        top.resizable(False, False)
        help_label = Label(top, text='Обратная связь', bg='#D5E8D4', font=("Arial Bold", 13))
        help_label.pack(pady=(20, 10))

        help_label_info = Label(top, text='VK: https://vk.com/zafires', bg='#D5E8D4')
        help_label_info.pack(pady=20)
