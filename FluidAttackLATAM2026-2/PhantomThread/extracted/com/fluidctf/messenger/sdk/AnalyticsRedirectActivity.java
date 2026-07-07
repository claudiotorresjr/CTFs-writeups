package com.fluidctf.messenger.sdk;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

public class AnalyticsRedirectActivity extends Activity {
    private static final String TAG = "AnalyticsSDK";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Log.d(TAG, "AnalyticsRedirectActivity launched");

        handleRedirect();
        finish();
    }

    private void handleRedirect() {
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
    }
}
