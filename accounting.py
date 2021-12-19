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
        test2.add_command(label='Обратная связь', command=self.help)
        test2.add_command(label='test2')
        test2.add_command(label='test3')

        menu.add_cascade(label='Действия', menu=test1)
        menu.add_cascade(label='Помощь', menu=test2)

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

        label_select_corpus = Label(top, text='Обратная связь', bg='#D5E8D4')
        label_select_corpus.pack(pady=(20, 10))

        label_select_corpus = Label(top, text='VK: https://vk.com/zafires\nVK: https://vk.com/al_shashkin',
                                    bg='#D5E8D4')
        label_select_corpus.pack(pady=20)
