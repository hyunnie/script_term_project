#-------------------------------------------------------------------------#
# import
import urllib.request
import xml.etree.ElementTree as etree
import os
#-------------------------------------------------------------------------#


#-------------------------------------------------------------------------#
# URL을 통해 XML 파일을 만드는 객체
class GetData:
    base_url = "http://openAPI.seoul.go.kr:8088/"
    key = "5a5372614368797534336564624552/"
    file_type = "xml/"
    service = "MetroPerformanceInfo/"
    start_idx = "1/"
    end_idx = "5/"
    date = "2016-06/"

    url = base_url + key + file_type + service + start_idx + end_idx + date

    def GetXMLDataByURL(self):
        data = urllib.request.urlopen(self.url).read()

        #print(data)

        f = open("Performance_Info.xml", "wb")
        f.write(data)
        f.close()
#-------------------------------------------------------------------------#


#-------------------------------------------------------------------------#
# 파싱 및 정보 출력 함수
def PrintPerformanceInfo():
    tree = etree.parse("Performance_Info.xml")
    root = tree.getroot()

    print("\n")

    for data in root.findall("row"):
        print("\t----------------------------------")
        print("\t일련번호 : ", data.findtext("PSCHE_SEQ"))
        print("\t공연자명 : ", data.findtext("NAME"))
        print("\t공연내용 : ", data.findtext("CMT"))
        print("\t공연장소 : ", data.findtext("PLACE"))
        print("\t시작시간 : ", data.findtext("SDATE"))
        print("\t종료시간 : ", data.findtext("EDATE"))
        print("\t----------------------------------")

    print("\n")
#-------------------------------------------------------------------------#


#-------------------------------------------------------------------------#
# main 함수
if __name__ == "__main__":
    get_xml_data = GetData()
    get_xml_data.GetXMLDataByURL()

    PrintPerformanceInfo()
#-------------------------------------------------------------------------#