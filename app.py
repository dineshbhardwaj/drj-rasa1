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
import io

from flask import Flask
from flask import request
from flask import make_response

from utils import next_event


maintain_history = []
max_song_num=5



# Flask app should start in global layout
app = Flask(__name__)



@app.route('/webhook', methods=['POST'])
def webhook():
    print("start req")
    mydata=request.data
    print(mydata)
    req_open = Request("http://ec2-54-197-17-247.compute-1.amazonaws.com",mydata)
    #req_open = urlopen('http://ec2-54-197-17-247.compute-1.amazonaws.com')
    print("start req 1")
    f = io.TextIOWrapper(req_open,encoding='utf-8')
    print("start req 2")
    req=f.read()
    print("done req")
    print(req)
    res = makeWebhookResult(str(req))
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    #if not session_id:
    return r



def makeWebhookResult(data):
    # print(json.dumps(item, indent=4))
    print("Response: " + data)
    return {
        "speech": data,
        "displayText": "Got the response"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
