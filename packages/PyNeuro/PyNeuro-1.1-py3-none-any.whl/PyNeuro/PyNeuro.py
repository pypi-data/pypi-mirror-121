"""
@Author Zach Wang
@Date 2021.9.27
@Version 1.0.0
"""
import json
from telnetlib import Telnet
from threading import Thread


class PyNeuro:
    """NeuroPy libraby, to get data from neurosky mindwave.
    Initialising: object1=PyNeuro() #windows
    After initialising , if required the callbacks must be set
    then using the start method the library will start fetching data from mindwave
    i.e. object1.start()
    similarly close method can be called to stop fetching the data
    i.e. object1.close()

    requirements:Telnet

    """

    __attention = 0
    __meditation = 0
    __blinkStrength = 0
    __status = "Scanning"

    __attention_records = []
    __meditation_records = []
    __blinkStrength_records = []

    __packetsReceived = 0
    __telnet = None

    __attention_callbacks = []
    __meditation_callbacks = []
    __blinkStrength__callbacks = []

    callBacksDictionary = {}  # keep a track of all callbacks

    def __init__(self):
        self.__parserThread = None
        self.__threadRun = False
        self.__connected = False

    def connect(self):
        """
        Connect the TCP socket via Telnet.

        """
        if self.__telnet is None:
            self.__telnet = Telnet('localhost', 13854)
            self.__telnet.write(b'{"enableRawOutput": true, "format": "Json"}');
            print("[PyNeuro] Connecting TCP Socket Host...")

    def disconnect(self):
        """
        Disconnect the TCP socket.
        """
        if self.__telnet is not None:
            self.__telnet.close()
            print("[PyNeuro] Disconnect TCP Socket.")

    def start(self):
        """
        Start Service.
        :return:
        """

        self.__parserThread = Thread(target=self.__packetParser, args=())
        self.__threadRun = True
        self.__parserThread.start()

    def close(self):
        """
        Close Service.
        :return:
        """
        self.__threadRun = False
        self.__parserThread.join()

    def __packetParser(self):
        while True:
            line = self.__telnet.read_until(b'\r');
            if len(line) > 20:
                try:
                    raw_str = (str(line).rstrip("\\r'").lstrip("b'"))
                    data = json.loads(raw_str)
                    if "status" in data.keys():
                        self.__status = data["status"]
                        if data["status"] == "scanning":
                            print("[PyNeuro] Scanning device..")
                        else:
                            print("[PyNeuro] Connection lost, trying to reconnect..")
                    else:
                        if "eSense" in data.keys():
                            if data["eSense"]["attention"] + data["eSense"]["meditation"] == 0:
                                self.__status = "fitting"
                            else:
                                self.__status = "connected"
                                self.attention = data["eSense"]["attention"]
                                self.meditation = data["eSense"]["meditation"]
                                self.__attention_records.append(data["eSense"]["attention"])
                                self.__attention_records.append(data["eSense"]["meditation"])
                        elif "blinkStrength" in data.keys():
                            self.blinkStrength = data["blinkStrength"]
                            self.__blinkStrength_records.append(data["blinkStrength"])
                except:
                    print()

    def set_attention_callback(self, callback):
        """
        Set callback function of attention value
        :param callback: function(attention: int)
        """

        self.__attention_callbacks.append(callback)

    def set_meditation_callback(self, callback):
        """
        Set callback function of meditation value
        :param callback: function(meditation: int)
        """

        self.__meditation_callbacks.append(callback)

    def set_blinkStrength_callback(self, callback):
        """
        Set callback function of meditation value
        :param callback: function(blinkStrength: int)
        """

        self.__blinkStrength_callbacks.append(callback)

    # attention
    @property
    def attention(self):
        "Get value for attention"
        return self.__attention

    @attention.setter
    def attention(self, value):
        self.__attention = value
        # if callback has been set, execute the function
        if len(self.__attention_callbacks) != 0:
            for callback in self.__attention_callbacks:
                callback(self.__attention)

    # meditation
    @property
    def meditation(self):
        "Get value for meditation"
        return self.__meditation

    @meditation.setter
    def meditation(self, value):
        self.__meditation = value
        # if callback has been set, execute the function
        if len(self.__meditation_callbacks) != 0:
            for callback in self.__meditation_callbacks:
                callback(self.__meditation)

    # blinkStrength
    @property
    def blinkStrength(self):
        "Get value for blinkStrength"
        return self.__blinkStrength

    @blinkStrength.setter
    def blinkStrength(self, value):
        self.__blinkStrength = value
        # if callback has been set, execute the function
        if len(self.__blinkStrength__callbacks) != 0:
            for callback in self.__blinkStrength__callbacks:
                callback(self.__blinkStrengthn)
