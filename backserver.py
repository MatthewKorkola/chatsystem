import grpc
from concurrent import futures
import time

import backup_pb2
import backup_pb2_grpc
from backup_database import BackupDatabase

class BackupService(backup_pb2_grpc.BackupServiceServicer):
    def __init__(self):
        self.db = BackupDatabase()

    def StoreMessage(self, request, context):
        self.db.store_message(request.username, request.message)
        return backup_pb2.StoreMessageResponse(message="Message stored")

    def GetAllMessages(self, request, context):
        all_messages = self.db.get_all_messages()
        user_messages = []

        current_username = None
        current_messages = []

        for username, message in all_messages:
            if username != current_username:
                if current_username is not None:
                    user_messages.append(backup_pb2.UserMessages(username=current_username, messages=current_messages))
                current_username = username
                current_messages = []

            current_messages.append(message)

        if current_username is not None:
            user_messages.append(backup_pb2.UserMessages(username=current_username, messages=current_messages))

        return backup_pb2.GetAllMessagesResponse(user_messages=user_messages)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    backup_pb2_grpc.add_BackupServiceServicer_to_server(BackupService(), server)
    server.add_insecure_port('[::]:8081')
    server.start()
    print("Backup server listening on port 8081")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()