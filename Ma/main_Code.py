from __future__ import unicode_literals
import queue
import threading
from tkinter import *

import lib.database as database
import lib.server as server
import lib.api as api
import lib.zym as zym
import lib.port as port
import lib.webcms as webcms
import lib.email_check as email
import lib.sql_check as sql

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.creatWidget()
        self.creatdata()

    # 创建窗口
    def creatWidget(self):

        # 创建主Frame
        self.main_frame = Frame(root)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # 标签和输入框
        self.url_label = Label(self.main_frame, text='请输入网站')
        self.url_label.pack(side="top")

        self.entry01 = Entry(self.main_frame, width=60)
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

        self.bt05 = Button(self.button_frame, text="服务器识别", width=10, command=self.scan_server)
        self.bt05.pack(side="top", padx=10, pady=10)

        self.bt06 = Button(self.button_frame,text="webcms识别",width=10,command=self.scan_webcms)
        self.bt06.pack(side="top", padx=10, pady=10)

        self.bt07 = Button(self.button_frame,text="email识别",width=10,command=self.scan_email)
        self.bt07.pack(side="top", padx=10, pady=10)

        self.bt08 = Button(self.button_frame,text="sql漏洞扫描",width=10,command=self.scan_sql)
        self.bt08.pack(side="top", padx=10, pady=10)
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
        # 存放扫描结果的队列
        self.result_queue_port = queue.Queue()
        self.result_queue_zym = queue.Queue()
        self.result_queue_api = queue.Queue()
        self.result_queue_database = queue.Queue()
        self.result_queue_server = queue.Queue()
        self.result_queue_webcms = queue.Queue()
        self.result_queue_email = queue.Queue()
        self.result_queue_sql = queue.Queue()
    #各模块的启动函数
    def start_scan(self,t_scan,result_queue):
        t_scan.start()
        def process_result():
            while True:
                try:
                    result = result_queue.get(timeout=0.1)
                except queue.Empty:
                    if not t_scan.is_alive():
                        break
                else:
                    self.w1.insert('end', result + '\n')
        t_process = threading.Thread(target=process_result)
        t_process.start()
    #扫描端口
    def scan_port(self):
        self.t_port=threading.Thread(target=port.portScan, args=(self.var01.get(),self.var02.get(),self.entry01.get(), self.result_queue_port))
        self.start_scan(self.t_port,self.result_queue_port)
    #扫描子域名
    def scan_zym(self):
        self.t_zym = threading.Thread(target=zym.zym_check, args=(self.entry01.get(), self.result_queue_zym))
        self.start_scan(self.t_zym,self.result_queue_zym)
    #扫描api
    def scan_api(self):
        self.t_api=threading.Thread(target=api.api_check, args=(self.entry01.get(), self.result_queue_api))
        self.start_scan(self.t_api,self.result_queue_api)
    #扫描数据库
    def scan_database(self):
        self.t_database=threading.Thread(target=database.database_check, args=(self.entry01.get(), self.result_queue_database))
        self.start_scan(self.t_database,self.result_queue_database)
    #扫描服务器框架
    def scan_server(self):
        self.t_server=threading.Thread(target=server.server_check, args=(self.entry01.get(), self.result_queue_server))
        self.start_scan(self.t_server,self.result_queue_server)
    #扫描网站cms
    def scan_webcms(self):
        self.t_webcms=threading.Thread(target=webcms.cmscheck, args=(self.entry01.get(), self.result_queue_webcms))
        self.start_scan(self.t_webcms,self.result_queue_webcms)
    #扫描网站email
    def scan_email(self):
        self.t_email=threading.Thread(target=email.email_check,args=(self.entry01.get(), self.result_queue_email))
        self.start_scan(self.t_email,self.result_queue_email)
    #扫描网站是否含有sql漏洞
    def scan_sql(self):
        self.t_sql=threading.Thread(target=sql.sql_check,args=(self.entry01.get(), self.result_queue_sql))
        self.start_scan(self.t_sql,self.result_queue_sql)

if __name__ == '__main__':
    root = Tk()
    root.title("信息收集")
    app = Application(master=root)
    root.mainloop()