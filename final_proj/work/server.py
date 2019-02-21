

# imports
import socket
import select
from seperate_to_words import separates_to_words


class Server:
    """
        this class has 2 parameters - ip and port
        which define the socket. in this class we have a constructor,
        we have functions on the socket and handling the client's request
    """
    def __init__(self, ip, port):
        """
        constructor
        :param ip:
        :param port:
        """
        self.ip = ip
        self.port = port

    def bind(self, a_server_socket):
        """
        building the connection with the socket
        :param a_server_socket:
        """
        a_server_socket.bind((self.ip, self.port))

    @staticmethod
    def listen(a_server_socket, num):
        """
        listens to the client's request
        :param a_server_socket:
        :param num:
        """
        a_server_socket.listen(num)

    @staticmethod
    def accept(a_server_socket):
        """
        accept the request of the client
        :param a_server_socket:
        """
        return a_server_socket.accept()

    @staticmethod
    def send(client1_socket, message):
        """
        send a message to the client
        :param client1_socket:
        :param message:
        """
        client1_socket.send(message)

    @staticmethod
    def receive(client_socket, data):
        """
        receive data from the client
        :param client_socket:
        :param data:
        :return:
        """
        return client_socket.recv(data)


def send_waiting_messages(w_list, messages_to_send):
    """
    sends numbers start option and end option to each thread
    :param w_list:
    :param messages_to_send:
    :return:
    """
    for msg in messages_to_send:
        client_socket, num = msg
        if client_socket in w_list:
            client_socket.send(str(num).encode())
            messages_to_send.remove(msg)


def main():
    """
    the main, here we can see the object of Server
    and the calls to the functions
    """
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # create an object
    my_server = Server('192.168.1.25', 1212)
    my_server.bind(server_socket)
    my_server.listen(server_socket, 0)
    open_client_sockets = []
    messages_to_send = []
    byte_arr = []
    flag = True
    i = 0
    while flag:
        r_list, w_list, x_list = select.select([server_socket] +
                                               open_client_sockets,
                                               open_client_sockets, [])
        for current_socket in r_list:
            if current_socket is server_socket:
                new_socket, address = server_socket.accept()
                open_client_sockets.append(new_socket)
            else:
                data = my_server.receive(current_socket, 4096)
                byte_arr.append(data)
                messages_to_send.append((current_socket, 1))
                if str(data) == "b''":
                    f = open('my_record1', 'wb')
                    while i < byte_arr.__len__():
                        f.write(byte_arr[i])
                        print(byte_arr[i], i)
                        i += 1
                    f.close()
                    open_client_sockets.remove(current_socket)
                    print("Connection with client closed")
                    separates_to_words()
                    break
    server_socket.close()


if __name__ == '__main__':
    main()
