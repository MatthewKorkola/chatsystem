# Multiuser chating system client
# Client can input account information and send messages
# by Zhenrui

# import library
import grpc
import chat_pb2
import chat_pb2_grpc

def start_chat(username, stub):
    print(f"Welcome, {username}")
    while True:
        # message UI instruction
        message=input("Enter your message (type 'exit' to disconnect): ")
        if message=="exit":
            stub.ClientDisconnected(chat_pb2.ClientDisconnectedRequest())
            break
        response=stub.SendMessage(chat_pb2.SendMessageRequest(username=username, message=message))
        #print(response.message)

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