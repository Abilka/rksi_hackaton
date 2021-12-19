import tkinter
import setting
import accounting
import admin
import tg
import typing

from user import User
from tkinter import *
from tkinter import messagebox

ROLE: typing.Dict = {
    'admin': admin.Window,
    'buh': accounting.Window,
    'tb': tg.Window
}


class AuthApp(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # параметры окна
        self.geometry('400x400+450+150')
        self.title("Turtle")
        self.config(bg='#D5E8D4')
        self.resizable(False, False)

        # навигационная панель (меню)
        menu = Menu(self)
        self.config(menu=menu)

        test1 = Menu(menu, tearoff=0)
        test1.add_command(label='Выйти', command=exit)

        test2 = Menu(menu, tearoff=0)
        test2.add_command(label='Обратная связь', font=("Arial Bold", 10), command=self.help)

        menu.add_cascade(label='Действия', menu=test1, font=("Arial Bold", 10))
        menu.add_cascade(label='Помощь', menu=test2, font=("Arial Bold", 10))

        Label(self, text='Авторизация', font=('Arial Bold', 20), justify='center', bg='#D5E8D4').grid(
            row=0, column=5, pady=(40, 10))

        self.login = Entry(self, width=20, font=("Arial Bold", 10))
        self.login.grid(
            row=1, column=5, pady=(10, 10), padx=140
        )

        self.password = Entry(self, width=20, show='*', font=("Arial Bold", 10))
        self.password.grid(
            row=2, column=5, padx=140
        )

        Button(self, text='Далее', width=10, height=1, font=("Arial Bold", 10),
               command=self.new_window).grid(
            row=3, column=5, pady=15,
        )

    def new_window(self):
        user = User(self.login.get(), self.password.get())
        if user.is_login is True:

            self.destroy()
            ROLE[user.role]().mainloop()

        else:
            messagebox.showerror('Ошибка', 'Не правильный логин или пароль')

    def help(self):
        top = Toplevel(self)
        top.geometry('200x200+450+150')
        top.config(bg='#D5E8D4')
        top.resizable(False, False)
        help_label = Label(top, text='Обратная связь', bg='#D5E8D4', font=("Arial Bold", 13))
        help_label.pack(pady=(20, 10))

        help_label_info = Label(top, text='VK: https://vk.com/zafires',
                                bg='#D5E8D4', font=("Arial Bold", 10))
        help_label_info.pack(pady=20)

    def exit(self):
        self.quit()
