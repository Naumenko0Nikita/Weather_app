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


def registration():
    register_window = ctk.CTk(fg_color= "#5DA7B1")
    width, height = 460, 640
    register_window.geometry(f"{width}x{height}")
    register_window.resizable(False, False)

    title = ctk.CTkLabel(master=register_window,width=100,height=25,text="User registration",font=("Arial",25),text_color="#FFFFFF")
    title.place(x= width // 2, y = height // 10, anchor= ctk.CENTER)



    reg_country = ctk.CTkLabel(master=register_window,width=100,height=25,text="Country:",font=("Arial",25),text_color="#FFFFFF")
    reg_country.place(x= width // 8, y = height // 5 - 25, anchor= ctk.CENTER)

    reg_country_enter = ctk.CTkEntry(master= register_window, width= 200, height= 40, placeholder_text= "Enter the country name", corner_radius= 28)
    reg_country_enter.place(x= width // 8 + 75, y = height // 5 + 25, anchor= ctk.CENTER)



    reg_city = ctk.CTkLabel(master=register_window,width=100,height=25,text="City:",font=("Arial",25),text_color="#FFFFFF")
    reg_city.place(x= width // 8, y = height // 3, anchor= ctk.CENTER)
    
    reg_city_enter = ctk.CTkEntry(master= register_window, width= 200, height= 40, placeholder_text= "Enter the city name", corner_radius= 28)
    reg_city_enter.place(x= width // 8 + 75, y = height // 3 + 50, anchor= ctk.CENTER)

    reg_name = ctk.CTkLabel(master=register_window,width=100,height=25,text="First name:",font=("Arial",25),text_color="#FFFFFF")
    reg_name.place(x= width // 8 + 25, y = height // 2, anchor= ctk.CENTER)
    
    reg_name_enter = ctk.CTkEntry(master= register_window, width= 200, height= 40, placeholder_text= "Enter your first name", corner_radius= 28)
    reg_name_enter.place(x= width // 8 + 75, y = height // 2 + 50, anchor= ctk.CENTER)

    reg_lastname = ctk.CTkLabel(master=register_window,width=100,height=25,text="Last name:",font=("Arial",25),text_color="#FFFFFF")
    reg_lastname.place(x= width // 8 + 25, y = height // 1.5, anchor= ctk.CENTER)
    
    reg_lastname = ctk.CTkEntry(master= register_window, width= 200, height= 40, placeholder_text= "Enter your last name", corner_radius= 28)
    reg_lastname.place(x= width // 8 + 75, y = height // 1.5 + 50, anchor= ctk.CENTER)

    def register_button():
        data_update(f"INSERT INTO USER (COUNTRY, CITY, NAME, LAST_NAME) VALUES ('{reg_country_enter.get()}', '{reg_city_enter.get()}', '{reg_name_enter.get()}', '{reg_lastname.get()}')")

        register_window.destroy()

    reg_button = ctk.CTkButton(master=register_window, width= 200, height= 30, text= "Registration", corner_radius= 28, command= register_button)
    reg_button.place(x= width // 2, y = height // 1.1, anchor = ctk.CENTER)

    register_window.mainloop()