import socket
import  threading
from tkinter import  *

PORT = 50001
SERVER = "192.168.243.128"# Here first run the sever python code then you will an IP adress. Put that IP adress here
ADDRESS = (SERVER, PORT)
FORMAT = "UTF-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

#GUI part
class chatbox:
    def __init__(self):
        self.window = Tk()
        self.window.withdraw() # OR Window.geometry()

        # Create window for user to add anme and connect with server
        self.login = Toplevel()

        # set the Title for  login window
        self.login.title("Login")
        self.login.resizable(width=False,height=False)

        self.login.configure(width=470,height=550,bg="#17202A")

        # Create a label

        self.label = Label(self.login,text="Please login to continue",justify=CENTER, font="Arial 20 bold",bg= "#17202A",fg="white")
        self.label.place(relheight = 0.1, relx = 0.2, rely = 0.01)

        # Create a label
        self.labelName = Label(self.login, text ="Name : ", font = "Arial 18 bold",bg= "#17202A",fg="white")
        self.labelName.place(relheight = 0.1, relx = 0.1, rely = 0.2)

        #create a entry box
        self.entryName = Entry(self.login, font = "Arial 14")
        self.entryName.place(relheight = 0.07, relx = 0.3, rely = 0.2)

        self.entryName.focus()

        #create a Continue window
        self.go = Button(self.login, text = "Continue",font = "Arial 14 bold", command=lambda: self.toChatWindow(self.entryName.get()))
        self.go.place(relx = 0.4, rely = 0.8)

        self.window.mainloop()
    def toChatWindow(self, name):
        self.login.destroy()
        self.layout(name)
        #thread created to recieve messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()
    # The main layout of the chat

    def layout(self, name):
        self.name = name
        self.window.deiconify()
        self.window.title("CHATROOM")
        self.window.resizable(width=False,height=False)
        self.window.configure(width=470,height=550,bg="#17202A")

        self.labelHead = Label(self.window, bg="#EAECEE", text=self.name, font= "Helvetica 13 bold", pady=5)
        self.labelHead.place(relwidth=1)

        self.line = Label(self.window, width=450, bg="#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textCons = Text(self.window,width = 20,height = 2, bg="#17202A", fg="#EAECEE", font="Helvetica 13 bold", padx=5, pady = 5)
        self.textCons.place(relheight = 0.745,relwidth = 1, rely = 0.08)

        self.labelButton = Label(self.window,bg = "#2C3E50",height = 80)
        self.labelButton.place(relwidth = 1,rely= 0.825)

        self.entryMsg = Entry(self.labelButton,bg="#2C3E50",fg ="#EAECEE",font= "Helvetica 13 bold")
        self.entryMsg.place(relwidth = 0.74,relheight = 0.06,rely=0.008,relx = 0.011)

        self.entryMsg.focus()

        #creating Send Button
        self.buttonMsg = Button(self.labelButton,text = "Send",font = "Helvetica 10 bold", width = 20, bg ="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx = 0.77,rely = 0.008,relheight = 0.06,relwidth = 0.22)

        self.textCons.config(cursor = "arrow")

        #creating a scroll Bar

        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight = 1,relx = 0.974)
        scrollbar.config(command =self.textCons.yview)

        self.textCons.config(state= DISABLED)

    def sendButton(self,msg):
        self.textCons.config(state = DISABLED)
        self.msg = msg
        self.entryMsg.delete(0,END)

        snd = threading.Thread(target= self.sendMessage)
        snd.start()

    # function for receive message
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)

                # If the message from the server is NAME send the client's name
                if message == "NAME":
                    client.send(self.name.encode(FORMAT))
                else:
                    # insert message to text box
                    self.textCons.config(state = NORMAL)
                    message = message + "\n\n"
                    self.textCons.insert(END, message)

                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
            except:
                # an error will be printed on the command line or console if there"s
                print("An error occured")
                client.close()
                break
    def sendMessage(self):
        self.textCons.config(state = DISABLED)
        while True:
            message = (f"{self.name} : {self.msg}")
            client.send((message.encode(FORMAT)))
            break
# create a chatroom class object
g = chatbox()
