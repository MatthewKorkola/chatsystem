# Multiuser chatting system server
# Server can read input from client and create a database to store user information
# Also can connect to backup server for storing message history
# by Zhenrui Zhang, Matthew Korkola, Irmene-Valerie Leonard

import grpc
from concurrent import futures
import time
import queue
import threading

import chat_pb2
import chat_pb2_grpc
from database import Database

import backup_pb2
import backup_pb2_grpc

# ConnectionService class that defines the server functionality
class ConnectionService(chat_pb2_grpc.ConnectionServiceServicer):
    def __init__(self):
        self.db = Database()
        self.clients_lock = threading.Lock()
        self.users_mood = []
        self.usersConnected = []
        # connected client list
        self.clients = {}
        # connect to a backup server
        self.connect_backup_server()
    
    # connect with backup server
    def connect_backup_server(self):
        channel = grpc.insecure_channel('localhost:8081')
        self.backup_stub = backup_pb2_grpc.BackupServiceStub(channel)

    # if there is a client connect add it
    def add_client(self, username, context):
        with self.clients_lock:
            self.clients[username] = context

    # if one client leave, just remove it
    def remove_client(self, username):
        with self.clients_lock:
            if username in self.clients:
                del self.clients[username]

    # broadcasting function
    def broadcast(self, sender_username, message):
        with self.clients_lock:
            for username, context in self.clients.items():
                # broadcast the messages to all other clients
                if username != sender_username:
                    context.send_message_queue.put((sender_username, message))
        self.backup_stub.StoreMessageHistory(backup_pb2.StoreMessageHistoryRequest(username=sender_username, message=message))

    # Create an account for a new user
    def CreateAccount(self, request, context):
        success = self.db.add_user(request.username, request.password)
        if success:
            return chat_pb2.CreateAccountResponse(message="Account created")
        else:
            return chat_pb2.CreateAccountResponse(message="Username already exists")

    # Login a user if their credentials are correct
    def Login(self, request, context):
        success = self.db.check_password(request.username, request.password)
        if success:
            self.usersConnected.append(request.username)
            return chat_pb2.LoginResponse(message="Logged in")
        else:
            return chat_pb2.LoginResponse(message="Invalid username or password")

    # Handle the disconnection of a client
    def ClientDisconnected(self, request, context):
        self.usersConnected.remove(request.username)
        users = self.db.show_db()
        print("Client disconnected. Users in the database:")
        # print out all clients account information
        for user in users:
            print(f"{user[0]}: {user[2]}")
        # print all message history
        self.print_message_history()
        return chat_pb2.ClientDisconnectedResponse(message="Message received")

    def SendMessage(self, request, context):
        print("receiving message")
        self.broadcast(request.username, request.message)
        return chat_pb2.SendMessageResponse(message="Message received")

    # Handle broadcasting the message to the clients
    def BroadcastMessage(self, request, context):
        username = request.username
        context.send_message_queue = queue.Queue()
        self.add_client(username, context)

        try:
            while True:
                sender_username, message = context.send_message_queue.get()
                if username != sender_username:
                    yield chat_pb2.BroadcastMessageResponse(sender_username=sender_username, message=message)
        except grpc.RpcError:
            self.remove_client(username)
    
    # helper function for print message history
    def print_message_history(self):
        # get all message history from backup server
        response = self.backup_stub.GetAllMessageHistory(backup_pb2.GetAllMessageHistoryRequest())
        print("Message History:")
        for message in response.message_history:
            print(f"{message.username}: {message.content}")

    def getUsers(self, request, context):
        with self.clients_lock:
            users_list = self.usersConnected
            return chat_pb2.UserList(users=users_list)


# Server setup and start
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionService(), server)
    server.add_insecure_port('[::]:8080')
    server.start()
    print("Server listening on port 8080")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

# Run the server
if __name__ == '__main__':
    serve()