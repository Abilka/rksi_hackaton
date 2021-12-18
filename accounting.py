from tkinter import *
from user import User



class MainApp(Tk):
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
        test1.add_command(label='test1')
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

        menu.add_cascade(label='test1', menu=test1)
        menu.add_cascade(label='test2', menu=test2)
        menu.add_cascade(label='test3', menu=test3)

        Label(self, text='Авторизация', font=('Arial Bold', 20), justify='center', bg='#D5E8D4').grid(
            row=0, column=5, pady=(40, 10))

        self.login = Entry(self, width=20)
        self.login.grid(
            row=1, column=5, pady=(10, 10), padx=140
        )

        self.password = Entry(self, width=20, show='*')
        self.password.grid(
            row=2, column=5, padx=140
        )

        Button(self, text='Далее', width=10, height=1, font=("Arial Bold", 10),
               command=self.new_window).grid(
            row=3, column=5, pady=15,
        )

    def new_window(self):

        if User(self.login.get(), self.password.get()).is_login is True:
            User(self.login.get(), self.password.get()).get_user()
            Window().mainloop()


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
        test1.add_command(label='test1')
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

        menu.add_cascade(label='test1', menu=test1)
        menu.add_cascade(label='test2', menu=test2)
        menu.add_cascade(label='test3', menu=test3)

        Button(self, text='Загрузить\nотсутствующих', width=15, height=3, font=("Arial Bold", 10)).grid(
            row=1, column=0, padx=140, sticky=NW, pady=(60, 10))
        Button(self, text='Загрузить\nприсутствующих', width=15, height=3, font=("Arial Bold", 10)).grid(
            row=2, column=0, pady=10, padx=140, sticky=NW)


if __name__ == '__main__':
    MainApp().mainloop()
