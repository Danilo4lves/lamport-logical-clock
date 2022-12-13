import socket
import json
import sys
from math import ceil

from checking_account import CheckingAccount
from database import Database

sys.path.append("..")

from shared.message import Message
from shared.message_type import MessageType


print("path", __name__)

def server(host='localhost', port=8082):
    clock_timestamp = 0
    data_payload = 4096  # The maximum amount of data to be received at once
    database = Database.instance()

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
    client, address = sock.accept()

    while True:
        print("Waiting to receive message from client")

        raw_data = client.recv(data_payload)
        message = Message.from_json(raw_data)

        if message:
            received_timestamp = message.timestamp

            clock_timestamp = max(clock_timestamp, received_timestamp) + 1

            print("Server timestamp: {}".format(clock_timestamp))

            rg = message.content['rg']

            match message.topic:
                case MessageType.LOGIN:
                    client_name = message.content['client_name']
                    checking_account = CheckingAccount.login(database, rg)

                    if (checking_account is None):
                        checking_account = CheckingAccount(database, rg, client_name)

                    msg = "Hello, {}!".format(checking_account.client_name).encode("UTF-8");
                    client.send(msg)
                case MessageType.DEPOSIT:
                    checking_account = CheckingAccount.login(database, rg)
                    amount_in_cents = ceil(int(message.content['amount']) * 100)

                    if (checking_account is None):
                        break

                    try:
                        checking_account.deposit(amount_in_cents)
                        msg = "Deposited successfully".encode("UTF-8");
                        client.send(msg)
                    except Exception as err:
                        client.send(str(err).encode("UTF-8"))

                case MessageType.WITHDRAW:
                    checking_account = CheckingAccount.login(database, rg)
                    amount_in_cents = ceil(message.content['amount'] * 100)

                    if (checking_account is None):
                        break

                    checking_account.withdraw(amount_in_cents)

                    msg = "Withdrawn successfully".encode("UTF-8");
                    client.send(msg)
                case MessageType.BALANCE:
                    checking_account = CheckingAccount.login(database, rg)

                    if (checking_account is None):
                        break

                    amount = int(checking_account.balance()) / 100

                    msg = "Balance: {}".format(str(amount)).encode("UTF-8");
                    client.send(msg)
                case MessageType.TRANSFER:
                    checking_account = CheckingAccount.login(database, rg)

                    if (checking_account is None):
                        break

                    destination_rg = message.content['destination_rg']
                    amount_in_cents = ceil(message.content['amount'] * 100)

                    checking_account.transfer_to(destination_rg, amount_in_cents)


    # end connection
    client.close()


server()
