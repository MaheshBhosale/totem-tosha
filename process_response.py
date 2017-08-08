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
                show_pieces(cur_AWBInfo_element)
            elif piece_enabled == 'b':
                show_shippment(cur_AWBInfo_element)
            else:
                show_pieces(cur_AWBInfo_element)
                show_shippment(cur_AWBInfo_elemen)

    def show_pieces(self, cur_AWBInfo_element):

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
