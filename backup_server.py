# Multiuser chating system backup server
# Backup Server can read messages from primary server and store them in backup database
# by Zhenrui Zhang

import grpc
from concurrent import futures
import time

import backup_pb2
import backup_pb2_grpc
from backup_database import BackupDatabase

class BackupService(backup_pb2_grpc.BackupServiceServicer):
    def __init__(self):
        self.backup_db = BackupDatabase()

    # send all received messges to backup database
    def StoreMessageHistory(self, request, context):
        self.backup_db.store_message(request.username, request.message)
        return backup_pb2.StoreMessageHistoryResponse(status="Stored")
    
    # get all messages history stored in bakup database
    def GetAllMessageHistory(self, request, context):
        message_history = self.backup_db.get_all_message_history()
        messages = [
            backup_pb2.Message(username=record[0], content=record[1])
            for record in message_history
        ]
        return backup_pb2.GetAllMessageHistoryResponse(message_history=messages)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    backup_pb2_grpc.add_BackupServiceServicer_to_server(BackupService(), server)
    server.add_insecure_port('[::]:8081')
    server.start()
    print("Backup Server listening on port 8081")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()