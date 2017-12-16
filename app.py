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
import utils

from flask import Flask
from flask import request
from flask import make_response
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from song_data import *
from rq import Queue
from worker import conn

q = Queue(connection=conn)

maintain_history = []



# Flask app should start in global layout
app = Flask(__name__)



#DEEPAK CODE FOR EVENT
CLIENT_ACCESS_TOKEN = '9ded4fd3df4b42b7b678b928add51dbf'


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
#    print(json.dumps(req, indent=4))
    res = utils.processRequest(req)
    res = json.dumps(res, indent=4)
    # print(res)
    r = utils.make_response(res)
    r.headers['Content-Type'] = 'application/json'
    #if not session_id:
    print("session id1")
    session_id=str(req.get("sessionId"))
    print("Session id2",session_id)
    #next_req = q.enqueue(requests.post('https://drj1.herokuapp.com/next', data = {'session_id1':session_id}))
    next_req = q.enqueue(utils.next(session_id))
    #result = q.enqueue(count_words_at_url, 'http://heroku.com')
    #time.sleep(1)
    print("queue working")
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
