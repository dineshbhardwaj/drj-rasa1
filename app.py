# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import re
import sys
import apiai
import requests
import time

from utils import next_event


maintain_history = []
max_song_num=5

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    print("inside webhook")
#    data = urllib.urlopen('http://diveintomark.org/xml/atom.xml').read()
#    print(data)
    req = urlopen('http://ec2-54-197-17-247.compute-1.amazonaws.com').read()
    print("done req")
    #req = requests.post('http://ec2-54-197-17-247.compute-1.amazonaws.com')
    print(req)
    res = json.dumps(req, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print("queue working")
    return r


def makeWebhookResult(data):
    # print(json.dumps(item, indent=4))
    print("Response: " + data)
    return {
        "speech": data,
        "displayText": "Got the response"
        # "data": data,
        # "contextOut": [],
        #"source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
