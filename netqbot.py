import tkinter as tk
from tkinter import tix
from tkinter import OptionMenu, messagebox
from db import Database
import time
import threading
import datetime
import assyst

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
        # Init api_assyst_running bool
        self.api_assyst_running = False
        # Init api api_assyst_running bool
        self.stopping_api_assyst_running = False
        # Database users into list 
        #self.users = list()
        # Tickets into a list
        #self.tickets = list()
        
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

        # Check Buttons
        self.check_one_bool = tk.BooleanVar()
        self.check_two_bool = tk.BooleanVar()
        self.check_three_bool = tk.BooleanVar()
        self.check_four_bool = tk.BooleanVar()
        self.check_five_bool = tk.BooleanVar()
        self.check_six_bool = tk.BooleanVar()
        # P1 check button
        self.check_one = tk.Checkbutton(self.master, text='P1 - 4HR', variable=self.check_one_bool,
                                        onvalue=True, offvalue=False)
        self.check_one.grid(row=4, column=5)
        # P2 check button
        self.check_two = tk.Checkbutton(self.master, text='P2 - 8HR', variable=self.check_two_bool,
                                        onvalue=True, offvalue=False)
        self.check_two.grid(row=5, column=5)
        # P3 check button
        self.check_three = tk.Checkbutton(self.master, text='P3 - 16HR', variable=self.check_three_bool,
                                        onvalue=True, offvalue=False)
        self.check_three.grid(row=6, column=5)
        # SR2 check button
        self.check_four = tk.Checkbutton(self.master, text='SR2 - 4 DAYS', variable=self.check_four_bool,
                                        onvalue=True, offvalue=False)
        self.check_four.grid(row=4, column=6)
        # SR3 check button
        self.check_five = tk.Checkbutton(self.master, text='SR3 - 10 DAYS', variable=self.check_five_bool,
                                        onvalue=True, offvalue=False)
        self.check_five.grid(row=5, column=6)
        # Work request check button
        self.check_six = tk.Checkbutton(self.master, text='WORK REQUEST', variable=self.check_six_bool,
                                        onvalue=True, offvalue=False)
        self.check_six.grid(row=6, column=6)

        # User list (listbox)
        self.user_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.user_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
        # Create scrollbar 1
        #self.scrollbar_1 = tk.Scrollbar(self.master)
        #self.scrollbar_1.grid(row=3, column=3, pady=20, sticky=tk.W) #REMOVED, scroll works without
        # Set scrollbar 1 to user list
        #self.user_list.configure(yscrollcommand=self.scrollbar_1.set)
        #self.scrollbar_1.configure(command=self.user_list.yview)
        # Bind select
        self.user_list.bind('<<ListboxSelect>>', self.select_item)

        # Log box (listbox)
        self.log_list = tk.Listbox(self.master, height=16, width=100, border=0)
        self.log_list.grid(row=10, column=0, columnspan=7, rowspan=6, pady=20, padx=20, sticky=tk.W)
        # Create scrollbar 2
        #self.scrollbar_2 = tk.Scrollbar(self.master)
        #self.scrollbar_2.grid(row=10, column=7, pady=20, sticky=tk.W) #REMOVED, scroll works without
        # Set scrollbar 2 to log box
        #self.log_list.configure(yscrollcommand=self.scrollbar_2.set)
        #self.scrollbar_2.configure(command=self.log_list.yview)

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
        self.create_log(message='{x} New user added to database: {y}'.format(x=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), y=self.user_text.get()))
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
            self.create_log(message='{x} User removed from database: {y}'.format(x=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), y=self.user_text.get()))
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
        self.create_log(message='{x} Database updated for user: {y}'.format(x=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), y=self.user_text.get()))
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

    # Start and Stop api_assyst_running of app
    def start_run(self):

        if self.stopping_api_assyst_running == True:
            self.create_log(message='{} There is an ongoing transaction with AssystREST. Please wait for this to stop and try again.'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            messagebox.showinfo(message='There is an ongoing transaction with AssystREST. Please wait for this to stop and try again.')
        else:
            # Disable/enable buttons while api_assyst_running
            self.add_btn['state'] = tk.DISABLED
            self.remove_btn['state'] = tk.DISABLED
            self.update_btn['state'] = tk.DISABLED
            self.run_btn['state'] = tk.DISABLED
            self.stop_btn['state'] = tk.NORMAL

            self.users = {}
            for entry in db.fetch():
                self.users[entry[1]] = 0
            self.users['Unassigned'] = 0

            self.tickets = []
            if self.check_one_bool.get():
                self.tickets.append('P1 - 4HR')
            if self.check_two_bool.get():
                self.tickets.append('P2 - 8HR')
            if self.check_three_bool.get():
                self.tickets.append('P3 - 16HR')
            if self.check_four_bool.get():
                self.tickets.append('SR2 - 4 DAYS')
            if self.check_five_bool.get():
                self.tickets.append('SR3 - 10 DAYS')
            if self.check_six_bool.get():
                self.tickets.append('WORK REQUEST')            

            self.assyst_thread = threading.Thread(target=self.assyst_run)
            self.assyst_thread.start()
            self.api_assyst_running = True
            self.create_log(message='{} Starting.'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def stop_run(self):

        # Disable/enable buttons while stoping/stopped
        self.add_btn['state'] = tk.NORMAL
        self.remove_btn['state'] = tk.NORMAL
        self.update_btn['state'] = tk.NORMAL
        self.run_btn['state'] = tk.NORMAL
        self.stop_btn['state'] = tk.DISABLED
        self.create_log(message='{} Stopping.'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.api_assyst_running = False
        self.stopping_api_assyst_thread = threading.Thread(target=self.stopping_assyst_run)
        self.stopping_api_assyst_thread.start()
        
    def assyst_run(self):
        self.log_list.insert(tk.END, '{} Successfully started.'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        while self.api_assyst_running:

            # Create fake API with tickets and people they're assigned to in JSON or w.e

            # 1) Fetch all the team tickets
            # 2) Sort how many tickets are assigned to who and their totals. Update ticket count locally in dict..
            # 3) If there are unassigned tickets that meet catagory of P1 etc add to dictionary then move on to next step.
            # 4) Sort who is compatible to receive a ticket. If nobody, then leave a log in system.
            # 5) If someone available to take ticket, then assign one then update dict and list.
            # 6) iterate over list until nobody can take more or list is empty.
            # 7) clear list and dictionary and sleep function.            


            assyst_connector = assyst.AssystREST(users=self.users, 
                                            tickets=self.tickets, 
                                            username='username', 
                                            password='password', 
                                            url='https://blahblah.com'
                                            )
            ticket_data = assyst_connector.get_tickets()

            print(ticket_data['tickets'])

            for i in ticket_data['tickets']:
                if ticket_data['tickets'][i]['ASSIGNEDUSER'] in self.users:
                    self.users[ticket_data['tickets'][i]['ASSIGNEDUSER']] += 1
                if ticket_data['tickets'][i]['ASSIGNEDUSER'] == '':
                    self.users['Unassigned'] += 1
            
            print(self.users)


            
            for i in range(1, 11):
                print(i)
                time.sleep(1)
            for t in threading.enumerate():
                if t.name == "MainThread":
                    if t.is_alive() == False:
                        self.api_assyst_running = False
            time.sleep(10)
            print('Successfully stopped thread for assyst_run') 
        
    def stopping_assyst_run(self):
        self.stopping_api_assyst_running = True
        while self.assyst_thread.is_alive():
            print('assyst_run thread is still alive. Checking again in 3 seconds')
            time.sleep(3)
            continue
        print('assyst_run thread has been closed. Finalizing stop of stopping_assyst_run thread.')
        self.stopping_api_assyst_running = False
        self.create_log(message='{} Successfully stopped'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))    
        
    # Log generator
    def create_log(self, message):
        self.log_list.insert(tk.END, message)
        self.log_list.yview(tk.END)
    



#### MUST CHANGE self.api_assyst_running to FALSE in the event that X button is pressed.

### Change stopping_assyst_run to check if threat.is_alive() and not rely on a time.sleep()

root = tix.Tk()
app = Application(master=root)
app.mainloop()




