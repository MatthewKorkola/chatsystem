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
        return chat_pb2.ClientDisconnectedResponse()

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
