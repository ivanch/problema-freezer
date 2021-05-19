import json
from random import randint, choice

# JSON CONSTS
LAST_REPAIR_RANGE = "lastRepairDateRange"
DATE_OF_MANUFACTURE = "dateOfManufactureRange"
BRANDS = "brands"

class MachineConfig:
    def __init__(self):
        self.year_of_manufacture = 0
        self.year_of_last_repair = 0
        self.brand = ""
        self.model = ""
        self.faulty = False

    def generate(self, faulty: bool):
        json_file = open("utils/config.json", "r")
        config_json = json.load(json_file)

        self.faulty = faulty
        reliability = "faulty" if faulty else "reliable"

        self.year_of_last_repair = randint(config_json[reliability][LAST_REPAIR_RANGE][0], config_json[reliability][LAST_REPAIR_RANGE][1])
        self.year_of_manufacture = randint(config_json[reliability][DATE_OF_MANUFACTURE][0], config_json[reliability][DATE_OF_MANUFACTURE][1])
        brand_model = choice(list(config_json[reliability][BRANDS].items()))

        self.brand = int(brand_model[0])
        self.model = int(choice(brand_model[1]))

class MockMachineConfig:
    def __init__(self):
        self.year_of_manufacture = 0
        self.year_of_last_repair = 0
        self.faulty = False

    def generate(self, faulty: bool):
        json_file = open("utils/config.json", "r")
        config_json = json.load(json_file)

        self.faulty = faulty
        reliability = "faulty" if faulty else "reliable"

        self.year_of_last_repair = randint(config_json[reliability][LAST_REPAIR_RANGE][0], config_json[reliability][LAST_REPAIR_RANGE][1])
        self.year_of_manufacture = randint(config_json[reliability][DATE_OF_MANUFACTURE][0], config_json[reliability][DATE_OF_MANUFACTURE][1])
        brand_model = choice(list(config_json[reliability][BRANDS].items()))