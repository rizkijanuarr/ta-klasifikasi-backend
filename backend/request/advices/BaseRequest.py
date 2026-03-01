import re
from typing import Tuple

URL_REGEX = re.compile(
    r"^(https?:\/\/)?"  
    r"([\w.-]+)"         
    r"(\:[0-9]+)?"      
    r"(\/.*)?$"      
)

def validate_url(url: str) -> Tuple[bool, str]:
    if not url:
        return False, ""
    url = url.strip()
    if not URL_REGEX.match(url):
        return False, url
    if not url.startswith("http"):
        url = "http://" + url
    return True, url
