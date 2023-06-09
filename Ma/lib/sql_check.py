import re, random,queue
import lib.Download as Download


class spider:
    def run(self, url,result_queue):
        if not url.startswith("http://"):
            url = "http://"+url
        if (url.find("?")==-1):
            result_queue.put("扫描失败！")
            result_queue.put("请输入类似的url:http://www.example.com/index.php?id=1")
            return False
        Downloader = Download.Download()
        BOOLEAN_TESTS = (" AND %d=%d", " OR NOT (%d=%d)")
        DBMS_ERRORS = {  # regular expressions used for DBMS recognition based on error message response
            "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"valid MySQL result", r"MySqlClient\."),
            "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"valid PostgreSQL result", r"Npgsql\."),
            "Microsoft SQL Server": (
            r"Driver.* SQL[\-\_\ ]*Server", r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*mssql_.*",
            r"(\W|\A)SQL Server.*[0-9a-fA-F]{8}", r"(?s)Exception.*\WSystem\.Data\.SqlClient\.",
            r"(?s)Exception.*\WRoadhouse\.Cms\."),
            "Microsoft Access": (r"Microsoft Access Driver", r"JET Database Engine", r"Access Database Engine"),
            "Oracle": (r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Oracle.*Driver", r"Warning.*\Woci_.*",
                       r"Warning.*\Wora_.*"),
            "IBM DB2": (r"CLI Driver.*DB2", r"DB2 SQL error", r"\bdb2_\w+\("),
            "SQLite": (
            r"SQLite/JDBCDriver", r"SQLite.Exception", r"System.Data.SQLite.SQLiteException", r"Warning.*sqlite_.*",
            r"Warning.*SQLite3::", r"\[SQLITE_ERROR\]"),
            "Sybase": (r"(?i)Warning.*sybase.*", r"Sybase message", r"Sybase.*Server message.*"),
        }
        _url = url + "%29%28%22%27"
        _content = Downloader.get(_url)
        for (dbms, regex) in ((dbms, regex) for dbms in DBMS_ERRORS for regex in DBMS_ERRORS[dbms]):
            if re.search(regex, str(_content)):
                result_queue.put("sql fonud")
                return True
        content = {"origin": Downloader.get(_url)}
        for test_payload in BOOLEAN_TESTS:
            RANDINT = random.randint(1, 255)
            _url = url + test_payload % (RANDINT, RANDINT)
            content["true"] = Downloader.get(_url)
            _url = url + test_payload % (RANDINT, RANDINT + 1)
            content["false"] = Downloader.get(_url)
            if content["origin"] == content["true"] != content["false"]:
                result_queue.put("sql fonud: %" % url)
                return "sql fonud: %" % url
        result_queue.put("sql not fonud")
def sql_check(url,result_queue):
    result_queue.put("开始扫描sql漏洞...")
    t = spider()
    t.run(url,result_queue)