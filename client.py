#start code for multiuser chating system
#client request
#by Zhenrui

import grpc
import chat_pb2
import chat_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:8080')
    stub = chat_pb2_grpc.ConnectionServiceStub(channel)

    response = stub.Connect(chat_pb2.ConnectRequest())
    print(response.message)

    response = stub.Disconnect(chat_pb2.DisconnectRequest())
    print(response.message)

if __name__ == '__main__':
    run()