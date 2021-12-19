from tkinter.ttk import Treeview

import auth
import scheduler

from tkinter import *
from tkinter import ttk


class Window(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        # параметры окна
        self.geometry('1000x400+150+150')
        self.title("Turtle")
        self.config(bg='#D5E8D4')



        # навигационная панель (меню)
        menu = Menu(self)
        self.config(menu=menu)
        test1 = Menu(menu, tearoff=0)
        test1.add_command(label='Выйти', command=self.back_auth)
        test1.add_command(label='test2')
        test1.add_command(label='test3')

        test2 = Menu(menu, tearoff=0)
        test2.add_command(label='Выбрать корпус', command=self.select_corpus)
        test2.add_command(label='test2')
        test2.add_command(label='test3')

        test3 = Menu(menu, tearoff=0)
        test3.add_command(label='test1')
        test3.add_command(label='test2')
        test3.add_command(label='test3')

        menu.add_cascade(label='Действия', menu=test1)
        menu.add_cascade(label='Выгрузка', menu=test2)
        menu.add_cascade(label='Помощь', menu=test3)

        schedul = scheduler.Schedule().changed_needed()

        heads = ['Предмет', 'Группа', 'Аудитория',
                  'Корпус', 'Пара', 'Начало', 'Конец',
                  'Преподаватели', 'Дата', 'Время', 'Вес']
        data = list(map(list, schedul.values))

        self.create_table(heads, data)
        # заполнение таблицы

        # schedul = scheduler.Schedule().changed_needed()
        #
        # heads = ['Предмет', 'Группа', 'Аудитория',
        #          'Корпус', 'Пара', 'Начало', 'Конец',
        #          'Преподаватели', 'Дата', 'Время', 'Вес']
        # data = list(map(list, schedul.values))
        #
        # # высота изменяеться в зависимости количества данных
        # self.table = ttk.Treeview(frame, show='headings', height=len(data))
        # self.table['columns'] = heads
        #
        # # перебираем данные из списка header и заполняем в таблицу
        # for header in heads:
        #     self.table.heading(header, text=header, anchor='center')
        #     self.table.column(header, anchor='center', minwidth=150, width=140)
        #
        # # перебираем данные из списка data и заполняем в таблицу
        # for row in data:
        #     self.table.insert('', END, values=row)





    def back_auth(self):
        auth.AuthApp()
        self.destroy()

    def select_corpus(self):
        top = Toplevel(self)
        choise = Entry(top)
        choise.pack()
        btn_top_level = Button(top, text='Далее', command=self.set_corputs)
        btn_top_level.pack()
        top.transient(self)
        top.grab_set()
        top.focus_get()
        top.wait_window()

    def set_corputs(self):
        self.clear_treeview()


    def create_table(self, heads, data):
        # фрейм
        frame = Frame(self, )
        frame.pack()

        schedul = scheduler.Schedule().changed_needed()

        heads = ['Предмет', 'Группа', 'Аудитория',
                 'Корпус', 'Пара', 'Начало', 'Конец',
                 'Преподаватели', 'Дата', 'Время', 'Вес']
        data = list(map(list, schedul.values))

        # высота изменяеться в зависимости количества данных
        self.table = ttk.Treeview(self, show='headings', height=len(data))
        self.table['columns'] = heads

        # перебираем данные из списка header и заполняем в таблицу
        for header in heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center', minwidth=150, width=140)

        # перебираем данные из списка data и заполняем в таблицу
        for row in data:
            self.table.insert('', END, values=row)

        # скроллинг по оси Y
        scroll_panel_y = ttk.Scrollbar(self, command=self.table.yview)
        self.table.configure(yscrollcommand=scroll_panel_y.set)
        scroll_panel_y.pack(side=RIGHT, fill=Y)

        # скроллинг по оси X
        scroll_panel_x = ttk.Scrollbar(self, command=self.table.xview, orient=HORIZONTAL)
        self.table.configure(xscrollcommand=scroll_panel_x.set)
        scroll_panel_x.pack(side=BOTTOM, fill=X)

        self.table.pack(expand=YES, fill=BOTH)


    def clear_treeview(self):
        for row in self.table.get_children():
           self.table.delete(row)
