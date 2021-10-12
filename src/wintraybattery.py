from infi.systray import SysTrayIcon
from time import sleep

import os
from tray_manager import *


    
#TODO:
#1. Dynamically add the options to the menu based on the metrics implemented
#2. Add two icons for the metrics, one is 'checked' as in a very good and the other is 'unchecked' / blank
    #3. These wil be updated when the metrics are enabled / disabled
#4. Make the metric enabled/disabled status persistent

#5. Add an option to select tray icon modes (dicharge rate maybe or time remaining etc. )


#right click menu options
menu_options = (
    # ('Options', "submenu.ico", (
                    # ('example thing 1', "simon.ico", ex1),
                    # ('some other thing', None, someOtherFunction),
                                            #   )),
               )

systray = SysTrayIcon((getImage('...','...',False)), "Starting Battery Monitor...", menu_options)


def main():
    #start the tray manager
    systray.start()
    print('Starting Tray Icon...')

    #wait fot tray icon to start
    while(not systray._hwnd):
        sleep(.1)
        print('Waiting for Tray Icon to start...')


    prev_state = True
    print('Starting battery Icon...')


    print(systray._hwnd)
    while systray._hwnd is not None:
        updateBatteries()       #get updated battery objects from wmi

        text = getBatteryText()   #get formatted text ready to display
        print(text)
        systray.update(getImage(*getIconInfo(prev_state)),text)     #update the tray icon
        
        sleep(2)


def safe_main():
    try:
        main()

        
    except KeyboardInterrupt:
        print('Interrupted\nShutting Down...')
        
        try:
            systray.shutdown()
        except SystemExit:
            os._exit(0)

if __name__ == '__main__':
    safe_main()
