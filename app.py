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


from flask import Flask
from flask import request
from flask import make_response
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from song_data import *
from rq import Queue
from worker import conn

from utils import next_event



maintain_history = []



# Flask app should start in global layout
app = Flask(__name__)



#DEEPAK CODE FOR EVENT
CLIENT_ACCESS_TOKEN = '9ded4fd3df4b42b7b678b928add51dbf'
##DEEPAK



@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    q = Queue(connection=conn)
    print("Request:")
#    print(json.dumps(req, indent=4))
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    #if not session_id:
    print("session id1")
    session_id=req.get("sessionId")
    print("Session id2",session_id)
    #next_req = q.enqueue(requests.post('https://drj1.herokuapp.com/next', data = {'session_id1':session_id}))
    #if "nextevent" not in str(req.get("result").get("resolvedQuery")):
        #next_req = q.enqueue(next_event,session_id)
    #result = q.enqueue(count_words_at_url, 'http://heroku.com')
    #time.sleep(1)
    print("queue working")
    return r



def processRequest(req):
    print("processing req")
    input_data = str(req)
    print(input_data)
    input_data = str(req.get("result").get("resolvedQuery"))
#    input_data = str(req.get("queryResult").get("queryText"))
    input_data = re.sub('[sS]ong', '', input_data)
    input_data = re.sub('^[pP]lay', '', input_data)
    print("processing req 2")
    print(input_data)
    choice_val = process.extract(input_data, choices, scorer=fuzz.partial_ratio, limit=1)
    print("processing req 3")
    print(str(choice_val))
    choice_song_path = map_choices[choice_val[0][0]]
    choice_song_path1 = map_choices["Tera Mera Pyar Amar"]
    print("processing req 4")
    print(str(choice_song_path))
    #data = "<speak> <audio src=\"" + choice_song_path + "\"> didn't get your MP3 audio file </audio> </speak>"
    data = "<speak> <audio src=\"" + choice_song_path + "\"> didn't get your MP3 audio file </audio> \
        <break time=\"3s\"/> \
        <audio src=\"" + choice_song_path1 + "\"> didn't get your MP3 audio file </audio> </speak>"
    res = makeWebhookResult(data)
    return res


def makeWebhookResult(data):
    # print(json.dumps(item, indent=4))
    print("Response: " + data)
    return {
        "speech": data,
        "displayText": "Got the response",
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
