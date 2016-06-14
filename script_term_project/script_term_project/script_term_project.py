#-------------------------------------------------------------------------#
# import
import urllib.request
import xml.etree.ElementTree as etree
import os
import mimetypes
import mysmtplib
import codecs

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
#-------------------------------------------------------------------------#


#-------------------------------------------------------------------------#
# URL을 통해 XML 파일을 만드는 객체
class GetData:
    base_url = "http://openAPI.seoul.go.kr:8088/"
    key = "5a5372614368797534336564624552/"
    file_type = "xml/"
    service = "MetroPerformanceInfo/"

    def GetXMLDataAll(self):
        for i in range(0, 21):
            start_idx = str(i * 1000 + 1) + "/"
            end_idx = str((i + 1) * 1000) + "/"
            
            url = self.base_url + self.key + self.file_type + self.service + start_idx + end_idx

            data = urllib.request.urlopen(url).read()

            file_name = "Performance_Info_" + str(i+1) + ".xml"

            f = open(file_name, "wb")
            f.write(data)
            f.close()

        
    def GetXMLDataByDate(self, date = ""):
        start_idx = "1/"
        end_idx = "100/"

        date += "/"
        
        url = self.base_url + self.key + self.file_type + self.service + start_idx + end_idx + date

        data = urllib.request.urlopen(url).read()

        #print(data)

        f = open("Performance_Info.xml", "wb")
        f.write(data)
        f.close()
#-------------------------------------------------------------------------#


#-------------------------------------------------------------------------#
# 파싱 함수
def Parse(file_name):
    tree = etree.parse(file_name)
    return tree.getroot()
#-------------------------------------------------------------------------#


#-------------------------------------------------------------------------#
# 정보 출력 함수
def PrintPerformanceInfo():
    root = Parse("Performance_Info.xml")

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
# 정보 검색 함수
def SearchPerformanceInfo(sel):
    os.system('cls')

    print("\n")

    if (sel == 1):
        date = input("\t날짜 입력 (XXXX-XX) : ")

    elif (sel == 2):
        date = input("\t날짜 입력 (XXXX-XX/XX) : ")

    get_xml_data = GetData()
    get_xml_data.GetXMLDataByDate(date)
#-------------------------------------------------------------------------#


#-------------------------------------------------------------------------#
# 이메일 전송 함수
def SendMail():
    os.system('cls')

    print("\n")
    print("\t---------------")
    print("\t 전송정보 검색")
    print("\t---------------")
    print("\t1) 월별 검색 ")
    print("\t2) 일별 검색 ")
    print("\t3) 나가기 ")
    print("\t--------------- \n")

    sel = int(input("\t선택: "))

    if (sel == 3):
        return

    SearchPerformanceInfo(sel)

    root = Parse("Performance_Info.xml")

    f = open("data.txt", "w")

    for data in root.findall("row"):
        f.write(" ----------------------------------\n")
        f.write(" 일련번호 : " + data.findtext("PSCHE_SEQ") + "\n")
        f.write(" 공연자명 : " + data.findtext("NAME") + "\n")
        f.write(" 공연내용 : " + data.findtext("CMT") + "\n")
        f.write(" 공연장소 : " + data.findtext("PLACE") + "\n")
        f.write(" 시작시간 : " + data.findtext("SDATE") + "\n")
        f.write(" 종료시간 : " + data.findtext("EDATE") + "\n")
        f.write(" ----------------------------------\n\n")

    f.close()

    # smtp 서버 주소
    smtp_host = "smtp.test.com"

    # gmail STMP 서버 주소
    host = "smtp.gmail.com"
    port = "587"
    
    file_name = "data.txt"

    send_addr = "hyunnieyoon@gmail.com"  
    recv_addr = input("\t받는 사람 : ")

    print("\n\t이메일 전송 준비 중...")
    
    msg = MIMEBase("multipart", "alternative")
    msg['Subject'] = "Performance Information"
    msg['From'] = send_addr
    msg['To'] = recv_addr
    
    # MIME 문서를 생성
    html_fd = open(file_name, "rb")

    message = html_fd.read()

    html_part = MIMEText(message, 'html', _charset = 'UTF-8')
    html_fd.close()
    
    # MIME를 MIMEBase에 첨부
    msg.attach(html_part)

    print("\t이메일 전송 중...")
    
    # 이메일 발송
    s = mysmtplib.MySMTP(host, port)
    #s.set_debuglevel(1)        
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("hyunnieyoon@gmail.com", "ekdlfprxm930")
    s.sendmail(send_addr, [recv_addr], msg.as_string())
    s.close()
#-------------------------------------------------------------------------#


#-------------------------------------------------------------------------#
# 역 이름으로 검색 함수
def SearchByStationName():
    os.system('cls')

    station_name = str(input("\t역 이름 : "))
    date = str(input("\t날짜 (XXXX-XX) : "))

    for i in range(20, 21):
        file_name = ""

        if (date == ""):
            file_name = "Performance_Info_" + str(i + 1) + ".xml"
        else:
            get_xml_data = GetData()
            get_xml_data.GetXMLDataByDate(date)

            file_name = "Performance_Info.xml"
        
        root = Parse(file_name)

        for data in root.findall("row"):
            if (str(data.findtext("PLACE")) == station_name):
                print("\t----------------------------------")
                print("\t일련번호 : ", data.findtext("PSCHE_SEQ"))
                print("\t공연자명 : ", data.findtext("NAME"))
                print("\t공연내용 : ", data.findtext("CMT"))
                print("\t공연장소 : ", data.findtext("PLACE"))
                print("\t시작시간 : ", data.findtext("SDATE"))
                print("\t종료시간 : ", data.findtext("EDATE"))
                print("\t----------------------------------")
#-------------------------------------------------------------------------#


#-------------------------------------------------------------------------#
# 공연 빈도 확인 함수
def SearchPerformanceCount():
    os.system('cls')

    print("\n\t공연빈도 계산 중...")
    
    d = {"zzz":0}

    for i in range(0, 21):
        file_name = "Performance_Info_" + str(i + 1) + ".xml"

        root = Parse(file_name)

        for data in root.findall("row"):
            station_name = data.findtext("PLACE")
            
            check = False

            for i in d.keys():
                if (i == station_name):
                    check = True
                    break

            if (check == True):
                d[station_name] += 1
            else:
                d[station_name] = 0

    most = 0
    snd = 0
    trd = 0

    first = ""
    second = ""
    third = ""
    
    for key in d.keys():
        if (most < d[key]):
            most = d[key]
            first = key

        if (snd < d[key] < most):
            snd = d[key]
            second = key

        if (trd < d[key] < snd):
            trd = d[key]
            third = key

    print("\n\t1위) " + first)
    print("\t2위) " + second)
    print("\t3위) " + third)
#-------------------------------------------------------------------------#


#-------------------------------------------------------------------------#
# 메뉴 출력 함수
def PrintMenu():
    os.system('cls')

    print("\n")
    print("\t---------------")
    print("\t1) 월별 검색 ")
    print("\t2) 일별 검색 ")
    print("\t3) 역 이름으로 검색 ")
    print("\t4) 이메일 전송 ")
    print("\t5) 역별 공연빈도 보기 ")
    print("\t9) 종료 ")
    print("\t---------------\n")
#-------------------------------------------------------------------------#


#-------------------------------------------------------------------------#
# main 함수
if __name__ == "__main__":

   #get_xml_data = GetData()
   #get_xml_data.GetXMLDataAll()

   while (True):
       PrintMenu()
       
       sel = int(input("\t선택: "))

       if (sel == 9):
           print("\n")
           break

       if (sel == 1) or (sel == 2):
           SearchPerformanceInfo(sel)
           PrintPerformanceInfo()

       elif (sel == 3):
           SearchByStationName()

       elif (sel == 4):
           SendMail()

       elif (sel == 5):
           SearchPerformanceCount()

       input("\n\t아무 키나 입력하세요. ")
#-------------------------------------------------------------------------#