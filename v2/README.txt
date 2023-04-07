Version: 2023/4/2

Server can store user information in a database by using database class

To run this code:
1. Compile proto file by:
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto

2. Run server and client in two terminals by:
python server.py
python client.py

Now thebackup server is build in the primary server. When client disconnect with server, primary server can print all the messages store in database.