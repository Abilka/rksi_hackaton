# Импорт модулей
import pandas
import webbrowser

from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter.colorchooser import askcolor
from tkinter.ttk import *
from tkinter import Tk, Frame, Button, BOTH, SUNKEN
# Импорт файлов
import auth
import recorder
import scheduler


class Window(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        # параметры окна
        self.geometry('1000x400+150+150')
        self.title("Turtle")
        self.config(bg='#83d798')

        # навигационная панель (меню)
        menu = Menu(self)
        self.config(menu=menu)

        test1 = Menu(menu, tearoff=0)
        test1.add_command(label='Выбрать корпус', command=self.select_corpus)
        test1.add_command(label='Выйти', command=self.back_auth)

        test2 = Menu(menu, tearoff=0)
        test2.add_command(label='Выгрузка текущих данных', command=self.uploading_current_data)
        test2.add_command(label='Выгрузка данных', command=self.uploading_data)

        test3 = Menu(menu, tearoff=0)
        test3.add_command(label='Обратная связь', command=self.help)

        test4 = Menu(menu, tearoff=0)
        test4.add_command(label='Выбрать цвет', command=self.colors)

        menu.add_cascade(label='Действия', menu=test1)
        menu.add_cascade(label='Выгрузка', menu=test2)
        menu.add_cascade(label='Помощь', menu=test3)
        menu.add_cascade(label='Цвета', menu=test4)

        self.schedul = scheduler.Schedule().changed_needed()

        self.heads = ['Предмет', 'Группа', 'Аудитория',
                      'Корпус', 'Пара', 'Начало', 'Конец',
                      'Преподаватели', 'Дата', 'Время', 'Вес']
        data = list(map(list, self.schedul.values))

        self.create_table(self.heads, data)

        self.table.bind('<Button-1>', self.header_sort)
        self.table.bind('<Double-Button-1>', self.color_row)

    def header_sort(self, event):
        region = self.table.identify("region", event.x, event.y)
        if region == "heading":
            self.treeview_sort_column(self.table.heading(self.table.identify_column(event.x))['text'], True)

    def back_auth(self):
        auth.AuthApp()
        self.destroy()

    def select_corpus(self):
        top = Toplevel(self)
        top.geometry('250x250+450+200')
        top.config(bg='#83d798')

        self.corpus_label = Label(top, text='Выберите корпус', font=("Arial Bold", 12), bg='#83d798')
        self.corpus_label.pack(pady=20)
        self.choise = Entry(top)
        self.choise.pack(pady=(0, 10))

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

    def color_row(self, event):
        tree = event.widget
        item = tree.identify_row(event.y)
        tree.tk.call(tree, "tag", "remove", "highlight")
        tree.tk.call(tree, "tag", "add", "highlight", item)


    def fill_data(self, data):
        tree = ttk.Treeview(self, style='W.TButton')
        vsb = ttk.Scrollbar(self, command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)

        tree.tag_configure('highlight', background='green')
        tree.bind("<Double-Button-1>", self.color_row)
        # перебираем данные из списка header и заполняем в таблицу
        for header in self.heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center', minwidth=150, width=140)

        # перебираем данные из списка data и заполняем в таблицу
        for row in data:
            self.table.insert('', END, values=row)
            tree.tag_bind(row, '<Double-Button-1>', self.color_row)

        for row in data: #range(100)
            tree.insert('', "end", values=row) #f"строка #{i+1}"
            tree.tag_bind(row, '<Double-Button-1>', self.color_row)

        data = list(map(lambda x: x[:11], data))
        self.visible_data = pandas.DataFrame(columns=self.heads, data=data)

    def uploading_current_data(self):
        top = Toplevel(self)
        top.geometry('170x240+450+150')
        top.resizable(False, False)
        top.config(bg='#83d798')

        uploading_current_data_label = Label(top, text='Выберите формат', bg='#83d798', font=("Arial Bold", 10))
        uploading_current_data_label.grid(
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

        top.transient(self)
        top.grab_set()
        top.focus_get()
        top.wait_window()

    def help(self):
        top = Toplevel(self)
        top.geometry('250x250+500+200')
        top.config(bg='#83d798')

        def callback(event):  # создаем функцию для гиперссылок
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

    def onChoose(self):
        (rgb, hx) = tkColorChooser.askcolor()
        self.frame.config(bg=hx)

    def colors(self):
        top = Toplevel(self)
        top.geometry('350x300+300+300')
        top.config(bg='white')

        self.pack(fill=BOTH, expand=True)

        self.btn = Button(top, text="Выберите цвет", command=self.onChoose)
        self.btn.place(x=20, y=30)

        self.frame = Frame(top, border=1, relief=SUNKEN, width=100, height=100)
        self.frame.place(x=160, y=30)

        top.transient(self)
        top.grab_set()
        top.focus_get()
        top.wait_window()

    def uploading_data(self):
        top = Toplevel(self)
        top.geometry('170x240+450+150')
        top.resizable(False, False)
        top.config(bg='#83d798')

        uploading_data_label = Label(top, text='Выберите формат', bg='#83d798', font=("Arial Bold", 10))
        uploading_data_label.grid(
            pady=(20, 10), padx=(30, 10)
        )

        btn_csv = Button(top, text='CSV')
        btn_csv.grid(
            row=3, column=0, padx=(30, 10)
        )

        btn_html = Button(top, text='HTML', command=self.s_html)
        btn_html.grid(
            row=4, column=0, padx=(30, 10), pady=(10, 0)
        )

        btn_excel = Button(top, text='EXCEL', command=self.s_excel)
        btn_excel.grid(
            row=5, column=0, padx=(30, 10), pady=(10, 0)
        )

        btn_json = Button(top, text='JSON', command=self.s_json)
        btn_json.grid(
            row=6, column=0, padx=(30, 10), pady=(10, 0)
        )

        btn_xml = Button(top, text='XML', command=self.s_xml)
        btn_xml.grid(
            row=7, column=0, padx=(30, 10), pady=(10, 0)
        )

        top.transient(self)
        top.grab_set()
        top.focus_get()
        top.wait_window()

    def s_html(self):
        recorder.Recorder(self.visible_data).save_html()

    def s_xml(self):
        recorder.Recorder(self.visible_data).save_xml()

    def s_json(self):
        recorder.Recorder(self.visible_data).save_json()

    def s_excel(self):
        recorder.Recorder(self.visible_data).save_excel()

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
