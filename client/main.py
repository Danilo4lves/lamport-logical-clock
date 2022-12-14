import socket

from command import Command


def client(host='localhost', port=8082):
    clock_timestamp = 0

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server
    server_address = (host, port)

    print("Connecting to %s port %s" % server_address)
    sock.connect(server_address)

    clock_timestamp += 1

    command = Command(sock)
    command.ask_for_rg(clock_timestamp)

    while True:
        clock_timestamp += 1

        print("1. Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")

        cmd_type = input()

        # sock.sendall("teste".encode("UTF-8"))

        match int(cmd_type):
            case 1:
                server_timestamp = command.balance(clock_timestamp)
                clock_timestamp = max(clock_timestamp, server_timestamp)
            case 2:
                server_timestamp = command.deposit(clock_timestamp)
                clock_timestamp = max(clock_timestamp, server_timestamp)
            case 3:
                server_timestamp = command.withdraw(clock_timestamp)
                clock_timestamp = max(clock_timestamp, server_timestamp)
            case 4:
                server_timestamp = command.transfer_to(clock_timestamp)
                clock_timestamp = max(clock_timestamp, server_timestamp)


        print("Client timestamp: {}".format(clock_timestamp))




client()
