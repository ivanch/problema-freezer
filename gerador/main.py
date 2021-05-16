from random import random, randint
import numpy as np
import matplotlib.pyplot as plt
import math

from config import MachineConfig

plt.figure(figsize=(1, 1), dpi=80)

# consts
RATE = 60/2 # 2 temperature reports in 1 minute

AMOUNT_OF_DAYS = 1
AMOUNT_OF_TIME = 60 * 60 * (60/30)
AMOUNT_OF_FREEZERS = 10
AMOUNT_OF_FAULTY_FREEZERS = 3

STD_DEVIATION = 5 # In Celsius
STD_TEMPERATURE = -80 # In Celsius, standard temperature of the freezer when closed
STD_TEMPERATURE_OPEN = -50 # In Celsius, temperature to close when its open
STD_TEMPERATURE_INCREASE = 20 # In Celsius, increase temperature when opening

STD_MAX_TEMPERATURE_OPEN = STD_TEMPERATURE_OPEN
STD_MAX_TEMPERATURE_CLOSED = -75
STD_MIN_TEMPERATURE = -95

OPEN_CHANCE = 15 # in 1000 of chances in opening the freezer

RATE = int(RATE)
AMOUNT_OF_TIME = int(AMOUNT_OF_TIME)

report = open("report.csv", "w+")
report.write("machine,instance,temperature,faulty,lastRepairYear,manufactureYear,brand,model\n")


def generate_temp(faulty):
    center = 0
    scale = 0
    if faulty:
        center = (STD_MAX_TEMPERATURE_CLOSED + STD_MIN_TEMPERATURE)/2
        scale = 3
    else:
        center = (STD_MAX_TEMPERATURE_CLOSED + STD_MIN_TEMPERATURE)/2
        scale = 5
    return np.random.normal(center, scale)

def generate_machine_report(machine_id: int, machineConfig: MachineConfig):
    recorded_temperatures = []

    last_temperature = STD_TEMPERATURE

    open_instance = -1

    for t in range(0, AMOUNT_OF_TIME, RATE):
        temperature = generate_temp(machineConfig.faulty)

        if machineConfig.faulty:
            pass
            # temperature should stay somewhat the same
        else:
            temperature = generate_temp(machineConfig.faulty)
            if open_instance >= 0:
                if open_instance == 4: # should be closing now
                    open_instance = -1
                    # temperature should be the standard right after closing
                else:
                    # slightly increase the temperature when its open
                    open_instance += 1
                    temperature = last_temperature + STD_TEMPERATURE_INCREASE*random()
            else:
                if randint(1, 1000) <= OPEN_CHANCE:
                    open_instance = 1

                if open_instance >= 0:
                    temperature = last_temperature + STD_TEMPERATURE_INCREASE*random()

                # if its not open, temperature should stay somewhat the same

        # write information on temperature
        report.write("%d,%d,%.1f,%s,%d,%d,%s,%s\n" % (machine_id, t, temperature, machineConfig.faulty,
                                        machineConfig.year_of_last_repair, machineConfig.year_of_manufacture,
                                        machineConfig.brand, machineConfig.model
                                        ))
        last_temperature = temperature
        recorded_temperatures.append(temperature)

    return recorded_temperatures

if AMOUNT_OF_FREEZERS < 2:
    print("Its required at least two freezers")

fig, axs = plt.subplots(math.ceil(AMOUNT_OF_FREEZERS/2), 2)

fig.set_figheight(15)
fig.set_figwidth(15)
fig.tight_layout(pad=4.0)

plt.setp(axs, xlim=(0, AMOUNT_OF_TIME), ylim=(-50,-100))

for machine in range(AMOUNT_OF_FREEZERS):
    row = math.floor(machine/2)
    column = machine % 2

    faulty = AMOUNT_OF_FAULTY_FREEZERS > 0
    if faulty:
        AMOUNT_OF_FAULTY_FREEZERS -= 1

    machineConfig = MachineConfig()
    machineConfig.generate(faulty)

    temperatures = generate_machine_report(machine, machineConfig)
    axs[row, column].plot(range(0, AMOUNT_OF_TIME, RATE), temperatures)
    axs[row, column].set_title("Machine %d (%s - %s)" % (machine, machineConfig.brand, machineConfig.model))

    for ax in axs.flat:
        ax.set(xlabel='Time', ylabel='Temperature (ºC)')

    plt.savefig('report.png')