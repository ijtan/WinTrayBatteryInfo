import wmi

c = wmi.WMI()
t = wmi.WMI(moniker = "//./root/wmi")

batts1 = c.CIM_Battery(Caption = 'Portable Battery')
for i, b in enumerate(batts1):
    print(f'Battery %d Design Capacity: { (i, b.DesignCapacity or 0)} mWh')


batts = t.ExecQuery('Select * from BatteryFullChargedCapacity')
for i, b in enumerate(batts):
    print ('Battery %d Fully Charged Capacity: %d mWh' % (i, b.FullChargedCapacity))
    
batts = t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
for i, b in enumerate(batts):
    print('\nBattery %d ***************' % i)
    print('Tag:               ' + str(b.Tag))
    print('Name:              ' + b.InstanceName)

    print('PowerOnline:       ' + str(b.PowerOnline))
    print('Discharging:       ' + str(b.Discharging))
    print('Charging:          ' + str(b.Charging))
    print('Voltage:           ' + str(b.Voltage))
    print('DischargeRate:     ' + str(b.DischargeRate))
    print('ChargeRate:        ' + str(b.ChargeRate))
    print('RemainingCapacity: ' + str(b.RemainingCapacity))
    print('Active:            ' + str(b.Active))
    print('Critical:          ' + str(b.Critical))