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
        test1.add_command(label='Выйти', command=self.back_auth)
        test1.add_command(label='test2')
        test1.add_command(label='test3')

        test2 = Menu(menu, tearoff=0)
        test2.add_command(label='test1')
        test2.add_command(label='test2')
        test2.add_command(label='test3')

        test3 = Menu(menu, tearoff=0)
        test3.add_command(label='test1')
        test3.add_command(label='test2')
        test3.add_command(label='test3')

        menu.add_cascade(label='Действия', menu=test1)
        menu.add_cascade(label='test2', menu=test2)
        menu.add_cascade(label='test3', menu=test3)

        Button(self, text='Загрузить\nотсутствующих', width=15, height=3, font=("Arial Bold", 10)).grid(
            row=1, column=0, padx=140, sticky=NW, pady=(60, 10))
        Button(self, text='Загрузить\nприсутствующих', width=15, height=3, font=("Arial Bold", 10)).grid(
            row=2, column=0, pady=10, padx=140, sticky=NW)

    def back_auth(self):
        auth.AuthApp()
        self.destroy()


