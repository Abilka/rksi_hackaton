import tkinter
import setting
import accounting
import admin
import tg
import typing
import webbrowser
import datetime

from PIL import Image, ImageTk
from user import User
from tkinter import *
from tkinter import messagebox
from tkinter import Tk


ROLE: typing.Dict = {
    'admin': admin.Window,
    'buh': accounting.Window,
    'tb': tg.Window
}


class AuthApp(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # параметры окна
        self.geometry('425x425+450+150')
        self.title("Turtle")
        self.config(bg='#83d798')
        self.resizable(False, False)

        '''filename = PhotoImage(file=r"C:\turtle.png")
        background_label = Label(self, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)'''

        # навигационная панель (меню)
        menu = Menu(self)
        self.config(menu=menu)

        test1 = Menu(menu, tearoff=0)
        test1.add_command(label='Выйти', command=exit)

        test2 = Menu(menu, tearoff=0)
        test2.add_command(label='Обратная связь', font=("Arial Bold", 10), command=self.help)

        menu.add_cascade(label='Действия', menu=test1, font=("Arial Bold", 10))
        menu.add_cascade(label='Помощь', menu=test2, font=("Arial Bold", 10))

        Label(self, text='Авторизация', font=('Arial Bold', 20), justify='center', bg='#83d798').grid(
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

        self.bind('<Return>', self.new_window)


    def new_window(self):
        user = User(self.login.get(), self.password.get())
        if user.is_login is True:

            self.destroy()
            ROLE[user.role]().mainloop()

        else:
            messagebox.showerror('Ошибка', 'Неправильный логин или пароль')


    def help(self):
        top = Toplevel(self)
        top.geometry('250x250+500+200')
        top.config(bg='#83d798')

        def callback(event): #создаем функцию для гиперссылок
            webbrowser.open_new(event.widget.cget("text"))

        label_help1 = Label(top, text='Обратная связь', bg='#83d798', font=("Arial Bold", 14))
        label_help1.pack(pady=(20, 10))

        label_help2 = Label(top, text='Егор Лядский:', bg='#83d798', font=("Arial Bold", 11))
        label_help2.pack()

        label_help_url2 = Label(top, text='https://vk.com/zafires',
                                    bg='#83d798', font=("Arial Bold", 10), fg='blue', cursor='hand2')
        label_help_url2.pack(pady=5)
        label_help_url2.bind("<Button-1>", callback)

        label_help3 = Label(top, text='Алексей Шашкин:', bg='#83d798', font=("Arial Bold", 11))
        label_help3.pack()

        label_help_url3 = Label(top, text='https://vk.com/al_shashkin',
                                bg='#83d798', font=("Arial Bold", 10), fg='blue', cursor='hand2')
        label_help_url3.pack(pady=5)
        label_help_url3.bind("<Button-1>", callback)

        label_help4 = Label(top, text='Максим Шимон:', bg='#83d798', font=("Arial Bold", 11))
        label_help4.pack()

        label_help_url4 = Label(top, text='https://vk.com/cisctem',
                                bg='#83d798', font=("Arial Bold", 10), fg='blue', cursor='hand2')
        label_help_url4.pack(pady=5)
        label_help_url4.bind("<Button-1>", callback)

        top.transient(self)
        top.grab_set()
        top.focus_get()
        top.wait_window()

    def exit(self):
        self.quit()
