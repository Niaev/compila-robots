"""Automate NF PDF gathering from Belém of Pará website using Requests Library"""

# General imports
from time import time

# Automation imports 
import requests

# Project imports 
from utils.robot import Robot

class RequestsRobot(Robot):
    def __init__(self, file='data/data.json', verbose=False):
        super().__init__(file)

        self.__v = verbose

