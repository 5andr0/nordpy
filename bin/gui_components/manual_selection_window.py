from tkinter import *

from bin.conf_util import get_available_servers_dict
from bin.logging_util import get_logger
SERVERS_DICT = get_available_servers_dict()
logger = get_logger(__name__)

class ManualServerWindow(Tk):
    def __init__(self, parent):
        super(ManualServerWindow, self).__init__()
        self.wm_title("Select your server")
        self.parent = parent  # this will be needed when a server is chosen

        self.center_window(300, 190)
        self.__init_listboxes__()
        self.__init_buttons__()

    def __init_listboxes__(self):
        self.listboxes_frame = Frame(self)

        # this frame will contain all the stuff of the domain_listbox
        self.domain_listbox_frame = Frame(self.listboxes_frame)
        self.domain_listbox = Listbox(self.domain_listbox_frame, selectmode=SINGLE)
        self.domain_listbox_frame.scrollbar = Scrollbar(self.domain_listbox_frame, orient=VERTICAL)
        self.domain_listbox.config(yscrollcommand=self.domain_listbox_frame.scrollbar.set)
        self.domain_listbox_frame.scrollbar.config(command=self.domain_listbox.yview)
        self.domain_listbox_frame.scrollbar.pack(side=RIGHT, fill='y')

        # adding keys from SERVERS_DICT
        for item in sorted(SERVERS_DICT.keys()):
            self.domain_listbox.insert(END, item)
        self.domain_listbox.pack(side=RIGHT)
        self.domain_listbox.bind('<<ListboxSelect>>', self.on_domain_select)
        self.domain_listbox_frame.pack(side=LEFT)

        self.domain_servers_listbox_frame = Frame(self.listboxes_frame)
        self.domain_servers_listbox = Listbox(self.domain_servers_listbox_frame, selectmode=SINGLE)
        self.domain_servers_listbox_frame.scrollbar = Scrollbar(self.domain_servers_listbox_frame, orient=VERTICAL)
        self.domain_servers_listbox.config(yscrollcommand=self.domain_servers_listbox_frame.scrollbar.set)
        self.domain_servers_listbox_frame.scrollbar.config(command=self.domain_servers_listbox.yview)
        self.domain_servers_listbox_frame.scrollbar.pack(side=RIGHT, fill='y')
        self.domain_servers_listbox.pack(side=RIGHT)
        self.domain_servers_listbox_frame.pack(side=LEFT)

        self.listboxes_frame.pack()

    def __init_buttons__(self):
        self.buttons_frame = Frame(self)
        self.accept_button = Button(self.buttons_frame, text='OK', command=self.ok_pressed)
        self.accept_button.pack(side=LEFT)
        self.cancel_button = Button(self.buttons_frame, text='Cancel', command=self.cancel_pressed)
        self.cancel_button.pack(side=LEFT)
        self.buttons_frame.pack(pady=6)

    def on_domain_select(self, event):
        selected_item_tuple = self.domain_listbox.curselection()
        if len(selected_item_tuple) == 0:   # checking if it is a deselection
            return
        selected_index = selected_item_tuple[0]

        domain_selected = self.domain_listbox.get(selected_index)

        self.domain_servers_listbox.delete(0, END)

        for server in SERVERS_DICT[domain_selected]:
            self.domain_servers_listbox.insert(END, server)

    def ok_pressed(self):
        selected_item_tuple = self.domain_servers_listbox.curselection()
        if not len(selected_item_tuple) == 0:  # checking if something is selected
            selected_index = selected_item_tuple[0]
            server_selected = self.domain_servers_listbox.get(selected_index)

            self.parent.manual_server_selected(server_selected)

        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def center_window(self, width=300, height=200):
        # gets screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculates position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))