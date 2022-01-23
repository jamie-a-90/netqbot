import tkinter as tk
from tkinter import tix
from tkinter import OptionMenu, messagebox
from db import Database
import time
import threading
import datetime

# Instanciate databse object
db = Database('user.db')

# Main Application/GUI class
class Application(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('netqbot')
        # Width height
        master.geometry("700x700")
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var
        self.selected_item = 0
        # Populate initial list
        self.populate_list()
        # Init running bool
        self.running = False
        # Init api running bool
        self.grace_running = False
        
    # Create widgets for gui
    def create_widgets(self):
        # User
        self.user_text = tk.StringVar()
        self.user_tip = tix.Balloon(self.master)
        self.user_label = tk.Label(self.master, text='User: ', font=('bold', 10), pady=20)
        self.user_label.grid(row=0, column=0, sticky=tk.W)
        self.user_entry = tk.Entry(self.master, textvariable=self.user_text)
        self.user_entry.grid(row=0, column=1)
        self.user_tip.bind_widget(self.user_entry, balloonmsg="The user as displayed in Assyst")
        # UserID
        self.userid_text = tk.StringVar()
        self.userid_tip = tix.Balloon(self.master)
        self.userid_label = tk.Label(self.master, text='User ID: ', font=('bold', 10), pady=20)
        self.userid_label.grid(row=0, column=2, sticky=tk.W)
        self.userid_entry = tk.Entry(self.master, textvariable=self.userid_text)
        self.userid_entry.grid(row=0, column=3)
        self.userid_tip.bind_widget(self.userid_entry, balloonmsg="The user's unqiue Assyst ID")
        # Queue Limit 
        self.qlimit_text = tk.StringVar()
        self.qlimit_tip = tix.Balloon(self.master)
        self.qlimit_label = tk.Label(self.master, text='Queue Limit: ', font=('bold', 10))
        self.qlimit_label.grid(row=1, column=0, sticky=tk.W)
        self.qlimit_entry = tk.Entry(self.master, textvariable=self.qlimit_text)
        self.qlimit_entry.grid(row=1, column=1)
        self.qlimit_tip_message = "Limit the user's queue. Type none, if unlimited."
        self.qlimit_tip.bind_widget(self.qlimit_entry, balloonmsg=self.qlimit_tip_message)
        # Shift
        self.shift_text = tk.StringVar()
        self.shift_tip = tix.Balloon(self.master)
        self.shift_label = tk.Label(self.master, text='Shift: ', font=('bold', 10))
        self.shift_label.grid(row=1, column=2, sticky=tk.W)
        self.shift_menu_options = ["Day (08:00-18:00)", "Late (15:30-00:00)", "On leave", "Exclude"]
        self.shift_text.set(self.shift_menu_options[0])
        self.shift_menu = OptionMenu(self.master, self.shift_text, *self.shift_menu_options)
        self.shift_menu.grid(row=1, column=3)
        self.shift_tip.bind_widget(self.shift_menu, balloonmsg="The shift will determain when/if the user is assigned tickets")



        ## QUEUE LIMIT TO GO HERE!
        ##
        ##
        ##
        ##
        ##
        ##
        ##

        # Buttons
        self.add_btn = tk.Button(
            self.master, text="Add User", width=12, activebackground='#345', 
            activeforeground='white', command=self.add_user)
        self.add_btn.grid(row=2, column=0, pady=20)
        self.remove_btn = tk.Button(
            self.master, text="Remove User", width=12, activebackground='#345', 
            activeforeground='white', command=self.remove_user)
        self.remove_btn.grid(row=2, column=1)
        self.update_btn = tk.Button(
            self.master, text="Update User", width=12, activebackground='#345', 
            activeforeground='white', command=self.update_user)
        self.update_btn.grid(row=2, column=2)
        self.clear_btn = tk.Button(
            self.master, text="Clear Input", width=12, activebackground='#345', 
            activeforeground='white', command=self.clear_text)
        self.clear_btn.grid(row=2, column=3)
        self.run_btn = tk.Button(
            self.master, text="Run", width=12, activebackground='#345', 
            activeforeground='white', command=self.start_run)
        self.run_btn.grid(row=3, column=5)
        self.stop_btn = tk.Button(
            self.master, text="Stop", width=12, activebackground='#345', 
            activeforeground='white', command=self.stop_run, state=tk.DISABLED)
        self.stop_btn.grid(row=3, column=6)

        # User list (listbox)
        self.user_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.user_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
        # Create scrollbar 1
        self.scrollbar_1 = tk.Scrollbar(self.master)
        #self.scrollbar_1.grid(row=3, column=3, pady=20, sticky=tk.W) #REMOVED, scroll works without
        # Set scrollbar 1 to user list
        self.user_list.configure(yscrollcommand=self.scrollbar_1.set)
        self.scrollbar_1.configure(command=self.user_list.yview)
        # Bind select
        self.user_list.bind('<<ListboxSelect>>', self.select_item)

        # Log box (listbox)
        self.log_list = tk.Listbox(self.master, height=16, width=100, border=0)
        self.log_list.grid(row=10, column=0, columnspan=7, rowspan=6, pady=20, padx=20, sticky=tk.W)
        # Create scrollbar 2
        self.scrollbar_2 = tk.Scrollbar(self.master)
        #self.scrollbar_2.grid(row=10, column=7, pady=20, sticky=tk.W) #REMOVED, scroll works without
        # Set scrollbar 2 to log box
        self.log_list.configure(yscrollcommand=self.scrollbar_2.set)
        self.scrollbar_2.configure(command=self.log_list.yview)

    # Add new item
    def add_user(self):
        if self.user_text.get() == '' or self.userid_text.get() == '' or self.shift_text.get() == '' or self.qlimit_text.get() == '':
            messagebox.showerror(
                "Required Fields", "Please include all fields")
            return
        # Insert into DB
        db.insert(self.user_text.get(), self.userid_text.get(),
                self.qlimit_text.get(), self.shift_text.get())
        # Clear list
        self.user_list.delete(0, tk.END)
        # Insert into list
        self.user_list.insert(tk.END, (self.user_text.get(), self.userid_text.get(
        ), self.qlimit_text.get(), self.shift_text.get()))
        self.clear_text()
        self.populate_list()
    
    # Remove item
    def remove_user(self):
        if self.user_text.get() == '' or self.userid_text.get() == '' or self.shift_text.get() == '' or self.qlimit_text.get() == '':
            messagebox.showerror(
        "Required Fields", "Please include all fields")
            return
        yesno = messagebox.askyesno(message="This will permentanly remove the user. Are you sure? ")
        if yesno: 
            db.remove(self.selected_item[0]) 
            self.clear_text()
            self.populate_list()
        else:
            pass
        
    # Update item
    def update_user(self):
        if self.user_text.get() == '' or self.userid_text.get() == '' or self.shift_text.get() == '' or self.qlimit_text.get() == '':
            messagebox.showerror(
        "Required Fields", "Please include all fields")
            return
        db.update(self.selected_item[0], self.user_text.get(
        ), self.userid_text.get(), self.qlimit_text.get(), self.shift_text.get())
        self.populate_list()

    # Clear all text fields
    def clear_text(self):
        self.user_entry.delete(0, tk.END)
        self.userid_entry.delete(0, tk.END)
        self.shift_text.set(self.shift_menu_options[0])
        self.shift_menu = OptionMenu(self.master, self.shift_text.set(self.shift_menu_options[0]), *self.shift_menu_options)
        self.qlimit_entry.delete(0, tk.END)

    # Select item & populate entry
    def select_item(self, event):
        # # Create global selected item to use in other functions
        # global self.selected_item
        try:
            # Get index
            index = self.user_list.curselection()[0]
            # Get selected item
            self.selected_item = self.user_list.get(index)

            # Add text to entries
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(tk.END, self.selected_item[1])
            self.userid_entry.delete(0, tk.END)
            self.userid_entry.insert(tk.END, self.selected_item[2])        
            self.qlimit_entry.delete(0, tk.END)
            self.qlimit_entry.insert(tk.END, self.selected_item[3])
            self.shift_menu = OptionMenu(self.master, self.shift_text.set(self.selected_item[4]), *self.shift_menu_options)
        except IndexError:
            pass
    
    # Populates user list from sql db
    def populate_list(self):
        # Delete items before update. So when you keep pressing it doesnt keep getting (show example by calling this twice)
        self.user_list.delete(0, tk.END)
        # Loop through records
        for row in db.fetch():
            # Insert into list
            self.user_list.insert(tk.END, row)

    # Start and Stop running of app
    def start_run(self):

        if self.grace_running == True:
            self.log_list.insert(
                tk.END, '{} There is an ongoing transaction with AssystREST. Please wait for this to stop and try again.'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            messagebox.showinfo(message='There is an ongoing transaction with AssystREST. Please wait for this to stop and try again.')
        else:
            try:
                self.add_btn['state'] = tk.DISABLED
                self.remove_btn['state'] = tk.DISABLED
                self.update_btn['state'] = tk.DISABLED
                self.run_btn['state'] = tk.DISABLED
                self.stop_btn['state'] = tk.NORMAL
                self.assyst_thread = threading.Thread(target=app.api_assyst)
                self.assyst_thread.start()
                self.running = True
                self.log_list.insert(tk.END, '{} Starting.'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            except:
                self.log_list.insert(tk.END, '{} ERROR: unable to start.'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def stop_run(self):
        self.add_btn['state'] = tk.NORMAL
        self.remove_btn['state'] = tk.NORMAL
        self.update_btn['state'] = tk.NORMAL
        self.run_btn['state'] = tk.NORMAL
        self.stop_btn['state'] = tk.DISABLED
        try:
            #self.assyst_mp.stop()
            self.log_list.insert(tk.END, '{} Stopping.'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            self.running = False
            self.grace_thread = threading.Thread(target=app.grace)
            self.grace_thread.start()

        except:
            self.log_list.insert(tk.END, '{} ERROR: unable to stop.'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
    def api_assyst(self):
        self.log_list.insert(tk.END, '{} Successfully started.'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        while self.running:
            for i in range(1, 11):
                print(str(i))
                time.sleep(1)
            time.sleep(10)

    def grace(self):
        self.grace_running = True
        time.sleep(25)
        self.grace_running = False        
        self.log_list.insert(tk.END, '{} Successfully stopped'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    # Log generator
    def create_log(self, message):
        None # Logs to be migrated from existing fuctions to here.


root = tix.Tk()
app = Application(master=root)
app.mainloop()




