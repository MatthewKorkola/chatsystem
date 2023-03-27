# Multiuser chating system client
# Client can input account information
# by Zhenrui

# import library
import grpc
import chat_pb2
import chat_pb2_grpc

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