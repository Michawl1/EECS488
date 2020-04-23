"""
Author: Michael Thompson
Date: 4/23/2020
About: This is handles sending tcp packets to the security system
"""
import socket


class CommandSender:
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connect_flag = False

    def connect(self, _ip, _port):
        self._socket.connect(_ip, _port)
        self._connect_flag = True

    def close(self):
        self._socket.close()

    def send(self, _message):
        if self._connect_flag:
            self._socket.send(_message)
