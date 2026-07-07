# Deadbolt

## Metadata

| Field | Value |
| --- | --- |
| Category | `mobile` |
| Difficulty | Hard |
| Points | 100 |
| Solves | 97 |
| First Blood | Redz |

## Challenge Description

```text
FluidVault is a mobile password manager. Biometrics, AES-256-GCM, the works.

You walked away with:
Decompiled Java sources from the APK
An encrypted vault backup (vault_backup.enc)
A decryption helper script (vault_decrypt.py)

No device or emulator required.
```

Target used during validation:

```text
https://cf6e095154604ced.chal.ctf.ae
```

## Artifacts

The provided archive was:

```text
public.zip
```

The extracted files used during the solve were:

```text
extracted/vault_backup.enc
extracted/vault_decrypt.py
extracted/decompiled/AndroidManifest.xml
extracted/decompiled/com/fluidvault/crypto/CryptoManager.java
extracted/decompiled/com/fluidvault/auth/BiometricAuthManager.java
extracted/decompiled/com/fluidvault/network/VaultApiClient.java
extracted/decompiled/com/fluidvault/data/VaultContentProvider.java
extracted/decompiled/com/fluidvault/ui/LoginActivity.java
```

Artifacts produced during the solve:

```text
solve_deadbolt.py
assets/01_key_derivation.json
assets/02_decrypted_vault.json
assets/03_admin_credential.json
assets/04_vault_info.json
assets/05_admin_response.json
```

No screenshot was needed. The challenge explicitly says no device or emulator is
required, and the solution is a static Android crypto review plus a remote API
submission.

## Recon

I started by listing the archive contents:

```bash
zipinfo public.zip
```

Relevant output:

```text
Archive:  public.zip
Zip file size: 9118 bytes
decompiled/AndroidManifest.xml
decompiled/com/fluidvault/crypto/CryptoManager.java
decompiled/com/fluidvault/auth/BiometricAuthManager.java
decompiled/com/fluidvault/network/VaultApiClient.java
vault_backup.enc
vault_decrypt.py
```

The Manifest showed a normal Android app shape:

```xml
<manifest package="com.fluidvault.app">
  <uses-permission android:name="android.permission.INTERNET" />
  <uses-permission android:name="android.permission.USE_BIOMETRIC" />

  <application android:allowBackup="true" android:usesCleartextTraffic="false">
    <activity android:name=".ui.LoginActivity" android:exported="true" />
    <activity android:name=".ui.VaultActivity" android:exported="false" />
    <provider android:name=".data.VaultContentProvider" android:exported="false" />
  </application>
</manifest>
```

That did not immediately give a remote exploit path. The exported
`LoginActivity` is only the launcher activity, while `VaultActivity`, the
content provider, and backup receiver are not exported
(`extracted/decompiled/AndroidManifest.xml:26` to
`extracted/decompiled/AndroidManifest.xml:56`). Since the prompt said "No
device or emulator required", I treated UI and IPC abuse as secondary and moved
to the crypto and backup files.

The helper script was the next useful artifact. Its header states that
`vault_backup.enc` is:

```text
[12-byte IV][ciphertext][16-byte GCM tag]
```

encrypted with AES-256-GCM, and that the key must be recovered by
reimplementing the derivation in `CryptoManager.java`
(`extracted/vault_decrypt.py:4` to `extracted/vault_decrypt.py:17`). That gave
the concrete analysis target: find exactly how `CryptoManager` derives the key.

I also checked the remote API documentation endpoint exposed by the mobile
client code:

```bash
curl -k -sS https://cf6e095154604ced.chal.ctf.ae/api/vault/info
```

Output:

```json
{
  "algorithm": "AES-256-GCM",
  "backup_format": "iv || ciphertext || tag",
  "iterations": 10000,
  "iv_length_bytes": 12,
  "kdf": "PBKDF2-HMAC-SHA256",
  "key_length_bits": 256,
  "tag_length_bits": 128
}
```

This matched the helper script and confirmed I was following the intended
artifact chain instead of guessing.

## Vulnerability

The vulnerability is deterministic, recoverable encryption-key derivation for a
portable vault backup. The backup uses AES-GCM, but the AES key is not protected
by a user secret or by the Android Keystore. It is derived from hardcoded
application constants plus a predictable fallback device identifier.

The relevant code is in `CryptoManager.java`:

```java
private static final String SEED = "fluidvault_master_seed_2026";
private static final byte[] SALT = hexToBytes("a915c3e00dbb5a55ba13d7cdaf3a126e");
private static final int ITERATIONS = 10000;
private static final int KEY_LENGTH = 256;
private static final String DEFAULT_DEVICE_ID = "DEFAULT_DEVICE_ID";
```

The key derivation is:

```java
String deviceId = getDeviceIdentifier();
String passphrase = SEED + deviceId;

SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
KeySpec spec = new PBEKeySpec(passphrase.toCharArray(), SALT, ITERATIONS, KEY_LENGTH);
byte[] keyBytes = factory.generateSecret(spec).getEncoded();
```

The device identifier is also deterministic:

```java
String serial = Build.SERIAL;
if (serial == null || serial.equals("unknown")) {
    serial = DEFAULT_DEVICE_ID;
}
return Integer.toHexString(serial.hashCode());
```

This was the key observation. Android documents `Build.UNKNOWN` as the string
`"unknown"`, and `Build.SERIAL` is deprecated and documented as always set to
`Build.UNKNOWN` on modern Android. The app handles that case by falling back to
the literal `DEFAULT_DEVICE_ID`. Oracle's Java documentation defines
`String.hashCode()` using the standard `31` multiplier formula, so the fallback
device id can be reproduced exactly.

For `DEFAULT_DEVICE_ID`, Java's `String.hashCode()` is:

```text
c8e21b06
```

Therefore the PBKDF2 passphrase is:

```text
fluidvault_master_seed_2026c8e21b06
```

This is why the bug is not "AES-GCM is weak"; AES-GCM is fine here. The weak
part is that every attacker with the decompiled source can reproduce the same
key for the provided backup.

This maps well to CWE-321, use of a hardcoded cryptographic key. CWE-321 also
explains the practical impact: hardcoded crypto keys significantly increase the
chance that encrypted data can be recovered. In this challenge, the hardcoded
seed and salt are enough once the device id fallback is understood.

## Exploitation

The exploit chain is:

1. Read `vault_decrypt.py` to confirm the backup format and expected AES key
   size.
2. Inspect `CryptoManager.java` and extract `SEED`, `SALT`, iteration count,
   key length, AES mode, and device-id logic.
3. Notice `Build.SERIAL -> "unknown" -> DEFAULT_DEVICE_ID`.
4. Recompute Java `String.hashCode("DEFAULT_DEVICE_ID")`.
5. Derive the AES-256 key with PBKDF2-HMAC-SHA256.
6. Decrypt `vault_backup.enc`.
7. Extract the `Admin Portal` password from the plaintext vault.
8. Use `VaultApiClient.java` to identify the remote endpoint and request body.
9. Submit the recovered password to `/api/vault/admin`.

I reproduced Java's `String.hashCode()` and PBKDF2 locally:

```python
import hashlib

serial = "DEFAULT_DEVICE_ID"
h = 0
for ch in serial:
    h = (31 * h + ord(ch)) & 0xffffffff

device_id = format(h, "x")
passphrase = "fluidvault_master_seed_2026" + device_id
salt = bytes.fromhex("a915c3e00dbb5a55ba13d7cdaf3a126e")
key = hashlib.pbkdf2_hmac("sha256", passphrase.encode(), salt, 10000, 32)

print(device_id)
print(key.hex())
```

Output:

```text
c8e21b06
c70cf882eaf48e1da954f0105594fef19704aeae00e86756501957a033faa91a
```

The key derivation evidence is saved in `assets/01_key_derivation.json`:

```json
{
  "device_id": "c8e21b06",
  "iterations": 10000,
  "key_hex": "c70cf882eaf48e1da954f0105594fef19704aeae00e86756501957a033faa91a",
  "passphrase": "fluidvault_master_seed_2026c8e21b06",
  "salt_hex": "a915c3e00dbb5a55ba13d7cdaf3a126e",
  "serial": "DEFAULT_DEVICE_ID"
}
```

Then I decrypted the backup:

```bash
python3 extracted/vault_decrypt.py \
  c70cf882eaf48e1da954f0105594fef19704aeae00e86756501957a033faa91a
```

Relevant plaintext:

```json
{
  "name": "Admin Portal",
  "username": "admin",
  "password": "Fl00d_G4t3s_0p3n!",
  "url": "https://vault.internal.fluidvault.io/admin",
  "notes": "Master admin - DO NOT SHARE"
}
```

The full decrypted vault is saved in `assets/02_decrypted_vault.json`.

`VaultApiClient.java` shows the final remote submission shape:

```java
URL url = new URL(BASE_URL + "/api/vault/admin");
conn.setRequestMethod("POST");
conn.setRequestProperty("Content-Type", "application/json");

JSONObject body = new JSONObject();
body.put("master_password", masterPassword);
```

The final request was:

```bash
curl -k -sS -X POST \
  https://cf6e095154604ced.chal.ctf.ae/api/vault/admin \
  -H 'Content-Type: application/json' \
  --data '{"master_password":"Fl00d_G4t3s_0p3n!"}'
```

Response:

```json
{
  "authenticated": true,
  "flag": "flag{96640ab8e93e4679}",
  "role": "admin"
}
```

The response is saved in `assets/05_admin_response.json`.

## Technical Details

AES-GCM expects a nonce/IV, ciphertext, and authentication tag. The helper
script handles the shipped backup as:

```python
iv = blob[:12]
ciphertext_and_tag = blob[12:]
plaintext = AESGCM(key).decrypt(iv, ciphertext_and_tag, None)
```

That matches both `vault_decrypt.py` and the remote `/api/vault/info` response.

The important cryptographic failure is before AES-GCM. The app has an
`initKeyStore()` method that creates a biometric Android Keystore key
(`extracted/decompiled/com/fluidvault/crypto/CryptoManager.java:120` to
`extracted/decompiled/com/fluidvault/crypto/CryptoManager.java:140`), but the
vault backup key used by `deriveVaultKey()` is not taken from the Keystore. It
comes from:

```text
hardcoded seed || deterministic Java hash of device identifier
```

For the fallback case:

```text
serial       = DEFAULT_DEVICE_ID
device_id    = Integer.toHexString(serial.hashCode())
device_id    = c8e21b06
passphrase   = fluidvault_master_seed_2026c8e21b06
PBKDF2 key   = c70cf882eaf48e1da954f0105594fef19704aeae00e86756501957a033faa91a
```

PBKDF2 does not save the design because all of its inputs are recoverable from
the shipped artifacts. It only slows down derivation; it does not add secrecy.

## Exploit Artifact

`solve_deadbolt.py` automates the full chain:

```text
reimplement Java String.hashCode()
derive fallback device id
derive PBKDF2-HMAC-SHA256 AES key
decrypt vault_backup.enc
extract Admin Portal password
optionally submit password to /api/vault/admin
save JSON evidence
```

Usage with remote validation:

```bash
python3 solve_deadbolt.py \
  --target https://cf6e095154604ced.chal.ctf.ae \
  --insecure \
  --evidence-dir assets
```

Output from the validated run:

```text
[+] Deriving fallback device id and AES-256 key
[+] device_id = c8e21b06
[+] key       = c70cf882eaf48e1da954f0105594fef19704aeae00e86756501957a033faa91a
[+] Decrypting vault backup
[+] Admin master password = Fl00d_G4t3s_0p3n!
[+] Reading remote vault info
[+] Submitting admin master password
{
  "authenticated": true,
  "flag": "flag{96640ab8e93e4679}",
  "role": "admin"
}
```

If the certificate is valid in the review environment, remove `--insecure`.

## Validation

Local syntax check:

```bash
python3 -m py_compile solve_deadbolt.py
```

Local backup decryption:

```bash
python3 extracted/vault_decrypt.py \
  c70cf882eaf48e1da954f0105594fef19704aeae00e86756501957a033faa91a
```

Remote validation:

```bash
python3 solve_deadbolt.py \
  --target https://cf6e095154604ced.chal.ctf.ae \
  --insecure \
  --evidence-dir assets
```

Result:

```text
flag{96640ab8e93e4679}
```

Evidence files:

```text
assets/01_key_derivation.json
assets/02_decrypted_vault.json
assets/03_admin_credential.json
assets/04_vault_info.json
assets/05_admin_response.json
```

## References

- <https://cwe.mitre.org/data/definitions/321.html>
- <https://cwe.mitre.org/data/definitions/798.html>
- <https://developer.android.com/reference/android/os/Build>
- <https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/String.html#hashCode()>

## Flag

```text
flag{96640ab8e93e4679}
```
