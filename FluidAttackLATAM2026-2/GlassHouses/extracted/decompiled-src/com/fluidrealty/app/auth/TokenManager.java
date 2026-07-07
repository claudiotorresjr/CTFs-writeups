package com.fluidrealty.app.auth;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Log;

public class TokenManager {

    private static final String TAG = "FluidRealty.Token";
    private static final String PREFS_NAME = "fluidrealty_auth";
    private static final String KEY_TOKEN = "session_token";
    private static TokenManager instance;
    private final SharedPreferences prefs;

    private TokenManager(Context context) {
        prefs = context.getApplicationContext()
            .getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
    }

    public static synchronized TokenManager getInstance(Context context) {
        if (instance == null) {
            instance = new TokenManager(context);
        }
        return instance;
    }

    public String getCurrentToken() {
        String token = prefs.getString(KEY_TOKEN, null);
        if (token == null) {
            Log.w(TAG, "No token stored, requesting new one from server");
            return requestNewToken();
        }
        return token;
    }

    public void saveToken(String token) {
        prefs.edit().putString(KEY_TOKEN, token).apply();
    }

    public void clearToken() {
        prefs.edit().remove(KEY_TOKEN).apply();
    }

    private String requestNewToken() {
        Log.d(TAG, "Requesting fresh auth token from backend");
        return null;
    }
}
