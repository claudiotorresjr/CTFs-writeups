package com.fluidrealty.app.bridge;

import android.content.Context;
import android.provider.Settings;
import android.util.Log;
import android.webkit.JavascriptInterface;
import android.widget.Toast;

import com.fluidrealty.app.auth.TokenManager;
import com.fluidrealty.app.BuildConfig;

public class AndroidBridge {

    private static final String TAG = "FluidRealty.Bridge";
    private final Context context;

    public AndroidBridge(Context context) {
        this.context = context;
    }

    @JavascriptInterface
    public String getAuthToken() {
        Log.d(TAG, "getAuthToken() called from JavaScript");
        return TokenManager.getInstance(context).getCurrentToken();
    }

    @JavascriptInterface
    public String getDeviceId() {
        return Settings.Secure.getString(
            context.getContentResolver(),
            Settings.Secure.ANDROID_ID
        );
    }

    @JavascriptInterface
    public String getAppVersion() {
        return BuildConfig.VERSION_NAME;
    }

    @JavascriptInterface
    public void showToast(String message) {
        Toast.makeText(context, message, Toast.LENGTH_SHORT).show();
    }

    @JavascriptInterface
    public void logEvent(String eventName, String eventData) {
        Log.i(TAG, "Analytics event: " + eventName + " data=" + eventData);
    }
}
