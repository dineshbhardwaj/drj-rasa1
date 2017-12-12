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

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    song1=re.compile('[tT]era.[mM]era*[sS]ong')
    song2=re.compile('[tT]ujhse [Nn]ara[jz].*[sS]ong')
    song3=re.compile('[tT]ere.*[Bb][ei]+n[a]+.*[sS]ong')
    song4=re.compile('[Kk]yon[ ]*[kK][ei].*[iI]tna.*[sS]ong')
    input_data = str(req.get("result").get("resolvedQuery"))
    if re.search(song1,input_data) :
        data = "<speak> <audio src=\"https://drj1.000webhostapp.com/tera.mp3\"> didn't get your MP3 audio file </audio> </speak>"
    elif re.search(song2,input_data) :
        data = "<speak> <audio src=\"https://drj1.000webhostapp.com/tujhse_naraaz_nahin_zindagi__male__-_masoom_songs_-__naseeruddin_shah_-_jugal_hansraj__-_filmigaane.mp3\"> didn't get your MP3 audio file </audio> </speak>"
    elif re.search(song3,input_data) :
        data = "<speak> <audio src=\"https://drj1.000webhostapp.com/bina.mp3\"> didn't get your MP3 audio file </audio> </speak>"
    elif re.search(song4,input_data) :
        data = "<speak> <audio src=\"https://drj1.000webhostapp.com/kyonki.mp3\"> didn't get your MP3 audio file </audio> </speak>"
    else :
        data = input_data        
    #if req.get("result").get("resolvedQuery") != "":
    #    return req.get("result").get("resolvedQuery")
    #baseurl = "https://query.yahooapis.com/v1/public/yql?"
    #yql_query = makeYqlQuery(req)
    #if yql_query is None:
    #    return {}
    #yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    #result = urlopen(yql_url).read()
    #data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    # print(json.dumps(item, indent=4))

    speech = "Response is fantastic " 
    print("Response:")
    print(speech)

    return {
        "speech": data,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
