#!/usr/bin/env python
#
# Copyright (c) <year> <copyright holders>
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
import random
from time import sleep, time
from paho.mqtt import publish

config = {
  "mqtt-address": "broker.hivemq.com",
  "mqtt-port": 1883,
  "mqtt-topic": "cisco/davigar/ir829",
  "pooling-internal": 15,
  "serial-interface": "/dev/ttyS1"
}

def load_config(filename='setup.json'):
    config_file = open(filename)
    return json.loads(config_file.read())

def collect_sensor_data():
    try:
        sensor = dict()
        sensor['timestamp'] = time()
        sensor['temperature'] =  random.randrange(0, 100)
        sensor['humidity'] = random.randrange(0, 100)
        sensor['alarm'] = random.choice([True, False])
        json_string = json.dumps(sensor)
        print('Sensor data collected: %s' % json_string)
        return json_string
    except:
        print('Unable to collect data from sensor. Returning None!')
        return None

def publish_data(data, config):
    try:
        publish.single(config['mqtt-topic'], data, hostname=config['mqtt-address'], port=config['mqtt-port'])
        print('Published MQTT message!')
    except IOError:
        print('Unable to publish MQTT message. Skiping this iteration!')

def run(config):
    while True:
        data = collect_sensor_data()
        publish_data(data, config)
        print('Sleeping for %s seconds.' % config['pooling-internal'])
        sleep(config['pooling-internal'])


if __name__ == '__main__':
    try:
        run(config)
    except KeyboardInterrupt:
        print('Interrupted!')
