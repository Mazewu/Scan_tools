from urllib.parse import urlparse
import socket

def gethostbyname(url):
    domain = urlparse(url)
    # domain.netloc
    if domain.netloc is None:
        return None
    ip = socket.gethostbyname(domain.netloc)
    return ip

def qurlparse(url):
    domain = urlparse(url)
    # domain.netloc
    if domain.netloc is None:
        return None
    return domain.netloc
