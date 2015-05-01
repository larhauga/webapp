#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import requests
import argparse
from flask import Flask
app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read('etc/app.cfg')


def get_version():
    version = None
    with open('etc/version.txt', 'r') as f:
        version = f.read().strip().split()
    return version


@app.route("/")
def front():
    version = get_version()

    return "Service %s. Version %s" % (version[0], version[1])


@app.route('/api')
def depend():
    txt = "Service %s: %s<br />" % (str(get_version()[0]),
                                    str(get_version()[1]))
    txt += "<b>Sub services:</b><br />"
    for service in config.get('main', 'service').split(','):
        try:
            r = requests.get(config.get(service, 'url'), timeout=1)
            txt += r.text
        except:
            txt += "No connection to configured subservice"
            print "Something went wrong"
        txt += "<br />"
    return txt


@app.route('/health')
def healthcheck():
    return "Up and ready"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, required=True)
    args = parser.parse_args()
    app.debug = config.get('main', 'debug')
    app.run(host='0.0.0.0', port=args.port)
