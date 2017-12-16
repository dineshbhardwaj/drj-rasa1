##DEEPAK
def next_event(sess_id):
    print(" FINALLY NEXT")
    time.sleep(60)
    print(" FINALLY NEXT + 60")
    session_id = sess_id
    print("session id ", session_id)
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.event_request(apiai.events.Event("nextevent"))
    request.lang = 'en'  # optional, default value equal 'en'
    request.session_id = session_id
    response = request.getresponse()
    print("event response")
    print(response)    



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
    #choice_song_path = map_choices["Tera Mera Pyar Amar"]
    print("processing req 4")
    print(str(choice_song_path))
    data = "<speak> <audio src=\"" + choice_song_path + "\"> didn't get your MP3 audio file </audio> </speak>"
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
