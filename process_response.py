import xml.etree.ElementTree as ET
import xmltodict

class Processor:
    def process_withAWBNumber(self, awb_number, piece_enabled):
        response_path = './UnitTestPlan/Tracking/Response/SingleknownTrackResponse-no-data-found.xml'
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
                    if int(AWBInfo_element['AWBNumber']) == awb_number:
                        st = AWBInfo_element['Status']
                        break
                if st == None:
                    print("Tracking request failed\n" + "Please check your AWBNumber")
                    return
            else:
                st = root['AWBInfo']['Status']
            if st['ActionStatus'] != "Success":
                print("Tracking request failed\n"+st['Condition']['ConditionData'])
                return
            else:
                print(("Tracking request is Successful for ")+str(awb_number))

            if piece_enabled == 'p':
                self.show_pieces(cur_AWBInfo_element)
            elif piece_enabled == 's':
                self.show_shippment(cur_AWBInfo_element)
            else:
                self.show_pieces(cur_AWBInfo_element)
                self.show_shippment(cur_AWBInfo_element)

    def show_pieces(self, cur_AWBInfo_element):
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

    def show_shippment(self, cur_AWBInfo_element):
        shipmentinfo = cur_AWBInfo_element['ShipmentInfo']
        print("Shipment informatyion is given below for your package\n Origin Service area :"+
              shipmentinfo["OriginServiceArea"]["Description"]+"\nDestination Service area :"+
              shipmentinfo["DestinationServiceArea"]["Description"]+"\nShipper name is :"+shipmentinfo["ShipperName"]+
              "\nDate of shipment is "+shipmentinfo["ShipmentDate"])
        if 'EstDlvyDate' in shipmentinfo:
            print("\nEstimated date of delivery is"+shipmentinfo['EstDlvyDate'])

    def process_withLPNumber(self, lp_number):
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
                    if AWBInfo_element['TrackedBy'] != None:
                        if int(AWBInfo_element['TrackedBy']['LPNumber']) == lp_number:
                            st = AWBInfo_element['Status']
                            break
                    else:
                        print("LPNumber doesnot exists")
                if st == None:
                    print("Tracking request failed\n" + "Please check your AWBNumber")
                    return
            else:
                st = root['AWBInfo']['Status']
            if st['ActionStatus'] != "Success":
                print("Tracking request failed\n" + st['Condition']['ConditionData'])
                return
            else:
                print(("Tracking request is Successful for ") + str(lp_number))

    def __init__(self, response_path):
        self.response_path = response_path


processor = Processor('./UnitTestPlan/Tracking/Response/SingleknownTrackResponse-no-data-found.xml')
processor.process_withAWBNumber(123444444, 'p')
