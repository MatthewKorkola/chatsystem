# Multiuser chating system client
# Client can input account information
# by Zhenrui, Matthew Korkola, Irmene-Valerie Leonard

# import library
import grpc
import chat_pb2
import chat_pb2_grpc
import threading
import os

# receive broadcasting message from primary server and print it out
def receive_messages_thread(stub, username):
    for response in stub.BroadcastMessage(chat_pb2.BroadcastMessageRequest(username=username)):
        print(f"{response.sender_username}: {response.message}")

def start_chat(username, stub):
    print(f"Welcome, {username}")
    print("Enter your message (type 'exit' to disconnect): ")
    threading.Thread(target=receive_messages_thread, args=(stub, username)).start()
    
    while True:
        #message = input("Enter your message (type 'exit' to disconnect): ")
        message = input("> ")

        if message == "exit":
            stub.ClientDisconnected(chat_pb2.ClientDisconnectedRequest(username = username))
            break

        response = stub.SendMessage(chat_pb2.SendMessageRequest(username=username, message=message))
        #print(response.message)

def run():
    channel = grpc.insecure_channel('localhost:8080')
    stub = chat_pb2_grpc.ConnectionServiceStub(channel)

    while True:
        choice = input("Press 1 to create an account, 2 to log in, or q to exit: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            response = stub.CreateAccount(chat_pb2.CreateAccountRequest(username=username, password=password))
            print(response.message)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            response = stub.Login(chat_pb2.LoginRequest(username=username, password=password))
            print(response.message)

            if response.message == "Logged in":
                start_chat(username, stub)
        elif choice == "q":
            print("##Exiting application##")
            os._exit(0)
        else:
            print("Invalid input")

if __name__ == '__main__':
    run()