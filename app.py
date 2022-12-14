import tkinter as tk
from auth import login, create_new_db, drop_db
from tkinter import messagebox


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('700x700')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.start_page = StartPage(parent=container, controller=self)
        self.start_page.place(relwidth=1, relheight=1)
        self.show_start_page()

    def show_start_page(self):
        self.start_page.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='gray')
        self.controller = controller
        self.parent = parent
        label = tk.Label(self, text="Sign in or sign up", bg='gray', font=25)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Sign in", font=25, bg='#2bbcd4')
        button2 = tk.Button(self, text="Sign in as superuser", font=25, bg='#2bbcd4',
                            command=self.redirect_to_admin_login_page)

        button1.pack()
        button2.pack()

    def redirect_to_admin_login_page(self):
        admin_login = AdminLogin(parent=self.parent, controller=self.controller)
        admin_login.place(relwidth=1, relheight=1)
        admin_login.tkraise()


class AdminLogin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='gray')
        self.controller = controller
        self.parent = parent
        label = tk.Label(self, text="Sign in as superuser", bg='gray', font=25)
        label.pack(side="top", fill="x", pady=10)

        username_input = tk.Entry(self, bg='white')
        password_input = tk.Entry(self, bg='white', show='*')
        username_input.pack()
        password_input.pack()

        button = tk.Button(self, text="Sign in", font=25, bg='#2bbcd4',
                           command=lambda: self.redirect_to_admin_page(username_input.get(), password_input.get()))
        self.controller.bind('<Return>', lambda event: self.redirect_to_admin_page(username_input.get(), password_input.get()))
        button.pack()

    def redirect_to_admin_page(self, username, password):
        try:
            conn = login(username, password)
            admin_page = AdminPage(parent=self.parent, connection=conn, controller=self.controller,
                                   username=username, password=password)
            admin_page.place(relwidth=1, relheight=1)
            admin_page.tkraise()
        except Exception:
            messagebox.showerror(title='Error', message='Wrong login or password')


class AdminPage(tk.Frame):

    def __init__(self, parent, connection, controller, username, password):
        tk.Frame.__init__(self, parent, bg='gray')
        self.controller = controller
        self.parent = parent
        self.conn = connection
        self.username = username
        self.password = password
        label = tk.Label(self, text="Superuser page", bg='gray', font=25)
        label.pack(side="top", fill="x", pady=10)

        button_create = tk.Button(self, text="Create user database", font=25, bg='#2bbcd4',
                                  command=lambda: create_new_db('user_db', self.conn,
                                                                self.username, self.password))
        button_create.pack()

        button_delete = tk.Button(self, text="Delete user database", font=25, bg='#2bbcd4',
                                  command=lambda: drop_db('user_db', self.username, self.password))
        button_delete.pack()
        print(type(controller.show_start_page))
        button_back = tk.Button(self, text="Back", font=25,
                                command=controller.show_start_page)
        button_back.pack()

    # def go_back(self):
    #     print('in here')
    #     sp = StartPage(parent=self, controller=self.controller)
    #     sp.place(relwidth=1, relheight=1)
    #     sp.tkraise()
    #     print('in here 2')
