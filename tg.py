from tkinter import *
from tkinter import ttk

import pandas

import auth
import scheduler


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
        test2.add_command(label='Выгрузить текущие данные')
        test2.add_command(label='Выгрузить данные')

        test3 = Menu(menu, tearoff=0)
        test3.add_command(label='test1')
        test3.add_command(label='test2')
        test3.add_command(label='test3')

        menu.add_cascade(label='Действия', menu=test1)
        menu.add_cascade(label='Выгрузка', menu=test2)
        menu.add_cascade(label='Помощь', menu=test3)

        self.schedul = scheduler.Schedule().changed_needed()

        self.heads = ['Предмет', 'Группа', 'Аудитория',
                      'Корпус', 'Пара', 'Начало', 'Конец',
                      'Преподаватели', 'Дата', 'Время', 'Вес']
        data = list(map(list, self.schedul.values))

        self.create_table(self.heads, data)

        self.table.bind('<Button-1>', self.header_sort)

    def header_sort(self, event):
        region = self.table.identify("region", event.x, event.y)
        if region == "heading":
            self.treeview_sort_column(self.table.heading(self.table.identify_column(event.x))['text'], True)

    def back_auth(self):
        auth.AuthApp()
        self.destroy()

    def select_corpus(self):
        top = Toplevel(self)
        self.choise = Entry(top)
        self.choise.pack()
        btn_top_level = Button(top, text='Далее', command=self.set_corpus)
        btn_top_level.pack()
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

    def treeview_sort_column(self, col, reverse: bool):
        """
        to sort the table by column when clicking in column
        """
        try:
            data_list = [
                (int(self.table.set(k, col)), k) for k in self.table.get_children("")
            ]
        except Exception:
            data_list = [(self.table.set(k, col), k) for k in self.table.get_children("")]

        data_list.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(data_list):
            self.table.move(k, "", index)

        # reverse sort next time
        self.table.heading(
            column=col,
            text=col,
            command=lambda _col=col: self.treeview_sort_column(_col, not reverse
                                                               ),
        )

    def clear_treeview(self):
        for row in self.table.get_children():
            self.table.delete(row)
