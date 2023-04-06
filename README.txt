Version: 2023/4/6

Server can store user information in a database by using database class

To run this code:
1. Compile proto file by:
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. backup.proto

2. Run server and backup server in two terminals by:
python server.py
python backup_server.py

3. Run multi clients open mulit terminals run on each one:
python client.py

It is better to separate the backup server from primary one, and the broadcasting function is well.