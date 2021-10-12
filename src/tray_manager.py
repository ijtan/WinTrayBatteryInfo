import wmi
from PIL import Image, ImageDraw,ImageFont
from classes import *

batteries = {}

#rate queue
history = []
max_history = 30
default_battery_index = 0


c = wmi.WMI()
t = wmi.WMI(moniker = "//./root/wmi")

icon_path = "BatteryIcon.ico"


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

    
def getIconInfo(prev_state,batt_index=default_battery_index):
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
        second_text = f"{ c.win32_battery()[default_battery_index].EstimatedChargeRemaining}%"


    return rate, second_text,b.Discharging



def default_battery_metrics():
    metrics = []
    metrics.append(metric("Voltage", "V", 'Voltage',hidden=True))
    metrics.append(metric('Battery Remaining Capacity', 'mAh', 'RemainingCapacity'))
    metrics.append(metric('Battery Estimated Charge Rate', 'mWh', 'ChargeRate'))
    metrics.append(metric('Battery Estimated Discharge Rate', 'mWh', 'DischargeRate'))
    metrics.append(metric('isCharging', '', 'Charging',hidden=True))

    return metrics

def updateBatteries():
    physical_batteries = t.ExecQuery('Select * from BatteryStatus where Voltage > 0')

    if(len(physical_batteries)==0):
        print("Error... No batteries found\nExiting...")
        exit()

    for b in physical_batteries:
        if b.Tag not in batteries:
            batteries[b.Tag] = battery(b,default_battery_metrics())
        else:
            batteries[b.Tag].batt = b


def getBatteryText():
    text = ''
    for key,val in batteries.items():
        text+=str(val)+'\n'
    
    return text