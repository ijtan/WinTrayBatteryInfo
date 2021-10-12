from infi.systray import SysTrayIcon
from time import sleep
import wmi
from PIL import Image, ImageDraw,ImageFont
import os

batteries = {}

#rate queue
history = []
max_history = 30


c = wmi.WMI()
t = wmi.WMI(moniker = "//./root/wmi")


icon_path = "BatteryIcon.ico"

defualt_battery_index = 0


def getImage(deltaRate, deltaMetric,negative=True):
    img = Image.new('RGBA', (50, 50), color = (0, 0, 0, 0))

    d = ImageDraw.Draw(img)
    font_type  = ImageFont.truetype("arialbd.ttf", 25)

    if(negative):
        d.text((0, 0), f"{deltaRate}\n{deltaMetric}", fill=(255, 255, 255, 255), font=font_type)
    else:
        d.text((0, 0), f"{deltaMetric}\n{deltaRate}", fill=(0, 255, 0, 255), font=font_type)

    img.save(icon_path)
    return icon_path


'''
Intention is to allow the user to choose which items to show throgh a submenu with checkboxes
'''
class metric:
    def __init__(self, name, unit, function_name,value=0, hidden=False):
        self.name = name
        self.unit = unit
        self.value = value
        self.function_name = function_name
        self.hidden = hidden

    
    def __str__(self):
        if self.hidden:
            return ""
        else:
            return str(self.name + ": " + str(self.value) + self.unit)
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name and self.unit == other.unit and self.value() == other.value()
    
    def __ne__(self, other):
        return not self.__eq__(other)


class battery:
    def __init__(self,batt,metrics=[]):
        self.batt = batt
        self.metrics = metrics
    
    def update(self):
        for m in self.metrics:
            m.value = getattr(self.batt, m.function_name)
        return self.metrics

    def __str__(self):
        self.update()
        return "".join([str(m)+'\n' for m in self.metrics])
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.metrics == other.metrics
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def add_metric(self, metric):
        self.metrics.append(metric)
        # return self.metrics.index(metric)
    
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

for b in physical_batteries:
    batteries[b.Tag] = battery(b)

    metrics = []
    metrics.append(metric("Voltage", "V", 'Voltage'))
    metrics.append(metric('Battery Remaining Capacity', 'mAh', 'RemainingCapacity'))
    metrics.append(metric('Battery Estimated Charge Rate', 'mWh', 'ChargeRate'))
    metrics.append(metric('Battery Estimated Discharge Rate', 'mWh', 'DischargeRate'))
    metrics.append(metric('isCharging', '', 'Charging'))

    for m in metrics:
        batteries[b.Tag].add_metric(m)
    


    # metrics.append(metric('Battery % Remaining', '%', b.EstimatedChargeRemaining))
    # metrics.append(metric('Battery Voltage', 'V', b.Voltage))
    # # metrics.append(metric('Battery Current', 'A', b.Current))
    # metrics.append(
    # # metrics.append(metric('Battery Full Capacity', 'mAh', b.FullCapacity))
    # # metrics.append(metric('Battery Design Capacity', 'mAh', b.DesignCapacity))
    # # metrics.append(metric('Battery Cycle Count', '', b.CycleCount))
    # # metrics.append(metric('Battery Temperature', 'C', b.Temperature))
    # # metrics.append(metric('Battery Estimated Time Remaining', '', b.EstimatedTime))
    # # metrics.append(metric('Battery Estimated Run Time', 'hours', b.EstimatedRunTime))
    # metrics.append(metric('Battery Estimated Charge Rate', 'mWh', b.ChargeRate))
    # metrics.append(metric('Battery Estimated Discharge Rate', 'mWh', b.DischargeRate))
    # metrics.append(metric('isCharging', '', b.Charging))
    
def getIconInfo(prev_state):
    rate = 0
    second_text = ''
    batts = t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
    for b in batts:
        raw_rate = b.dischargeRate if b.dischargeRate else b.chargeRate
        rate=raw_rate/1000
        rate = str(round(rate,1))+'k'
        # rate = str("{:,}".format(rate)) 
    

    if len(history) > max_history:
        history.pop(0)

    if prev_state!=b.Discharging:
        history.clear()
        prev_state = b.Discharging

    history.append(raw_rate)
    avg_rate = sum(history)/len(history)

    if(b.Discharging and float(b.DischargeRate)!=0):
                time_left = float(b.RemainingCapacity)/float(avg_rate)
                hours_left = int(time_left)
                mins_left = int((time_left % 1.0)*60)
                # second_text = f"{hours_left}h : {mins_left}m"
                second_text = f"{hours_left}:{mins_left}"
    elif not b.Discharging:
        second_text = f"{ c.win32_battery()[defualt_battery_index].EstimatedChargeRemaining}%"


    return rate, second_text,b.Discharging
    


# def getUpdatedText():
#     new_text = ""
#     batts = t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
#     for i, b in enumerate(batts):
#         # new_text+=(f'Battery: {i}\n')
#         # new_text+=('isCharging: ' + str(b.PowerOnline)) + '\n'
#         # new_text+=('Discharging:       ' + str(b.Discharging)) + '\n'
#         # new_text+=('Charging:          ' + str(b.Charging)) + '\n'
        
#         if(b.Discharging):
#             new_text+=('Discharge Rate: -' + str("{:,}".format(b.DischargeRate))) + 'mWh\n'
#         else:
#             new_text+=('Charge Rate: ' + str("{:,}".format(b.ChargeRate))) + '\n'

#         if(b.Discharging and float(b.DischargeRate)!=0):
#             time_left = float(b.RemainingCapacity)/float(b.DischargeRate)
#             hours_left = int(time_left)
#             mins_left = (time_left % 1.0)*60
#             new_text += 'Time Remaining: ' + '%i hr %i min' % (hours_left, mins_left)+'\n'


#         new_text+=('Voltage:           ' + str(b.Voltage)) + '\n'


    '''
    CANNOT CALCULATE TIME LEFT FOR CHARGING BATTERIES WELL
    AS DESIGN CAPACITY NOT WORKING
    '''

        # new_text+=('RemainingCapacity: ' + str(b.RemainingCapacity)) + '\n'
    # return new_text

def ex1(sysTrayIcon):
    print('example 1')

def someOtherFunction(sysTrayIcon):
    print('some other function')

#things TODO:
#1. Dynamically add the options to the menu based on the metrics implemented
#2. Add two icons for the metrics, one is 'checked' as in a very good and the other is 'unchecked' / blank
    #3. These wil be updated when the metrics are enabled / disabled
#4. Make the metric enabled/disabled status persistent

#5. Add an option to select tray icon modes (dicharge rate maybe or time remaining etc. )


menu_options = (
    # ('Options', "submenu.ico", (
                    # ('example thing 1', "simon.ico", ex1),
                    # ('some other thing', None, someOtherFunction),
                                            #   )),
               )

systray = SysTrayIcon((getImage('...','...',False)), "Starting Battery Monitor...", menu_options)


def main():
    
    systray.start()
    print('Starting Tray Icon...')
    # sleep(5) # requires sleep to allow the systray to start
    while(not systray._hwnd):
        sleep(.1)
        print('Waiting for Tray Icon to start...')

    prev_state = True
    print('Starting battery Icon...')
    print(systray._hwnd)
    while systray._hwnd is not None:
        # new_text = getUpdatedText()
        # # new_image = getImage(
        # print(f'Got new text: \n{new_text}')
        # systray.update(getImage(*getIconInfo(prev_state)), new_text)
        # print(f'history length: {len(history)}')
        # print(f'history: {history}')
        # print(f'Battery print: "{[val for key,val in batteries.items()]}"')

        text = ''
        for key,val in batteries.items():
            text+=str(val)+'\n'
        
        print(text)
        systray.update(getImage(*getIconInfo(prev_state)),text)
        
        sleep(2)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted\nShutting Down...')
        

        try:
            systray.shutdown()
        except SystemExit:
            os._exit(0)
