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

import sched
import time
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

        users = stub.getUsers(chat_pb2.Empty())
    
        # Greet the user
        messagebox.showinfo("Greeting", f"Hello {username}, Welcome to the chat")
        
        window.destroy()

        # Start the chat
        chatUser = chatClient(username,password,stub, users)
    else:
        # Inform the user about the error
        messagebox.showerror("Warning", f"Invalid username or password")

        window.destroy()
        
        startingPage(stub)

# Function to create users account in the chat server
def createAccount(stub, userString, passwordString, window):
    # Get the user username
    username = userString.get()

    # Get the user password
    password = passwordString.get()

    response = stub.CreateAccount(chat_pb2.CreateAccountRequest(username=username, password=password))
    
    if response.message == "Account created":
        
        # Greet the user
        messagebox.showinfo("Success", f"Hello {username}, Account Created")

        window.destroy()

        startingPage(stub)
    else:

        # Inform the user about the error
        messagebox.showerror("Warning", f'Username already exists')

        window.destroy()

        startingPage(stub)


# Function to display the login page
def getLoginPage(stub, window):

    window.destroy()

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
    
    button =  Button(login_screen, text ="Login", width=10, height=2, command=lambda: loginUser(stub, username, password,login_screen)).grid(row=6,column=1)
    
    login_screen.mainloop()
    
# Function to display the account page
def getAccountPage(stub, window):

    window.destroy()

    account_screen=Tk()

    account_screen.title("Create Account")
    
    account_screen.geometry("450x250")

    Label(account_screen, text="Please choose a username and a password", font='Helvetica 12 bold').grid(row=0,column=1)
    
    Label(account_screen, text="").grid(row=1,column=0)

    Label(account_screen, text="Username").grid(row=2,column=0)

    username = tk.StringVar()
    
    username_login_entry = Entry(account_screen, textvariable=username).grid(row=2,column=1)
    
    Label(account_screen, text="").grid(row=3,column=0)

    Label(account_screen, text="Password").grid(row=4, column=0)

    password = StringVar()
    
    password__login_entry = Entry(account_screen, textvariable=password, show= '*').grid(row=4,column=1)

    Label(account_screen, text="").grid(row=5,column=0)
    
    button =  Button(account_screen, text ="Create Account", width=15, height=2, command=lambda: createAccount(stub, username, password,account_screen)).grid(row=6,column=1)
    
    account_screen.mainloop()


# Function to display the startingPage
def startingPage(stub):

    # Create the frame for getting the user choice
    root = Tk()  
    
    root.withdraw()

    # Get the user choice for actions in the chat server
    while True:
        choice = simpledialog.askstring("Choice", "Press:\n\n *1 to create an account\n\n *2 to log in\n\n  *q to exit\n\n",parent=root)
        
        if choice == "1":
            getAccountPage(stub, root)

        if choice == "2":
            getLoginPage(stub,root)

        elif choice == "q":
            stub.ClientDisconnected(chat_pb2.ClientDisconnectedRequest())
            
            # Inform the user the chat is closing
            answer = messagebox.showinfo("Close Chat", f"Closing chat, Bye!")
            if answer:
                root.destroy()
        else:
            # Inform the user the chat is closing
            messagebox.showerror("Error", f"Invalid input")
            
        


# ChatClient class that offer the chat services to clients
class chatClient:

    def __init__(self, username, password, stub, list_Users):
        
        self.stub = stub

        self.users = stub.getUsers(chat_pb2.Empty())

        print(self.users.users)

        self.username = username

        self.password= password

        root = Tk()

        root.withdraw()

        self.guide_done = False

        self.running = True

        self.scheduler = sched.scheduler(time.time, time.sleep)

        # Thread for the GUI
        guiThread = threading.Thread(target=self.gui_mainpage)

        # Thread for incoming messages
        guiMessage = threading.Thread(target=self.receive_messages_thread)

        # Start both threads
        guiThread.start()

        guiMessage.start()

        self.schedule_timer()

    # Function to get launch the thread to get the users in the chat
    def launch_thread(self):
        # Thread for users in chat
        usersThread = threading.Thread(target=self.get_Lits_Users)
        usersThread.start()
       
    # Function to schedule a timer to retrieve the list of users every 2 minutes
    def schedule_timer(self): 
        print("insde timer")
        while True:  
            if self.guide_done:
                print("timer")
                self.launch_thread()
                time.sleep(120)

    # Function to get list of users in the chat
    def get_Lits_Users(self):
        users = stub.getUsers(chat_pb2.Empty())
        # If the list of users is not empty, disply it
        if len(users.users) > 0:
            print(users)
            self.users = users
            if self.guide_done:
                self.msg_area3.config(state='normal')
                self.msg_area3.delete(1.0,END)
                for user in users.users:
                    self.msg_area3.insert('end',f"{user}\n")
                    self.msg_area3.yview('end')
                self.msg_area3.config(state='disabled')


        
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
       
        print('sending msg')
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
            else:
                response = self.stub.SendMessage(chat_pb2.SendMessageRequest(username=self.username, message=user_input))


                # Show the message to the client text area
                client_msg = f"{self.username} : {user_input}\n"
                if self.guide_done:
                    self.msg_area.config(state='normal')
                    self.msg_area.insert('end',client_msg)
                    self.msg_area.yview('end')
                    self.msg_area.config(state='disabled')
                self.input_msg.delete(1.0,"end-1c")

    # Create the main chat page
    def gui_mainpage(self):

        # Create the frame
        root = Tk()
        root.geometry("1000x700")
        root.title("Chat Client")
        root.config(bg="lightgray")

       
        self.frame_Users = Frame(root)
        #self.frame_Users.pack(padx=5,pady=5, side= LEFT)
        self.frame_Users.place(x=0,y=0,width=200, height=680)

        self.frame = Frame(root,width=100)
        #self.frame.pack(padx=10,pady=5, side=LEFT)
        self.frame.place(x=220,y=0,width=780, height=680)


        # Create the text at the top of the chat area 
        self.chat_label = Label(self.frame,text=f"Chat User: {self.username}", bg="lightgray")
        self.chat_label.config(font=("Arial",12,'bold'))
        self.chat_label.pack(padx=10,pady=5)

        # Create the text at the top of the user lists
        self.chat_label2 = Label( self.frame_Users,text=f"Users in the Chat")
        self.chat_label2.config(font=("Arial",12,'bold'))
        self.chat_label2.pack(padx=5,pady=5)


        # Create the chat area
        self.msg_area = scrolledtext.ScrolledText(self.frame, bg='lightyellow')
        self.msg_area.pack(padx=10, pady=5)
        self.msg_area.config(state="disabled")

        # Create the users list area
        self.msg_area3 = scrolledtext.ScrolledText( self.frame_Users, bg='lightblue', height=680)
        self.msg_area3.pack(padx=10, pady=2)
        self.msg_area3.config(state="disabled")

        # If there are users already connected to the chat, display their list
        if len(self.users.users) > 0:
            self.msg_area3.config(state='normal')
            for user in self.users.users:
                self.msg_area3.insert('end',f"{user}\n")
                self.msg_area3.yview('end')
            self.msg_area3.config(state='disabled')


        # Create the area for the user to enter message to send to the chat
        self.msg_label = Label(self.frame, text="Message", bg="lightgray")
        self.msg_label.config(font=("Arial",12))
        self.msg_label.pack(padx=10,pady=5)

        self.input_msg = Text(self.frame, height=3)
        self.input_msg.pack(padx=10,pady=5)


        # Create the send button to send messages to the chat
        self.send_button = Button(self.frame, text="send", bg='gray', command= self.sendMessageToChat)
        self.send_button.config(font=("Arial",12))
        self.send_button.pack(padx=10,pady=5)

        self.guide_done = True

        self.frame.mainloop()

# Main function
if __name__ == '__main__':

    # Create the grpc channel and stub for the client
    channel = grpc.insecure_channel('localhost:8080')
        
    stub = chat_pb2_grpc.ConnectionServiceStub(channel)

    stub.getUsers(chat_pb2.Empty())

    # Display the starting page
    startingPage(stub)
    
    
    
    

    
