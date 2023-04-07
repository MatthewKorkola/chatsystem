# Multiuser chatting system server
# Server can read input from client and create a database to store user information
# Also can connect to backup server for storing message history
# by Zhenrui, Matthew Korkola, Irmene-Valerie Leonard

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import scrolledtext

import grpc
import chat_pb2
import chat_pb2_grpc
import threading  # New import
from concurrent import futures



# Function to log user to the chat server
def loginUser(stub, userString, passwordString, window):

    # Get the user username
    username = userString.get()

    # Get the user password
    password = passwordString.get()
    
    # Get the server response
    response = stub.Login(chat_pb2.LoginRequest(username=username, password=password))

    # If the user was successful logged into the server 
    if response.message =="Logged in":
    
        # Greet the user
        messagebox.showinfo("Greeting", f"Hello {username}, Welcome to the chat")
        
        window.destroy()

        # Start the chat
        chatUser = chatClient(username,password,stub)

        


# ChatClient class that offer the chat services to clients
class chatClient:

    def __init__(self, username, password, stub):
        
        self.stub = stub

        self.username = username

        self.password= password

        root = Tk()

        root.withdraw()

        self.guide_done = False

        self.running = True

        # Thread for the GUI
        guiThread = threading.Thread(target=self.gui_mainpage)

        # Thread for incoming messages
        guiMessage = threading.Thread(target=self.receive_messages_thread)

        # Start both threads
        guiThread.start()

        guiMessage.start()

        
    # Function to receive incomping messages
    def receive_messages_thread(self):
        for response in self.stub.BroadcastMessage(chat_pb2.BroadcastMessageRequest(username=self.username)):
            print(f"{response.sender_username}: {response.message}")

            # Create the message text to display on the chat text area
            client_msg = f"{response.sender_username} : {response.message}\n"
            if self.guide_done:
                self.msg_area.config(state='normal')
                self.msg_area.insert('end',client_msg)
                self.msg_area.yview('end')
                self.msg_area.config(state='disabled')

    # Function to send messages to the chat
    def sendMessageToChat(self):
       
       # Get the user input
        user_input = self.input_msg.get(1.0, "end-1c")
       
        # If the user input is not an empty text send it to the chat server
        if user_input != "":

            # If the user want to ext
            if user_input == "exit":
                self.stub.ClientDisconnected(chat_pb2.ClientDisconnectedRequest())
                self.running = False
                
                # Inform the user the chat was closed
                messagebox.showinfo("Greeting", f"Bye {self.username}")
                self.frame.destroy()
            
            #else
            # Send the message to the chat
            response = self.stub.SendMessage(chat_pb2.SendMessageRequest(username=self.username, message=user_input))

            # Show the message to the client text area
            client_msg = f"{self.username} : {user_input}\n"
            if self.guide_done:
                self.msg_area.config(state='normal')
                self.msg_area.insert('end',client_msg)
                self.msg_area.yview('end')
                self.msg_area.config(state='disabled')
            self.input_msg.delete(1.0,"end-1c")

        

    # Is not used anymore, will remove in the next version
    def login(self, username, passowrd):
        if username!="" and passowrd!="":
            response = self.stub.CreateAccount(chat_pb2.CreateAccountRequest(username=username, password=password))
        print(response.message)
        if response.message == "Logged in":
            self.username = username
            self.password = password
            self.status = "connected"
        return self.status
        
    # Is not implemented yet, will be done in the next version
    def createAccount(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        response = self.stub.Login(chat_pb2.LoginRequest(username=username, password=password))
        print(response.message)
        if response.message == "Account created":
            self.username = username
            self.password = password

    # Create the main chat page
    def gui_mainpage(self):

        # Create the frame
        self.frame = Tk()
        self.frame.title("Chat Client")
        self.frame.config(bg="lightgray")

        # Create the text at the top of the chat area
        self.chat_label = Label(self.frame,text=f"Chat User: {self.username}", bg="lightgray")
        self.chat_label.config(font=("Arial",14,'bold'))
        self.chat_label.pack(padx=20,pady=5)


        # Create the chat area
        self.msg_area = scrolledtext.ScrolledText(self.frame, bg='lightyellow')
        self.msg_area.pack(padx=20, pady=5)
        self.msg_area.config(state="disabled")

        # Create the area for the user to enter message to send to the chat
        self.msg_label = Label(self.frame, text="Message", bg="lightgray")
        self.chat_label.config(font=("Arial",12))
        self.chat_label.pack(padx=20,pady=5)

        self.input_msg = Text(self.frame, height=3)
        self.input_msg.pack(padx=20,pady=5)

        # Create the send button to send messages to the chat
        self.send_button = Button(self.frame, text="send", bg='gray', command= self.sendMessageToChat)
        self.send_button.config(font=("Arial",12))
        self.send_button.pack(padx=20,pady=5)


        self.guide_done = True

        self.frame.mainloop()

# Main function
if __name__ == '__main__':

    # Create the grpc channel and stub for the client
    channel = grpc.insecure_channel('localhost:8080')
        
    stub = chat_pb2_grpc.ConnectionServiceStub(channel)

    # Create the frame for getting the user choice
    root = Tk()  
    root.withdraw()

    # Get the user choice
    while True:
        choice = simpledialog.askstring("Choice", "Press:\n\n *1 to create an account\n\n *2 to log in\n\n  *q to exit\n\n",parent=root)
        # Not yet implemented, will be done in the next version
        if choice == "1":
            print("choice 1")
        # If the user chose to connect to the chat
        elif choice == "2":
                
                # Destroy the current fram and display the login frame
                root.destroy()
                login_screen=Tk()
                login_screen.title("Login")
                login_screen.geometry("350x250")

                Label(login_screen, text="Please enter your credentials", font='Helvetica 12 bold').grid(row=0,column=1)
               
                Label(login_screen, text="").grid(row=1,column=0)

                Label(login_screen, text="Username").grid(row=2,column=0)

                username = tk.StringVar()
                
                username_login_entry = Entry(login_screen, textvariable=username).grid(row=2,column=1)
                
                Label(login_screen, text="").grid(row=3,column=0)

                Label(login_screen, text="Password").grid(row=4, column=0)


                password = StringVar()
                password__login_entry = Entry(login_screen, textvariable=password, show= '*').grid(row=4,column=1)

                Label(login_screen, text="").grid(row=5,column=0)
                
                button =  Button(login_screen, text ="Login", width=10, height=1, command=lambda: loginUser(stub, username, password,login_screen)).grid(row=6,column=1)
                login_screen.mainloop()
                
    
    
    
    

    
