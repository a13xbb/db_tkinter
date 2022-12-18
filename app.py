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
        tk.Frame.__init__(self, parent, bg='light blue')
        self.controller = controller
        self.parent = parent
        label = tk.Label(self, text="Hello!", bg='light blue', font=25)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Sign in", font=25, bg='#2bbcd4',
                            command=self.redirect_to_sign_in_page)
        button2 = tk.Button(self, text="Sign in as superuser", font=25, bg='#2bbcd4',
                            command=self.redirect_to_superuser_login_page)

        button1.pack()
        button2.pack()

    def redirect_to_superuser_login_page(self):
        admin_login = SuperUserLogin(parent=self.parent, controller=self.controller)
        admin_login.place(relwidth=1, relheight=1)
        admin_login.tkraise()

    def redirect_to_sign_in_page(self):
        sign_in = SignIn(parent=self.parent, controller=self.controller)
        sign_in.place(relwidth=1, relheight=1)
        sign_in.tkraise()


class SuperUserLogin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='light blue')
        self.controller = controller
        self.parent = parent
        label = tk.Label(self, text="Sign in as superuser", bg='light blue', font=25)
        label.pack(side="top", fill="x", pady=10)

        username_input = tk.Entry(self, bg='white')
        password_input = tk.Entry(self, bg='white', show='*')
        username_input.pack()
        password_input.pack()

        button = tk.Button(self, text="Sign in", font=25, bg='#2bbcd4',
                           command=lambda: self.redirect_to_superuser_page(username_input.get(), password_input.get()))
        self.controller.bind('<Return>',
                             lambda event: self.redirect_to_superuser_page(username_input.get(), password_input.get()))
        button.pack()

        button_back = tk.Button(self, text="Back", font=25,
                                command=controller.show_start_page)
        button_back.pack()

    def redirect_to_superuser_page(self, username, password):
        try:
            conn = login(username, password, 'super_db')
            admin_page = SuperUserPage(parent=self.parent, connection=conn, controller=self.controller,
                                       username=username, password=password)
            admin_page.place(relwidth=1, relheight=1)
            admin_page.tkraise()
        except Exception:
            messagebox.showerror(title='Error', message='Wrong login or password')


class SuperUserPage(tk.Frame):

    def __init__(self, parent, connection, controller, username, password):
        tk.Frame.__init__(self, parent, bg='light blue')
        self.controller = controller
        self.parent = parent
        self.conn = connection
        self.username = username
        self.password = password
        label = tk.Label(self, text="Superuser page", bg='light blue', font=25)
        label.pack(side="top", fill="x", pady=10)

        button_create = tk.Button(self, text="Create user database", font=25, bg='#2bbcd4',
                                  command=lambda: create_new_db('user_db', self.conn,
                                                                self.username, self.password))
        button_create.pack()

        button_delete = tk.Button(self, text="Delete user database", font=25, bg='#2bbcd4',
                                  command=lambda: drop_db('user_db', self.conn, self.username, self.password))
        button_delete.pack()
        button_back = tk.Button(self, text="Back", font=25,
                                command=controller.show_start_page)
        button_back.pack()


class SignIn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='light blue')
        self.controller = controller
        self.parent = parent
        label = tk.Label(self, text="Sign in", bg='light blue', font=25)
        label.pack(side="top", fill="x", pady=10)

        username_input = tk.Entry(self, bg='white')
        password_input = tk.Entry(self, bg='white', show='*')
        username_input.pack()
        password_input.pack()

        button = tk.Button(self, text="Sign in", font=25, bg='#2bbcd4',
                           command=lambda: self.redirect(username_input.get(), password_input.get()))
        self.controller.bind('<Return>',
                             lambda event: self.redirect(username_input.get(), password_input.get()))
        button.pack()

        button_back = tk.Button(self, text="Back", font=25,
                                command=controller.show_start_page)
        button_back.pack()

    def redirect(self, username, password):
        try:
            conn = login(username, password, 'user_db')
            if username == 'admin':
                admin_page = AdminPage(parent=self.parent, connection=conn, controller=self.controller,
                                       username=username, password=password)
                admin_page.place(relwidth=1, relheight=1)
                admin_page.tkraise()
        except Exception:
            messagebox.showerror(title='Error', message='Wrong login or password')


# admin can registrate new users with a certain roles
class AdminPage(tk.Frame):
    def __init__(self, parent, connection, controller, username, password):
        tk.Frame.__init__(self, parent, bg='light blue', padx=180)
        self.controller = controller
        self.parent = parent
        self.conn = connection
        self.username = username
        self.password = password
        label = tk.Label(self, text="Admin page", bg='light blue', font='Times 25', pady=40)
        label.grid(row=0, column=0, columnspan=2)

        # self.controller.grid_columnconfigure((0, 1), weight=1)

        username_label = tk.Label(self, bg='light blue', font='Times 15', text='New user handle', pady=10, padx=10)
        username_input = tk.Entry(self, font='Times 15')
        password_label = tk.Label(self, bg='light blue', font='Times 15', text='New user password', pady=10, padx=10)
        password_input = tk.Entry(self, font='Times 15', show='*')

        username_label.grid(row=1, column=0)
        username_input.grid(row=1, column=1, pady=10, padx=10)
        password_label.grid(row=2, column=0)
        password_input.grid(row=2, column=1, pady=10, padx=10)

        role_label = tk.Label(self, bg='light blue', font='Times 15', text='New user role', pady=10, padx=10)
        roles = [
            'accountant',
            'merchandiser'
        ]
        default_var = tk.StringVar(self)
        default_var.set(roles[0])
        dropdown = tk.OptionMenu(self, default_var, *roles)
        dropdown.config(font='Times 15')

        role_label.grid(row=3, column=0, pady=10, padx=10)
        dropdown.grid(row=3, column=1, pady=10, padx=10)

        registrate_btn = tk.Button(self, text="Registrate new user", font='Times 15')
        registrate_btn.grid(row=4, column=0, columnspan=2)

        button_back = tk.Button(self, text="Back", font='Times 15',
                                command=controller.show_start_page)
        button_back.place(anchor='nw', y=40)


    # def go_back(self):
    #     print('in here')
    #     sp = StartPage(parent=self, controller=self.controller)
    #     sp.place(relwidth=1, relheight=1)
    #     sp.tkraise()
    #     print('in here 2')
