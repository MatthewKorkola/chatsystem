Version: 2023/4/1

Server can store user information in a database by using database class

To run this code:
1. Compile proto file by
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. backup.proto

2. Run server and client in three terminals by
python server.py
python backserver.py
python client.py

When client disconnect with server, promary server can print all the messages store in database.