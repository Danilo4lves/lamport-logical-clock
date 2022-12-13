import sys

sys.path.append("..")

from shared.message import Message
from shared.message_type import MessageType

class Command:
    def __init__(self, socket):
        self._socket = socket

    def __send_message(self, message):
        self._socket.sendall(message.to_json())

    def __receive_message(self):
        data = self._socket.recv(4096).decode("UTF-8")

        print(data)

    def ask_for_rg(self, timestamp):
        print("Please, inform your RG:")

        rg = input()

        self._rg = rg

        print("Please, inform your name:")

        client_name = input()

        message = Message(timestamp, MessageType.LOGIN, { "rg": rg, "client_name": client_name })

        self.__send_message(message)
        self.__receive_message()
        
    def balance(self, timestamp):
        message = Message(timestamp, MessageType.BALANCE, { "rg": self._rg })

        self.__send_message(message)
        self.__receive_message()

    def deposit(self, timestamp):
        print("Type how much you want to deposit:")

        amount = input()

        message = Message(timestamp, MessageType.DEPOSIT, { "rg": self._rg, "amount": amount })

        self.__send_message(message)
        self.__receive_message()
