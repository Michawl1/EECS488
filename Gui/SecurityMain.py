"""
Author: Michael Thompson
Date: 4/23/2020
About: This is the main file for the security system gui
"""
import tkinter as tk
import tkinter.ttk as ttk
import Gui.Resources.constants as constants
import Gui.TCPDataSender.CommandSender as CommandSender
import Gui.Frames.connect as connect


class SecuritySystemGui:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title(constants.APPLICATION_STRING)
        self._root.grid_rowconfigure(0, weight=1)
        self._root.grid_columnconfigure(0, weight=1)
        self._root.protocol("WM_DELETE_WINDOW",
                            lambda: self._exit())
        self._root.minsize(500, 500)
        self._root.resizable(2560, 1440)

        self._command_sender = CommandSender.CommandSender()

        self._control_frame()
        self._display_frame()

    def _exit(self):
        self._root.destroy()

    def _control_frame(self):
        """
        Set up the side window that will have all the buttons to control the logic analyzer
        """
        control_frame = ttk.Frame(self._root)
        control_frame.pack(expand=False,
                           fill='both',
                           side='left',
                           anchor='nw',
                           padx=2,
                           pady=2)
        self._connect = connect.Connect(control_frame, 0, 0, self._command_sender)

    def _display_frame(self):
        """
        Set up a tabbed display window to show data
        """
        display_frame = ttk.Frame(self._root)
        display_frame.pack(expand=True,
                           fill='both',
                           side='right',
                           padx=2,
                           pady=2)

    def start(self):
        """
        Starts the gui main event loop
        :return:
        """
        self._root.mainloop()


if __name__ == '__main__':
    gui = SecuritySystemGui()
    gui.start()
