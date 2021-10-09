from infi.systray import SysTrayIcon
from time import sleep
import wmi

c = wmi.WMI()
t = wmi.WMI(moniker = "//./root/wmi")


'''
Intention is to allow the user to choose which items to show throgh a submenu with checkboxes
'''
class metric:
    def __init__(self, name, unit, value, hidden=False):
        self.name = name
        self.unit = unit
        self.value = value
        self.hidden = hidden
    
    def __str__(self):
        if self.hidden:
            return ""
        else:
            return self.name + ": " + str(self.value()) + self.unit
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name and self.unit == other.unit and self.value() == other.value()
    
    def __ne__(self, other):
        return not self.__eq__(other)


class battery:
    def __init__(self,battery,metrics=[]):
        self.battery = battery
        self.metrics = metrics
    
    def __str__(self):
        return "\n".join([str(m) for m in self.metrics])
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.metrics == other.metrics
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def add_metric(self, metric):
        self.metrics.append(metric)
    
    def remove_metric(self, metric):
        self.metrics.remove(metric)
    
    def get_metric(self, name):
        for m in self.metrics:
            if m.name == name:
                return m
        return None
    
    def get_metrics(self):
        return self.metrics
    

physical_batteries = t.ExecQuery('Select * from BatteryStatus where Voltage > 0')

if(len(physical_batteries)==0):
    print("Error... No batteries found\nExiting...")
    exit()

batteries = {}

for b in physical_batteries:
    batteries[b.Tag] = battery(b)

    metrics = []
    # metrics.append(metric('Battery % Remaining', '%', b.EstimatedChargeRemaining))
    metrics.append(metric('Battery Voltage', 'V', b.Voltage))
    # metrics.append(metric('Battery Current', 'A', b.Current))
    metrics.append(metric('Battery Remaining Capacity', 'mAh', b.RemainingCapacity))
    # metrics.append(metric('Battery Full Capacity', 'mAh', b.FullCapacity))
    # metrics.append(metric('Battery Design Capacity', 'mAh', b.DesignCapacity))
    # metrics.append(metric('Battery Cycle Count', '', b.CycleCount))
    # metrics.append(metric('Battery Temperature', 'C', b.Temperature))
    # metrics.append(metric('Battery Estimated Time Remaining', '', b.EstimatedTime))
    # metrics.append(metric('Battery Estimated Run Time', 'hours', b.EstimatedRunTime))
    metrics.append(metric('Battery Estimated Charge Rate', 'mWh', b.ChargeRate))
    metrics.append(metric('Battery Estimated Discharge Rate', 'mWh', b.DischargeRate))
    metrics.append(metric('isCharging', '', b.Charging))
    



def getUpdatedText():
    new_text = ""
    batts = t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
    for i, b in enumerate(batts):
        # new_text+=(f'Battery: {i}\n')
        # new_text+=('isCharging: ' + str(b.PowerOnline)) + '\n'
        # new_text+=('Discharging:       ' + str(b.Discharging)) + '\n'
        # new_text+=('Charging:          ' + str(b.Charging)) + '\n'
        # new_text+=('Voltage:           ' + str(b.Voltage)) + '\n'
        if(b.Discharging):
            new_text+=('Discharge Rate: -' + str("{:,}".format(b.DischargeRate))) + 'mWh\n'
        else:
            new_text+=('Charge Rate: ' + str("{:,}".format(b.ChargeRate))) + '\n'

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


# menu_options = (("Say Hello", None, say_hello),)
# systray = SysTrayIcon("icon.ico", "Example tray icon", menu_options)

def ex1(sysTrayIcon):
    print('example 1')

def someOtherFunction(sysTrayIcon):
    print('some other function')

menu_options = (
    ('Options', "submenu.ico", (
                    ('example thing 1', "simon.ico", ex1),
                    ('some other thing', None, someOtherFunction),
                                              )),
               )

systray = SysTrayIcon("icon.ico", "Starting Battery Monitor...", menu_options)
systray.start()

print('Starting Tray Icon...')
sleep(5) # requires sleep to allow the systray to start


print('Starting battery monitor...')
print(systray._hwnd)
while systray._hwnd is not None:
    new_text = getUpdatedText()
    print(f'Got new text: \n{new_text}')
    systray.update("icon.ico", new_text)
    sleep(3)
