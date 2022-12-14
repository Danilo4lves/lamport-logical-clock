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
        raw_response = self._socket.recv(4096).decode("UTF-8")

        response = Message.from_json(raw_response)

        server_timestamp = response.timestamp
        msg = response.content['msg']

        return Message(server_timestamp, MessageType.RESPONSE, msg)

    def ask_for_rg(self, timestamp):
        print("Please, inform your RG:")

        rg = input()

        self._rg = rg

        print("Please, inform your name:")

        client_name = input()

        message = Message(timestamp, MessageType.LOGIN, { "rg": rg, "client_name": client_name })

        self.__send_message(message)
        response = self.__receive_message()

        msg = response.content
        server_timestamp = response.timestamp

        print(msg)

        return server_timestamp
        
    def balance(self, timestamp):
        message = Message(timestamp, MessageType.BALANCE, { "rg": self._rg })

        self.__send_message(message)
        response = self.__receive_message()

        msg = response.content
        server_timestamp = response.timestamp

        print(msg)

        return server_timestamp

    def deposit(self, timestamp):
        print("Type how much you want to deposit:")

        amount = input()

        message = Message(timestamp, MessageType.DEPOSIT, { "rg": self._rg, "amount": amount })

        self.__send_message(message)
        response = self.__receive_message()

        msg = response.content
        server_timestamp = response.timestamp

        print(msg)

        return server_timestamp

    def withdraw(self, timestamp):
        print("How much do you want to withdraw:")

        amount = input()

        message = Message(timestamp, MessageType.WITHDRAW, { "rg": self._rg, "amount": amount })

        self.__send_message(message)
        response = self.__receive_message()

        msg = response.content
        server_timestamp = response.timestamp

        print(msg)

        return server_timestamp

    def transfer_to(self, timestamp):
        print("Inform destination rg:")

        destination_rg = input()

        print("Inform amount to transfer:")

        amount = input()

        message = Message(timestamp, MessageType.TRANSFER, { "rg": self._rg, "destination_rg": destination_rg, "amount": amount})

        self.__send_message(message)
        response = self.__receive_message()

        msg = response.content
        server_timestamp = response.timestamp

        print(msg)

        return server_timestamp
