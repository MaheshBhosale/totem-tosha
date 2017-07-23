import xml.etree.ElementTree as ET
tree = ET.parse('sample.xml')
root = tree.getroot()
siteID = 'CustomerTest'
password = 'alkd89nBV'
message_time = '2003-06-25T11:28:56-08:00'
message_reference = '1234567890123456789012345678'
awb_number = 4948884640 
root[0][0][0].text = message_time
root[0][0][1].text = message_reference
root[0][0][2].text = siteID
root[0][0][3].text = password
root[2].text = str(awb_number)	
tree.write('output.xml')
