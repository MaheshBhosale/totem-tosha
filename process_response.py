import xml.etree.ElementTree as ET
import xmltodict

class Processor:
    def process_withAWBNumber(self, awb_number, piece_enabled, more_info):
        response_path = './UnitTestPlan/Tracking/Response/TrackingResponse_SingleAWB_CheckpointWithEventRemarks.xml'
        print(response_path)
        tree = ET.parse(response_path)
        st = None
        with open('/home/mahesh/Mahesh/heroku-basic-flask/UnitTestPlan/Tracking/Response/TrackingResponse_SingleAWB_CheckpointWithEventRemarks.xml') as fd:
            doc = xmltodict.parse(fd.read())
            if 'res:TrackingResponse' in doc:
                root = doc['res:TrackingResponse']
            elif 'req:TrackingResponse' in doc:
                root = doc['req:TrackingResponse']
            print(root['AWBInfo'])
            if type(root['AWBInfo']) == list:
                l = root['AWBInfo']
                for AWBInfo_element in l:
                    cur_AWBInfo_element = AWBInfo_element
                    if int(AWBInfo_element['AWBNumber']) == awb_number:
                        st = AWBInfo_element['Status']
                        break
                if st == None:
                    self.response += "Tracking request failed\n" + "Please check your AWBNumber"
                    return self.response
            else:
                st = root['AWBInfo']['Status']
            if str(st['ActionStatus']) != "Success" and str(st['ActionStatus']) != "success":
                self.response += "Tracking request failed\n"+str(st['Condition']['ConditionData'])
                return self.response
            else:
                self.response += "Tracking request is Successful for "+str(awb_number)

            if piece_enabled == 'p':
                self.show_pieces(cur_AWBInfo_element, more_info)
            elif piece_enabled == 's':
                self.show_shippment(cur_AWBInfo_element, more_info)
            else:
                self.show_pieces(cur_AWBInfo_element, more_info)
                self.show_shippment(cur_AWBInfo_element, more_info)

    def show_pieces(self, cur_AWBInfo_element, more_info):
        pieces = cur_AWBInfo_element['Pieces']
        if type(pieces['PieceInfo']) == list:
            l = pieces['PieceInfo']
            for pieces_Info in l:
                piece_details = pieces_Info['PieceDetails']
                print("Piece details for peices are as follows,\n")
                print("Depth of you package is "+piece_details['ActualDepth']+"\nWidth of the package is "+
                      piece_details['ActualWidth']+"Height of you package is "+piece_details['ActualHeight'] +
                      "Weight of you package is "+piece_details['ActualWeight']+piece_details["'WeightUnit"])
        else:
            pieces_Info = pieces['PieceInfo']
            piece_details = pieces_Info['PieceDetails']
            print("Piece details for peices are as follows,\n")
            print("Depth of you package is " + piece_details['ActualDepth'] + "\nWidth of the package is " +
                  piece_details['ActualWidth'] + "Height of you package is " + piece_details['ActualHeight'] +
                  "Weight of you package is " + piece_details['ActualWeight'] + piece_details["'WeightUnit"])

    def show_shippment(self, cur_AWBInfo_element, more_info):
        shipmentinfo = cur_AWBInfo_element['ShipmentInfo']
        self.response += "Shipper name is :"+str(shipmentinfo["ShipperName"])+"\nDate of shipment is "+ (shipmentinfo["ShipmentDate"])
        if 'EstDlvyDate' in shipmentinfo:
            self.response += "\nEstimated date of delivery is"+str(shipmentinfo['EstDlvyDate'])
        if more_info == "yes":
            l = shipmentinfo['ShipmentEvent']
            i = 1
            for shipment_event in l:
                self.response += i + "Date:" + str(shipment_event['Date']) + "Time:" + str(shipment_event['Time']) + " " + str(shipment_event['ServiceEvent']['Description'])
                i += 1

    def process_withLPNumber(self, lp_number, piece_enabled, more_info):
        response_path = './UnitTestPlan/Tracking/Response/TrackingResponse_SingleLP_PieceEnabled_B_1.xml'
        tree = ET.parse(response_path)
        root = tree.getroot()
        st = None
        with open('./UnitTestPlan/Tracking/Response/SingleknownTrackResponse-no-data-found.xml') as fd:
            doc = xmltodict.parse(fd.read())
            root = doc['res:TrackingResponse']
            if type(root['AWBInfo']) == list:
                l = root['AWBInfo']
                for AWBInfo_element in l:
                    cur_AWBInfo_element = AWBInfo_element
                    if AWBInfo_element['TrackedBy'] != None:
                        if int(AWBInfo_element['TrackedBy']['LPNumber']) == lp_number:
                            st = AWBInfo_element['Status']
                            break
                    else:
                        self.response += "LPNumber doesnot exists"
                if st == None:
                    self.response += "Tracking request failed\n" + "Please check your AWBNumber"
                    return
            else:
                st = root['AWBInfo']['Status']
            if st['ActionStatus'] != "Success":
                self.response += "Tracking request failed\n" + str(st['Condition']['ConditionData'])
                return
            else:
                self.response += "Tracking request is Successful for " + str(lp_number)
            if piece_enabled == 'p':
                self.show_pieces(cur_AWBInfo_element, more_info)
            elif piece_enabled == 's':
                self.show_shippment(cur_AWBInfo_element, more_info)
            else:
                self.show_pieces(cur_AWBInfo_element, more_info)
                self.show_shippment(cur_AWBInfo_element, more_info)


    def __init__(self, response_path):
        self.response_path = response_path
        self.response = ""
        self.more_response = ""


processor = Processor('./UnitTestPlan/Tracking/Response/TrackingResponse_SingleAWB_CheckpointWithEventRemarks.xml')
processor.process_withAWBNumber(6372653501, 's', 'yes')
