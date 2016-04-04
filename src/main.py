#!/usr/bin/env python
#
# Copyright (c) 2016 Davi Garcia (davigar@cisco.com)
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import json
import serial
from time import sleep, time
from paho.mqtt import publish


SERIAL_DEVICE = serial.Serial(
    port='/dev/ttyS1',
    baudrate=19200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=2
)

MQTT_CONFIG = {
    "hostname": "192.168.1.6",
    "port": 1883,
    "topic": "cisco/davigar/ir829-iox-demo",
    "publish-interval": 5,
}


def collect_sensor_data():
    try:
        sensor_data = SERIAL_DEVICE.readline()
        return sensor_data
    except serial.SerialTimeoutException:
        return None

def publish_data(data):
    try:
        publish.single(MQTT_CONFIG['topic'], data, hostname=MQTT_CONFIG['hostname'], port=MQTT_CONFIG['port'])
    except IOError:
        pass

def run(interval):
    while True:
        data = collect_sensor_data()
        if data is not None:
            publish_data(data)
        sleep(interval)


if __name__ == '__main__':
    try:
        run(MQTT_CONFIG['publish-interval'])
    except KeyboardInterrupt:
        print('Interrupted!')
