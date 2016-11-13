import requests
from time import sleep
from itertools import cycle
from sys import argv

from helpers.utils import raw_mac
from models.primitives.time import Time
from config import config
from db import PathDAO


class ApiJSON(object):
    API_URL = config["ap_data"]["endpoint"]

    def __init__(self, db_obj):
        self.__dict__.update({
            "data": [
                {
                    "clientMac": raw_mac(db_obj["device_mac"])
                }
            ],
            "apMac": raw_mac(db_obj["router_mac"]),
            "time": db_obj["created_at"],
            "band": db_obj["signal"]["channel"]
        })

        for n, v in db_obj["rssis"].items():
            self.__dict__["data"][0]["rss" + n] = v

    def __getattr__(self, item):
        return self.__dict__[item]

    def send(self):
        self.time = Time().millis
        res = requests.post(self.API_URL, json=self.__dict__)
        return res.status_code


class SimulatorPathStep(object):
    def __init__(self, tup):
        api_json, break_millis = tup
        self.break_millis = break_millis
        self.api_json = api_json

    def simulate_step(self):
        res = self.api_json.send()
        sleep(self.break_millis / 1000)
        return res
        

class SimulatorPath(object):
    def __init__(self, steps):
        self.sent = 0
        self.steps = steps

    @classmethod
    def create(cls, jsons):
        there_and_back_again = cls.create_returning(jsons)
        intervals = cls.count_intervals(there_and_back_again)
        return cls(list(map(SimulatorPathStep, zip(there_and_back_again, intervals))))

    @classmethod
    def create_returning(cls, jsons):
        api_jsons = list(map(ApiJSON, jsons))
        return api_jsons + api_jsons[-2:0:-1]

    @classmethod
    def count_intervals(cls, path):
        times = [item.time for item in path]
        return list(map(lambda t: abs(t[1] - t[0]),  zip(times, reversed(times))))

    def run_cycled(self):
        for step in cycle(self.steps):
            result = step.simulate_step()
            if result == 200:
                self.sent += 1
                print(self.sent)
            else:
                print("error " + result)


class Simulator(object):
    def __init__(self, collection_name, path_dao):
        self.path_name = collection_name
        self.path_dao = path_dao
        self.path = self.prepare()
        print(ApiJSON.API_URL)

    def fetch(self):
        return self.path_dao.fetch_path(self.path_name)

    def prepare(self):
        return SimulatorPath.create(self.fetch())

    def run(self):
        self.path.run_cycled()


if __name__ == '__main__':
    Simulator(argv[1], PathDAO()).run()



