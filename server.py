# Multiuser chating system server
# Server can read input from client
# Server create database to store user information
# by Zhenrui

# import library
import grpc
from concurrent import futures
import time

import chat_pb2
import chat_pb2_grpc

import backup_pb2
import backup_pb2_grpc
# import database class
from database import Database

class ConnectionService(chat_pb2_grpc.ConnectionServiceServicer):
    def __init__(self):
        # initialize database
        self.db=Database()

    def CreateAccount(self, request, context):
        # adduser status
        success=self.db.add_user(request.username, request.password)
        if success:
            # successfully create
            return chat_pb2.CreateAccountResponse(message="Account created")
        else:
            # username key already exist
            return chat_pb2.CreateAccountResponse(message="Username already exists")

    def Login(self, request, context):
        # login status
        success=self.db.check_password(request.username, request.password)
        if success:
            # successfully login
            return chat_pb2.LoginResponse(message="Logged in")
        else:
            # existed username, but password fail to match
            return chat_pb2.LoginResponse(message="Invalid username or password")

    def ClientDisconnected(self, request, context):
        # client disconnect, report dabase content on server side
        users=self.db.show_db()
        print("Client disconnected. Users in the database:")
        # print all existed accounts in database
        for user in users:
            print(f"{user[0]}: {user[1]}")

        backup_channel = grpc.insecure_channel('localhost:8081')
        backup_stub = backup_pb2_grpc.BackupServiceStub(backup_channel)
        backup_response = backup_stub.GetAllMessages(backup_pb2.GetAllMessagesRequest())

        # Print message history on the primary server
        print("\nMessage history in the backup server:")
        for user_messages in backup_response.user_messages:
            print(f"{user_messages.username}:")
            for message in user_messages.messages:
                print(f"    {message}")

        return chat_pb2.ClientDisconnectedResponse()

    def SendMessage(self, request, context):
        # Print the message on the primary server
        #print(f"{request.username}: {request.message}")

        # Send the message to the backup server
        backup_channel = grpc.insecure_channel('localhost:8081')
        backup_stub = backup_pb2_grpc.BackupServiceStub(backup_channel)
        backup_response = backup_stub.StoreMessage(backup_pb2.StoreMessageRequest(username=request.username, message=request.message))
        print(backup_response.message)
        return chat_pb2.SendMessageResponse(message="Message received")

    
    def broadcast_message(self, username, message):
        # Find the client's response stream
        client_peer = next((client_peer for client_username, client_peer in self.connected_clients if client_username == username), None)

        if client_peer:
            # Send the message using the client's response stream
            with grpc.insecure_channel(client_peer) as channel:
                stub = chat_pb2_grpc.ConnectionServiceStub(channel)
                stub.SendMessage(chat_pb2.SendMessageRequest(message=message))

# server start
def serve():
    server=grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionService(), server)
    #assume port number is 8080
    server.add_insecure_port('[::]:8080')
    server.start()
    print("Server listening on port 8080")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
