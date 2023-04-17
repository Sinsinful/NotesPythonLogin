from tkinter import *
from tkinter import ttk
import os
import mysql.connector
from mysql.connector import Error
import pandas as pd


db = "notes"
pw = "Liverpool24"
current_user = ""

def register_user():
    username_info = username.get()
    password_info = password.get()

    file=open(username_info, "w")
    file.write(username_info+"\n")
    file.write(password_info)
    file.close

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(screen1, text= "Registration sucessful", fg = "green", font = ("calibri", 11)).pack()
    create_user_table = """
    CREATE TABLE {tab} (
        date DATETIME PRIMARY KEY,
        note VARCHAR(45) NOT NULL
    );""".format(tab=username_info)
    connection = create_db_connection("localhost", "root", pw, db) # Connect to the Database
    execute_query(connection, create_user_table) # Execute our defined query

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_entry1.delete(0, END)
    password_entry1.delete(0, END)
    global current_user
    current_user  = username1
    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            print("login sucessful")
            screen2.destroy()
            notes_screen()

        else:
            print("Password not reconised")
    else:
        print("User not found")



def register():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("300x250")
    
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(screen1, text = "Please enter details below").pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Username *").pack()
    username_entry = Entry(screen1, textvariable = username)
    username_entry.pack()
    Label(screen1, text = "Password *").pack()
    password_entry = Entry(screen1, textvariable = password)
    password_entry.pack()
    Label(screen1, text = "").pack()
    Button(screen1, text="Register", width = "10", height = "1", command = register_user).pack()

def login():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("300x250")
    Label(screen2, text = "Please enter details below to login").pack()
    Label(screen2, text = "").pack()
    global username_verify
    global password_verify
    
    username_verify = StringVar()
    password_verify = StringVar()

    global username_entry1
    global password_entry1

    Label(screen2, text = "Username *").pack()
    username_entry1 = Entry(screen2, textvariable= username_verify)
    username_entry1.pack()
    Label(screen2, text = "").pack()

    Label(screen2, text = "Password *").pack()
    password_entry1 = Entry(screen2, textvariable= password_verify)
    password_entry1.pack()

    Label(screen2, text = "").pack()
    Button(screen2, text = "Login", width = 10, height = 1, command = login_verify).pack()

def notes_screen():
    global screen3
    screen3 = Toplevel(screen)
    screen3.title("Current notes:")
    screen3.geometry("600x500")

    q1 = """ SELECT * FROM notes.{tab};""".format(tab = current_user )
    connection = create_db_connection("localhost", "root", pw, db)
    results = read_query(connection, q1)

    i=0 
    for entry in results:
        for j in range(len(entry)):
            e = Entry(screen3, width=30, fg='black') 
            e.grid(row=i, column=j) 
            e.insert(END, entry[j])
        i=i+1
    


def main_screen():
    global screen
    screen = Tk()
    screen.geometry("300x250")
    screen.title("Notes 1.0")
    Label(text = "Notes 1.0", bg = "grey", width= "300", height = "2", font = ("Calibri", 13)).pack()
    Label(text = "").pack()
    Button(text = "Login", height = "2", width = "30", command = login).pack()
    Label(text = "").pack()
    Button(text = "Register", height = "2", width = "30", command = register).pack()
    screen.mainloop()


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def add_note():
    return 1

connection = create_server_connection("localhost", "root", pw) # Connect to the Database
main_screen()