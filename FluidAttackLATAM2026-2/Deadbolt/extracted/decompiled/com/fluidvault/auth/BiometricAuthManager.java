package com.fluidvault.auth;

import android.content.Context;
import android.util.Log;

import androidx.annotation.NonNull;
import androidx.biometric.BiometricPrompt;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.FragmentActivity;

import com.fluidvault.crypto.CryptoManager;

import javax.crypto.Cipher;

public class BiometricAuthManager {

    private static final String TAG = "BiometricAuth";

    private final CryptoManager cryptoManager;
    private final Context context;
    private BiometricPrompt biometricPrompt;
    private Cipher preInitializedCipher;
    private AuthCallback authCallback;

    public interface AuthCallback {
        void onAuthSuccess(Cipher cipher);
        void onAuthFailure(String reason);
    }

    public BiometricAuthManager(Context context) {
        this.context = context;
        this.cryptoManager = new CryptoManager();
    }

    public void authenticate(
        FragmentActivity activity,
        AuthCallback callback
    ) {
        this.authCallback = callback;

        try {
            preInitializedCipher = cryptoManager.getInitializedCipher(
                Cipher.ENCRYPT_MODE
            );
        } catch (Exception e) {
            Log.e(TAG, "Cipher init failed", e);
            callback.onAuthFailure("Cipher initialization failed");
            return;
        }

        BiometricPrompt.CryptoObject cryptoObject =
            new BiometricPrompt.CryptoObject(preInitializedCipher);

        biometricPrompt = new BiometricPrompt(
            activity,
            ContextCompat.getMainExecutor(context),
            new BiometricPrompt.AuthenticationCallback() {
                @Override
                public void onAuthenticationSucceeded(
                    @NonNull BiometricPrompt.AuthenticationResult result
                ) {
                    Log.d(TAG, "Biometric auth succeeded");
                    handleAuthSuccess(result);
                }

                @Override
                public void onAuthenticationError(
                    int errorCode,
                    @NonNull CharSequence errString
                ) {
                    Log.e(TAG, "Auth error: " + errString);
                    authCallback.onAuthFailure(errString.toString());
                }

                @Override
                public void onAuthenticationFailed() {
                    Log.w(TAG, "Auth failed - fingerprint not recognized");
                }
            }
        );

        BiometricPrompt.PromptInfo promptInfo =
            new BiometricPrompt.PromptInfo.Builder()
                .setTitle("FluidVault Authentication")
                .setSubtitle("Verify your identity to access the vault")
                .setNegativeButtonText("Cancel")
                .build();

        biometricPrompt.authenticate(promptInfo, cryptoObject);
    }

    private void handleAuthSuccess(
        BiometricPrompt.AuthenticationResult result
    ) {
        authCallback.onAuthSuccess(preInitializedCipher);
    }

    public CryptoManager getCryptoManager() {
        return cryptoManager;
    }
}
