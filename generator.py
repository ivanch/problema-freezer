from random import random, randint
import numpy as np
import math

from utils.config import *

# consts
RATE = 2 # 2 temperature reports in 1 minute

STD_TEMPERATURE = -82.5 # In Celsius, standard temperature of the freezer when closed
STD_TEMPERATURE_OPEN = -50 # In Celsius, temperature to close when its open
STD_TEMPERATURE_INCREASE = 20 # In Celsius, increase temperature when opening

STD_MAX_TEMPERATURE_OPEN = STD_TEMPERATURE_OPEN
STD_MAX_TEMPERATURE_CLOSED = -75
STD_MIN_TEMPERATURE = -95

OPEN_CHANCE = 2 # in 1000 of chances in opening the freezer

class Generator:
    def __init__(self, file_name = "data/report.csv", amount_of_days = 1, is_mock = False):
        if not file_name.endswith(".csv"):
            file_name += ".csv"

        self.amount_of_days = amount_of_days
        self.amount_of_time = amount_of_days * 24 * 60 * (60/RATE)
        self.amount_of_time = int(self.amount_of_time)

        self.file_name = file_name
        self.report = open(file_name, "w+")

        if not is_mock:
            self.report.write("machine,instance,temperature,faulty,lastRepairYear,manufactureYear,brand,model\n")
        else:
            self.report.write("instance,temperature,lastRepairYear,manufactureYear\n")

    def generate_temp(self, faulty):
        center = 0
        scale = 0
        if faulty:
            center = (STD_MAX_TEMPERATURE_CLOSED + STD_MIN_TEMPERATURE)/2
            scale = 0.2
        else:
            center = (STD_MAX_TEMPERATURE_CLOSED + STD_MIN_TEMPERATURE)/2
            scale = 1.25
        return np.random.normal(center, scale)

    def generate_machine_report(self, machine_id: int, machineConfig: MachineConfig):
        recorded_temperatures = []

        last_temperature = STD_TEMPERATURE

        open_instance = -1

        for t in range(0, self.amount_of_time, RATE):
            temperature = self.generate_temp(machineConfig.faulty)

            if machineConfig.faulty:
                pass
                # temperature should stay somewhat the same
            else:
                temperature = self.generate_temp(machineConfig.faulty)
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
            self.report.write("%d,%d,%.1f,%s,%d,%d,%d,%d\n" % (machine_id, t, temperature, machineConfig.faulty,
                                            machineConfig.year_of_last_repair, machineConfig.year_of_manufacture,
                                            machineConfig.brand, machineConfig.model
                                            ))
            last_temperature = temperature
            recorded_temperatures.append(temperature)

        return recorded_temperatures


    def generate_mock_machine_report(self, machinmachineConfig: MockMachineConfig):
        recorded_temperatures = []

        last_temperature = STD_TEMPERATURE

        open_instance = -1

        for t in range(0, self.amount_of_time, RATE):
            temperature = self.generate_temp(machinmachineConfig.faulty)

            if machinmachineConfig.faulty:
                pass
                # temperature should stay somewhat the same
            else:
                temperature = self.generate_temp(machinmachineConfig.faulty)
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
            self.report.write("%d,%.1f,%d,%d\n" % (t, temperature, machinmachineConfig.year_of_last_repair, machinmachineConfig.year_of_manufacture))
            last_temperature = temperature
            recorded_temperatures.append(temperature)

        return recorded_temperatures

    def generate_csv(self, amount_of_freezers = 10, amount_of_faulty_freezers = 3, plot = False):
        if plot:
            import matplotlib.pyplot as plt

            plt.figure(figsize=(1, 1), dpi=80)
            fig, axs = plt.subplots(math.ceil(amount_of_freezers/2), 2)

            fig.set_figheight(5 * math.floor(amount_of_freezers/2))
            fig.set_figwidth(15)
            fig.tight_layout(pad=4.0)

            plt.setp(axs, xlim=(0, self.amount_of_time), ylim=(-45,-95))

        for machine in range(amount_of_freezers):
            faulty = amount_of_faulty_freezers > 0
            if faulty:
                amount_of_faulty_freezers -= 1

            machineConfig = MachineConfig()
            machineConfig.generate(faulty)

            temperatures = self.generate_machine_report(machine, machineConfig)

            if plot:
                row = math.floor(machine/2)
                column = machine % 2

                axs[row, column].plot(range(0, self.amount_of_time, RATE), temperatures)
                axs[row, column].set_title("Machine %d (%s - %s)" % (machine, machineConfig.brand, machineConfig.model))

                for ax in axs.flat:
                    ax.set(xlabel='Time', ylabel='Temperature (ºC)')

                plt.savefig('data/report.png')

    def generate_mock_csv(self, is_faulty = True):
        machineConfig = MachineConfig()
        machineConfig.generate(is_faulty)

        temperatures = self.generate_mock_machine_report(machineConfig)