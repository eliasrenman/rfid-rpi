#  Written by Elias Renman, 2019.

# !/usr/bin/env python
import os
from time import time, sleep
from dotenv import load_dotenv

load_dotenv()


class Reader:

    def __init__(self):
        self.last_card_id = 0
        self.last_interaction_timestamp = int(round(time()))
        if not Util.debug_input():
            import RPi.GPIO as GPIO
            self.GPIO = GPIO

    def loop(self):
        req = HttpRequest()
        try:
            while True:
                card_id = self.read()
                Util.print("Card ID: %s\n" % card_id)
                if self.debounce(card_id):
                    req.handle_req(card_id)
                else:
                    sleep(1)
        except KeyboardInterrupt:
            if not Util.debug_input():
                self.GPIO.cleanup()

            raise

    def read(self):
        from mfrc522 import SimpleMFRC522
        reader = SimpleMFRC522()
        Util.print("Hold a tag near the reader")
        return reader.read_id()

    def debounce(self, card_id):

        if card_id != self.last_card_id:
            Util.print("Card id is not the same")
            self.update_last(card_id)
            return True
        else:
            if self.last_interaction_timestamp + 15 < int(round(time())):
                Util.print("Card id is the same but time elapsed is over the limit")
                self.update_last(card_id)
                return True
            else:
                return False

    def update_last(self, card_id):
        self.last_card_id = card_id
        self.last_interaction_timestamp = int(round(time()))


class DebugReader(Reader):

    def read(self):
        input('write anything to run:')
        return DebugReader.get_random_cid()

    @staticmethod
    def get_random_cid():
        import random
        return random.randint(1, 100000000)


class HttpRequest:

    def __init__(self):
        self.controller = (GPIOController(), DebugGPIOController())[Util.debug_output()]

    def handle_req(self, card_id):
        self.controller.process()
        response = HttpRequest.send_request(card_id)
        self.handle_response(response)

    @staticmethod
    def send_request(card_id):
        import requests
        url = os.getenv("HOST_ENDPOINT")
        current_time = int(round(time() * 1000))
        payload = "token=" + os.getenv("TOKEN") + "&" \
            "card=" + str(card_id) + "&" \
            "timestamp=" + str(current_time)
        Util.print(payload)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'User-Agent': "PostmanRuntime/7.16.3",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "5c7f1b44-0fa9-4619-b653-ab27c0f16761,1a3976a8-fe2b-4561-97ef-a3abd381d4d5",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        text = response.text
        response.close()
        return text

    def handle_response(self, response):
        import json
        Util.print(response)
        response_json = json.loads(response)

        self.controller.process()
        if response_json["write"]:
            self.controller.write_success()
        elif response_json["success"]:
            if response_json["check_in"]:
                self.controller.check_in()
            else:
                self.controller.check_out()

        else:
            self.controller.error()



class GPIOController:

    def __init__(self):
        if os.getenv("DEBUG_OUTPUT") != "true":
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(18, GPIO.OUT)
            self.GPIO = GPIO
        self.processing = False

    def process(self):
        if self.processing:
            self.processing = False
            self.GPIO.output(1, self.GPIO.LOW)
        else:
            self.processing = True
            self.GPIO.output(1, self.GPIO.HIGH)
    def write_success(self):
        self.blink_output([0,1,2,3],3, 0.5)
    def check_in(self):
        self.blink_output([0], 1, 0.5)

    def check_out(self):
        self.blink_output([0], 1, 0.5)

    def error(self):
        self.blink_output([0], 3, 0.3)

    def blink_output(self, pins, amount, timeout):
        counter = 1
        for i in range(amount):
            for pin in pins:
                self.GPIO.output(pin, self.GPIO.HIGH)
            sleep(timeout)
            for pin in pins:
                self.GPIO.output(pin, self.GPIO.LOW)
            sleep(timeout)
            if amount != counter:
                sleep(timeout)
            counter += 1


class DebugGPIOController(GPIOController):

    def process(self):
        if self.processing:
            self.processing = False
            Util.print("Proccesing LED off")
        else:
            self.processing = True
            Util.print("Proccesing LED on")
    def write_success(self):
        Util.print("write successfully triggerd")
        super().write_success()

    def check_in(self):
        Util.print("check in triggered")
        super().check_in()

    def check_out(self):
        Util.print("check out triggered")
        super().check_out()

    def error(self):
        Util.print("error triggered")
        super().error()

    def blink_output(self, pins, amount, timeout):
        counter = 1
        for i in range(amount):
            for pin in pins:
                Util.print("blinking on pin: " + str(pin))
            sleep(timeout)
            Util.print("Timeout lasted: " + str(timeout) + " seconds")
            for pin in pins:
                Util.print("blinking off pin: " + str(pin))
            if amount != counter:
                sleep(timeout)
                Util.print("Timeout lasted: " + str(timeout) + " seconds")

            counter += 1


class Util:
    @staticmethod
    def debug_output():
        return os.getenv("DEBUG_OUTPUT") == "true"

    @staticmethod
    def debug_input():
        return os.getenv("DEBUG_INPUT") == "true"
    
    @staticmethod
    def print(_str):
        if os.getenv("CONSOLE_PRINT") == "true":
            print(_str)


reader = (Reader(), DebugReader())[Util.debug_input()]
reader.loop()
