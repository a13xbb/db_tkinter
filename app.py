import tkinter as tk
from auth import login, create_new_db, drop_db, registrate_user, check_role, is_enough_items_for_order, create_order, is_in_storage, register_item, add_to_storage
from auth import search_purchase_by_name, search_purchase_by_status, search_purchase_by_id, get_order_items
from auth import mark_as_paid as auth_mark_as_paid, get_transaction_by_name, get_all_transactions
from tkinter import messagebox, ttk
from utils import VerticalScrolledFrame


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('1000x700')
        self.option_add('*Dialog.msg.font', 'Times 10')
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
        label = tk.Label(self, text="Hello!", bg='light blue', font='Times 17')
        label.pack(side="top", fill="x", pady=20)

        button1 = tk.Button(self, text="Sign in", font=25, bg='#2bbcd4',
                            command=self.redirect_to_sign_in_page)
        button2 = tk.Button(self, text="Sign in as superuser", font=25, bg='#2bbcd4',
                            command=self.redirect_to_superuser_login_page)

        button1.pack(pady=10)
        button2.pack(pady=10)

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
        label = tk.Label(self, text="Sign in as superuser", bg='light blue', font='Times 17')
        label.pack(side="top", fill="x", pady=10)

        username_input = tk.Entry(self, bg='white', font='Times 15')
        password_input = tk.Entry(self, bg='white', show='*', font='Times 15')
        username_input.pack(pady=10)
        password_input.pack(pady=10)

        button = tk.Button(self, text="Sign in", font=25, bg='#2bbcd4',
                           command=lambda: self.redirect_to_superuser_page(username_input.get(), password_input.get()))
        self.controller.bind('<Return>',
                             lambda event: self.redirect_to_superuser_page(username_input.get(), password_input.get()))
        button.pack(pady=10)

        button_back = tk.Button(self, text="Back", font=25,
                                command=controller.show_start_page)
        button_back.pack(pady=10)

    def redirect_to_superuser_page(self, username, password):
        try:
            if username != 'postgres':
                raise Exception
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
        label = tk.Label(self, text="Superuser page", bg='light blue', font='Times 17')
        label.pack(side="top", fill="x", pady=10)

        button_create = tk.Button(self, text="Create user database", font=25, bg='#2bbcd4',
                                  command=lambda: create_new_db('user_db', self.engine,
                                                                self.username, self.password))
        button_create.pack(pady=10)

        button_delete = tk.Button(self, text="Delete user database", font=25, bg='#2bbcd4',
                                  command=lambda: drop_db('user_db', self.engine, self.username, self.password))
        button_delete.pack(pady=10)
        button_back = tk.Button(self, text="Back", font=25,
                                command=controller.show_start_page)
        button_back.pack(pady=10)


class SignIn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='light blue')
        self.controller = controller
        self.parent = parent
        label = tk.Label(self, text="Sign in", bg='light blue', font='Times 17')
        label.pack(side="top", fill="x", pady=10)

        username_input = tk.Entry(self, bg='white', font='Times 15')
        password_input = tk.Entry(self, bg='white', show='*', font='Times 15')
        username_input.pack(pady=10)
        password_input.pack(pady=10)

        button = tk.Button(self, text="Sign in", font=25, bg='#2bbcd4',
                           command=lambda: self.redirect(username_input.get(), password_input.get()))
        self.controller.bind('<Return>',
                             lambda event: self.redirect(username_input.get(), password_input.get()))
        button.pack(pady=10)

        button_back = tk.Button(self, text="Back", font=25,
                                command=controller.show_start_page)
        button_back.pack(pady=10)

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
        add_order_goto_button.grid(row=4, column=0, columnspan=2, pady=10)

        itm_goto_button = tk.Button(self, text="Manage Items", font='Times 15',
                                        command=lambda: self.redirect_itm())
        itm_goto_button.grid(row=5, column=0, columnspan=2)

        button_back = tk.Button(self, text="Back", font='Times 15',
                                command=controller.show_start_page)
        button_back.grid(row=7, column=0, columnspan=2, pady=10)

    def redirect_ord(self):
        disp_page = ManageOrders(parent=self, engine=self.engine, controller=self.controller)
        disp_page.place(relwidth=1, relheight=1)
        disp_page.tkraise()

    def redirect_itm(self):
        disp_page = ManageItems(parent=self, engine=self.engine, controller=self.controller)
        disp_page.place(relwidth=1, relheight=1)
        disp_page.tkraise()


class ManageItems(tk.Frame):
    def __init__(self, parent: MerchandiserPage, engine, controller: App):
        tk.Frame.__init__(self, parent, bg='light blue')
        self.parent = parent
        self.engine = engine
        self.controller = controller

### Register new item for storage suoervision

        add_item_label = tk.Label(self, text="Register New Item", bg='light blue', font='Times 20', pady=30)
        add_item_label.grid(row=1,column=0, columnspan=2)

        itemname_label = tk.Label(self, bg='light blue', font='Times 15', text='Item\'s name', pady=10, padx=10)
        itemname_input = tk.Entry(self, font='Times 15')
        weight_label = tk.Label(self, bg='light blue', font='Times 15', text='Weight of this item', pady=10, padx=10)
        weight_input = tk.Entry(self, font='Times 15')
        price_label = tk.Label(self, bg='light blue', font='Times 15', text='Price of this item', pady=10, padx=10)
        price_input = tk.Entry(self, font='Times 15')

        def reg_item():
            if is_in_storage(itemname_input.get(), 0, self.engine):
                messagebox.showerror(title='Error', message='Not enough items')
            elif weight_input.get() == '' or float(weight_input.get()) < 0:
                messagebox.showerror(title='Error', message='Enter valid not negative float for weight')
            elif price_input.get() == '' or float(price_input.get()) <= 0:
                messagebox.showerror(title='Error', message='Enter valid positive float for price')
            else:
                register_item(item_name=itemname_input.get(), weight=weight_input.get(), price=price_input.get(), engine=engine)

        itemname_label.grid(row=2, column=0)
        itemname_input.grid(row=2, column=1, pady=10, padx=10)
        weight_label.grid(row=3, column=0)
        weight_input.grid(row=3, column=1, pady=10, padx=10)
        price_label.grid(row=4, column=0)
        price_input.grid(row=4, column=1, pady=10, padx=10)
        reg_item_btn = tk.Button(self, text="Add new item", font='Times 15',
                                   command=reg_item)
        reg_item_btn.grid(row=6, column=0, columnspan=2, pady=20)

### Add quantity for known items

        row_displacement = 10

        add_item_label_2 = tk.Label(self, text="Register New Item", bg='light blue', font='Times 20', pady=30)
        add_item_label_2.grid(row=row_displacement+1,column=0, columnspan=2)

        itemname_label_2 = tk.Label(self, bg='light blue', font='Times 15', text='Item\'s name', pady=10, padx=10)
        itemname_input_2 = tk.Entry(self, font='Times 15')
        quant_label = tk.Label(self, bg='light blue', font='Times 15', text='Amount of addition', pady=10, padx=10)
        quant_input = tk.Entry(self, font='Times 15')

        def add_item():
            if not is_in_storage(itemname_input_2.get(), 0, self.engine):
                messagebox.showerror(title='Error', message='Item name unknown')
            elif quant_input.get() == '' and int(quant_input.get()) > 0:
                messagebox.showerror(title='Error', message='Enter valid positive amount')
            else:
                add_to_storage(item_name=itemname_input_2.get(), quantity=int(quant_input.get()), engine=engine)

        itemname_label_2.grid(row=row_displacement+2, column=0)
        itemname_input_2.grid(row=row_displacement+2, column=1, pady=10, padx=10)
        quant_label.grid(row=row_displacement+3, column=0)
        quant_input.grid(row=row_displacement+3, column=1, pady=10, padx=10)
        add_item_btn = tk.Button(self, text="Add items to storage", font='Times 15',
                                   command=add_item)
        add_item_btn.grid(row=row_displacement+5, column=0, columnspan=2, pady=20)

        button_back = tk.Button(self, text="Back", font='Times 15',
                                command=self.goback)
        button_back.place(anchor='nw', y=40)
###
    def goback(self):

        self.parent.tkraise()
        self.destroy()


class ManageOrders(VerticalScrolledFrame):
    def __init__(self, parent: MerchandiserPage, engine, controller: App):
        VerticalScrolledFrame.__init__(self, parent)
        self.parent = parent
        self.engine = engine
        self.controller = controller
        create_order_label = tk.Label(self.interior, text="Add order", bg='light blue', font='Times 20', pady=30)
        create_order_label.grid(row=1,column=0, columnspan=2)

        buyername_label = tk.Label(self.interior, bg='light blue', font='Times 15', text='Buyer\'s name', pady=10, padx=10)
        buyername_input = tk.Entry(self.interior, font='Times 15')
        status_var = tk.StringVar(self.controller)
        status_var.set('unpaid')
        status_dropdown = tk.OptionMenu(self.interior, status_var, *['unpaid', 'credit', 'paid'])
        status_dropdown.config(font='Times 15')

        status_label = tk.Label(self.interior, bg='light blue', font='Times 15', text='Payment status of \nthe order inplace', pady=10, padx=10)
        # status_input = tk.Entry(self.interior, font='Times 15')
        items_label = tk.Label(self.interior, bg='light blue', font='Times 15', text='Items (coma-separated)',
                                pady=10, padx=10)
        items_input = tk.Text(self.interior, height=7, width=29, font='Times 15', wrap='word')

        def get_order():
            if not is_enough_items_for_order(items_input.get('1.0', 'end')[:-1], self.engine):
                messagebox.showerror(title='Error', message='Not enough items')
            elif buyername_input.get() == '':
                messagebox.showerror(title='Error', message='Enter buyer\'s name')
            elif status_var.get() == '':
                messagebox.showerror(title='Error', message='Enter status')
            elif items_input.get('1.0', 'end')[:-1] == '':
                messagebox.showerror(title='Error', message='Enter 1 item at least')
            else:
                create_order(buyer_name=buyername_input.get(), items=items_input.get('1.0', 'end'), status=status_var.get(), engine=engine)

        buyername_label.grid(row=2, column=0)
        buyername_input.grid(row=2, column=1, pady=10, padx=10)
        status_label.grid(row=3, column=0)
        status_dropdown.grid(row=3, column=1, pady=10, padx=10)
        # status_input.grid(row=3, column=1, pady=10, padx=10)
        items_label.grid(row=4, column=0, columnspan=2)
        items_input.grid(row=5, column=0, columnspan=2)
        add_order_btn = tk.Button(self.interior, text="Add new order", font='Times 15',
                                   command=get_order)
        add_order_btn.grid(row=6, column=0, columnspan=2, pady=20)

#search orders

        create_order_label = tk.Label(self.interior, text="Search orders", bg='light blue', font='Times 20', pady=30)
        create_order_label.grid(row=7, column=0, columnspan=2)

        filter_label = tk.Label(self.interior, bg='light blue', font='Times 15', text='Choose the filter', pady=10, padx=0)
        drop_var = tk.StringVar(self.controller)
        drop_var.set('id')
        dropdown = tk.OptionMenu(self.interior, drop_var, *['id', 'name', 'status'])
        dropdown.config(font='Times 15')

        filter_label.grid(row=9, column=0, pady=10, padx=10)
        dropdown.grid(row=9, column=1, pady=10, padx=10)

        val_label = tk.Label(self.interior, bg='light blue', font='Times 15',
                             text='Enter value', pady=10, padx=10)
        val_input = tk.Entry(self.interior, font='Times 15')
        val_label.grid(row=10, column=0, pady=10, padx=10)
        val_input.grid(row=10, column=1, pady=10, padx=10)

        purchases_table = ttk.Treeview(self.interior)
        purchases_table.tag_configure('TkTextFont', font='Times 15')
        purchases_table['columns'] = ('Id', 'Buyer_name', 'Weight', 'Price', 'Status')

        purchases_table.column("#0", width=0, stretch='no')
        purchases_table.column("Id", anchor='center', width=120)
        purchases_table.column("Buyer_name", anchor='center', width=120)
        purchases_table.column("Weight", anchor='center', width=120)
        purchases_table.column("Price", anchor='center', width=120)
        purchases_table.column("Status", anchor='center', width=120)

        purchases_table.heading("#0", text="", anchor='center')
        purchases_table.heading("Id", text="Id", anchor='center')
        purchases_table.heading("Buyer_name", text="Buyer name", anchor='center')
        purchases_table.heading("Weight", text="Weight", anchor='center')
        purchases_table.heading("Price", text="Price", anchor='center')
        purchases_table.heading("Status", text="Status", anchor='center')

        id_input = tk.Entry(self.interior, font='Times 15', )
        get_order_items_btn = tk.Button(self.interior, text="Check items in order by its id", font='Times 15',
                                        command=lambda: get_order_items(id_input.get(), self.engine))
        get_order_items_btn.grid(row=8, column=0)
        id_input.grid(row=8, column=1)

        search_btn = tk.Button(self.interior, text="Search", font='Times 15',
                               command=lambda: self.search_by_filter(drop_var.get(), val_input.get(), purchases_table, self.engine))
        search_btn.grid(row=11, column=0, columnspan=2, pady=20)

        button_back = tk.Button(self.interior, text="Back", font='Times 15',
                                command=self.goback)
        button_back.place(anchor='nw', y=40)



        # my_game.grid(row=11, column=0, columnspan=2)

    def search_by_filter(self, _filter, val, table, engine):
        res = None
        if _filter == 'id':
            res = search_purchase_by_id(val, engine)
        elif _filter == 'status':
            res = search_purchase_by_status(val, engine)
        elif _filter == 'name':
            res = search_purchase_by_name(val, engine)

        table.delete(*table.get_children())
        for i, s in enumerate(res):
            row = s[0].strip('(').strip(')').split(',')
            table.insert(parent='', index='end', iid=i, text='',
                         values=tuple(row))
        table.grid(row=12, column=0, columnspan=2)

    def goback(self):

        self.parent.tkraise()
        self.destroy()


class AccountantPage(VerticalScrolledFrame):
    def __init__(self, parent, engine, controller, username, password):
        VerticalScrolledFrame.__init__(self, parent)
        #
        self.controller = controller
        self.engine = engine
        self.interior.name_label = None
        self.interior.price_label = None
        self.interior.status_label = None
        self.interior.set_paid_btn = None
        #

        self.interior.controller = controller
        self.interior.parent = parent
        self.interior.engine = engine
        self.interior.username = username
        self.interior.password = password
        label = tk.Label(self.interior, text="Accountant page", bg='light blue', font='Times 25', pady=40, padx=100)
        label.grid(row=0, column=0, columnspan=2, padx=100)

        id_input = tk.Entry(self.interior, bg='white', font='Times 15', width=6)
        check_info_btn = tk.Button(self.interior, text="Check order info by id", font='Times 15',
                                   command=lambda: self.get_order_info(id_input.get(), self.interior.engine))
        check_info_btn.grid(row=1, column=0, pady=10)
        id_input.grid(row=1, column=1, pady=10)

        button_back = tk.Button(self.interior, text="Back", font='Times 15',
                                command=self.interior.controller.show_start_page)
        button_back.place(anchor='nw', y=40, x=100)

        #------------------------------------ ACCOUNTANT SEARCH ---------------------------------------
        search_label = tk.Label(self.interior, text="Search transactions", bg='light blue', font='Times 18', pady=40, padx=100)
        search_label.grid(row=6, column=0, columnspan=2, padx=100)
        filter_label = tk.Label(self.interior, bg='light blue', font='Times 15', text='Choose the filter', pady=10,
                                padx=0)
        drop_var = tk.StringVar(self.controller)
        drop_var.set('all')
        dropdown = tk.OptionMenu(self.interior, drop_var, *['all', 'name'])
        dropdown.config(width=7)
        dropdown.config(font='Times 15')

        filter_label.grid(row=7, column=0, pady=10, padx=10)
        dropdown.grid(row=7, column=1, pady=10, padx=10)

        purchases_table = ttk.Treeview(self.interior)
        purchases_table.tag_configure('TkTextFont', font='Times 15')
        purchases_table['columns'] = ('Id', 'Cost', 'Counteragent')

        purchases_table.column("#0", width=0, stretch='no')
        purchases_table.column("Id", anchor='center', width=120)
        purchases_table.column("Cost", anchor='center', width=120)
        purchases_table.column("Counteragent", anchor='center', width=120)

        purchases_table.heading("#0", text="", anchor='center')
        purchases_table.heading("Id", text="Id", anchor='center')
        purchases_table.heading("Cost", text="Cost", anchor='center')
        purchases_table.heading("Counteragent", text="Counteragent", anchor='center')

        name_input = tk.Entry(self.interior, font='Times 15')

        search_btn = tk.Button(self.interior, text="Search", font='Times 15',
                               command=lambda: self.search_by_filter(drop_var.get(), name_input.get(), purchases_table,
                                                                     self.engine))
        search_btn.grid(row=9, column=0, columnspan=2, pady=20)

        name_input.grid(row=8, column=0, columnspan=2, pady=20)

    def search_by_filter(self, _filter, val, table, engine):
        res = None
        if _filter == 'all':
            res = get_all_transactions(self.engine)
        elif _filter == 'name':
            res = get_transaction_by_name(val, engine)

        table.delete(*table.get_children())
        for i, s in enumerate(res):
            row = s[0].strip('(').strip(')').split(',')
            table.insert(parent='', index='end', iid=i, text='',
                         values=tuple(row))
        table.grid(row=10, column=0, columnspan=2)
        # ------------------------------------ ACCOUNTANT SEARCH ---------------------------------------



    def get_order_info(self, _id: int, engine):
        if self.interior.name_label is not None:
            self.interior.name_label.destroy()
            self.interior.price_label.destroy()
            self.interior.status_label.destroy()
        if self.interior.set_paid_btn is not None:
            self.interior.set_paid_btn.destroy()
        res = search_purchase_by_id(_id, engine)
        res = res[0][0].strip('(').strip(')').split(',')
        name, price, status = [res[1], res[3], res[4]]
        self.interior.name_label = tk.Label(self.interior, text=f'Buyer: {name}', bg='light blue', font='Times 18', pady=10, fg='#0260fd')
        self.interior.price_label = tk.Label(self.interior, text=f'Price: {price}', bg='light blue', font='Times 18', pady=10, fg='#0260fd')
        self.interior.status_label = tk.Label(self.interior, text=f'Status: {status}', bg='light blue', font='Times 18', pady=10, fg='#0260fd')
        self.interior.name_label.grid(row=2, column=0, columnspan=2)
        self.interior.price_label.grid(row=3, column=0, columnspan=2)
        self.interior.status_label.grid(row=4, column=0, columnspan=2)
        if status in ['unpaid', 'credit']:
            self.interior.set_paid_btn = tk.Button(self.interior, text="Mark as paid", font='Times 15',
                                                   command=lambda: self.mark_as_paid(_id, engine))
            self.interior.set_paid_btn.grid(row=5, column=0, columnspan=2, padx=10)
        print(name, price, status)

    def mark_as_paid(self, _id, engine):
        auth_mark_as_paid(_id, engine)
        self.interior.get_order_info(_id, engine)
