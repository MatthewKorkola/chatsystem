# Multiuser chatting system server
# Server can read input from client and create a database to store user information
# Also define a built-in backup server for storing message history
# by Zhenrui

import grpc
from concurrent import futures
import time

import chat_pb2
import chat_pb2_grpc

from database import Database
from backup_server import BackupServer

# ConnectionService class that defines the server functionality
class ConnectionService(chat_pb2_grpc.ConnectionServiceServicer):
    def __init__(self):
        self.db = Database()
        self.backup_server = BackupServer()
        self.connected_clients = {}  # New

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
            self.connected_clients[request.username] = context.peer()  # New
            return chat_pb2.LoginResponse(message="Logged in")
        else:
            return chat_pb2.LoginResponse(message="Invalid username or password")

    # Handle the disconnection of a client
    def ClientDisconnected(self, request, context):
        users = self.db.show_db()
        print("Client disconnected. Users in the database:")
        for user in users:
            print(f"{user[0]}: {user[1]}")

        messages = self.backup_server.get_messages()
        print("Backup server stored message history:")
        for message in messages:
            print(f"{message[1]}: {message[2]}")

        if request.username in self.connected_clients:  # New
            del self.connected_clients[request.username]

        return chat_pb2.ClientDisconnectedResponse()

    # Broadcast a message from the sender to all other clients
    def broadcast_message(self, sender_username, message):  # New method
        for username, channel in self.connected_clients.items():
            if username != sender_username:
                request = chat_pb2.BroadcastMessageRequest(username=sender_username, message=message)
                self.BroadcastMessage(request, None)

    # Send a message from a client
    def SendMessage(self, request, context):
        print(f"{request.username}: {request.message}")
        self.backup_server.store_message(request.username, request.message)
        self.broadcast_message(request.username, request.message)  # Call the new method
        return chat_pb2.SendMessageResponse(message="Message received")

    # Handle broadcasting the message to the clients
    def BroadcastMessage(self, request, context):  # Updated
        while True:
            new_messages = self.backup_server.get_new_messages()
            for message in new_messages:
                yield chat_pb2.BroadcastMessageResponse(username=message[0], message=message[1])


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
        raise SystemExit

# Run the server
if __name__ == '__main__':
    serve()
