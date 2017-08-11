#!/usr/bin/env python
 
import urllib
import json
import os
 
from flask import Flask
from flask import request
from flask import make_response
from datetime import datetime
import xml.etree.ElementTree as ET
import requests

from process_response import Processor

HOST = "https://xmlpitest-ea.dhl.com"
API_URL = "/XMLShippingServlet"
awb = 0
# Flask app should start in global layout
app = Flask(__name__)
 
 
@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)
 
    print("Request:")
    print(json.dumps(req, indent=4))
 
    res = makeWebhookResult(req)
 
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
 
def makeWebhookResult(req):
    result = req.get("result")
    parameters = result.get("parameters")
    track_id = parameters.get("track-id")
    xml_generate(track_id)
    text, speech = do_request()
    print("Response:")
 
    return {
         "speech": speech,
         "displayText": text,
         #"data": {},
         # "contextOut": [],
         "source": "apiai-onlinestore-shipping"
    }

def do_request():
    request = open("./output.xml", "r").read()
    print(request)
    url=HOST+API_URL
    req = requests.post(url, data=request, headers={'Content-Type': 'application/xml-www-form-urlencoded'})
    with open('./result.xml', 'w') as f:
        f.write(req.text)
    processor = Processor("./result.xml")
    text, speech = processor.process_withAWBNumber(awb, 's', 'yes')
    return text, speech


def xml_generate(track_id):
    tree = ET.parse('sample.xml')
    root = tree.getroot()
    siteID = 'DServiceVal'
    password = 'testServVal'
    naive_dt = datetime.now()
    message_time = '2003-06-25T11:28:56-08:00'
    message_reference = '1234567890123456789012345678'
    awb_number = track_id 
    root[0][0][0].text = message_time
    root[0][0][1].text = message_reference
    root[0][0][2].text = siteID
    root[0][0][3].text = password
    global awb
    awb = awb_number
    root[2].text = str(awb_number)	
    tree.write('output.xml')

@app.route('/update', methods=['POST'])
def update():
    res = {
        "speech": "Sample speech",
        "displayText": "Sample Text",
        # "data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port"+ str(port))
    app.run(debug=True, port=port, host='0.0.0.0')