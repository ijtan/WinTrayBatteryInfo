from infi.systray import SysTrayIcon
from time import sleep

import wmi

c = wmi.WMI()
t = wmi.WMI(moniker = "//./root/wmi")

# batts1 = c.CIM_Battery(Caption = 'Portable Battery')
# for i, b in enumerate(batts1):
#     print(f'Battery %d Design Capacity: { (i, b.DesignCapacity or 0)} mWh')

# batts = t.ExecQuery('Select * from BatteryFullChargedCapacity')
# for i, b in enumerate(batts):
#     print('\nBattery %d ***************' % i)
#     print('Tag:               ' + str(b.Tag))
#     print('Name:              ' + b.InstanceName)

#     print('PowerOnline:       ' + str(b.PowerOnline))
#     print('Discharging:       ' + str(b.Discharging))
#     print('Charging:          ' + str(b.Charging))
#     print('Voltage:           ' + str(b.Voltage))
#     print('DischargeRate:     ' + str(b.DischargeRate))
#     print('ChargeRate:        ' + str(b.ChargeRate))
#     print('RemainingCapacity: ' + str(b.RemainingCapacity))
#     print('Active:            ' + str(b.Active))
#     print('Critical:          ' + str(b.Critical))


def say_hello(systray):
    print("Hello, World!")




def get_new_text():
    print('fethcing new text')
    new_text = ""
    batts = t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
    for i, b in enumerate(batts):
        # new_text+=(f'Battery: {i}\n')
        # new_text+=('isCharging:       ' + str(b.PowerOnline)) + '\n'
        # new_text+=('Discharging:       ' + str(b.Discharging)) + '\n'
        # new_text+=('Charging:          ' + str(b.Charging)) + '\n'
        # new_text+=('Voltage:           ' + str(b.Voltage)) + '\n'
        if(b.Discharging):
            new_text+=('Discharge Rate: -' + str(b.DischargeRate)) + 'mWh\n'
        else:
            new_text+=('Charge Rate: ' + str(b.ChargeRate)) + '\n'

        if(b.Discharging and float(b.DischargeRate)!=0):
            time_left = float(b.RemainingCapacity)/float(b.DischargeRate)
            hours_left = int(time_left)
            mins_left = (time_left % 1.0)*60
            new_text += 'Time Remaining: ' + '%i hr %i min' % (hours_left, mins_left)+'\n'
        
        '''
        CANNOT CALCULATE TIME LEFT FOR CHARGING BATTERIES WELL
        AS DESIGN CAPACITY NOT WORKING
        '''


        # if(not b.Discharging and float(b.ChargeRate)!=0):
        #     # new_text += 'Charge Time Remaining: ' + str(float(b.RemainingCapacity) / float(b.ChargeRate)) + '\n'
        #     time_left = float(b.RemainingCapacity)/float(b.ChargeRate)
        #     hours_left = int(time_left)
        #     mins_left = (time_left % 1.0)*60
        #     new_text += 'Charge Time Remaining: ' + '%i hr %i min' % (hours_left, mins_left)+'\n'


        # new_text+=('RemainingCapacity: ' + str(b.RemainingCapacity)) + '\n'
        # new_text+=('Active:            ' + str(b.Active)) + '\n'
        # new_text+=('Critical:          ' + str(b.Critical)) + '\n'
    return new_text


menu_options = (("Say Hello", None, say_hello),)
systray = SysTrayIcon("icon.ico", "Example tray icon", menu_options)

systray.start()

sleep(5)
print(systray._hwnd)
while systray._hwnd is not None:
    new_text = get_new_text()
    print(f'Got new text: {new_text}')
    systray.update("icon.ico", new_text)
    sleep(4)

# while(True):
#     print(systray._hwnd)
#     sleep(2)