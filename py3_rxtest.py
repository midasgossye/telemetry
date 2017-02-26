

import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import system

pld_RX = False

def play_sound(file_name):
    play_str = "omxplayer /home/pi/telemetry/sounds/"
    play_str += file_name
    os.system(play_str)

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 7)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[1])
radio.printDetails()
radio.startListening()
play_sound("STARTUP.mp3")

while(1):
    # ackPL = [1]
    while not radio.available(0):
        time.sleep(1 / 100)
    if pld_RX == False:
        pld_RX = True
        play_sound("DATARX.mp3")
    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print("Received: {}".format(receivedMessage))

    print("Translating the receivedMessage into unicode characters")
    string = ""
    for n in receivedMessage:
        # Decode into standard unicode set
        if (n > 31 and n  <126):
            string += chr(n)
    print("Out received message decodes to: {}".format(string))

