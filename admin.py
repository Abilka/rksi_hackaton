#Импорт модулей
import tkinter
import webbrowser

from tkinter import *
from tkinter import ttk
from tkinter.tix import ComboBox
from tkinter import messagebox

#Импорт файлов
import scheduler
import auth
import user



class Window(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        # параметры окна
        self.geometry('1000x400+150+150')
        self.title("Turtle")
        self.config(bg='#83d798')

        # фрейм
        frame = Frame(self)
        frame.pack()

        # навигационная панель (меню)
        menu = Menu(self)
        self.config(menu=menu)
        test1 = Menu(menu, tearoff=0)
        test1.add_command(label='Добавить пользователя', font=("Arial Bold", 10), command=self.new_window2)
        test1.add_command(label='Выйти', font=("Arial Bold", 10), command=self.back_auth)

        test2 = Menu(menu, tearoff=0)
        test2.add_command(label='Обратная связь', font=("Arial Bold", 10), command=self.help)

        menu.add_cascade(label='Действия', menu=test1)
        menu.add_cascade(label='Помощь', menu=test2)

        # заполнение таблицы

        schedul = scheduler.Schedule().changed_needed()

        heads = ['Предмет', 'Группа', 'Аудитория',
                 'Корпус', 'Пара', 'Начало', 'Конец',
                 'Преподаватели', 'Дата', 'Время', 'Вес']

        data = list(map(list, schedul.values))

        # высота изменяеться в зависимости количества данных
        table = ttk.Treeview(frame, show='headings', height=len(data))
        table['columns'] = heads

        # перебираем данные из списка header и заполняем в таблицу
        for header in heads:
            table.heading(header, text=header, anchor='center')
            table.column(header, anchor='center', minwidth=150, width=140)

        # перебираем данные из списка data и заполняем в таблицу
        for row in data:
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

    def new_window2(self):
        add_User().mainloop()

    def back_auth(self):
        auth.AuthApp()
        self.destroy()

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


class add_User(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        # параметры окна
        self.geometry('300x300+450+150')
        self.title("Регистрация нового пользователя")
        self.config(bg='#83d798')

        label_login = Label(self, text='Логин:', bg='#83d798', font=("Arial Bold", 10))
        label_login.grid(
            column=0, row=0, padx=120, pady=(20, 0)
        )

        self.login = Entry(self, width=20)
        self.login.grid(
            row=1, column=0, pady=(10, 10)
        )

        label_password = Label(self, text='Пароль:', bg='#83d798', font=("Arial Bold", 10),)
        label_password.grid(
            column=0, row=3
        )

        self.password = Entry(self, width=20)
        self.password.grid(
            row=4, column=0, pady=(10, 10)
        )

        self.combo_Box = ttk.Combobox(self, values=[
            'admin',
            'buh',
            'tb'
        ])

        self.combo_Box.current(0)
        self.combo_Box.grid(
            row=6, column=0, pady=20
        )

        self.btn_next = Button(self, text='Добавить', font=("Arial Bold", 10), command=self.requests_registration)
        self.btn_next.grid(row=9, column=0)

    def requests_registration(self):
        login = self.login.get()
        password = self.password.get()
        role = self.combo_Box.get()
        if user.User.new_user(login,
                              password,
                              role)['result'] is True:

            messagebox.showinfo('Уведомление', "Новый пользователь создан!\n{}\n{}".format(login, role))
        else:
            messagebox.showerror('Ошибка', "Такой пользователь уже существует.")
        self.destroy()
