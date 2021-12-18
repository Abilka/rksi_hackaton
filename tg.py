from tkinter import *
from tkinter import ttk


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
        test1.add_command(label='Загрузить')
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
        menu.add_cascade(label='Помощь', menu=test3)

        Label(self, text='Авторизация', font=('Arial Bold', 20), justify='center', bg='#D5E8D4').grid(
            row=0, column=5, pady=(40, 10))

        entry_login = Entry(self, width=20).grid(
            row=1, column=5, pady=(10, 10), padx=140
        )

        entry_password = Entry(self, width=20, show='*').grid(
            row=2, column=5, padx=140
        )

        Button(self, text='Далее', width=10, height=1, font=("Arial Bold", 10),
               command=self.new_window).grid(
            row=3, column=5, pady=15,
        )

    # открытие второго окна
    def new_window(self):
        Window().mainloop()


class Window(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        # параметры окна
        self.geometry('1000x400+150+150')
        self.title("Turtle")
        self.config(bg='#D5E8D4')

        # фрейм
        frame = Frame(self, )
        frame.pack()

        # навигационная панель (меню)
        menu = Menu(self)
        self.config(menu=menu)
        test1 = Menu(menu, tearoff=0)
        test1.add_command(label='Загрузить')
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
        menu.add_cascade(label='Помощь', menu=test3)

        # заполнение таблицы

        heads = ['doctrine', 'teacher', 'auditoria', 'corpus',
                 'number', 'start', 'end', 'warn', 'group', 'day',
                 'hour', 'weight', 'changled']

        list = [
            ('test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
            ('test11233', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
             'test12', 'test13'),
        ]

        # высота изменяеться в зависимости количества данных
        table = ttk.Treeview(frame, show='headings', height=len(list))
        table['columns'] = heads

        # перебираем данные из списка header и заполняем в таблицу
        for header in heads:
            table.heading(header, text=header, anchor='center')
            table.column(header, anchor='center', minwidth=150, width=140)

        # перебираем данные из списка list и заполняем в таблицу
        for row in list:
            table.insert('', END, values=row)

        # скроллинг по оси Y
        scroll_panel_y = ttk.Scrollbar(frame, command=table.yview)
        table.configure(yscrollcommand=scroll_panel_y.set)
        scroll_panel_y.pack(side=RIGHT, fill=Y)

        # скроллинг по оси X
        scroll_panel_x = ttk.Scrollbar(frame, command=table.xview, orient=HORIZONTAL)
        table.configure(xscrollcommand=scroll_panel_x.set)
        scroll_panel_x.pack(side=BOTTOM, fill=X)

        table.pack(expand=YES, fill=BOTH)


if __name__ == '__main__':
    MainApp().mainloop()