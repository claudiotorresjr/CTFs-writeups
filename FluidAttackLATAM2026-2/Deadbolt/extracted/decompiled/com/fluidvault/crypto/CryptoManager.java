package com.fluidvault.crypto;

import android.os.Build;
import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyProperties;
import android.util.Log;

import java.security.KeyStore;
import java.security.spec.KeySpec;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;

public class CryptoManager {

    private static final String TAG = "CryptoManager";
    private static final String KEYSTORE_ALIAS = "FluidVaultBiometricKey";
    private static final String ANDROID_KEYSTORE = "AndroidKeyStore";

    private static final String SEED = "fluidvault_master_seed_2026";
    private static final byte[] SALT = hexToBytes("a915c3e00dbb5a55ba13d7cdaf3a126e");
    private static final int ITERATIONS = 10000;
    private static final int KEY_LENGTH = 256;
    private static final String DEFAULT_DEVICE_ID = "DEFAULT_DEVICE_ID";

    private static final String AES_MODE = "AES/GCM/NoPadding";
    private static final int GCM_IV_LENGTH = 12;
    private static final int GCM_TAG_LENGTH = 128;

    private Cipher cipher;
    private SecretKey vaultKey;

    public CryptoManager() {
        try {
            this.vaultKey = deriveVaultKey();
            this.cipher = Cipher.getInstance(AES_MODE);
        } catch (Exception e) {
            Log.e(TAG, "Failed to initialize CryptoManager", e);
        }
    }

    private SecretKey deriveVaultKey() throws Exception {
        String deviceId = getDeviceIdentifier();
        String passphrase = SEED + deviceId;

        SecretKeyFactory factory = SecretKeyFactory.getInstance(
            "PBKDF2WithHmacSHA256"
        );
        KeySpec spec = new PBEKeySpec(
            passphrase.toCharArray(),
            SALT,
            ITERATIONS,
            KEY_LENGTH
        );
        byte[] keyBytes = factory.generateSecret(spec).getEncoded();
        return new SecretKeySpec(keyBytes, "AES");
    }

    private String getDeviceIdentifier() {
        String serial = Build.SERIAL;
        if (serial == null || serial.equals("unknown")) {
            serial = DEFAULT_DEVICE_ID;
        }
        return Integer.toHexString(serial.hashCode());
    }

    public Cipher getInitializedCipher(int opMode) throws Exception {
        if (opMode == Cipher.ENCRYPT_MODE) {
            cipher.init(Cipher.ENCRYPT_MODE, vaultKey);
        } else {
            throw new UnsupportedOperationException(
                "Decrypt requires IV parameter"
            );
        }
        return cipher;
    }

    public Cipher getInitializedCipher(int opMode, byte[] iv) throws Exception {
        if (opMode == Cipher.DECRYPT_MODE) {
            GCMParameterSpec paramSpec = new GCMParameterSpec(
                GCM_TAG_LENGTH, iv
            );
            cipher.init(Cipher.DECRYPT_MODE, vaultKey, paramSpec);
        }
        return cipher;
    }

    public byte[] encrypt(byte[] data) throws Exception {
        Cipher c = getInitializedCipher(Cipher.ENCRYPT_MODE);
        byte[] iv = c.getIV();
        byte[] encrypted = c.doFinal(data);
        byte[] result = new byte[GCM_IV_LENGTH + encrypted.length];
        System.arraycopy(iv, 0, result, 0, GCM_IV_LENGTH);
        System.arraycopy(encrypted, 0, result, GCM_IV_LENGTH, encrypted.length);
        return result;
    }

    public byte[] decrypt(byte[] encryptedData) throws Exception {
        byte[] iv = new byte[GCM_IV_LENGTH];
        System.arraycopy(encryptedData, 0, iv, 0, GCM_IV_LENGTH);
        byte[] ciphertext = new byte[encryptedData.length - GCM_IV_LENGTH];
        System.arraycopy(
            encryptedData, GCM_IV_LENGTH,
            ciphertext, 0,
            ciphertext.length
        );
        Cipher c = getInitializedCipher(Cipher.DECRYPT_MODE, iv);
        return c.doFinal(ciphertext);
    }

    public SecretKey getVaultKey() {
        return vaultKey;
    }

    private void initKeyStore() throws Exception {
        KeyStore keyStore = KeyStore.getInstance(ANDROID_KEYSTORE);
        keyStore.load(null);

        if (!keyStore.containsAlias(KEYSTORE_ALIAS)) {
            KeyGenerator keyGen = KeyGenerator.getInstance(
                KeyProperties.KEY_ALGORITHM_AES, ANDROID_KEYSTORE
            );
            KeyGenParameterSpec spec = new KeyGenParameterSpec.Builder(
                KEYSTORE_ALIAS,
                KeyProperties.PURPOSE_ENCRYPT
                    | KeyProperties.PURPOSE_DECRYPT
            )
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .setUserAuthenticationRequired(true)
                .setInvalidatedByBiometricEnrollment(true)
                .build();
            keyGen.init(spec);
            keyGen.generateKey();
        }
    }

    private static byte[] hexToBytes(String hex) {
        int len = hex.length();
        byte[] data = new byte[len / 2];
        for (int i = 0; i < len; i += 2) {
            data[i / 2] = (byte) (
                (Character.digit(hex.charAt(i), 16) << 4)
                + Character.digit(hex.charAt(i + 1), 16)
            );
        }
        return data;
    }
}
