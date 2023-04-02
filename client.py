# Multiuser chating system client
# Client can input account information
# by Zhenrui

# import library
import grpc
import chat_pb2
import chat_pb2_grpc

from concurrent import futures
import threading

def start_chat(username, stub):
    print(f"Welcome, {username}")
    
    while True:
        message = input("Enter your message (type 'exit' to disconnect): ")
        
        if message == "exit":
            stub.ClientDisconnected(chat_pb2.ClientDisconnectedRequest())
            break

        response = stub.SendMessage(chat_pb2.SendMessageRequest(username=username, message=message))
        #print(response.message)


def SendMessage(self, request, context):
        username = self.get_username_by_peer(context.peer())
        if username:
            message = f"{username}: {request.message}"
            print(message)
            return chat_pb2.SendMessageResponse(message="Message received")
        else:
            return chat_pb2.SendMessageResponse(message="You are not logged in")

# client start
def run():
    # connect channel 8080
    channel=grpc.insecure_channel('localhost:8080')
    stub=chat_pb2_grpc.ConnectionServiceStub(channel)

    # client active
    while True:
        # client instruction
        choice=input("Press 1 to create an account, 2 to log in, or q to exit: ")
        # create user account
        if choice == "1":
            username=input("Enter username: ")
            password=input("Enter password: ")
            # server response
            response=stub.CreateAccount(chat_pb2.CreateAccountRequest(username=username, password=password))
            print(response.message)
        # log in account
        elif choice == "2":
            username=input("Enter username: ")
            password=input("Enter password: ")
            # server response
            response=stub.Login(chat_pb2.LoginRequest(username=username, password=password))
            print(response.message)

            if response.message == "Logged in":
                start_chat(username, stub)

        # client disconnect
        elif choice == "q":
            # trigger print database content
            stub.ClientDisconnected(chat_pb2.ClientDisconnectedRequest())
            break
        # undefined input
        else:
            print("Invalid input")

if __name__ == '__main__':
    run()