#start code for multiuser chating system
#User connect and disconnect
#by Zhenrui

import grpc
from concurrent import futures
import time

import chat_pb2
import chat_pb2_grpc

class ConnectionService(chat_pb2_grpc.ConnectionServiceServicer):
    def Connect(self, request, context):
        return chat_pb2.ConnectResponse(message="Client connected")

    def Disconnect(self, request, context):
        return chat_pb2.DisconnectResponse(message="Client disconnected")

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

if __name__ == '__main__':
    serve()