package com.fluidvault.ui;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.fluidvault.auth.BiometricAuthManager;
import com.fluidvault.crypto.CryptoManager;
import com.fluidvault.network.VaultApiClient;

import javax.crypto.Cipher;

public class LoginActivity extends AppCompatActivity {

    private static final String TAG = "LoginActivity";

    private BiometricAuthManager authManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        authManager = new BiometricAuthManager(this);

        findViewById(R.id.btn_unlock).setOnClickListener(v -> {
            startBiometricAuth();
        });
    }

    private void startBiometricAuth() {
        authManager.authenticate(this, new BiometricAuthManager.AuthCallback() {
            @Override
            public void onAuthSuccess(Cipher cipher) {
                Log.d(TAG, "Authentication successful, launching vault");
                launchVault();
            }

            @Override
            public void onAuthFailure(String reason) {
                Log.w(TAG, "Authentication failed: " + reason);
                Toast.makeText(
                    LoginActivity.this,
                    "Authentication failed: " + reason,
                    Toast.LENGTH_SHORT
                ).show();
            }
        });
    }

    private void launchVault() {
        Intent intent = new Intent(this, VaultActivity.class);
        startActivity(intent);
        finish();
    }
}
