#This file keeps track of constants and parameters
SIMPLE_DRIVER_ACCELERATION = 0.42
SIMPLE_DRIVER_DECELERATION = 0.42

#Engine constants
#acceleration due to gravity, m/s^2
g = 9.8
#mass of bus in kg (30000 lbs)
MASS = 13607.771
#drag parameters
#density of air
ro = 1.225
#cross section area of bus
A = 9
#drag coefficient
Cd = 0.2

#Joules/liter
DIESEL_ENGINE_EFFICIENCY = 1.8/0.0000001
ELECTRIC_ENGINE_EFFICIENCY = 1
#power 20kWatts
POWER_CAP_ELECTRIC = 20000
#power
MAX_BATTERY_CHARGE_RATE = 20000
#battery capacity 1.3kWh (kilowatt hours)
BATTERY_CAP = 4680000
#battery charging when using diesel
BATTERY_CHARGE_FROM_DIESEL = 1000


