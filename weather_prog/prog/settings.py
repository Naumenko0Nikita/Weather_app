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


PATH = os.path.abspath(__file__ + "/../..")

def data_update(command: str = None):
    global cursor
    data_base = sqlite3.connect("user.db")
    cursor = data_base.cursor()
    if command != None:
        cursor.execute(command)
        data_base.commit()
    data_base.close()