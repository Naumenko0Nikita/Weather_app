import customtkinter as ctk
import requests
from PIL import Image, ImageTk, ImageFont
import os
import json
from .app import count, big_screen
from .register import registration
import sqlite3
from win32com.client import Dispatch
from .settings import *
import wget


if count != 0:
    data_base = sqlite3.connect("user.db")
    cursor = data_base.cursor()
    cursor.execute("SELECT CITY FROM USER WHERE ID=1")
    data_city = cursor.fetchone()[0]
    data_base.close()

def start_widget():
    app = ctk.CTk(fg_color= "#5DA7B1")
    width, height = 250, 250
    app.geometry(f"{width}x{height}")
    app.resizable(False, False)
    app.wm_title("Widget")
    app.wm_attributes("-topmost", True)
    
    timg = Image.open(os.path.join(PATH, "images/user.png"))
    #timg.thumbnail(size = (500, 500),resample=Image.NEAREST)
    timg = timg.resize((100,100))
    temperature_img = ImageTk.PhotoImage(image=timg)
    img = ctk.CTkLabel(master = app, width = 125, height = 125, text = "", image = temperature_img)
    img.place(x = 0, y = 0)
    
    weather_status = ctk.CTkLabel(master=app,width=100,height=25,text="",font=("Roboto Slab", 15),text_color="#FFFFFF")
    weather_status.place(x= width // 4, y = height // 2 + 25, anchor= ctk.CENTER)
    
    # temperature_range = ctk.CTkLabel(master=app,width=100,height=25,text="",font=("Roboto Slab", 15),text_color="#FFFFFF")
    # temperature_range.place(x= width // 4, y = height // 1.7 + 25, anchor= ctk.CENTER)
    
    temperature = ctk.CTkLabel(master=app,width=100,height=35,text="",font=("Roboto Slab", 35),text_color="#FFFFFF")
    temperature.place(x= width // 1.3, y = height // 1.6, anchor= ctk.CENTER)
    
    city_name = ctk.CTkLabel(master=app,width=100,height=30,text="",font=("Roboto Slab", 30),text_color="#FFFFFF")
    city_name.place(x= width // 1.3, y = height // 1.2, anchor= ctk.CENTER)

    def wrequest():
        api_key = "bc4bea9a5f764be8895151033230312"
        data = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={data_city}&aqi=no")
        if data.status_code == 200:
            temp = json.loads(data.text)
            weather_status.configure(text = temp["current"]["condition"]["text"])
            #temperature_range.configure(text = f"↓{round(float(temp['main']['temp_min']-273.15), 1)}° ↑{round(float(temp['main']['temp_max']-273.15), 1)}°")
            temperature.configure(text = temp['current']['temp_c'])
            city_name.configure(text = temp['location']["name"])
            if not os.path.exists(PATH+f"/images/{temp['current']['condition']['text']}.png"):
                wget.download(f"https:{temp['current']['condition']['icon']}", PATH+f"/images/{temp['current']['condition']['text']}.png")
            #temperature_img = ImageTk.PhotoImage(Image.open(os.path.join(PATH+f"/images/{temp['current']['condition']['text']}.png")))
            timg = Image.open(os.path.join(PATH+f"/images/{temp['current']['condition']['text']}.png"))
            #timg.thumbnail(size = (500, 500),resample=Image.NEAREST)
            timg = timg.resize((100,100))
            temperature_img = ImageTk.PhotoImage(image=timg)
            img.configure(image=temperature_img)
    update_button_image = ImageTk.PhotoImage(Image.open(os.path.join(PATH, "images/captcha.png")))
    update_button = ctk.CTkButton(master= app, width= 20, height= 20, text= "", image= update_button_image, fg_color= "#5DA7B1", hover_color= "#5DA7B1",  command=wrequest)
    update_button.place(x = 210, y = 10)
    
    def change_screen(event):
        big_screen(app)

    app.bind("<Double-Button-1>",change_screen)

    def weather_request():
        wrequest()
        #api_key = '07c15c9587b9d5c7e8ed7c35930c21e5'
        #data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={data_city}&appid={api_key}")
        #if data.status_code == 200:
        #    temp = json.loads(data.text)
        #    weather_status.configure(text = temp['weather'][0]['main'])
        #    # temperature_range.configure(text = f"↓{round(float(temp['main']['temp_min']-273.15), 1)}° ↑{round(float(temp['main']['temp_max']-273.15), 1)}°")
        #    temperature.configure(text = round(float(temp['main']['temp']-273.15), 1))
        #    city_name.configure(text = temp['name'])
        #    #temperature_img = ImageTk.PhotoImage(Image.open(os.path.join(PATH, "images/sunny.png")))
        #    #img.configure(image=temperature_img)
        app.after(10000,weather_request)

    app.after(0,weather_request)

    app.mainloop()

print(count)

if count == 0:
    registration()
else:
    start_widget()