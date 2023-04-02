import sys 
from lib.Download import Download
from urllib.parse import urlparse
DIR_PROBE_EXTS = ['.tar.gz', '.zip', '.rar', '.tar.bz2']
FILE_PROBE_EXTS = ['.bak', '.swp', '.1']
download = Download()

def get_parent_paths(path):
    paths = []
    if not path or path[0] != '/':
        return paths
    paths.append(path)
    tph = path
    if path[-1] == '/':
        tph = path[:-1]
    while tph:
        tph = tph[:tph.rfind('/')+1]
        paths.append(tph)
        tph = tph[:-1]
    return paths
class spider:
    def run(self, url,html,result_queue):
        pr = urlparse(url)
        paths = get_parent_paths(pr.path)
        web_paths = []
        for p in paths:
            if p == "/":
                for ext in DIR_PROBE_EXTS:
                    u = '%s://%s%s%s' % (pr.scheme, pr.netloc, p, pr.netloc+ext)
                    web_paths.append(u)
            else:
                if p[-1] == '/':
                    for ext in DIR_PROBE_EXTS:
                        u = '%s://%s%s%s' % (pr.scheme, pr.netloc, p[:-1], ext)
                        web_paths.append(u)
                else:
                    for ext in FILE_PROBE_EXTS:
                        u = '%s://%s%s%s' % (pr.scheme, pr.netloc, p, ext)
                        web_paths.append(u)
        for path in web_paths:
            result_queue.put("[web path]:%s" %path)
            print("[web path]:%s" %path)
            if download.get(path) is not None:
                result_queue.put("[+] bak file has found :%s" % path)
                print("[+] bak file has found :%s" % path)
                return False
        return False