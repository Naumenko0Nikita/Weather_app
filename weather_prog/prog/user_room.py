from typing import Optional, Tuple, Union
import customtkinter as ctk
import requests
import os 
import json
import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
import sqlite3
from PIL import Image, ImageTk
from .settings import *

def user_room(master):
    room_window = ctk.CTkToplevel(master= master, fg_color= "#5DA7B1")
    width, height = 460, 640
    room_window.geometry(f"{width}x{height}")
    room_window.resizable(False, False)
    room_window.wm_title("UserRoom")
    #room_window.wm_attributes('-topmost', True)

    data_base = sqlite3.connect("user.db")
    cursor = data_base.cursor()

    cursor.execute("SELECT COUNTRY FROM USER WHERE ID=1")
    data_country = cursor.fetchone()[0]

    cursor.execute("SELECT CITY FROM USER WHERE ID=1")
    data_city = cursor.fetchone()[0]

    cursor.execute("SELECT NAME FROM USER WHERE ID=1")
    data_name = cursor.fetchone()[0]

    cursor.execute("SELECT LAST_NAME FROM USER WHERE ID=1")
    data_lastname = cursor.fetchone()[0]    

    data_base.close()

    title = ctk.CTkLabel(master=room_window,width=100,height=25,text="User room",font=("Arial",25),text_color="#FFFFFF")
    title.place(x= width // 2, y = height // 10, anchor= ctk.CENTER)

    reg_country = ctk.CTkLabel(master=room_window,width=100,height=25,text=data_country,font=("Arial",25),text_color="#FFFFFF")
    reg_country.place(x= width // 8, y = height // 5 - 25, anchor= ctk.CENTER)

    reg_city = ctk.CTkLabel(master=room_window,width=100,height=25,text=data_city,font=("Arial",25),text_color="#FFFFFF")
    reg_city.place(x= width // 8, y = height // 3, anchor= ctk.CENTER)

    reg_name = ctk.CTkLabel(master=room_window,width=100,height=25,text=data_name,font=("Arial",25),text_color="#FFFFFF")
    reg_name.place(x= width // 8, y = height // 2, anchor= ctk.CENTER)

    reg_lastname = ctk.CTkLabel(master=room_window,width=100,height=25,text=data_lastname,font=("Arial",25),text_color="#FFFFFF")
    reg_lastname.place(x= width // 8 + 25, y = height // 1.5, anchor= ctk.CENTER)

    def room_button():
        room_window.destroy()

    reg_button = ctk.CTkButton(master=room_window, width= 200, height= 30, text= "Leave", corner_radius= 28, command= room_button)
    reg_button.place(x= width // 2, y = height // 1.1, anchor = ctk.CENTER)

    #room_window.mainloop()
    room_window.attributes('-topmost', 'true')
    room_window.focus_set()