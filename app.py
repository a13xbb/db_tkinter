import tkinter as tk
from auth import login, create_new_db, drop_db, registrate_user, check_role, is_enough_items_for_order
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
            engine = login(username, password, 'super_db')
            admin_page = SuperUserPage(parent=self.parent, engine=engine, controller=self.controller,
                                       username=username, password=password)
            admin_page.place(relwidth=1, relheight=1)
            admin_page.tkraise()
        except Exception:
            messagebox.showerror(title='Error', message='Wrong login or password')


class SuperUserPage(tk.Frame):

    def __init__(self, parent, engine, controller, username, password):
        tk.Frame.__init__(self, parent, bg='light blue')
        self.controller = controller
        self.parent = parent
        self.engine = engine
        self.username = username
        self.password = password
        label = tk.Label(self, text="Superuser page", bg='light blue', font=25)
        label.pack(side="top", fill="x", pady=10)

        button_create = tk.Button(self, text="Create user database", font=25, bg='#2bbcd4',
                                  command=lambda: create_new_db('user_db', self.engine,
                                                                self.username, self.password))
        button_create.pack()

        button_delete = tk.Button(self, text="Delete user database", font=25, bg='#2bbcd4',
                                  command=lambda: drop_db('user_db', self.engine, self.username, self.password))
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
            engine = login(username, password, 'user_db')
            if username == 'admin':
                admin_page = AdminPage(parent=self.parent, engine=engine, controller=self.controller,
                                       username=username, password=password)
                admin_page.place(relwidth=1, relheight=1)
                admin_page.tkraise()
            elif check_role(username) == 'accountant':
                acc_page = AccountantPage(parent=self.parent, engine=engine, controller=self.controller,
                                       username=username, password=password)
                acc_page.place(relwidth=1, relheight=1)
                acc_page.tkraise()
            elif check_role(username) == 'merchandiser':
                merch_page = MerchandiserPage(parent=self.parent, engine=engine, controller=self.controller,
                                       username=username, password=password)
                merch_page.place(relwidth=1, relheight=1)
                merch_page.tkraise()

        except Exception:
            messagebox.showerror(title='Error', message='Wrong login or password')


# admin can registrate new users with a certain roles
class AdminPage(tk.Frame):
    def __init__(self, parent, engine, controller, username, password):
        tk.Frame.__init__(self, parent, bg='light blue', padx=180)
        self.controller = controller
        self.parent = parent
        self.engine = engine
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
        drop_var = tk.StringVar(self.controller)
        drop_var.set(roles[0])
        dropdown = tk.OptionMenu(self, drop_var, *roles)
        dropdown.config(font='Times 15')

        role_label.grid(row=3, column=0, pady=10, padx=10)
        dropdown.grid(row=3, column=1, pady=10, padx=10)

        registrate_btn = tk.Button(self, text="Registrate new user", font='Times 15',
                                   command=lambda: registrate_user(username_input.get(),
                                                                   password_input.get(),
                                                                   drop_var.get(),
                                                                   self.engine))
        registrate_btn.grid(row=4, column=0, columnspan=2)

        button_back = tk.Button(self, text="Back", font='Times 15',
                                command=controller.show_start_page)
        button_back.place(anchor='nw', y=40)


class AccountantPage(tk.Frame):
    def __init__(self, parent, engine, controller, username, password):
        tk.Frame.__init__(self, parent, bg='light blue', padx=180)
        self.controller = controller
        self.parent = parent
        self.engine = engine
        self.username = username
        self.password = password
        label = tk.Label(self, text="Accountant page", bg='light blue', font='Times 25', pady=40)
        label.grid(row=0, column=0, columnspan=2)


class MerchandiserPage(tk.Frame):
    def __init__(self, parent, engine, controller, username, password):
        tk.Frame.__init__(self, parent, bg='light blue', padx=180)
        self.controller = controller
        self.parent = parent
        self.engine = engine
        self.username = username
        self.password = password
        label = tk.Label(self, text="Merchandiser page", bg='light blue', font='Times 25', pady=40)
        label.grid(row=0, column=0, columnspan=2)

        add_order_goto_button = tk.Button(self, text="Manage orders", font='Times 15',
                                        command=lambda: self.redirect_ord())
        add_order_goto_button.grid(row=4, column=0, columnspan=2)

        button_back = tk.Button(self, text="Back", font='Times 15',
                                command=controller.show_start_page)
        button_back.grid(row=5, column=0, columnspan=2)

    def redirect_ord(self):
        disp_page = AddOrder(parent=self, engine=self.engine, controller=self.controller)
        disp_page.place(relwidth=1, relheight=1)
        disp_page.tkraise()


class AddOrder(tk.Frame):
    def __init__(self, parent: MerchandiserPage, engine, controller: App):
        tk.Frame.__init__(self, parent, bg='light blue')
        self.parent = parent
        self.engine = engine
        create_order_label = tk.Label(self, text="Add order", bg='light blue', font='Times 15', pady=30)
        create_order_label.grid(row=1,column=0, columnspan=2)

        buyername_label = tk.Label(self, bg='light blue', font='Times 15', text='Buyer\'s name', pady=10, padx=10)
        buyername_input = tk.Entry(self, font='Times 15')
        status_label = tk.Label(self, bg='light blue', font='Times 15', text='Payment status of \nthe order inplace', pady=10, padx=10)
        status_input = tk.Entry(self, font='Times 15')
        items_label = tk.Label(self, bg='light blue', font='Times 15', text='Items (coma-separated)',
                                pady=10, padx=10)
        items_input = tk.Text(self, height=7, width=29, font='Times 15', wrap='word')

        buyername_label.grid(row=2, column=0)
        buyername_input.grid(row=2, column=1, pady=10, padx=10)
        status_label.grid(row=3, column=0)
        status_input.grid(row=3, column=1, pady=10, padx=10)
        items_label.grid(row=4, column=0, columnspan=2)
        items_input.grid(row=5, column=0, columnspan=2)
        add_order_btn = tk.Button(self, text="Add new order", font='Times 15',
                                   command=lambda: print(is_enough_items_for_order(items_input.get('1.0', 'end')[:-1], self.engine)))
        add_order_btn.grid(row=6, column=0, columnspan=2, pady=20)


        button_back = tk.Button(self, text="Back", font='Times 15',
                        command=self.goback)
        button_back.place(anchor='nw', y=40)



    def goback(self):

        self.parent.tkraise()
        self.destroy()


#TODO:
#   1) идем в айтемы и проверяем, есть ли на складе все необходимые айтемы
#   2) если нет, то дропаем ошибку
#   3) если да, то высчитываем вес заказа, его цену (sum(items) + tanh(С * sum(weights) - 1) + 1)
#   4) добавляем заказ в таблицу purchase
#   5) добавляем в таблицу purchase_item order_id:item