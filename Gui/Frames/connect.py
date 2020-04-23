"""
Author: Michael Thompson
Date: 4/23/2020
About: This is the connection frame for the gui
"""

import Gui.Resources.packetmessages as packetmessages
import Gui.Resources.constants as constants
import tkinter
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk

class Connect(object):
    def __init__(self,
                 parent,
                 row,
                 column,
                 command_sender):
        self._parent = parent
        self._row = row
        self._column = column
        self._command_sender = command_sender

        self._frame = ttk.LabelFrame(self._parent)
        self._frame.configure(text='Connect')
        self._frame.grid(row=self._row,
                         column=self._column,
                         sticky='we',
                         padx=2,
                         pady=2,
                         ipadx=5,
                         ipady=5)
        self._button = tkinter.Button(self._frame, text="Connect", command=self._connect)
        self._button.grid(row=0, column=0, sticky='we', padx=2, pady=2)

        self._ip_input()

        self._update()

    def _connect(self):
        """
        This opens the connection to the security system
        """
        return

    def _update(self):
        if self._command_sender.get_connect_flag():
            self.disable()
        else:
            self.enable()

    def _ip_input(self):
        ip_label = ttk.Label(self._frame)
        ip_label.configure(text = "IP Address:")
        ip_label.grid(row=1, column=0, sticky='we', padx=2, pady=2)

        self._ip_box = ttk.Entry(self._frame)
        self._ip_box.grid(row=1, column=1, sticky='we',
                                     padx=2, pady=2)

    def disable(self):
        """
        Disables the connect button
        """
        self._button.configure(text='Disconnect')

    def enable(self):
        """
        Enables the connect button
        """
        self._button.configure(text="Connect")
