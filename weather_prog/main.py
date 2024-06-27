import pyshortcuts
import os

PATH = os.path.abspath(__file__ + "/..")

user_folder = os.path.expanduser("~")

pyshortcuts.make_shortcut(__file__,working_dir=PATH,folder=user_folder + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")


import prog