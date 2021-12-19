from tkinter.ttk import Treeview

import pandas

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

        test2 = Menu(menu, tearoff=0)
        test2.add_command(label='Выбрать корпус', command=self.select_corpus)
        test2.add_command(label='Выгрузка текущих данных', command=self.uploading_current_data)
        test2.add_command(label='Выгрузка данных', command=self.uploading_data)

        test3 = Menu(menu, tearoff=0)
        test3.add_command(label='Обратная связь', command=self.help)

        menu.add_cascade(label='Действия', menu=test1)
        menu.add_cascade(label='Выгрузка', menu=test2)
        menu.add_cascade(label='Помощь', menu=test3)

        self.schedul = scheduler.Schedule().changed_needed()

        self.heads = ['Предмет', 'Группа', 'Аудитория',
                      'Корпус', 'Пара', 'Начало', 'Конец',
                      'Преподаватели', 'Дата', 'Время', 'Вес']
        data = list(map(list, self.schedul.values))

        self.create_table(self.heads, data)
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
        top.geometry('200x200+450+150')
        top.config(bg='#D5E8D4')
        label_select_corpus = Label(top, text='Выберите корпус', bg='#D5E8D4')
        label_select_corpus.pack(pady=(20, 10))
        self.choise = Entry(top)
        self.choise.pack()
        btn_top_level = Button(top, text='Далее', command=self.set_corpus)
        btn_top_level.pack(pady=20)
        top.transient(self)
        top.grab_set()
        top.focus_get()
        top.wait_window()

    def set_corpus(self):
        self.clear_treeview()
        data = self.schedul[self.schedul['corpus'] == self.choise.get()]
        data = list(map(list, data.values))
        self.fill_data(data)

    def fill_data(self, data):
        # перебираем данные из списка header и заполняем в таблицу
        for header in self.heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center', minwidth=150, width=140)

        # перебираем данные из списка data и заполняем в таблицу
        for row in data:
            self.table.insert('', END, values=row)

        data = list(map(lambda x: x[:11], data))
        self.visible_data = pandas.DataFrame(columns=self.heads, data=data)

    def create_table(self, heads, data):
        # фрейм
        frame = Frame(self, )
        frame.pack()

        # высота изменяеться в зависимости количества данных
        self.table = ttk.Treeview(self, show='headings', height=len(data))
        self.table['columns'] = heads

        self.fill_data(data)

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

    def help(self):
        top = Toplevel(self)
        top.geometry('200x200+450+150')
        top.config(bg='#D5E8D4')

        label_select_corpus = Label(top, text='Обратная связь', bg='#D5E8D4')
        label_select_corpus.pack(pady=(20, 10))

        label_select_corpus = Label(top, text='VK: https://vk.com/zafires\nVK: https://vk.com/al_shashkin',
                                    bg='#D5E8D4')
        label_select_corpus.pack(pady=20)

        self.choise.pack()
        top.transient(self)
        top.grab_set()
        top.focus_get()
        top.wait_window()

    def uploading_current_data(self):
        top = Toplevel(self)
        top.geometry('170x240+450+150')
        top.resizable(False, False)
        top.config(bg='#D5E8D4')

        label_select_corpus = Label(top, text='Выберите формат', bg='#D5E8D4')
        label_select_corpus.grid(
            pady=(20, 10), padx=(30, 10)
        )

        btn_csv = Button(top, text='CSV')
        btn_csv.grid(
            row=3, column=0, padx=(30, 10)
        )

        btn_html = Button(top, text='HTML')
        btn_html.grid(
            row=4, column=0, padx=(30, 10), pady=(10, 0)
        )

        btn_excel = Button(top, text='EXCEL')
        btn_excel.grid(
            row=5, column=0, padx=(30, 10), pady=(10, 0)
        )

        btn_json = Button(top, text='JSON')
        btn_json.grid(
            row=6, column=0, padx=(30, 10), pady=(10, 0)
        )

        btn_xml = Button(top, text='XML')
        btn_xml.grid(
            row=7, column=0, padx=(30, 10), pady=(10, 0)
        )

        self.choise.pack()
        top.transient(self)
        top.grab_set()
        top.focus_get()
        top.wait_window()

    def uploading_data(self):
        top = Toplevel(self)
        top.geometry('170x240+450+150')
        top.resizable(False, False)
        top.config(bg='#D5E8D4')

        label_select_corpus = Label(top, text='Выберите формат', bg='#D5E8D4')
        label_select_corpus.grid(
            pady=(20, 10), padx=(30, 10)
        )

        btn_csv = Button(top, text='CSV')
        btn_csv.grid(
            row=3, column=0, padx=(30, 10)
        )

        btn_html = Button(top, text='HTML')
        btn_html.grid(
            row=4, column=0, padx=(30, 10), pady=(10, 0)
        )

        btn_excel = Button(top, text='EXCEL')
        btn_excel.grid(
            row=5, column=0, padx=(30, 10), pady=(10, 0)
        )

        btn_json = Button(top, text='JSON')
        btn_json.grid(
            row=6, column=0, padx=(30, 10), pady=(10, 0)
        )

        btn_xml = Button(top, text='XML')
        btn_xml.grid(
            row=7, column=0, padx=(30, 10), pady=(10, 0)
        )

        self.choise.pack()
        top.transient(self)
        top.grab_set()
        top.focus_get()
        top.wait_window()
