import xml.etree.ElementTree as ET
import requests

HOST = "https://xmlpitest-ea.dhl.com"
API_URL = "/XMLShippingServlet"


def do_request():
    #tree = ET.parse('./output.xml')
    request = open("./output.xml", "r").read()
    #xml_string = str(request)
    url=HOST+API_URL
    req = requests.post(url, data=request, headers={'Content-Type': 'application/xml-www-form-urlencoded'})
    print(req.text)
    speech = process(req)
    

def process(req):
    root = ET.fromstring(req.content)
    speech = "tracking information for AWB no:" + (root[1][0].text) + "\n"
    if root[1][1][0].text != 'success':
        specch += "No shipment data found\nPlease check your AWB number and try again"
        return
    speech += "Shippment information:\n"
    speech += "Shipment started at " + root[1][2][0][0].text +" " + root[1][2][0][1].text + "\n"
    speech += "Shipment ended at " + root[1][2][1][0].text +" " + root[1][2][1][1].text + "\n"
    speech += "Shippers name is " + root[1][2][2].text + "\n"
    speech += "Consignee name is " + root[1][2][4].text + "\n"
    speech += "Shipped on " + root[1][2][5].text + "\n"  
 
do_request()
