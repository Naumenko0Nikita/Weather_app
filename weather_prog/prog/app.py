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
from .user_room import user_room
import wget

def data_update(command: str = None):
    global cursor
    data_base = sqlite3.connect("user.db")
    cursor = data_base.cursor()
    if command != None:
        cursor.execute(command)
        data_base.commit()
    data_base.close()


with open(PATH + "/cities.json", "r", encoding="utf-8") as file:
    cities = file.read()
    cities = json.loads(cities)
    cities_list = list(cities["cities"])

data_update("CREATE TABLE IF NOT EXISTS USER (ID INTEGER PRIMARY KEY, COUNTRY TEXT, CITY TEXT, NAME TEXT, LAST_NAME TEXT)")

city_dict = {
    'city_name': ''
}

data_base = sqlite3.connect("user.db")
cursor = data_base.cursor()
cursor.execute("SELECT COUNT(*) FROM USER")
count = cursor.fetchone()[0]
data_base.close()

class Weather_object(ctk.CTkFrame):
    def __init__(self, master: any, corner_radius: int | str | None = None, border_width: int | str | None = None, fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, time: str = "", temp: str = "",desc: str = "",x=None,y=None):
        super().__init__(master,50, 100, corner_radius, border_width, fg_color=fg_color, border_color=border_color)
        self.time_label = ctk.CTkLabel(master= self, width= 35, height= 25, font= ("Roboto Slab", 15), text= time, text_color="#FFFFFF")
        self.time_label.pack(pady=5,padx=1)
        self.temperature_img = ImageTk.PhotoImage(Image.open(PATH+f"/images/{desc}.png"))
        self.img = ctk.CTkLabel(master = self, width = 125, height = 125, text = "", image = self.temperature_img)
        self.img.pack(pady=1,padx=5)
        self.desc_label = ctk.CTkLabel(master= self,width= 35, height= 25, font= ("Roboto Slab", 15), text= desc, text_color="#FFFFFF")
        self.desc_label.pack(pady=1,padx=1)
    
        self.temp_label = ctk.CTkLabel(master= self,width= 35, height= 25, font= ("Roboto Slab", 15), text= temp, text_color="#FFFFFF")
        self.temp_label.pack(pady=5,padx=1)
        self.grid(row=y, column=x, padx=20)
def big_screen(master):
    global y
    app = ctk.CTkToplevel(master= master, fg_color= "#5DA7B1")
    width, height = 1200, 800
    app.geometry(f"{width}x{height}")
    app.resizable(False, False)
    app.wm_title("BigScreen")
    #app.wm_attributes('-topmost', True)

    cities = []

    data_base = sqlite3.connect("user.db")
    cursor = data_base.cursor()
    cursor.execute("SELECT NAME FROM USER WHERE ID=1")
    data_name = cursor.fetchone()[0]
    cursor.execute("SELECT LAST_NAME FROM USER WHERE ID=1")
    data_last_name = cursor.fetchone()[0]
    cursor.execute("SELECT CITY FROM USER WHERE ID=1")
    city_dict["city_name"] = cursor.fetchone()[0]
    data_base.close()

    user = ctk.CTkButton(master = app, width= 100, height= 55, text= f"{data_name} {data_last_name}", font=("Roboto Slab",35),text_color="#FFFFFF",command =lambda: user_room(master),fg_color= "#5DA7B1", hover_color= "#5DA7B1")
    user.place(x= width // 2.75 + 270, y = height // 4 - 150, anchor= ctk.E)

    weather_image = Image.open(PATH + "\\images\\Sunny.png")
    weather_image = ImageTk.PhotoImage(image=weather_image)
    weather_image_label = ctk.CTkLabel(
        master=app,
        image=weather_image,
        text=""
    )
    weather_image_label.place(x= 350, y=250)

    user_image = Image.open(PATH + "\\images\\user.png")
    user_image = ImageTk.PhotoImage(image=user_image.resize((50,50)))
    #print(PATH + "\\images\\user.png")
    #user_image = ImageTk.PhotoImage(Image.open(os.path.join(PATH, "images\\user.png")))
    user_button = ctk.CTkButton(master=app,width=50,height=50, image=user_image, fg_color= "#5DA7B1", hover_color= "#5DA7B1", text = "",command =lambda: user_room(master))
    user_button.place(x= width // 2.75 - 80, y = height // 4 - 150, anchor= ctk.CENTER)

    def search_command(event):
        global y
        city_dict["city_name"] = search.get()
        for child in scroll_frame2.winfo_children():
            child.destroy()

        with open(PATH + "/cities.json", "r+", encoding="utf-8") as file:
            citiesf = file.read()
            citiesf = json.loads(citiesf)
        if search.get() not in citiesf["cities"]:
            citiesf["cities"].append(search.get())
            city1 = City_object(master= scroll_frame, width= 250, height= 75, fg_color= "#096C82", corner_radius= 28, x = y, y = x, city_name= search.get())
            city1.weather_request()
            cities.append(city1)
            y += 1
            cities_file = json.dumps(citiesf)
            with open(PATH + "/cities.json", "w", encoding="utf-8") as file:
                file.write(cities_file)
        weather_request()
        weather_request2()
    search = ctk.CTkEntry(master = app, width = 150, height = 50, corner_radius= 28, fg_color= "#096C82", placeholder_text= "Search", text_color= "#FFFFFF", border_color= "#FFFFFF")
    search.place(x = width // 1.3, y = height // 40)
    search.bind("<Return>", search_command)

    title = ctk.CTkLabel(master = app, width= 100, height= 55, text= "Current position", font=("Roboto Slab",45),text_color="#FFFFFF")
    title.place(x= width // 2 + 100, y = height // 2.5 - 100, anchor= ctk.CENTER)

    weather_status = ctk.CTkLabel(master=app,width=100,height=25,text="",font=("Roboto Slab",25),text_color="#FFFFFF")
    weather_status.place(x= width // 2 + 100, y = height // 2.5 + 50, anchor= ctk.CENTER)
    
    # temperature_range = ctk.CTkLabel(master=app,width=100,height=25,text="",font=("Roboto Slab",15),text_color="#FFFFFF")
    # temperature_range.place(x= width // 2, y = height // 2.5 + 75, anchor= ctk.CENTER)

    temperature = ctk.CTkLabel(master= app, width= 100, height= 55, text= "", font= ("Roboto Slab", 55), text_color="#FFFFFF")
    temperature.place(x= width // 2 + 100, y = height // 2.5, anchor= ctk.CENTER)
    
    city_name = ctk.CTkLabel(master=app,width=100,height=30,text="",font=("Roboto Slab",30),text_color="#FFFFFF")
    city_name.place(x= width // 2 + 100, y = height // 2.5 - 50, anchor= ctk.CENTER)

    day = ctk.CTkLabel(master = app, width= 100, height= 35, text= "Monday", font=("Roboto Slab",35),text_color="#FFFFFF")
    day.place(x= width // 1.2, y = height // 2.5 - 100, anchor= ctk.CENTER)

    date = ctk.CTkLabel(master = app, width= 100, height= 35, text= "23.11.2023", font=("Roboto Slab",25),text_color="#FFFFFF")
    date.place(x= width // 1.2, y = height // 2.5 - 50, anchor= ctk.CENTER)

    time = ctk.CTkLabel(master = app, width= 100, height= 35, text= "20:51", font=("Roboto Slab",25),text_color="#FFFFFF")
    time.place(x= width // 1.2, y = height // 2.5, anchor= ctk.CENTER)

    scroll_frame = ctk.CTkScrollableFrame(master = app, width= 300, height= 1600, fg_color= "#096C82")
    scroll_frame.pack(anchor=ctk.W)
    
    scroll_frame2 = ctk.CTkScrollableFrame(master = app, width = 750, height = 225, fg_color= "#5DA7B1", border_color = "#FFFFFF",border_width = 5, corner_radius = 28, orientation = "horizontal") 
    scroll_frame2.place(x= 350, y= 500)
    
    x = 0
    y = 0
    class City_object(ctk.CTkFrame):
        def __init__(self,master,width,height,fg_color,corner_radius,x,y,city_name):
            super().__init__(master=master,width=width,height=height,fg_color=fg_color,corner_radius=corner_radius)
            self.x = x
            self.y = y
            self.configure(border_width = 5, border_color = "#FFFFFF")
            self.bind("<ButtonPress-1>", self.on_click)
            #self.font_size = height/3
            self.font_size = height/3 - (len(city_name)- 6 ) * 2.2
            for i in city_name:
                if i.lower() == "w":
                    self.font_size -= 2 
            self.city_label = ctk.CTkLabel(master=self, width=width/3, height=height/4,font=("Roboto Slab",self.font_size),text_color="#FFFFFF",text=city_name)
            self.loop = asyncio.get_event_loop()
            self.city_label.grid(row=0,column=0, padx=20, pady=20)

            self.temperature_label = ctk.CTkLabel(master= self, width= width/3, height= height/4, font = ("Roboto Slab", height/3), text_color="#FFFFFF", text = "None")
            self.temperature_label.grid(row=0,column=5,padx=20, pady=20)
            self.grid(row=self.x,column=self.y, padx=20, pady=20)

            self.desk_label = ctk.CTkLabel(master= self, width= width/3, height= height/4, font = ("Roboto Slab", 17), text_color="#FFFFFF", text = "None")
            self.desk_label.grid(row=2,column=0,padx=5, pady=10)

            self.range_label = ctk.CTkLabel(master= self, width= width/3, height= height/4, font = ("Roboto Slab", 17), text_color="#FFFFFF", text = "None")
            self.range_label.grid(row=2,column=5,padx=5, pady=10)


        def weather_request(self):
            api_key = '07c15c9587b9d5c7e8ed7c35930c21e5'

            data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={self.city_label._text}&appid={api_key}")
            if data.status_code == 200:
                temp = json.loads(data.text)
                self.temperature_label.configure(text= round(float(temp['main']['temp'] - 273.15), 1))
                self.desk_label.configure(text = temp['weather'][0]['main'])
                self.range_label.configure(text = f"↓{round(float(temp['main']['temp_min']-273.15), 1)}° ↑{round(float(temp['main']['temp_max']-273.15), 1)}°")

        def on_click(self, event):
            city_dict["city_name"] = self.city_label._text
            for child in scroll_frame2.winfo_children():
                child.destroy()
            weather_request()
            weather_request2()
    for city in cities_list:
        city1 = City_object(master= scroll_frame, width= 250, height= 75, fg_color= "#096C82", corner_radius= 28, x = y, y = x, city_name= city)
        cities.append(city1)
        y += 1
            

    def date_update():
        day.configure(text = datetime.date.today().strftime('%A'))
        date.configure(text = datetime.datetime.now().date().strftime('%d.%m.%y'))
        time.configure(text = datetime.datetime.now().time().strftime('%H:%M'))
        
        app.after(1000, date_update)
        
    def weather_request():
        api_key = "bc4bea9a5f764be8895151033230312"
        data = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_dict['city_name']}&aqi=no")
        if data.status_code == 200:
            temp = json.loads(data.text)
            weather_status.configure(text = temp["current"]["condition"]["text"])
            # temperature_range.configure(text = f"↓{round(float(temp['main']['temp_min']-273.15), 1)}° ↑{round(float(temp['main']['temp_max']-273.15), 1)}°")
            temperature.configure(text = temp['current']['temp_c'])
            city_name.configure(text = temp['location']["name"])
            if not os.path.exists(PATH+f"/images/{temp['current']['condition']['text']}.png"):
                wget.download(f"https:{temp['current']['condition']['icon']}", PATH+f"/images/{temp['current']['condition']['text']}.png")

            
            weather_image = Image.open(os.path.join(PATH+f"/images/{temp['current']['condition']['text']}.png")).resize(size=(150, 150))
            weather_image = ImageTk.PhotoImage(image=weather_image)
            weather_image_label.configure(image= weather_image)

        app.after(10000,weather_request)

    def weather_request2():
        api_key = "bc4bea9a5f764be8895151033230312"
        data = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city_dict['city_name']}&days=1")
        temp = json.loads(data.text)
        hours = temp["forecast"]["forecastday"][0]["hour"]
        x=0
        y=0
        for hour in hours:
            if not os.path.exists(PATH+f"/images/{hour['condition']['text']}.png"):
                wget.download(f"https:{hour['condition']['icon']}", PATH+f"/images/{hour['condition']['text']}.png")
            Weather_object(master = scroll_frame2, corner_radius = 28, border_width = 3, fg_color = "#5DA7B1", border_color = "#FFFFFF", time = hour["time"].split()[1], temp = hour["temp_c"],desc = hour["condition"]["text"],x=x,y=y)
            x += 1
    weather_request2()

    def cities_update():
        for city in cities:
            city.loop.run_in_executor(None, city.weather_request)
        app.after(300000,cities_update)
    
    app.after(0,cities_update)
    app.after(0,date_update)
    app.after(0,weather_request)
    #app.attributes('-topmost', 'true')
    #app.focus_set()
    #app.mainloop()