This is a start code for multiuser chating system project

Only provide client connect and dis connect so far

To run this code:
First, do "python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto" to compile proto file

Then, do "python server.py" and "python client.py" in two terminals