# Challenge Name

## Metadata

| Field | Value |
| --- | --- |
| Category | `crypto` / `web` / `pwn` / `rev` / `forensics` / `misc` |
| Difficulty | Easy / Medium / Hard |
| Points | 000 |
| Solves | 000 |
| First Blood | name / N/A |

## Challenge Description

Paste or paraphrase the challenge description.

```text
Original challenge text here.
```

## Artifacts

List the provided files, passwords, extracted sources, services, and local helper
scripts used during the solve.

```text
public.zip
extracted/app.py
solve.py
```

## Recon

Explain the first pass through the artifact. This section should show how the
challenge was classified before naming the vulnerability.

- Entry points, routes, binaries, protocols, or file formats.
- Important imports, libraries, constants, or configuration.
- Security boundary: what normal users can do, and what the flag requires.

## Vulnerability

Explain the vulnerable behavior and the reasoning that led to it.

- Suspicious artifact or code snippet.
- Search terms or references used to confirm the idea.
- Why the behavior breaks the expected security property.

```python
# Minimal vulnerable snippet
```

## Exploitation

Give a step-by-step chain from first primitive to flag.

1. Collect or trigger the primitive.
2. Transform it into useful data.
3. Build the exploit payload.
4. Submit the final payload.
5. Confirm the flag.

Include real commands and representative output.

```bash
curl -s "$BASE_URL/endpoint"
python solve.py "$BASE_URL"
```

## Technical Details

Use this section for math, protocol internals, memory layout, crypto formulas,
or source-to-sink reasoning. Keep it tied to the actual exploit.

## Exploit Artifact

Describe the final script, important functions, and how to run it.

```bash
python solve.py "$BASE_URL"
```

## Validation

Show local and remote validation.

```text
local output
remote output
```

## References

- <https://example.com/reference-1>
- <https://example.com/reference-2>

## Flag

```text
flag{...}
```
