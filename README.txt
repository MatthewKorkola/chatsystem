Version: 2023/3/26

Server can store user information in a database by using database class

To run this code:
1. Compile proto file by
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto

2. Run server and client in two terminals by
python server.py
python client.py

Generally, user follow "Press 1 to create an account, 2 to log in, or q to exit: " instruction to invoke different operations, and once client disconnect by pressing q, server side report all the content in database.