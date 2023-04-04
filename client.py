# Multiuser chating system client
# Client can input account information and send messages
# by Zhenrui and Matthew Korkola

import grpc
import chat_pb2
import chat_pb2_grpc
import threading  # New import

def start_chat(username, stub):
    print(f"Welcome, {username}")

    def listen_for_broadcasts():  # New
        for message in stub.BroadcastMessage(chat_pb2.BroadcastMessageRequest()):
                print(f"{message.username}: {message.message}")

    threading.Thread(target=listen_for_broadcasts, daemon=True).start()  # New

    while True:
        message = input("Enter your message (type 'exit' to disconnect): ")
        if message == "exit":
            stub.ClientDisconnected(chat_pb2.ClientDisconnectedRequest(username=username))  # Changed
            break
        response = stub.SendMessage(chat_pb2.SendMessageRequest(username=username, message=message))

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
            stub.ClientDisconnected(chat_pb2.ClientDisconnectedRequest(username=""))  # Changed
            break
        else:
            print("Invalid input")

if __name__ == '__main__':
    run()
