import queue
import socket

PORT_1 = {80: "HTTP", 443: "HTTPS", 21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP", 110: "POP3",
                143: "IMAP",
                53: "DNS", 161: "SNMP", 162: "SNMP Trap", 389: "LDAP", 445: "Microsoft-DS", 548: "AFP",
                1080: "SOCKS", 1433: "Microsoft SQL Server", 1521: "Oracle", 3306: "MySQL", 5432: "PostgreSQL",
                5900: "VNC", 3389: "RDP", 8000: "HTTP Alternate", 8080: "HTTP Alternate",
                8443: "HTTPS Alternate",
                8888: "HTTP Alternate", 9090: "HTTP Alternate"}
# 非常用端口
PORT_2 = {17: "Quote of the Day", 79: "Finger", 873: "rsync", 1194: "OpenVPN",
                1434: "Microsoft SQL Monitor", 1701: "L2TP",
                1812: "RADIUS", 1813: "RADIUS Accounting", 2222: "DirectAdmin", 3000: "Ruby on Rails",
                3306: "MySQL Remote Administration", 3689: "iTunes", 5000: "UPnP", 5001: "UPnP Secure",
                5432: "PostgreSQL", 5901: "VNC Remote Desktop", 8000: "iRDMI", 8081: "HTTP Alternate",
                9000: "Joomla Remote Administration", 9418: "Git", 9999: "URD - Remote Desktop",
                27017: "MongoDB",
                27018: "MongoDB", 28017: "MongoDB HTTP Interface", 49152: "Reserved", 49153: "Reserved",
                49154: "Reserved", 49155: "Reserved", 49156: "Reserved", 49157: "Reserved"}
# 扫描端口模块
def portScan(check1,check2,url, result_queue):
    q = queue.Queue()
    ip = url
    if check1 == 1:
        result_queue.put("开始扫描常用端口...")
        for port in PORT_1.keys():
            q.put(port)  # 队尾插入
        while not q.empty():
            port = q.get()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            try:
                s.connect((ip, port))
                result_queue.put("%s:%s open [%s]" % (ip, port, PORT_1[port]))
            except:
                result_queue.put("%s:%s Close" % (ip, port))
            finally:
                s.close()
    if check2 == 1:
        result_queue.put("开始扫描非常用端口...")
        for port in PORT_2.keys():
            q.put(port)  # 队尾插入
        while not q.empty():
            port = q.get()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            try:
                s.connect((ip, port))
                result_queue.put("%s:%s open [%s]" % (ip, port, PORT_2[port]))
            except:
                result_queue.put("%s:%s Close" % (ip, port))
            finally:
                s.close()
    if check1 == 0 and check2 == 0:
        result_queue.put("请选择扫描选项！")
    else:
        result_queue.put('[portScan] The scan is complete!')