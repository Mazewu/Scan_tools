from __future__ import unicode_literals
import queue
import socket
import sys
import threading
import requests
from tkinter import *
from tkinter import messagebox
import database


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.creatdata()
        self.creatWidget()

    # 创建窗口
    def creatWidget(self):

        # 创建主Frame
        self.main_frame = Frame(root)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # 标签和输入框
        self.url_label = Label(self.main_frame, text='请输入网站')
        self.url_label.pack(side="top")

        self.entry01 = Entry(self.main_frame, width=40)
        self.entry01.pack(side="top", padx=10, pady=10)

        # 按钮
        self.button_frame = Frame(self.main_frame)
        self.button_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        self.bt01 = Button(self.button_frame, text="端口扫描", width=10, command=self.scan_port)
        self.bt01.pack(side="top", padx=10, pady=10)

        self.var01 = IntVar()
        self.checkbutton01 = Checkbutton(self.button_frame, text='  常用端口', variable=self.var01)
        self.checkbutton01.pack(padx=10, pady=10, side="top")

        self.var02 = IntVar()
        self.checkbutton02 = Checkbutton(self.button_frame, text='非常用端口', variable=self.var02)
        self.checkbutton02.pack(padx=10, pady=10, side="top")

        self.bt02 = Button(self.button_frame, text="子域名扫描", width=10, command=self.scan_zym)
        self.bt02.pack(side="top", padx=10, pady=10)

        self.bt03 = Button(self.button_frame, text="api扫描", width=10, command=self.scan_api)
        self.bt03.pack(side="top", padx=10, pady=10)

        self.bt04 = Button(self.button_frame, text="数据库识别", width=10, command=self.scan_database)
        self.bt04.pack(side="top", padx=10, pady=10)

        # 文本框和滚动条
        self.text_frame = Frame(self.main_frame)
        self.text_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        self.res_label = Label(self.text_frame, text='扫描结果')
        self.res_label.pack(side="top")

        self.scrollbar = Scrollbar(self.text_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.w1 = Text(self.text_frame, width=80, height=20, yscrollcommand=self.scrollbar.set)
        self.w1.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.w1.yview)

    def creatdata(self):
        # 扫描结果队列
        self.result_queue_port = queue.Queue()
        self.result_queue_zym = queue.Queue()
        self.result_queue_api = queue.Queue()
        self.result_queue_database = queue.Queue()

        # 端口扫描需要的数据
        # 常用端口
        self.PORT_1 = {80: "HTTP", 443: "HTTPS", 21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP", 110: "POP3",
                       143: "IMAP",
                       53: "DNS", 161: "SNMP", 162: "SNMP Trap", 389: "LDAP", 445: "Microsoft-DS", 548: "AFP",
                       1080: "SOCKS", 1433: "Microsoft SQL Server", 1521: "Oracle", 3306: "MySQL", 5432: "PostgreSQL",
                       5900: "VNC", 3389: "RDP", 8000: "HTTP Alternate", 8080: "HTTP Alternate",
                       8443: "HTTPS Alternate",
                       8888: "HTTP Alternate", 9090: "HTTP Alternate"}
        # 非常用端口
        self.PORT_2 = {17: "Quote of the Day", 79: "Finger", 873: "rsync", 1194: "OpenVPN",
                       1434: "Microsoft SQL Monitor", 1701: "L2TP",
                       1812: "RADIUS", 1813: "RADIUS Accounting", 2222: "DirectAdmin", 3000: "Ruby on Rails",
                       3306: "MySQL Remote Administration", 3689: "iTunes", 5000: "UPnP", 5001: "UPnP Secure",
                       5432: "PostgreSQL", 5901: "VNC Remote Desktop", 8000: "iRDMI", 8081: "HTTP Alternate",
                       9000: "Joomla Remote Administration", 9418: "Git", 9999: "URD - Remote Desktop",
                       27017: "MongoDB",
                       27018: "MongoDB", 28017: "MongoDB HTTP Interface", 49152: "Reserved", 49153: "Reserved",
                       49154: "Reserved", 49155: "Reserved", 49156: "Reserved", 49157: "Reserved"}

    # 扫描端口模块
    def portScan(self, url, result_queue):
        self.q = queue.Queue()
        self.ip = url
        if self.var01.get() == 1:
            result_queue.put("开始扫描常用端口！")
            for port in self.PORT_1.keys():
                self.q.put(port)  # 队尾插入
            while not self.q.empty():
                port = self.q.get()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                try:
                    s.connect((self.ip, port))
                    result_queue.put("%s:%s open [%s]" % (self.ip, port, self.PORT_1[port]))
                except:
                    result_queue.put("%s:%s Close" % (self.ip, port))
                finally:
                    s.close()
        if self.var02.get() == 1:
            result_queue.put("开始扫描非常用端口！")
            for port in self.PORT_2.keys():
                self.q.put(port)  # 队尾插入
            while not self.q.empty():
                port = self.q.get()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                try:
                    s.connect((self.ip, port))
                    result_queue.put("%s:%s open [%s]" % (self.ip, port, self.PORT_2[port]))
                except:
                    result_queue.put("%s:%s Close" % (self.ip, port))
                finally:
                    s.close()
        if self.var01.get() == 0 and self.var02.get() == 0:
            result_queue.put("请选择扫描选项！")
        else:
            result_queue.put('[portScan] The scan is complete!')

    def scan_port(self):
        t_scan = threading.Thread(target=self.portScan, args=(self.entry01.get(), self.result_queue_port))
        t_scan.start()

        def process_result():
            while True:
                try:
                    result = self.result_queue_port.get(timeout=0.1)
                except queue.Empty:
                    if not t_scan.is_alive():
                        break
                else:
                    self.w1.insert('end', result + '\n')

        t_process = threading.Thread(target=process_result)
        t_process.start()

    # 扫描子域名模块
    def zym_check(self, url, result_queue):
        result_queue.put('开始扫描网站子域名！')
        urls = url.replace('www', '')
        for zym_data in open("Ma/sub11.txt", encoding='utf-8'):
            zym_data = zym_data.replace('\n', '')
            url = zym_data + urls
            try:
                ip = socket.gethostbyname(url)
                result_queue.put(url + ' -> ' + ip)
            except Exception as e:
                pass
        result_queue.put('[zym_check] The scan is complete!')

    def scan_zym(self):
        t_scan = threading.Thread(target=self.zym_check, args=(self.entry01.get(), self.result_queue_zym))
        t_scan.start()

        def process_result():
            while True:
                try:
                    result = self.result_queue_zym.get(timeout=0.1)
                except queue.Empty:
                    if not t_scan.is_alive():
                        break
                else:
                    self.w1.insert('end', result + '\n')

        t_process = threading.Thread(target=process_result)
        t_process.start()

    # 扫描api模块
    def api_check(self, url, result_queue):
        result_queue.put('开始扫描网站api模块！')
        api_list = []
        for api_data in open(r'Ma/api.txt', encoding='utf-8'):
            api_data = api_data.replace('\n', '')
            Url = self.entry01.get()
            url = 'https://' + Url + api_data
            api_list.append(url)
            r = requests.get(url)
            if r.status_code == 200:
                status = '该网址存在'
                result_queue.put(url + ' ' + status)
                with open('Ma/api9.csv', 'w', encoding='gbk') as f:
                    for line in api_list:
                        f.write(line.strip() + '\n')
            else:
                status = '该网址不存在'
        result_queue.put('[api_check] The scan is complete!')

    def scan_api(self):
        t_scan = threading.Thread(target=self.api_check, args=(self.entry01.get(), self.result_queue_api))
        t_scan.start()

        def process_result():
            while True:
                try:
                    result = self.result_queue_api.get(timeout=0.1)
                except queue.Empty:
                    if not t_scan.is_alive():
                        break
                else:
                    self.w1.insert('end', result + '\n')

        t_process = threading.Thread(target=process_result)
        t_process.start()

    # 扫描数据库模块
    def database_check(self, url, result_queque):
        # 解析网址
        ext = database.tldextract.extract(url)
        host = database.get_host(url)
        result_queque.put("开始识别网站数据库！")
        # 尝试连接到MySQL数据库
        db_type = database.try_mysql(host, "root", "", ext.domain)
        if db_type:
            result_queque.put(f"The database type for {url} is {db_type}")
            result_queque.put('[database_check] The scan is complete!')
            return
        # 尝试连接到PostgreSQL数据库
        db_type = database.try_postgresql(host, "postgres", "", ext.domain)
        if db_type:
            result_queque.put(f"The database type for {url} is {db_type}")
            result_queque.put('[database_check] The scan is complete!')
            return
        # 尝试连接到SQLite数据库
        db_type = database.try_sqlite(host, "", "", ext.domain + ".db")
        if db_type:
            result_queque.put(f"The database type for {url} is {db_type}")
            result_queque.put('[database_check] The scan is complete!')
            return
        # 尝试连接到Oracle数据库
        db_type = database.try_oracle(host, "system", "oracle", "xe")
        if db_type:
            result_queque.put(f"The database type for {url} is {db_type}")
            result_queque.put('[database_check] The scan is complete!')
            return
        # 返回未知类型
        result_queque.put(f"The database type for {url} is Unknown")
        result_queque.put('[database_check] The scan is complete!')

    def scan_database(self):
        t_scan = threading.Thread(target=self.database_check, args=(self.entry01.get(), self.result_queue_database))
        t_scan.start()

        def process_result():
            while True:
                try:
                    result = self.result_queue_database.get(timeout=0.1)
                except queue.Empty:
                    if not t_scan.is_alive():
                        break
                else:

                    self.w1.insert('end', result + '\n')

        t_process = threading.Thread(target=process_result)
        t_process.start()


def on_closing():
    root.destroy()
    sys.exit()


if __name__ == '__main__':
    root = Tk()
    root.title("信息收集")
    app = Application(master=root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()