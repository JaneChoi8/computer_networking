import socket
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk 
import threading
from datetime import datetime


HOST = "127.0.0.1"
PORT = 65234
HEADER = 64
FORMAT = "utf8"
DISCONNECT = "x"

LARGE_FONT = ("verdana", 13,"bold")

#option
SIGNUP = "signup"
LOGIN = "login"
LOGOUT = "logout"
SEARCH = "search"
LIST = "listall"

ADMIN_USERNAME = 'admin'
ADMIN_PSWD = 'database'

INSERT_NEW_MATCH='insert_a_match'
UPDATE_SCORE = "upd_score"
UPDATE_DATETIME = "upd_date_time"
INSERT_DETAIL = "insert_detail"

#GUI intialize
class Books_App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.geometry("500x200")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, HomePage, SearchPage):
            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)
    
    def showFrame(self, container):
        frame = self.frames[container]
        if container==HomePage:
            self.geometry("700x500")
        elif container == SearchPage:
            self.geometry("700x500")
        else:
            self.geometry("500x200")
        frame.tkraise()

    # close-programe function
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            try:
                option = LOGOUT
                client.sendall(option.encode(FORMAT))
            except:
                pass

    def logIn(self,curFrame,sck):
        try:
            user = curFrame.entry_user.get()
            pswd = curFrame.entry_pswd.get()

            if user == "" or pswd == "":
                curFrame.label_notice = "Fields cannot be empty"
                return 
       
            #notice server for starting log in
            option = LOGIN
            sck.sendall(option.encode(FORMAT))

            #send username and password to server
            sck.sendall(user.encode(FORMAT))
            print("input:", user)

            sck.recv(1024)
            print("s responded")

            
            sck.sendall(pswd.encode(FORMAT))
            print("input:", pswd)


            # see if login is accepted
            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: "+ accepted)

            if accepted == "1":
                self.showFrame(HomePage)
                curFrame.label_notice["text"] = ""
            elif accepted == "2":
                curFrame.label_notice["text"] = "invalid username or password"
            elif  accepted == "0":
                curFrame.label_notice["text"] = "user already logged in"

        except:
            curFrame.label_notice["text"] = "Error: Server is not responding"
            print("Error: Server is not responding")

    def signUp(self,curFrame, sck):
        
        try:
        
            user = curFrame.entry_user.get()
            pswd = curFrame.entry_pswd.get()

            if pswd == "":
                curFrame.label_notice["text"] = "password cannot be empty"
                return 

            #notice server for starting log in
            option = SIGNUP
            sck.sendall(option.encode(FORMAT))
            
            
            #send username and password to server
            sck.sendall(user.encode(FORMAT))
            print("input:", user)

            sck.recv(1024)
            print("s responded")

            sck.sendall(pswd.encode(FORMAT))
            print("input:", pswd)


            # see if login is accepted
            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: "+ accepted)

            if accepted == "True":
                self.showFrame(HomePage)
                curFrame.label_notice["text"] = ""
            else:
                curFrame.label_notice["text"] = "username already exists"

        except:
            curFrame.label_notice["text"] = "Error 404: Server is not responding"
            print("404")

    def logout(self,curFrame, sck):
        try:
            option = LOGOUT
            sck.sendall(option.encode(FORMAT))
            accepted = sck.recv(1024).decode(FORMAT)
            print(accepted)
            if accepted == "True":
                self.showFrame(StartPage)
        except:
            curFrame.label_notice["text"] = "Error: Server is not responding"


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#b08968")

        label_title = tk.Label(self, text="LOG IN", font=LARGE_FONT,fg='#ede0d4',bg="#b08968")
        label_user = tk.Label(self, text="username ",fg='#ede0d4',bg="#b08968",font='verdana 10 ')
        label_pswd = tk.Label(self, text="password ",fg='#ede0d4',bg="#b08968",font='verdana 10 ')

        self.label_notice = tk.Label(self,text="",bg="#b08968")
        self.entry_user = tk.Entry(self,width=20,bg='light yellow')
        self.entry_pswd = tk.Entry(self,width=20,bg='light yellow')

        button_log = tk.Button(self,text="LOG IN", bg="#ede0d4",fg='#7f5539',command=lambda: controller.logIn(self, client)) 
        button_log.configure(width=10)
        button_sign = tk.Button(self,text="SIGN UP",bg="#ede0d4",fg='#7f5539', command=lambda: controller.signUp(self, client)) 
        button_sign.configure(width=10)
        
        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        self.label_notice.pack()

        button_log.pack()
        button_sign.pack()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#b08968")
        
        label_title = tk.Label(self, text="HOME PAGE", font=LARGE_FONT,fg='#ede0d4',bg="#b08968")
        button_back = tk.Button(self, text="Logout",bg="#ede0d4",fg='#7f5539', command=lambda: controller.logout(self,client))
        button_list = tk.Button(self, text="List all",bg="#ede0d4",fg='#7f5539',command=lambda: controller.listall(self,client))
        button_search = tk.Button(self, text="Search",bg="#ede0d4",fg='#7f5539',command=lambda: controller.showFrame(SearchPage))

        label_title.pack(pady=10)
        button_back.pack()
        button_back.configure(width=10)
        button_list.pack()
        button_list.configure(width=10)
        button_search.pack()
        button_search.configure(width=10)


        #code them UI o day
    def recieveBooks(self):
        book = []
    
        books = []
        data = ''
        while True:
            data = client.recv(1024).decode(FORMAT)
            client.sendall(data.encode(FORMAT))
            if data == "end":
                break
            
            # book : [ID, Book_Name, Author, Publishing_year]

            for i in range(6):
                data = client.recv(1024).decode(FORMAT)
                client.sendall(data.encode(FORMAT))
                book.append(data) 

            
            books.append(book)
            book = []

        return books

    def listAll(self):
        try:
            self.frame_detail.pack_forget()

            option = LIST
            client.sendall(option.encode(FORMAT))
            
            books = self.recieveBooks()
            
            x = self.tree.get_children()
            for item in x:
                self.tree.delete(item)

            i = 0
            for m in books:
                self.tree.insert(parent="", index="end", iid=i, 
                        values=( m[0], m[1], m[3], m[2]) )
                
                i += 1

            self.frame_list.pack(pady=10)
        except:
            self.label_notice["text"] = "Error"
            
class SearchPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#b08968")
        
        label_title = tk.Label(self, text="SEARCH PAGE", font=LARGE_FONT,fg='#ede0d4',bg="#b08968")
        button_searchID = tk.Button(self, text="Search ID",bg="#ede0d4",fg='#7f5539', command=lambda: controller.logout(self,client))
        button_searchNAME = tk.Button(self, text="Search NAME",bg="#ede0d4",fg='#7f5539')
        button_searchAU = tk.Button(self, text="Search AUTHOR",bg="#ede0d4",fg='#7f5539')
        button_searchYEAR = tk.Button(self, text="Search PUBLICING YEAR",bg="#ede0d4",fg='#7f5539')
        button_back = tk.Button(self, text="Go back",bg="#ede0d4",fg='#7f5539', command=lambda: controller.showFrame(HomePage))

        label_title.pack(pady=10)

        self.entry_user = tk.Entry(self,width=45,bg='light yellow')
        self.entry_user.pack()

        button_searchID.pack()
        button_searchID.configure(width=20)
        button_searchNAME.pack()
        button_searchNAME.configure(width=20)
        button_searchAU.pack()
        button_searchAU.configure(width=20)
        button_searchYEAR.pack()
        button_searchYEAR.configure(width=20)
        button_back.pack()
        button_back.configure(width=20)


        #code them UI o day



#GLOBAL socket initialize
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)

client.connect(server_address)

app = Books_App()



#main
try:
    app.mainloop()
except:
    print("Error: server is not responding")
    client.close()

finally:
    client.close()


