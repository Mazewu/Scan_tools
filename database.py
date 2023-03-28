import tldextract
import socket
import urllib.parse
import pymysql
import psycopg2
import sqlite3
import pyodbc

# 从网址解析主机地址
def get_host(url):
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc.split(":")[0]

# 尝试连接到MySQL数据库
def try_mysql(host, user, password, database):
    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        return "MySQL"
    except:
        pass

# 尝试连接到PostgreSQL数据库
def try_postgresql(host, user, password, database):
    try:
        conn = psycopg2.connect(host=host, user=user, password=password, database=database)
        return "PostgreSQL"
    except:
        pass

# 尝试连接到SQLite数据库
def try_sqlite(host, user, password, database):
    try:
        conn = sqlite3.connect(database)
        return "SQLite"
    except:
        pass

# 尝试连接到Oracle数据库
def try_oracle(host, user, password, database):
    try:
        conn_str = 'DRIVER={Oracle in XE};DBQ=' + host + ':1521/' + database + ';Uid=' + user + ';Pwd=' + password + ';'
        conn = pyodbc.connect(conn_str)
        return "Oracle"
    except:
        pass

# 根据网址获取数据库信息
def identify_database(url):
    # 解析网址
    ext = tldextract.extract(url)
    host = get_host(url)

    # 尝试连接到MySQL数据库
    db_type = try_mysql(host, "root", "", ext.domain)
    if db_type:
        return db_type

    # 尝试连接到PostgreSQL数据库
    db_type = try_postgresql(host, "postgres", "", ext.domain)
    if db_type:
        return db_type

    # 尝试连接到SQLite数据库
    db_type = try_sqlite(host, "", "", ext.domain + ".db")
    if db_type:
        return db_type

    # 尝试连接到Oracle数据库
    db_type = try_oracle(host, "system", "oracle", "xe")
    if db_type:
        return db_type

    # 返回未知类型
    return "Unknown"

# 测试程序
if __name__ == "__main__":
    url = "www.sian.com"
    db_type = identify_database(url)
    print(f"The database type for {url} is {db_type}")
