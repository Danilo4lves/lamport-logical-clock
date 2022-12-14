import socket
import json
import sys
import threading
from math import ceil
from threading import Thread

from checking_account import CheckingAccount
from database import Database

sys.path.append("..")

from shared.message import Message
from shared.message_type import MessageType


print("path", __name__)

# Create db and clock as global, because have to be access between threads
clock_timestamp = 0
database = Database.instance()

# Function to run in Thread to wait for client requests
def on_new_client(client, address, data_payload):
    # define database and clock as global
    global clock_timestamp
    global database

    while True:
        print("Waiting to receive message from client")

        # Wait for new request, because is inside thread its dont block the main thread
        raw_data = client.recv(data_payload)

        # use Message class to parse received json
        message = Message.from_json(raw_data)

        if message:
            # gets message timestamp
            received_timestamp = message.timestamp

            # define clock_timestamp as the max betwenn server clock and received clock
            clock_timestamp = max(clock_timestamp, received_timestamp) + 1

            # print in terminal the actual timestamp
            print("Server timestamp: {}".format(clock_timestamp))

            # gets rg from json
            rg = message.content['rg']

            # switch case to define which type the message received is
            match message.topic:
                case MessageType.LOGIN:
                    # Login procedure
                    client_name = message.content['client_name']
                    checking_account = CheckingAccount.login(database, rg)

                    if (checking_account is None):
                        checking_account = CheckingAccount(database, rg, client_name)

                    msg = Message(clock_timestamp, MessageType.RESPONSE, {"msg": "Hello, {}!".format(checking_account.client_name) })

                    client.send(msg.to_json())
                case MessageType.DEPOSIT:
                    # getting existing account from database
                    checking_account = CheckingAccount.login(database, rg)

                    # Amount received in cents
                    amount_in_cents = ceil(int(message.content['amount']) * 100)

                    if (checking_account is None):
                        break

                    try:
                        # Call checking account to deposit amount
                        checking_account.deposit(amount_in_cents)

                        # Building deposit succesfully message
                        msg = Message(clock_timestamp, MessageType.RESPONSE, { "msg": "Deposited successfully" })
                        client.send(msg.to_json())
                    except Exception as err:
                        msg = Message(clock_timestamp, MessageType.RESPONSE, { "msg": str(err) })
                        client.send(msg.to_json())

                case MessageType.WITHDRAW:
                    checking_account = CheckingAccount.login(database, rg)

                    # Amount to withdrawl in cents
                    amount_in_cents = ceil(int(message.content['amount']) * 100)

                    if (checking_account is None):
                        break

                    try:
                        # Processing withdraw
                        checking_account.withdraw(amount_in_cents)

                        # Build withdraw succesfully message
                        msg = Message(clock_timestamp, MessageType.RESPONSE, { "msg": "Withdrawn successfully" })
                        client.send(msg.to_json())
                    except Exception as err:
                        #Throwing message error if occur
                        msg = Message(clock_timestamp, MessageType.RESPONSE, { "msg": str(err) })
                        client.send(msg.to_json())
                case MessageType.BALANCE:
                    checking_account = CheckingAccount.login(database, rg)

                    if (checking_account is None):
                        break

                    # calculate balance in cents
                    amount = int(checking_account.balance()) / 100

                    # Building return message
                    msg = Message(clock_timestamp, MessageType.RESPONSE, { "msg": "Balance: {}".format(str(amount)) })
                    client.send(msg.to_json())
                case MessageType.TRANSFER:
                    checking_account = CheckingAccount.login(database, rg)

                    if (checking_account is None):
                        break

                    # getting rg destination of transfer
                    destination_rg = message.content['destination_rg']
                    amount_in_cents = ceil(int(message.content['amount']) * 100)

                    try:
                        # Processing transfer
                        checking_account.transfer_to(destination_rg, amount_in_cents)
                        msg = Message(clock_timestamp, MessageType.RESPONSE, { "msg": "The transfer was finished succesfully" })
                        client.send(msg.to_json())
                    except Exception as err:
                        msg = Message(clock_timestamp, MessageType.RESPONSE, { "msg": str(err)})
                        client.send(msg.to_json())



    # end connection
    client.close()


def server(host='localhost', port=8082):
    data_payload = 4096  # The maximum amount of data to be received at once
    #database = Database.instance()

    # Create a TCP socket
    sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)

    # Enable reuse address/port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = (host, port)

    print("Starting up echo server  on %s port %s" % server_address)
    sock.bind(server_address)

    # Listen to clients, argument specifies the max no. of queued connections
    sock.listen(5)
    

    while True:
        client, address = sock.accept()
        Thread(target=on_new_client, args=(client, address, data_payload)).start()

    


server()
