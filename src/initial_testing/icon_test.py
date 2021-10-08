from infi.systray import SysTrayIcon
from time import sleep

def say_hello(systray):
    print("Hello, World!")
menu_options = (("Say Hello", None, say_hello),)
systray = SysTrayIcon("icon.ico", "Example tray icon", menu_options)
systray.start()

sleep(5)
systray.update("icon.ico", "Yoo new things")